# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import typing
import socket
import itertools

import grpc

from contextvars import ContextVar

from .server import GRPCServer, Router
from .client import GRPCClient

from ...extend.asyncio.base import Utils
from ...extend.asyncio.command import MainProcess, SubProcess


GRPC_UDS_ENTRYPOINT = r'/tmp/grpc_balance_{}.sock'


class GrpcRequestInterceptor(grpc.aio.ServerInterceptor):

    def __init__(self, clients: typing.List[GRPCClient]):

        self._method_context: ContextVar = ContextVar[str](r'grpc_method_context', default=None)

        self._terminator: grpc.RpcMethodHandler = grpc.unary_unary_rpc_method_handler(self._terminate)

        self._clients: typing.Iterator[GRPCClient] = itertools.cycle(clients)

    async def _terminate(self, request: bytes, context: grpc.aio.ServicerContext) -> typing.Any:

        client = next(self._clients)
        method = self._method_context.get()

        return await client.unary_unary(method, request)

    async def intercept_service(
            self,
            continuation: typing.Callable[[grpc.HandlerCallDetails], typing.Awaitable[grpc.RpcMethodHandler]],
            handler_call_details: grpc.HandlerCallDetails
    ) -> grpc.RpcMethodHandler:

        self._method_context.set(getattr(handler_call_details, r'method'))

        return self._terminator


class GRPCMainProcess(MainProcess):

    def __init__(
            self, address: typing.Union[str, typing.Tuple[str, int]], routers: typing.List[Router],
            worker: typing.Type[r'GRPCWorker'], sub_process_num: int, *,
            grpc_family: int = socket.AF_INET, grpc_server_credentials: typing.Optional[grpc.ServerCredentials] = None,
            cpu_affinity: bool = False, join_timeout: int = 10
    ):

        super().__init__(
            worker.create, sub_process_num,
            cpu_affinity=cpu_affinity, join_timeout=join_timeout,
            routers=routers
        )

        self._grpc_server: typing.Optional[GRPCServer] = None
        self._grpc_clients: typing.List[GRPCClient] = []

        self._grpc_address: typing.Union[str, typing.Tuple[str, int]] = address
        self._grpc_family: int = grpc_family
        self._grpc_server_credentials: typing.Optional[grpc.ServerCredentials] = grpc_server_credentials

    async def _initialize_grpc(self):

        self._grpc_server = GRPCServer(
            interceptors=[GrpcRequestInterceptor(self._grpc_clients)],
            request_deserializer=None,
            response_serializer=None
        )

        for _idx in range(self._sub_process_num):

            _grpc_uds_entrypoint = GRPC_UDS_ENTRYPOINT.format(_idx)

            grpc_client = GRPCClient(request_serializer=None, response_deserializer=None)
            await grpc_client.open([f'unix:{_grpc_uds_entrypoint}'])

            self._grpc_clients.append(grpc_client)

        await self._grpc_server.start(self._grpc_address, self._grpc_family, self._grpc_server_credentials)

    async def _release_grpc(self):

        await self._grpc_server.stop()

        for _client in self._grpc_clients:
            await _client.close()

    async def _execute(self):

        self._fill_process()

        await self._initialize_grpc()

        while self._check_process():
            await Utils.sleep(1)

        await self._release_grpc()


class GRPCWorker(SubProcess):

    def __init__(self, process_num: int, routers: typing.List[Router]):

        super().__init__(process_num)

        self._grpc_server: typing.Optional[GRPCServer] = None
        self._grpc_routers: typing.List[Router] = routers

    def close(self, *_):
        Utils.call_soon(self._grpc_server.stop)

    async def _execute(self):

        grpc_uds_entrypoint = GRPC_UDS_ENTRYPOINT.format(self._process_num)

        if os.path.exists(grpc_uds_entrypoint):
            os.remove(grpc_uds_entrypoint)

        self._grpc_server = GRPCServer()

        for _router in self._grpc_routers:
            self._grpc_server.bind_router(_router)

        await self._grpc_server.start(grpc_uds_entrypoint, family=socket.AF_UNIX)
        await self._grpc_server.wait()
