"""
Module to extract the correct syntactic pattern froma  given verb+dobj relation.

Obs.:

    ---- some english personal pronouns can be parsed as direct objects of verbs. In these cases, we assume
    they are singular or plural based on their lemma.

    --- We consider the pronoun 'YOU' always as plural.

author: Giancarlo D. Salton
"""

_SINGULAR_NOUN = "NN"
_PLURAL_NOUN = "NNS"
_SINGULAR_PROPER = "NNP"
_PLURAL_PROPER = "NNPS"

_PERSONAL_ENGLISH_SINGULAR = ["I", "he", "she", "it"]

_PERSONAL_ENGLISH_PLURAL = ["you", "we", "they"]

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

    elif noun["POS"] in [_PLURAL_NOUN, _PLURAL_PROPER]:

        return _extract_plural_pattern(det)

    else:
        return _extract_undefined_pattern(det)


def _extract_singlular_pattern(det):
    """

    Args:
        det:

    Returns:

    """
    if det is None:
        return 1, "NULL"

    elif det in ["a", "an"]:
        return 2, "a/an"

    elif det == "the":
        return 3, "the"

    elif det in _ENGLISH_DEMONSTRATIVE:
        return 4, "DEM"

    elif det in _ENGLISH_POSSESSIVE:
        return 5, "POSS"

    else:
        return 10, "other"


def _extract_plural_pattern(det):
    """

    Args:
        det:

    Returns:

    """
    if det is None:
        return 6, "NULL"

    elif det == "the":
        return 7, "the"

    elif det in _ENGLISH_DEMONSTRATIVE:
        return 8, "DEM"

    elif det in _ENGLISH_POSSESSIVE:
        return 9, "POSS"

    else:
        return 10, "other"


def extract_passive_patterns():
    """

    Returns:

    """
    return 11, "ANY"


def _extract_undefined_pattern(det):

    if det is None:
        return 0, "NULL"

    elif det in ["a", "an"]:
        return 0, "a/an"

    elif det == "the":
        return 0, "the"

    elif det in _ENGLISH_DEMONSTRATIVE:
        return 0, "DEM"

    elif det in _ENGLISH_POSSESSIVE:
        return 0, "POSS"

    else:
        return 0, "other"
