"""
Module to extract the correct syntactic pattern froma  given verb+dobj relation.

author: Giancarlo D. Salton
"""

_SINGULAR_NOUN = "NN"
_PLURAL_NOUN = "NNS"
_SINGULAR_PROPER = "NNP"
_PLURAL_PROPER = "NNPS"

_ENGLISH_POSSESSIVE = ["my", "he", "she", "we", "you", "its", "they"
                       "'s", "whose", "mine", "thine", "thy"]

_ENGLISH_DEMONSTRATIVE = ["this", "that", "these", "those"]


def extract_active_patterns(noun, det):
    """

    Args:
        noun: a python dictionary representing the noun with the following formatr
            noun: {
                id,
                word,
                lemma,
                POS
            }
        det:

    Returns:
        a python int indicating the syntactic pattern

    """

    if noun["POS"] in [_SINGULAR_NOUN, _SINGULAR_PROPER]:
        return _extract_singlular_pattern(det)
    elif noun["POS"] in [_SINGULAR_NOUN, _SINGULAR_PROPER]:
        return _extract_plural_pattern(det)


def _extract_singlular_pattern(det):
    """

    Args:
        det:

    Returns:

    """
    if det is None:
        return 1
    elif det in ["a", "an"]:
        return 2
    elif det == "the":
        return 3
    elif det in _ENGLISH_DEMONSTRATIVE:
        return 4
    elif det in _ENGLISH_POSSESSIVE:
        return 5
    else:
        return 10


def _extract_plural_pattern(det):
    """

    Args:
        det:

    Returns:

    """
    if det is None:
        return 6
    elif det == "the":
        return 7
    elif det in _ENGLISH_DEMONSTRATIVE:
        return 8
    elif det in _ENGLISH_POSSESSIVE:
        return 9
    else:
        return 10


def extract_passive_patterns():
    """

    Returns:

    """
    return 11
