#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/8 22:11
@Author  : thezehui@gmail.com
@File    : 4.复用提示模板.py
"""
from langchain_core.prompts import PromptTemplate, PipelinePromptTemplate

full_template = PromptTemplate.from_template("""{instruction}

{example}

{start}""")

# 描述模板
instruction_prompt = PromptTemplate.from_template("你正在模拟{person}")

# 示例模板
example_prompt = PromptTemplate.from_template("""下面是一个交互例子：

Q: {example_q}
A: {example_a}""")

# 开始模板
start_prompt = PromptTemplate.from_template("""现在，你是一个真实的人，请回答用户的问题:

Q: {input}
A:""")

pipeline_prompts = [
    ("instruction", instruction_prompt),
    ("example", example_prompt),
    ("start", start_prompt)
]

pipeline_prompt = PipelinePromptTemplate(
    final_prompt=full_template,
    pipeline_prompts=pipeline_prompts,
)

print(pipeline_prompt.invoke({
    "person": "雷军",
    "example_q": "你最喜欢的汽车是什么?",
    "example_a": "小米su7",
    "input": "你最喜欢的手机是什么?"
}).to_string())
