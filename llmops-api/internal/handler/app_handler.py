#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/29 14:59
@Author  : thezehui@gmail.com
@File    : app_handler.py
"""
import os
import uuid
from uuid import UUID
from dataclasses import dataclass

from flask import request
from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from openai import OpenAI

from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message
from langchain_core.prompts import ChatPromptTemplate


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已经成功创建，id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"应用已经成功获取，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，修改的名字是:{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，id为:{app.id}")

    def debug(self, app_id: UUID):
        """聊天接口"""
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)
        # query = request.json.get("query")

        # # 2.构建OpenAI客户端，并发起请求
        # client = OpenAI(
        #     api_key=os.getenv("OPENAI_API_KEY"),
        #     base_url=os.getenv("OPENAI_API_BASE"),
        # )

        # 3.得到请求响应，然后将OpenAI的响应传递给前端
        # completion = client.chat.completions.create(
        #     model="gpt-3.5-turbo-16k",
        #     messages=[
        #         {"role": "system", "content": "你是OpenAI开发的聊天机器人，请根据用户的输入回复对应的信息"},
        #         {"role": "user", "content": req.query.data},
        #     ]
        # )
        # content = completion.choices[0].message.content

        # 2.构建组件
        prompt = ChatPromptTemplate.from_template("{query}")
        llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
        parser = StrOutputParser()

        # ai_message = llm.invoke(prompt.invoke({"query": req.query.data}))
        # content = parser.invoke(ai_message)

        # 3.构建链
        chain = prompt | llm | parser

        # 4.调用链得到结果
        content = chain.invoke({"query": req.query.data})

        return success_json({"content": content})

    def ping(self):
        # raise FailException("数据未找到")
        return {"ping": "pong"}
