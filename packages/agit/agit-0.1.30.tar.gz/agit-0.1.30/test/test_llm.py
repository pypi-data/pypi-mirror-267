#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/11 10:52:54
@Author  :   ChenHao
@Description  : 测试llm接口
@Contact :   jerrychen1990@gmail.com
'''

import json
from unittest import TestCase
from agit.llm import call_llm
from loguru import logger
from snippets import set_logger


# unit test
class TestLLM(TestCase):
    
    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start llm")

    def test_zhipu_api(self):
        # set_logger("dev", "")
        messages = [dict(role="user", content="你好呀，你是谁")]
        _system = "请用英语回答我的问题，你的名字叫XAgent"
        # 测试zhipu api
        resp = call_llm(messages, model="glm-3-turbo", system=_system, temperature=0.7, top_p=0.95, max_tokens=100, stream=False)
        logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.content)        
        self.assertIsNotNone(resp.usage)        


        ## 流式
        resp = call_llm(messages, model="glm-3-turbo", system=_system, temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=True)
        for chunk in resp.content:
            logger.info(chunk)
        logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.usage)
