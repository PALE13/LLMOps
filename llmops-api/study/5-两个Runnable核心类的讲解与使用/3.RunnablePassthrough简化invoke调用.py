#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/10 18:05
@Author  : thezehui@gmail.com
@File    : 3.RunnablePassthrough简化invoke调用.py
"""
from operator import itemgetter

import dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def retrieval(query: str) -> str:
    """一个模拟的检索器函数"""
    print("正在检索:", query)
    return "我是慕小课"


# 1.编排prompt
prompt = ChatPromptTemplate.from_template("""请根据用户的问题回答，可以参考对应的上下文进行生成。

<context>
{context}
</context>

用户的提问是: {query}""")

# 2.构建大语言模型
llm = ChatOpenAI(model="gpt-3.5-turbo-16k")

# 3.输出解析器
parser = StrOutputParser()

# 4.构建链
# chain = RunnableParallel(
#     context=retrieval,
#     query=RunnablePassthrough()
# ) | prompt | llm | parser

# RunnablePassthrough是获取整个输入的内容，字符春或者字典都可以
chain = {"query":RunnablePassthrough()} | prompt | llm | parser
content = chain.invoke("你好，我是谁?")
print(content)

# 如果想在传递的数据中添加其他数字，可以使用assign方法
chain = RunnablePassthrough.assign(context=lambda x: retrieval(x["query"])) | prompt | llm | parser
# 5.调用链
content = chain.invoke({"query": "你好，我是谁?"})

print(content)
