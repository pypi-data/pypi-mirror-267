#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/07 17:57:13
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


import os
from typing import Generator, List, Optional

from pydantic import BaseModel, Field

from agit.common import LLMResp
from xagents.model.common import LLMGenConfig
from xagents.agent.common import AbstractAgent, AgentResp, KBConfig
from xagents.config import LOG_DIR
from xagents.kb.common import RecalledChunk
from xagents.kb.api import KBSearchConfig, get_knowledge_base
from xagents.model.api import get_llm_model
from xagents.agent.memory import BaseMemory
from xagents.tool.api import invoke_tool_call
from xagents.tool.core import BaseTool, ToolCall
from snippets import dump, load

from loguru import logger

agent_log_path = os.path.join(LOG_DIR, "xagent.log")


class XAgentInfo(BaseModel):
    name: str = Field(description="agent的名称，唯一键")
    llm_config: dict = Field(description="llm的配置信息")
    memory_config: dict = Field(description="memory的配置信息")
    kb_config: Optional[KBConfig] = Field(description="kb的配置信息")
    tools: List[BaseTool] = Field(description="工具列表")


class XAgent(AbstractAgent):

    def __init__(self, name: str,
                 llm_config: dict,
                 memory_config: dict,
                 kb_config: KBConfig,
                 tools: List[BaseTool] = []) -> None:
        super().__init__(name=name)
        self.info = XAgentInfo(name=name, llm_config=llm_config, memory_config=memory_config, kb_config=kb_config, tools=tools)

        self.llm_model = get_llm_model(llm_config)
        self.memory = BaseMemory(**memory_config)
        self._load_kb(kb_config)
        self.tools = tools

    def _load_kb(self, kb_config: KBConfig):
        if not kb_config:
            self.kb = None
            self.kb_prompt_template = None
        else:
            self.kb = get_knowledge_base(kb_config.name)
            self.kb_prompt_template = kb_config.prompt_template
            logger.info("load kb finish")

    def get_info(self):
        return self.info

    def search_kb(self, query: str, **kwargs) -> List[RecalledChunk]:
        chunks = self.kb.search(query=query, **kwargs)
        return chunks

    def use_tool(self, tool_call: ToolCall):
        resp = invoke_tool_call(tool_call)
        tool_call.resp = resp
        return resp

    @staticmethod
    def _get_agent_config_path(dir_path: str, agent_name: str):
        return os.path.join(dir_path, agent_name+".json")

    def save(self, save_dir: str):
        save_path = self._get_agent_config_path(save_dir, self.name)
        logger.info(f"save agent:{self.name} to {save_path}")
        logger.debug(f"agent info:{self.get_info()}")
        dump(self.get_info().model_dump(), save_path)

    @classmethod
    def load(cls, save_dir: str, name: str) -> "XAgent":
        config_path = cls._get_agent_config_path(save_dir, name)
        if not os.path.exists(config_path):
            raise FileExistsError(f"config file {config_path} not found")

        kwargs = load(config_path)
        if kwargs.get("kb_config"):
            kwargs["kb_config"] = KBConfig.model_validate(kwargs["kb_config"])
        logger.debug(f"{kwargs=}")

        return XAgent(**kwargs)

    def chat(self, message: str, do_remember=True, details=False, stream=False,
             use_kb=False, kb_search_config: KBSearchConfig = KBSearchConfig(),
             fake_chat=False, llm_gen_config: LLMGenConfig = LLMGenConfig(), **kwargs) -> AgentResp:
        logger.info(f"agent get message:{message}")

        if use_kb:

            if not self.kb or not self.kb_prompt_template:
                logger.warning(f"agent:{self.name} has no related knowledge base, will not chat with kb! ")
                prompt = message
                chunks = None

            else:
                logger.info("agent searching kb")
                chunks = self.search_kb(query=message, **kb_search_config.model_dump())
                # logger.info(f"agent get {len(chunks)} chunks :{chunks}")
                # logger.info(f"sample chunks:{chunks[:3]}")
                context = "\n".join(f"{idx+1}." + c.to_plain_text() for idx, c in enumerate(chunks))

                prompt = self.kb_prompt_template.format(question=message, context=context)
        else:
            prompt = message
            chunks = None

        if fake_chat:
            fake_resp = "这是MOCK的回答信息,如果需要真实回答,请设置fake_chat=False"
            llm_resp = (e for e in fake_resp) if stream else fake_resp
            tool_call = None
        else:
            history = self.memory.to_llm_history()
            llm_resp: LLMResp = self.llm_model.generate(prompt=prompt, history=history, tools=self.tools, details=details, stream=stream,
                                                        **llm_gen_config.model_dump(), **kwargs)
            # 调用tool
            tool_calls = llm_resp.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    logger.debug(f"calling tool:{tool_call.name}")
                    self.use_tool(tool_call)
                    llm_resp = self.llm_model.observe(prompt=prompt, tool_call=tool_call, tools=self.tools, history=history, details=details, stream=stream,
                                                      **llm_gen_config.model_dump(), **kwargs)

        def _remember_callback(resp_str):
            if do_remember:
                self.remember("user", message)
                self.remember("assistant", resp_str)

        def _add_remember_callback(gen: Generator) -> Generator:
            acc = []
            for ele in gen:
                acc.append(ele)
                yield ele
            resp_str = "".join(acc)
            logger.info(f"agent generate response:{resp_str}")
            _remember_callback("".join(acc))

        if stream:
            content = _add_remember_callback(llm_resp.content)
        else:
            content = llm_resp.content
            logger.info(f"generate response:{content}")
            _remember_callback(content)

        resp = AgentResp(content=content, tool_calls=llm_resp.tool_calls, usage=llm_resp.usage, references=chunks, details=llm_resp.details)
        return resp

    def remember(self, role: str, message: str):
        logger.debug(f"remembering {role=}, {message=}")
        self.memory.remember(role, message)

    def clear_memory(self):
        # logger.info("clearing memory")
        self.memory.clear()


if __name__ == "__main__":
    llm_config = dict(model_cls="GLM", name="glm", version="chatglm_turbo")
    memory_config = dict(size=10)
    agent = XAgent(name="xagent", llm_config=llm_config, memory_config=memory_config)
    resp = agent.chat("推荐三首歌", stream=True)
    for item in resp:
        print(item, end="")
    resp = agent.chat("其中第二首是谁唱的？", stream=True)
    for item in resp:
        print(item, end="")
