#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/10/24 11:32
@Author  : thezehui@gmail.com
@File    : agent_queue_manager.py
"""
import queue
import time
from enum import Enum
from queue import Queue
from typing import Generator
from uuid import UUID

from redis import Redis

from internal.entity.conversation_entity import InvokeFrom


class PublishFrom(str, Enum):
    """发布来源，用于记录队列管理器中的发布来源"""
    APPLICATION_MANAGER = 1
    TASK_PIPELINE = 2


class AgentQueueManager:
    """智能体队列管理器"""
    q: Queue  # 队列
    user_id: UUID  # 队列任务归属的用户id
    task_id: UUID  # 本次任务的id
    invoke_from: InvokeFrom
    redis_client: Redis  # redis缓存客户端

    def __init__(
            self,
            user_id: UUID,
            task_id: UUID,
            invoke_from: InvokeFrom,
            redis_client: Redis,
    ) -> None:
        """构造函数，初始化智能体队列管理器"""
        # 1.初始化数据
        self.q = Queue()
        self.user_id = user_id
        self.task_id = task_id
        self.invoke_from = invoke_from
        self.redis_client = redis_client

        # 2.判断用户的类型，目前有账号(Debugger/WebAPP调用)以及终端用户(开放API调用)两种类型
        user_prefix = "account" if invoke_from in [InvokeFrom.WEB_APP, InvokeFrom.DEBUGGER] else "end-user"

        # 3.设置任务对应的缓存键，代表此次任务队列开始
        self.redis_client.setex(
            self._generate_task_belong_cache_key(task_id),
            1800,
            f"{user_prefix}-{str(user_id)}"
        )

    def listen(self) -> Generator:
        """监听队列返回生成式数据"""
        # 1.定义基础数据记录超时时间、开始时间、最后一次ping通时间
        listen_timeout = 600
        start_time = time.time()
        last_ping_time = 0

        # 2.创建循环列表执行死循环监听队列数据
        while True:
            try:
                # 3.从队列中提取数据并检测数据是否存在，如果存在则直接返回
                item = self.q.get(timeout=1)
                if item is None:
                    break

                yield item
            except queue.Empty:
                continue
            finally:
                # 4.计算获取数据的总耗时并判断是否超时，如果超时则往队列添加停止事件
                elapsed_time = time.time() - start_time
                if elapsed_time >= listen_timeout:
                    pass

                # 5.每10秒发起一个ping请求避免接口中断
                if elapsed_time // 10 > last_ping_time:
                    last_ping_time = elapsed_time // 10

    def stop_listen(self) -> None:
        """停止监听队列信息"""
        self.q.put(None)

    def publish(self):
        """发布事件信息到队列中"""
        pass

    def publish_error(self):
        """发布错误信息事件到队列中"""
        pass

    def _is_stopped(self) -> bool:
        """检查任务是否停止"""
        task_stopped_cache_key = self._generate_task_stopped_cache_key(self.task_id)
        result = self.redis_client.get(task_stopped_cache_key)

        if result is not None:
            return True
        return False

    def set_stop_flask(self, task_id: UUID, invoke_from: InvokeFrom, user_id: UUID) -> None:
        """设置任务停止标志"""
        # 1.检测当前任务是否存在，如果不存在则直接结束
        result: bytes = self.redis_client.get(self._generate_task_belong_cache_key(task_id))
        if result is None:
            return

        # 2.查询当前任务和用户的信息是否匹配，如果不匹配则直接结束
        user_prefix = "account" if invoke_from in [InvokeFrom.WEB_APP, InvokeFrom.DEBUGGER] else "end-user"
        if result.decode("utf-8") != f"{user_prefix}-{str(user_id)}":
            return

        # 3.构建停止缓存键，并设置缓存记录，时间为600s
        task_stopped_cache_key = self._generate_task_stopped_cache_key(task_id)
        self.redis_client.setex(task_stopped_cache_key, 600, 1)

    @classmethod
    def _generate_task_belong_cache_key(cls, task_id: UUID) -> str:
        """生成任务专属的缓存键"""
        return f"generate_task_belong:{str(task_id)}"

    @classmethod
    def _generate_task_stopped_cache_key(cls, task_id: UUID) -> str:
        """生成任务已停止的缓存键"""
        return f"generate_task_stopped:{str(task_id)}"
