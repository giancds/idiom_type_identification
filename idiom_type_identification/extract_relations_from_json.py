"""
Module to extract the dependencies (direct object and determiner introducing the noun) from
    a parsed file saved as json objects.

    For efficiency reasons, we pre-parsed the Corpus with the Stanford CoreNLP using the python
     wrapper pycorenlp ().:

    Each parsed sentence is saved in a json string in the following format:

    {
        'sentences_50': [
            {
                'basic-dependencies': [
                    {
                        'dep': '...',
                        'dependent': ...,
                        'dependentGloss': '...',
                        'governor': 0,
                        'governorGloss': '...'
                    },
                    {...},
                ]
                'index': ...,
                'parse': 'SENTENCE_SKIPPED_OR_UNPARSABLE',
                'tokens': [
                    {
                        'after': '...',
                        'before': '...',
                        'characterOffsetBegin': ...,
                        'characterOffsetEnd': ...,
                        'index': ...,
                        'lemma': '...',
                        'originalText': '...',
                        'pos': '...',
                        'word': '...'
                    },
                ]
            }
        ]
    }

    Please note that the key "sentences_50" indicates the number of the sentence in the corpus. Each of the elements
        "basic-dependencies" and "tokens" may contain more than one sub-element. For efficiency reasons, we did not
        extracted the parse-trees of each sentences so the "parse" element in general will contain the value
        "SENTENCE_SKIPPED_OR_UNPARSABLE". Check the scripts parse_%language%_to_json.py to check how to include
        the parse-trees when re-parsing the corpus.

author: Giancarlo D. Salton

"""
import pandas as pd
import json
import codecs
from relations import process_dependencies

sent_count = 0
verbosity = 0

i = 1
cols = ["verb", "verb_POS", "noun", "noun_POS", "det", "pattern", "count"]
df = pd.DataFrame(index=[i], columns=cols)
# df = pd.read_pickle("/home/gian/datasets/vnics_type_counts.pkl")

for line in codecs.open("sample.en.json", "r", "utf-8"):

    line = line.replace("\n", "").strip()

    if line != "{\"corpus\":[" and line != "]}":
        sent_count += 1

        if sent_count > 0:

            json_obj = json.loads(line[:-1])

            for key in json_obj.keys():

                sent = json_obj[key][0]

                tokens = sent["tokens"]
                deps = sent["basic-dependencies"]

                deps_found = process_dependencies(deps, tokens)

                for dep in deps_found:

                    v = dep["verb"]
                    v_pos = dep["verb_POS"]
                    n = dep["noun"]
                    n_pos = dep["noun_POS"]
                    p = dep["pattern"]

                    if df.loc[(df["verb"] == v) & (df["verb_POS"] == v_pos) &
                            (df["noun"] == n) & (df["noun_POS"] == n_pos) &
                            (df["pattern"] == p)].empty:

                        dep["count"] = 1

                        if verbosity > 1:
                            print("Adding index {:d} = {:s}".format(i, str(dep)))

                        df.loc[i] = dep
                        i += 1

                    else:

                        idx = df.loc[(df["verb"] == v) & (df["verb_POS"] == v_pos) &
                                     (df["noun"] == n) & (df["noun_POS"] == n_pos) &
                                     (df["pattern"] == p)]["count"].index

                        count = int(df.loc[(df["verb"] == v) & (df["verb_POS"] == v_pos) &
                                           (df["noun"] == n) & (df["noun_POS"] == n_pos) &
                                           (df["pattern"] == p)]["count"])
                        count += 1
                        dep["count"] = count

                        if verbosity > 1:
                            print("Updating index {:d} = {:s}".format(idx[0], str(dep)))

                        df.set_value(idx, "count", count)

                if sent_count % 10000 == 0:
                    df.to_csv("/home/gian/datasets/vnics_type_counts.csv", encoding="utf-8", index="")
                    df.to_pickle("/home/gian/datasets/vnics_type_counts.pkl")

        else:
            print("Skipping sentence #{:d}".format(sent_count))

print("Done!\nSaving the datasets...")
df.to_csv("/home/gian/datasets/vnics_type_counts.csv", encoding="utf-8", index="")
df.to_pickle("/home/gian/datasets/vnics_type_counts.pkl")
print("Done!")
