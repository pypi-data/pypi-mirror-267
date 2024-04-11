#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/10 11:04:36
@Author  :   ChenHao
@Description  :   
@Contact :   jerrychen1990@gmail.com
'''

from typing import Generator, Optional
from pydantic import BaseModel, Field


class Usage(BaseModel):
    prompt_tokens:Optional[int] = Field(description="输入token数量")
    completion_tokens:Optional[int] = Field(description="输出token数量")
    total_tokens:Optional[int] = Field(description="输入输出token数量总和")
    
class Perf(BaseModel):
    first_token_latency:Optional[float] = Field(description="第一个token的延迟,单位s")
    total_cost:float = Field(description="输出所有内容总耗时,单位s")
    decode_speed:Optional[float] = Field(description="解码速度, tokens/s")
    encode_speed:Optional[float] = Field(description="编码速度, tokens/s") 
    total_speed:float = Field(description="编码和解码的平均速度, tokens/s")
   


class LLMResp(BaseModel):
    content:str|Generator = Field(description="模型的回复，字符串或者生成器")
    usage:Optional[Usage] = Field(description="token使用情况")
    perf:Optional[Perf] = Field(description="性能指标", default=None)
    details:Optional[dict] = Field(description="请求模型的细节信息", default=dict())    
