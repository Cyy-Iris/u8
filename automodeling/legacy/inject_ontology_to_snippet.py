def inject_ontology_into_snippet(snippet, ontologies):
    # have to handle "," when multiple words
    ontologies_keep = [
        ontology
        for ontology in ontologies
        if ontology["word"].lower() in snippet.lower()
    ]

    snippet_ontology = ""
    for ontology in ontologies_keep:
        snippet_ontology += f"\n{ontology['word']} means {ontology['definition']} with scope {ontology['scope']}"

    return f"{snippet_ontology}\n\n{snippet}"
