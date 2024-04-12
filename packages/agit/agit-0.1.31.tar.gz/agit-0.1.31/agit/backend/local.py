#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/12 13:32:19
@Author  :   ChenHao
@Description  : 本地模型
@Contact :   jerrychen1990@gmail.com
'''

import requests
from typing import List

from tqdm import tqdm
from snippets import batchify
from loguru import logger


def call_embedding(text: str | List[str], url:str, batch_size=16, norm:bool = True) -> List[float] | List[List[float]]:
    texts = text if isinstance(text, list) else [text]
    batches = batchify(texts, batch_size)
    embeddings = []
    for batch in tqdm(batches):    
        params = dict(texts=batch, norm=norm)
        resp = requests.post(url=url, json=params)
        resp.raise_for_status()
        resp_data = resp.json()["data"]
        # logger.debug(f"{resp_data=}")
        embeddings.extend(resp_data["embeddings"])
    return embeddings if isinstance(text, list) else embeddings[0]



