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
verbosity = 1

i = 1
cols = ["verb", "verb_POS", "noun", "noun_POS", "det", "pattern", "count"]
df = pd.DataFrame(index=[i], columns=cols)


for _, sentences in etree.iterparse(xml_file, tag="sentences"):

    for sentence in sentences.findall("sentence"):

        parsed_sentence = sentence.findall("parse")[0]
        sent_count += 1

        dependencies = sentence.findall("dependencies")

        basic_dependencies = None

        for dependencie in dependencies:
            if dependencie.get("type") == "basic-dependencies":
                basic_dependencies = dependencie
                break

        if basic_dependencies is not None:

            print("Sentence: {:s}".format(parsed_sentence.text))

            deps = basic_dependencies.findall("dep")
            tokens = sentence.findall("tokens")[0].findall("token")
            deps_found = process_dependencies(deps, tokens)

            for dep in deps_found:

                if verbosity > 0:
                    print("Processing sentence {:d}".format(sent_count))

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

                    df.loc[p] = dep
                    i += 1

                else:

                    idx = df[(df["verb"] == v) & (df["verb_POS"] == v_pos) &
                             (df["noun"] == n) & (df["noun_POS"] == n_pos) &
                             (df["pattern"] == p)]["count"].index

                    x = int(df[(df["verb"] == v) & (df["noun"] == n) & (df["pattern"] == p)]["count"])
                    x += 1
                    dep["count"] = x

                    if verbosity > 1:
                        print("Updating index {:d} = {:s}".format(idx[0], str(dep)))

                    df.set_value(idx, "count", x)

    sentences.clear()
