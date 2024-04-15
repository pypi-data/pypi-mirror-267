#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/12 15:02:40
@Author  :   ChenHao
@Description  :   测试loader
@Contact :   jerrychen1990@gmail.com
'''
from unittest import TestCase
from loguru import logger
from snippets import set_logger
from xagents.loader.api import load_file
from xagents.config import *


# unit test
class TestEMBD(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start test embd")
        
    def test_load_pdf(self):
        file_path=os.path.join(DATA_DIR,"kb_file", "multi_column.pdf") 
        pages = load_file(file_path, max_page=4)
        for page in pages:
            logger.info(f"{page=}")

    def test_load_doc(self):
        file_path=os.path.join(DATA_DIR,"kb_file", "Xagents中间件.docx") 
        pages = load_file(file_path, max_page=4)
        for page in pages:
            logger.info(f"{page=}")
        
