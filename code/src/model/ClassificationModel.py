from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List, Optional


class SubRequestType(BaseModel):
    sub_request_type: str
    confidence_score: float
    sub_reasoning: str

class RequestType(BaseModel):
    request_type: str
    confidence_score: float = []
    reasoning: str = []
    sub_request_type: List[SubRequestType] = []

class Response(BaseModel):
    resposne: List[RequestType]


def getClassificationParser():
    return PydanticOutputParser(pydantic_object=Response)
