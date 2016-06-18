"""

"""
from idiom_type_identification.patterns import extract_active_patterns, extract_passive_patterns

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
        dep_type = dep.get("type")
        dependencies_dictionary[dep_type] = {"governor": {}, "dependent": {}}

        governor = dep.find("governor")
        dependent = dep.find("dependent")

        dependencies_dictionary[dep_type]["governor"]["idx"] = governor.get("idx")
        dependencies_dictionary[dep_type]["governor"]["word"] = governor.text
        dependencies_dictionary[dep_type]["dependent"]["idx"] = dependent.get("idx")
        dependencies_dictionary[dep_type]["dependent"]["word"] = dependent.text

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
        id = token.get("id")
        word = token.findall("word")[0].text
        lemma = token.findall("lemma")[0].text
        pos = token.findall("POS")[0].text
        tokens_dictionary[id] = {
            "id": id,
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

            token_id = dep["governor"]["idx"]
            token = tokens[token_id]

            if token["POS"] in ["POS", "DT", "PRP$"]:
                determiner = token["lemma"]

            elif dependencie == "possessive":
                determiner = token["lemma"]

    return determiner


def process_dependencies(raw_dependencies, raw_tokens):

    dependencies = _dependencies_to_dict(raw_dependencies)
    tokens = _tokens_to_dictionary(raw_tokens)

    for dependencie in dependencies:

        dep = dependencies[dependencie]

        if dependencie in [_dobj, _nsubjpass]:

            verb_id = dep["governor"]["idx"]
            noun_id = dep["dependent"]["idx"]

            verb_token = tokens[verb_id]
            noun_token = tokens[noun_id]

            verb = verb_token["lemma"]
            noun = noun_token["lemma"]

            det = _extract_determiner(dependencies, tokens, noun_token["lemma"])

            if dependencie == _dobj:

                pattern = extract_active_patterns(verb_token, noun_token, det)

            elif dependencie == _nsubjpass:

                pattern = extract_passive_patterns(verb_token, noun_token, det)

