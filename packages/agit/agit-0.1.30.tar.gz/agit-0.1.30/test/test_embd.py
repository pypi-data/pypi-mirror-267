#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/11 11:38:48
@Author  :   ChenHao
@Description  :  测试embedding模型
@Contact :   jerrychen1990@gmail.com
'''


import os
from unittest import TestCase
from agit.embd import EMBD_TYPE, call_embedding
from loguru import logger
from snippets import set_logger


# unit test
class TestEMBD(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start test embd")

    def test_zhipu_api(self):
        # set_logger("dev", "")
        texts = ["你好", "hello"]
        embds = call_embedding(text=texts, model="embedding-2", embd_type=EMBD_TYPE.ZHIPU_API,
                               norm=True, batch_size=4, api_key=os.environ["ZHIPU_API_KEY"])
        logger.info(len(embds))
        self.assertEqual(len(embds), 2)
        import numpy as np
        logger.info(np.linalg.norm(embds[0]))
        self.assertAlmostEqual(np.linalg.norm(embds[0]), 1.0)

        print(embds[0][:4])
        embd = call_embedding(text=texts[0], model="embedding-2", embd_type=EMBD_TYPE.ZHIPU_API,
                              norm=True, batch_size=4, api_key=os.environ["ZHIPU_API_KEY"])
        print(embd[:4])
        self.assertListEqual(embds[0], embd)
