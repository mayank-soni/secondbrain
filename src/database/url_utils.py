from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import TokenTextSplitter

from src.model.summariser import summarise


def get_text_from_link(link: str) -> list[str]:
    webpage_text = WebBaseLoader(link).load()
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_webpage_text = text_splitter.split_documents(webpage_text)
    return split_webpage_text


def summarise_link(link: str) -> str:
    documents = get_text_from_link(link)
    print(documents)
    summary = summarise(documents)
    return summary
