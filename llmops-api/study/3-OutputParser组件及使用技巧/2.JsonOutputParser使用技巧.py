#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/10 1:33
@Author  : thezehui@gmail.com
@File    : 2.JsonOutputParser使用技巧.py
"""
import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


# 1.创建一个json数据结构，用于告诉大语言模型这个json长什么样子
class Joke(BaseModel):
    # 冷笑话
    joke: str = Field(description="回答用户的冷笑话")
    # 冷笑话的笑点
    punchline: str = Field(description="这个冷笑话的笑点")


parser = JsonOutputParser(pydantic_object=Joke)

# 2.构建一个提示模板
prompt = ChatPromptTemplate.from_template("请根据用户的提问进行回答。\n{format_instructions}\n{query}").partial(
    format_instructions=parser.get_format_instructions())

print(prompt)

# 3.构建一个大语言模型
llm = ChatOpenAI(model="gpt-3.5-turbo-16k")

# 4.传递提示并进行解析
joke = parser.invoke(llm.invoke(prompt.invoke({"query": "请讲一个关于程序员的冷笑话"})))

print(type(joke))
print(joke.get("punchline"))
print(joke)
