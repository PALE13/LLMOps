#!/usr/bin/env python
# -*- coding: utf-8 -*-

from langchain_core.pydantic_v1 import Field

from internal.core.workflow.entities.node_entity import BaseNodeData
from internal.core.workflow.entities.variable_entity import VariableEntity, VariableValueType


class TemplateTransformNodeData(BaseNodeData):
    """模板转换节点数据"""
    template: str = ""  # 需要拼接转换的字符串模板
    inputs: list[VariableEntity] = Field(default_factory=list)  # 输入列表信息
    outputs: list[VariableEntity] = Field(
        exclude=True,
        default_factory=lambda: [
            VariableEntity(name="output", value={"type": VariableValueType.GENERATED})
        ]
    )
