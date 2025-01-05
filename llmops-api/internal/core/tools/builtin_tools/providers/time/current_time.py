#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any

from langchain_core.tools import BaseTool, StructuredTool


def get_current_time() -> str:
    """获取当前系统的时间并进行格式化后返回"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")


def current_time(**kwargs) -> BaseTool:
    """返回获取当前时间的LangChain工具"""
    return StructuredTool.from_function(
        func=get_current_time,
        name = "current_time",
        description = "一个用于获取当前时间的工具",
    )

