"""Tools to generate strings from regular expressions."""

import logging
import re
import string
import sys
import warnings

import numpy as np
import pandas as pd

import sre_parse  # isort:skip

LOGGER = logging.getLogger(__name__)

MAX_DECIMALS = sys.float_info.dig - 1


def _literal(character, max_repeat):
    del max_repeat
    return iter([chr(character)]), 1


def _in(options, max_repeat):
    generators = []
    sizes = []
    for option, args in options:
        generator, size = _GENERATORS[option](args, max_repeat)
        generators.append(generator)
        sizes.append(size)

    return (value for generator in generators for value in generator), np.sum(sizes)


def _range(options, max_repeat):
    del max_repeat
    min_value, max_value = options
    max_value += 1
    return (chr(value) for value in range(min_value, max_value)), max_value - min_value


def _any(options, max_repeat):
    del options
    del max_repeat
    return iter(string.printable), len(string.printable)


def _max_repeat(options, max_repeat):
    min_, max_, options = options
    if max_ == sre_parse.MAXREPEAT:
        max_ = max_repeat

    option, args = options[0]
    _, size = _GENERATORS[option](args, max_repeat)

    generators = []
    sizes = []
    for repeat in range(min_, max_ + 1):
        if repeat:
            sizes.append(pow(int(size), repeat, 2 ** 63 - 1))
            repeat_generators = [
                (_GENERATORS[option](args, max_repeat)[0], option, args)
                for _ in range(repeat)
            ]
            generators.append(_from_generators(repeat_generators, max_repeat))

    return (
        value
        for generator in generators
        for value in generator
    ), np.sum(sizes) + int(min_ == 0)


def _category_chars(regex):
    return [char for char in string.printable if regex.match(char)]


_CATEGORIES = {
    sre_parse.CATEGORY_SPACE: _category_chars(re.compile(r'\s')),
    sre_parse.CATEGORY_NOT_SPACE: _category_chars(re.compile(r'\S')),
    sre_parse.CATEGORY_DIGIT: _category_chars(re.compile(r'\d')),
    sre_parse.CATEGORY_NOT_DIGIT: _category_chars(re.compile(r'\D')),
    sre_parse.CATEGORY_WORD: _category_chars(re.compile(r'\w')),
    sre_parse.CATEGORY_NOT_WORD: _category_chars(re.compile(r'\W')),
}


def _category(category, max_repeat):
    del max_repeat
    characters = _CATEGORIES[category]
    return iter(characters), len(characters)


_GENERATORS = {
    sre_parse.LITERAL: _literal,
    sre_parse.IN: _in,
    sre_parse.RANGE: _range,
    sre_parse.ANY: _any,
    sre_parse.MAX_REPEAT: _max_repeat,
    sre_parse.CATEGORY: _category,
}


def _from_generators(generators, max_repeat):
    previous = [None] + [next(generator) for generator, _, _ in generators[1:]]

    remaining = True
    while remaining:
        generated = []
        for index, (generator, option, args) in enumerate(generators):
            remaining = True
            try:
                value = next(generator)
                generated.append(value)
                previous[index] = value
                generated.extend(previous[index + 1:])
                break
            except StopIteration:
                generator = _GENERATORS[option](args, max_repeat)[0]
                generators[index] = generator, option, args
                value = next(generator)
                previous[index] = value
                generated.append(value)
                remaining = False

        if remaining:
            yield ''.join(reversed(generated))


def strings_from_regex(regex, max_repeat=16):
    """Generate strings that match the given regular expression.

    The output is a generator that produces regular expressions that match
    the indicated regular expressions alongside an integer indicating the
    total length of the generator.

    WARNING: Subpatterns are currently not supported.

    Args:
        regex (str):
            String representing a valid python regular expression.
        max_repeat (int):
            Maximum number of repetitions to produce when the regular
            expression allows an infinte amount. Defaults to 16.

    Returns:
        tuple:
            * Generator that produces strings that match the given regex.
            * Total length of the generator.
    """
    parsed = sre_parse.parse(regex, flags=sre_parse.SRE_FLAG_UNICODE)
    generators = []
    sizes = []
    for option, args in reversed(parsed):
        if option != sre_parse.AT:
            generator, size = _GENERATORS[option](args, max_repeat)
            generators.append((generator, option, args))
            sizes.append(size)

    return _from_generators(generators, max_repeat), np.prod(sizes, dtype=np.complex128).real


def fill_nan_with_none(data):
    """Replace all nan values with None.

    Args:
        data (pd.DataFrame or pd.Series)

    Returns:
        data:
            Original data with nan values replaced by None.
    """
    return data.fillna(np.nan).replace([np.nan], [None])


def flatten_column_list(column_list):
    """Flatten a list of columns.

    Args:
        column_list (list):
            List of columns to flatten.

    Returns:
        list:
            Flattened list of columns.
    """
    flattened = []
    for column in column_list:
        if isinstance(column, tuple):
            flattened.extend(column)
        else:
            flattened.append(column)

    return flattened


def check_nan_in_transform(data, dtype):
    """Check if there are null values in the transformed data.

    Args:
        data (pd.Series or numpy.ndarray):
            Data that has been transformed.
        dtype (str):
            Data type of the transformed data.
    """
    if pd.isna(data).any().any():
        message = (
            'There are null values in the transformed data. The reversed '
            'transformed data will contain null values'
        )
        is_integer = pd.api.types.is_integer_dtype(dtype)
        if is_integer:
            message += " of type 'float'."
        else:
            message += '.'

        warnings.warn(message)


def try_convert_to_dtype(data, dtype):
    """Try to convert data to a given dtype.

    Args:
        data (pd.Series or numpy.ndarray):
            Data to convert.
        dtype (str):
            Data type to convert to.

    Returns:
        data:
            Data converted to the given dtype.
    """
    try:
        data = data.astype(dtype)
    except ValueError as error:
        is_integer = pd.api.types.is_integer_dtype(dtype)
        if is_integer:
            data = data.astype(float)
        else:
            raise error

    return data


def learn_rounding_digits(data):
    """Learn the number of digits to round data to.

    Args:
        data (pd.Series):
            Data to learn the number of digits to round to.

    Returns:
        int or None:
            Number of digits to round to.
    """
    # check if data has any decimals
    name = data.name
    data = np.array(data)
    roundable_data = data[~(np.isinf(data) | pd.isna(data))]

    # Doesn't contain numbers
    if len(roundable_data) == 0:
        return None

    # Doesn't contain decimal digits
    if ((roundable_data % 1) == 0).all():
        return 0

    # Try to round to fewer digits
    if (roundable_data == roundable_data.round(MAX_DECIMALS)).all():
        for decimal in range(MAX_DECIMALS + 1):
            if (roundable_data == roundable_data.round(decimal)).all():
                return decimal

    # Can't round, not equal after MAX_DECIMALS digits of precision
    LOGGER.info("No rounding scheme detected for column '%s'. Data will not be rounded.", name)
    return None
