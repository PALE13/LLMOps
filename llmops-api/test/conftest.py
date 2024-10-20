#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/4 16:39
@Author  : thezehui@gmail.com
@File    : conftest.py.py
"""
import pytest

from app.http.app import app


@pytest.fixture
def client():
    """获取Flask应用的测试应用，并返回"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
