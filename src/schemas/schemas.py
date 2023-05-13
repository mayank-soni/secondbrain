import pydantic
from typing import Union
from dataclasses import dataclass


class SemanticResult(pydantic.BaseModel):
    result: list[
        dict[str, Union[str, dict]]
    ]  # List of results, each of which is a dictionary
    humanized_answer: str


@dataclass(frozen=False)
class TextQuery:
    query: str
    desired_result_num: int
