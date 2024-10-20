#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/10 11:06
@Author  : thezehui@gmail.com
@File    : 2.LCEL表达式简化版本.py
"""

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
parser = StrOutputParser()

# 2.创建链
chain = prompt | llm | parser

# 3.调用链得到结果
print(chain.invoke({"query": "请讲一个程序员的冷笑话"}))
