"""
Module to process part of json objects to remove the unwanted entries.

author: Giancarlo D. Salton
"""
import json


def process_json(json_str, idx, keep_all_dependencies=False):

    json_str = json_str.replace("\u0000", "")
    json_str = json_str.replace("sentences", "sentences_{:d}".format(idx))
    json_obj = json.loads(json_str, )

    if not keep_all_dependencies:
        for sent in json_obj["sentences_{:d}".format(idx)]:
            del sent["collapsed-dependencies"]
            del sent["collapsed-ccprocessed-dependencies"]

    return json_obj
