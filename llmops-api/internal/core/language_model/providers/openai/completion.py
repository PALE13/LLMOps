#!/usr/bin/env python
# -*- coding: utf-8 -*-

from langchain_openai import OpenAI

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class Completion(OpenAI, BaseLanguageModel):
    """OpenAI聊天模型基类"""
    pass
