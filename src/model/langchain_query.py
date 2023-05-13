import logging
from src.schemas.schemas import SemanticResult, TextQuery
from src.database.database import ChromaUtils


class DatabaseQuery:
    def __init__(self):
        """Load database to memory"""
        print(f"zzz intialize DatabaseQuery")
        self.database = ChromaUtils()
        print(
            f"Database loaded. It contains {self.database.chroma._collection.count()} documents."
        )

    def search_texts(self, query: TextQuery) -> list[str]:
        results = self.search_texts_return_docs(query=query)
        return SemanticResult(result=results, humanized_answer="")

    def search_texts_return_docs(self, query: TextQuery) -> list[str]:
        return self.database.chroma.similarity_search(
            query.query, query.desired_result_num
        )


# # Testing function
# if __name__ == '__main__':
#     databasequery = DatabaseQuery()
#     search_results = databasequery.search_texts(TextQuery(query='machine learning models', result_num=1))
#     print(search_results)
#     print(type(search_results))
