#!/usr/bin/env python
# -*- coding: utf-8 -*-



from langchain_community.utilities import  SearchApiAPIWrapper
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool, StructuredTool

from internal.lib.helper import add_attribute


class GoogleSerperArgsSchema(BaseModel):
    """谷歌SerperAPI搜索参数描述"""
    query: str = Field(description="需要检索查询的语句")

def get_search(query: str) -> dict:
    search = SearchApiAPIWrapper()
    return search.results(query)


@add_attribute("args_schema", GoogleSerperArgsSchema)
def google_serper(**kwargs) -> BaseTool:
    """谷歌Serp搜索"""
    google_search = StructuredTool.from_function(
        func=get_search,
        name="google_serper",
        description="一个低成本的谷歌搜索API,当你需要回答有关时事的问题时，可以调用该工具,该工具的输入是搜索查询语句。",
        args_schema=GoogleSerperArgsSchema,
    )
    return google_search




