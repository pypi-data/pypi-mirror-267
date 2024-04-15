#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/12 15:00:12
@Author  :   ChenHao
@Description  :  doc/docx文档解析
@Contact :   jerrychen1990@gmail.com
'''



from typing import Iterable
from xagents.config import *
from xagents.loader.common import Chunk, ContentType, AbstractLoader
from loguru import logger



class DOCLoader(AbstractLoader):
    def __init__(self, max_page:int=None, **kwargs):
        """构建pdf加载器

        Args:
            max_page (int, optional): 最大页数. Defaults to None：不限定页数
            extract_images (bool, optional): 是否使用ocr抽取其中的图片. Defaults to False.
        """
        super().__init__(**kwargs)
        self.max_page = max_page


    def load(self, file_path: str) -> Iterable[Chunk]:
        from langchain_community.document_loaders import Docx2txtLoader
        # from langchain_community.document_loaders import UnstructuredWordDocumentLoader




        logger.info(f"loading pdf file {file_path}")
        loader = Docx2txtLoader(file_path)
        pages = loader.lazy_load()
        idx = 0
        for page in pages:
            idx +=1
            if self.max_page and idx > self.max_page:
                break
            chunk = Chunk(content=page.page_content, page_idx=idx, content_type=ContentType.TEXT)
            yield chunk
