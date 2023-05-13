import pandas as pd
import pathlib
from typing import Union
import validators

from src.database.url_utils import summarise_link
from src.config import TELEGRAM_DATA_PATH


class TelegramReader:
    """Class to read Telegram data.json file and extract plaintext messages, summaries of links.
    Stored in a DataFrame that can be read through Langchain DataFrameLoader()."""

    def __init__(
        self,
        data_path: pathlib.Path = TELEGRAM_DATA_PATH,
        read_length: int = 15,
        random_state: int = 36,
    ) -> None:
        self.df = pd.read_json(data_path)
        # Default short read_length for experimenting with a smaller dataset
        if read_length is not None:
            self.df = self.df.sample(read_length, random_state=random_state)
        # Get Series of text_entities from self.df
        self.text_entities = self.get_text_entities()
        # Get DataFrame of metadata from self.df
        self.metadata = self.get_metadata()
        # Combine into output dataframe
        self.plaintext = pd.DataFrame
        self.output = self.get_plaintext_df()

    def get_text_entities(self) -> pd.Series:
        """Extract Series of text_entities from self.df."""
        if not isinstance(self.df, pd.DataFrame):
            raise ValueError("self.df needs to be defined.")
        self.text_entities = (
            self.df["messages"]  # Series of dictionaries
            .apply(
                lambda x: x["text_entities"]
            )  # Extract key text_entities from each dictionary. Each is a list -> series of lists
            .rename("text_entities")
        )
        return self.text_entities

    def get_metadata(self) -> pd.DataFrame:
        """Extract DataFrame of metadata from self.df."""
        if not isinstance(self.df, pd.DataFrame):
            raise ValueError("self.df needs to be defined.")
        # Extract date and from keys from each dictionary in messages column
        self.metadata = self.df["messages"].apply(pd.Series)[["date", "from"]]
        return self.metadata

    def get_plaintext_df(self) -> pd.DataFrame:
        """Extract DataFrame of plaintext from self.text_entities."""
        for attribute in ["text_entities", "metadata"]:
            if not isinstance(getattr(self, attribute), Union[pd.Series, pd.DataFrame]):
                raise ValueError(f"self.{attribute} needs to be a DataFrame.")
        # Get plaintext from text_entities
        self.plaintext = self.text_entities.apply(
            self._get_plaintext_from_textentities
        ).rename("plaintext")
        # Concatenate metadata and plaintext columns together
        self.output = pd.concat([self.plaintext, self.metadata], axis=1)
        self.output = self._clean_output()
        return self.output

    def _get_plaintext_from_textentities(self, text_entities: list) -> str:
        """Takes a list of text entities from a single message, and combines them into a plain text string"""
        # Initialise empty return string
        plaintext = ""
        # Loop through each entity in text entities, and concatenate their text to output string
        for entity in text_entities:
            # If entity type is a url, summarise text in link and append the summary to plaintext
            plaintext += entity["text"]
            if entity["type"] == "link" and self._check_url(entity["text"]):
                print("Summarising link: ", entity["text"])
                plaintext += f' (Summary of link: {summarise_link(entity["text"])})'
        return plaintext

    def _check_url(self, url: str) -> bool:
        # Look into adding videos etc here.
        return (
            validators.url(url)
            and "www.straitstimes.com" not in url
            and "gitlab.aisingapore.net" not in url
            and ".pdf" not in url
        )

    def _clean_output(self) -> pd.DataFrame:
        """Cleans plaintext column of self.output.
        Removes whitespace, removes empty messages, resets index."""
        if not isinstance(self.output, pd.DataFrame):
            raise ValueError("self.output needs to be defined.")
        # Remove whitespaces on either end of string
        self.output["plaintext"] = self.output["plaintext"].str.strip()
        # Drop empty strings i.e. boolean value = False
        self.output = self.output[self.output["plaintext"].astype(bool)]
        self.output = self.output.reset_index(drop=True)
        return self.output

    def save_plaintext_csv(self, save_path: pathlib.Path) -> None:
        """Unused, not updated. Saves self.plaintext to CSV."""
        if not isinstance(self.plaintext, pd.DataFrame):
            raise ValueError("self.plaintext needs to be defined.")
        # Save to csv. Have an index label so langchain's CSV reader can save the indices for each message.
        self.plaintext.to_csv(save_path, index_label="index")
        return self.plaintext

    def get_links_series(self) -> pd.Series:
        """Unused. Get Series of links in each message
        Except for links to straitstimes.com and gitlab.aisingapore.net and .pdf files.
        Had problems with these earlier, just avoided first.
        """
        if not isinstance(self.text_entities, pd.Series):
            raise ValueError("self.text_entities needs to be defined.")

        # Get list of urls from each message
        def get_links(text_entities):
            links = []
            for text_entity in text_entities:
                if text_entity["type"] == "link" and self._check_url(
                    text_entity["text"]
                ):
                    links.append(text_entity["text"])
            return links

        self.links_series = self.text_entities.apply(get_links).rename("links")
        return self.links_series
