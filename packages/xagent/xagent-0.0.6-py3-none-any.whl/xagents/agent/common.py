#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/07 17:54:34
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

from typing import List, Optional

from abc import abstractmethod

from pydantic import BaseModel, Field

from agit.common import LLMResp
from xagents.config import DEFAULT_KB_PROMPT_TEMPLATE
from xagents.kb.common import RecalledChunk


class AgentResp(LLMResp):
    references: Optional[List[RecalledChunk]] = Field(description="召回的片段")



class AbstractAgent:

    def __init__(self, name) -> None:
        self.name = name

    @abstractmethod
    def chat(self, message: str, stream=True, do_remember=True) -> AgentResp:
        raise NotImplementedError

    @abstractmethod
    def remember(self, role: str, message: str):
        raise NotImplementedError

class KBConfig(BaseModel):
    name: str = Field(description="知识库名称")
    prompt_template:str = Field(description="应用知识库的提示词模板, 必须包含{context}和{question}两个字段", default=DEFAULT_KB_PROMPT_TEMPLATE)