from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.schema import Document

from src.model.langchain_query import DatabaseQuery
from src.schemas.schemas import TextQuery, SemanticResult


class LLMChain:
    def __init__(self):
        self._chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
        self._database_coordinator = DatabaseQuery()

    def send_query(self, query: TextQuery) -> str:
        """This sends a query to the database coordinator"""
        docs: list[Document] = self._database_coordinator.search_texts_return_docs(
            query
        )
        humanized_answer = self._chain.run(input_documents=docs, question=query.query)
        results = SemanticResult(result=docs, humanized_answer=humanized_answer)
        return results
