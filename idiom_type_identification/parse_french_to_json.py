"""
Module to parse a French corpus and save the JSON output.

Before running this script, make sure a CoreNLP server is running.

To do this, follow the instructions at
    http://stanfordnlp.github.io/CoreNLP/corenlp-server.html.

author: Giancarlo D. Salton
"""

from pycorenlp import StanfordCoreNLP
import codecs
import json
import utils

properties = {
    "annotators": "tokenize,ssplit,pos,depparse,lemma",
    "parse.model": "edu/stanford/nlp/models/lexparser/frenchFactored.ser.gz",
    "pos.model": "edu/stanford/nlp/models/pos-tagger/french/french.tagger",
    "tokenize.language": "fr",
    "outputFormat": "json"
}

nlp = StanfordCoreNLP('http://localhost:9000')

input_file = "sample.fr"
output_file = "{:s}.json".format(input_file)

keep_all_dependencies = False
sent_count = 0
with codecs.open(output_file, "w", "utf-8") as outfile:
    outfile.write("{\"corpus\":[")

    for line in codecs.open(input_file, "r", "utf-8"):

        sent_count += 1
        print("Processing sent #{:d}".format(sent_count))
        if sent_count == 16:
            print()

        output = nlp.annotate(line.replace("\n", "").strip(), properties, encoding="utf-8")

        if isinstance(output, str):
            json_obj = utils.process_json(output, keep_all_dependencies)
        else:
            json_obj = utils.process_json(json.dumps(output, ensure_ascii=False), keep_all_dependencies)

        json_str = json.dumps(json_obj, ensure_ascii=False, sort_keys=True)
        outfile.write("{:s},\n".format(json_str))

    outfile.write("]}")

print("Done!")
