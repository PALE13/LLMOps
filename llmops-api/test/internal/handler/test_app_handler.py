#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from pkg.response import HttpCode


class TestAppHandler:
    """app控制器的测试类"""

    @pytest.mark.parametrize(
        "app_id, query",
        [
            ("1a95b17a-7cc8-4c6e-9c31-1dc2534ca869", None),
            ("1a95b17a-7cc8-4c6e-9c31-1dc2534ca869", "你好，你是?")
        ]
    )
    def test_completion(self, app_id, query, client):
        resp = client.post(f"/apps/{app_id}/debug", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
