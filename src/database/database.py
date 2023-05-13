from langchain.document_loaders import DataFrameLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from src.database.telegram import TelegramReader
from src.config import CHROMA_DATABASE_PATH


class ChromaUtils:
    """Wrapper around Chroma database loaded in memory.
    Allows addition of new data by setting persist = True.
    """

    def __init__(self, persist: bool = False):
        self.chroma = Chroma(
            persist_directory=str(CHROMA_DATABASE_PATH),
            embedding_function=OpenAIEmbeddings(),
        )
        # Use persist=True to save to disk
        self.persist = persist
        if self.persist:
            self.chroma.persist()

    def add_telegram_plaintext(self, telegramreader: TelegramReader) -> Chroma:
        """Adds plaintext data from a TelegramReader instance to the Chroma
        database.
        Expects telegramreader.plaintext to be defined.
        """
        messages = DataFrameLoader(
            telegramreader.output, page_content_column="plaintext"
        ).load()
        self.chroma.add_documents(messages)
        if self.persist:
            self.chroma.persist()
        return self.chroma

    # def add_links(self, link: str, doclimitperlink: int = 10) -> Chroma:
    #     """Adds documents from a link to the Chroma database.
    #     For now, only adds the first 10 documents from the link.
    #     """
    #     documents = get_link_text(link)
    #     if len(documents) > doclimitperlink:
    #         logging.warning(f'Site: {link} is of length {len(documents)} which is greater than the limit of {doclimitperlink}. Truncating to {doclimitperlink} documents.')
    #     self.chroma.add_documents(documents[:doclimitperlink])
    #     if self.persist:
    #         self.chroma.persist()
    #     return self.chroma

    # # Youtube video loader on langchain seems to be buggy when trying it out. Skipping this for now.
    # def add_youtube(self, links: list[str]) -> Chroma:
    #     self.add_links(youtube_links)
    #     self.add_links(other_links)

    # @staticmethod
    # def split_youtube(links: list[str]) -> tuple[list[str], list[str]]:
    #     """Takes in a list of urls, and returns two lists.
    #     The first list contains YouTube video IDs, and the second contains other links.
    #     """
    #     youtube_pattern = re.compile(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})')
    #     other_links = []
    #     youtube_ids = []
    #     for url in links:
    #         match = youtube_pattern.search(url)
    #         if match:
    #             # Get the 11 digit video IDs only
    #             youtube_ids.append(match.group(1))
    #         else:
    #             other_links.append(url)
    #     return youtube_ids, other_links
