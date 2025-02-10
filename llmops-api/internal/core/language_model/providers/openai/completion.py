from internal.core.language_model.entities.model_entity import BaseLanguageModel

from langchain_openai import OpenAI


class Completion(OpenAI, BaseLanguageModel):
    """OpenAI聊天模型基类"""
    pass