"""
Module to extract the dependencies over the direct objects and determiners of each sentence.

The file format must be:

<bnc>
    <root>
        <sentences>
            <sentence>
                <token>
                    ...
                </token>
                <parse>
                    ...
                </parse>
                <dependencies type="">
                    <dep type="">
                        <governor idx="">...</governor>
                        <dependent idx="">...</dependent>
                    </dep>
                </dependencies>
            </sentence>
        </sentences>
    </root>
</bnc>

author: Giancarlo D. Salton
"""
import pandas as pd
from lxml import etree
from relations import process_dependencies


xml_file = '/home/gian/data/Parsed_BNC.xml'

sent_count = 0
verbosity = 0

i = 1
cols = ["verb", "verb_POS", "noun", "noun_POS", "det", "pattern", "count"]
df = pd.DataFrame(index=[i], columns=cols)


for _, sentences in etree.iterparse(xml_file, tag="sentences"):

    for sentence in sentences.findall("sentence"):

        parsed_sentence = sentence.findall("parse")[0]
        sent_count += 1

        if parsed_sentence.text.strip() == "(ROOT (S (ADVP (RB Often)) (NP (JJ infected) (NNS people)) (VP (VBP are) (VP (VBN rejected) (PP (IN by) (NP (NN family) (CC and) (NNS friends))) (, ,) (S (VP (VBG leaving) (S (NP (PRP them)) (VP (TO to) (VP (VB face) (NP (DT this) (JJ chronic) (NN condition)) (ADVP (RB alone))))))))) (. .)))":
            print()

        if verbosity > -1:
            print("Processing sentence #{:d}".format(sent_count))

        dependencies = sentence.findall("dependencies")

        basic_dependencies = None

        for dependencie in dependencies:
            if dependencie.get("type") == "basic-dependencies":
                basic_dependencies = dependencie
                break

        if basic_dependencies is not None:

            if verbosity > 0:
                print("Sentence: {:s}".format(parsed_sentence.text))

            deps = basic_dependencies.findall("dep")
            tokens = sentence.findall("tokens")[0].findall("token")
            deps_found = process_dependencies(deps, tokens)

            for dep in deps_found:

                v = dep["verb"]
                v_pos = dep["verb_POS"]
                n = dep["noun"]
                n_pos = dep["noun_POS"]
                p = dep["pattern"]

                if df[(df["verb"] == v) & (df["verb_POS"] == v_pos) &
                        (df["noun"] == n) & (df["noun_POS"] == n_pos) &
                        (df["pattern"] == p)].empty:

                    dep["count"] = 1

                    if verbosity > 1:
                        print("Adding index {:d} = {:s}".format(i, str(dep)))

                    df.loc[i] = dep
                    i += 1

                else:

                    idx = df[(df["verb"] == v) & (df["verb_POS"] == v_pos) &
                             (df["noun"] == n) & (df["noun_POS"] == n_pos) &
                             (df["pattern"] == p)]["count"].index

                    count = int(df[(df["verb"] == v) & (df["verb_POS"] == v_pos) &
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

        sentences.clear()

df.to_csv("/home/gian/datasets/vnics_type_counts.csv", encoding="utf-8", index="")
df.to_pickle("/home/gian/datasets/vnics_type_counts.pkl")