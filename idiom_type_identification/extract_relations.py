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
from lxml import etree
from idiom_type_identification.relations import process_dependencies


xml_file = '/home/gian/data/Test_BNC.xml'


for _, sentences in etree.iterparse(xml_file, tag="sentences"):

    for sentence in sentences.findall("sentence"):

        dependencies = sentence.findall("dependencies")

        basic_dependencies = None

        for dependencie in dependencies:
            if dependencie.get("type") == "basic-dependencies":
                basic_dependencies = dependencie
                break

        if basic_dependencies is not None:
            deps = basic_dependencies.findall("dep")
            tokens = sentence.findall("tokens")[0].findall("token")
            process_dependencies(deps, tokens)
    sentences.clear()
