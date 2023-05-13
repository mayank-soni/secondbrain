import logging

from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI


def summarise(documents, document_limit: int = 5):
    # llm summarizer
    # temperature=0 for repeatable results
    llm = OpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    if len(documents) > document_limit:
        logging.warning(
            f"Too many documents: {len(documents)} greater than the limit of {document_limit}. Truncating to {document_limit} documents."
        )
        documents = documents[:document_limit]
    summary = str(chain.run(documents))
    return summary
