from __future__ import annotations

import spacy
import textdescriptives as td
from langchain_core.documents import Document


def filter_text_by_td(text_list: list[str | Document], filter_type: bool = True) -> list[Document]:
    """
    Filter documents by the textdescriptives quality check, converts strings to langchain Docs

    Args:
        text_list: A list of text strings or Document objects.
        filter_type: A boolean defining whether to filter by texts that passed (True) or failed (False) the textdescriptives quality check.

    Returns:
        A list of Document objects that passed the textdescriptives quality check.
    """
    nlp = spacy.blank("da")  # Assuming 'da' is the desired model
    nlp.add_pipe("sentencizer")
    nlp.add_pipe("textdescriptives/quality")

    # Process the texts with SpaCy, handling both strings and Document objects
    processed_docs = list(nlp.pipe(doc.page_content if isinstance(doc, Document) else doc for doc in text_list))

    # Filter based on the quality check, merge with existing metadata
    filtered_docs = [
        Document(page_content=doc.text, metadata=getattr(original_doc, "metadata", {}))
        for original_doc, doc in zip(text_list, processed_docs)
        if doc._.passed_quality_check == filter_type
    ]

    return filtered_docs
