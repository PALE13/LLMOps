#!/usr/bin/env python
# -*- coding: utf-8 -*-


import weaviate
from injector import inject
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_weaviate import WeaviateVectorStore
from weaviate import WeaviateClient
from weaviate.auth import  AuthApiKey
from weaviate.collections import Collection
from .embeddings_service import EmbeddingsService



# 向量数据库的集合名字
COLLECTION_NAME = "Dataset"


@inject
class VectorDatabaseService:
    """向量数据库服务"""
    client: WeaviateClient
    vector_store: WeaviateVectorStore
    embeddings_service: EmbeddingsService

    def __init__(self, embeddings_service: EmbeddingsService):
        """构造函数，完成向量数据库服务的客户端+LangChain向量数据库实例的创建"""
        # 1.赋值embeddings_service
        self.embeddings_service = embeddings_service
        # 2.创建/连接weaviate向量数据库
        self.client = weaviate.connect_to_custom(
            skip_init_checks=False,
            http_host="60.205.122.6",
            http_port=8080,
            http_secure=False,
            grpc_host="60.205.122.6",
            grpc_port=50051,
            grpc_secure=False,
            # 对应AUTHENTICATION_APIKEY_ALLOWED_KEYS中的密钥
            # 注意：此处只需要密钥即可，不需要用户名称
            auth_credentials=AuthApiKey("123456")
        )
        #  创建/连接远程weaviate向量数据库
        # self.client = weaviate.connect_to_wcs(
        #     cluster_url="https://9vvgkr6tadte58z87gma.c0.asia-southeast1.gcp.weaviate.cloud",
        #     auth_credentials=AuthApiKey("aHNHUyfdzKtJjiswAXmaRPNoEPEigUDM7xk6"),
        #     additional_config=AdditionalConfig(timeout=Timeout(init=10)),
        # )


        # 3.创建LangChain向量数据库
        self.vector_store = WeaviateVectorStore(
            client=self.client,
            index_name=COLLECTION_NAME,
            text_key="text",
            embedding=self.embeddings_service.embeddings,
        )

    def get_retriever(self) -> VectorStoreRetriever:
        """获取检索器"""
        return self.vector_store.as_retriever()


    @property
    def collection(self) -> Collection:
        return self.client.collections.get(COLLECTION_NAME)





