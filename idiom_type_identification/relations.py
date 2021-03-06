"""

"""
from patterns import extract_active_patterns, extract_passive_patterns

_dobj = "dobj"
_nsubjpass = "nsubjpass"


def _dependencies_to_dict(dependencies):
    """

    Args:
        dependencies:

    Returns:
        a python dictionary with the followinf format:

        dependencies_dictionary: {
            type: {
                governor: {
                    idx,
                    word
                },
                dependent: {
                    idx,
                    word
                }
            }
        }

    """
    dependencies_dictionary = dict()

    for dep in dependencies:
        dep_type = dep["dep"]
        dependencies_dictionary[dep_type] = {
            "governor": {
                "idx": dep["governor"],
                "word": dep["governorGloss"]
            },
            "dependent": {
                "idx": dep["dependent"],
                "word": dep["dependentGloss"]
            }
        }

    return dependencies_dictionary


def _tokens_to_dictionary(raw_tokens):
    """

    Args:
        raw_tokens:

    Returns:
        a python dictionary with the following format:
        tokens_dictionary: {
            id: {
                id,
                word,
                lemma,
                POS
            }
        }

    """
    tokens_dictionary = dict()

    for token in raw_tokens:
        idx = token["index"]
        word = token["word"]
        lemma = token["lemma"]
        pos = token["pos"]
        tokens_dictionary[idx] = {
            "id": idx,
            "word": word,
            "lemma": lemma,
            "POS": pos
        }

    return tokens_dictionary


def _extract_determiner(dependencies, tokens, noun):
    """

    Args:
        dependencies:
        tokens:
        noun:

    Returns:
        a Python str representing the deteminer's lemma
    """

    determiner = None

    for dependencie in dependencies:
        dep = dependencies[dependencie]

        if (dependencie == "det" or dependencie == "poss") and dep["governor"]["word"] == noun:

            token_id = dep["dependent"]["idx"]
            token = tokens[token_id]

            if token["POS"] in ["POS", "DT", "PRP$"]:
                determiner = token["lemma"]

            elif dependencie == "possessive":
                determiner = token["lemma"]

    return determiner


def process_dependencies(raw_dependencies, raw_tokens):
    """

    Args:
        raw_dependencies:
        raw_tokens:
        json:

    Returns:

    """
    dependencies = _dependencies_to_dict(raw_dependencies)
    tokens = _tokens_to_dictionary(raw_tokens)

    deps_found = []

    for dependencie in dependencies:

        dep = dependencies[dependencie]

        if dependencie in [_dobj, _nsubjpass]:

            verb_id = dep["governor"]["idx"]
            noun_id = dep["dependent"]["idx"]

            verb_token = tokens[verb_id]
            noun_token = tokens[noun_id]

            verb = verb_token["lemma"]
            verb_pos = verb_token["POS"]
            noun = noun_token["lemma"]
            noun_pos = noun_token["POS"]

            det_lemma = _extract_determiner(dependencies, tokens, noun_token["lemma"])

            pattern = None

            if dependencie == _dobj:

                pattern, det = extract_active_patterns(noun_token, det_lemma)

            elif dependencie == _nsubjpass:

                pattern, det = extract_passive_patterns()

            if pattern is not None:
                deps_found.append({"verb": verb,
                                   "verb_POS": verb_pos,
                                   "noun": noun,
                                   "noun_POS": noun_pos,
                                   "det": det,
                                   "pattern": pattern})

    return deps_found
