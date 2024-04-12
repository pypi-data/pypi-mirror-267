import re
import threading
import warnings
import logging
from typing import Optional

import google.protobuf.empty_pb2
import grpc
import random

from . import types
from . import vector_db_pb2
from . import vector_db_pb2_grpc

empty = google.protobuf.empty_pb2.Empty()

logger = logging.getLogger(__name__)

class ChannelAndEndpoints(object):
    def __init__(
        self, channel: grpc.aio.Channel, endpoints: vector_db_pb2.ServerEndpointList
    ) -> None:
        self.channel = channel
        self.endpoints = endpoints


class VectorDbChannelProvider(object):
    """Proximus Channel Provider"""
    def __init__(
        self, seeds: tuple[types.HostPort, ...], listener_name: Optional[str] = None, is_loadbalancer: Optional[bool] = False
    ) -> None:
        if not seeds:
            raise Exception("at least one seed host needed")
        self._nodeChannels: dict[int, ChannelAndEndpoints] = {}
        self._seedChannels: dict[grpc.aio.Channel] = {}
        self._closed = False
        self._clusterId = 0
        self.seeds = seeds
        self.listener_name = listener_name
        self._is_loadbalancer = is_loadbalancer
        self._seedChannels = [
            self._create_channel_from_host_port(seed) for seed in self.seeds
        ]
        self._tend()

    async def close(self):
        self._closed = True
        for channel in self._seedChannels:
            await channel.close()

        for k, channelEndpoints in self._nodeChannels.items():
            if channelEndpoints.channel:
                await channelEndpoints.channel.close()

    def get_channel(self) -> grpc.Channel:
        if not self._is_loadbalancer:
            discovered_channels: list[ChannelAndEndpoints] = list(
                self._nodeChannels.values())
            if len(discovered_channels) <= 0:
                return self._seedChannels[0]


            # Return a random channel.
            channel = random.choice(discovered_channels).channel
            if channel:
                return channel

        return self._seedChannels[0]

    def _tend(self):
        if self._is_loadbalancer:
            # Skip tend if we are behind a load-balancer
            return

        # TODO: Worry about thread safety
        temp_endpoints: dict[int, vector_db_pb2.ServerEndpointList] = {}

        if self._closed:
            return

        try:
            update_endpoints = False
            channels = self._seedChannels + [
                x.channel for x in self._nodeChannels.values()
            ]
            for seedChannel in channels:
                try:
                    stub = vector_db_pb2_grpc.ClusterInfoStub(seedChannel)
                    newClusterId = stub.GetClusterId(empty).id

                    if newClusterId == self._clusterId:
                        continue

                    update_endpoints = True
                    self._clusterId = newClusterId
                    endpoints = stub.GetClusterEndpoints(
                        vector_db_pb2.ClusterNodeEndpointsRequest(
                            listenerName=self.listener_name
                        )
                    ).endpoints

                    if len(endpoints) > len(temp_endpoints):
                        temp_endpoints = endpoints

                except Exception as e:
                    logger.debug("failure tending cluster endpoints: " + str(e))

            if update_endpoints:
                for node, newEndpoints in temp_endpoints.items():
                    channel_endpoints = self._nodeChannels.get(node)
                    add_new_channel = True
                    if channel_endpoints:
                        # We have this node. Check if the endpoints changed.
                        if channel_endpoints.endpoints == newEndpoints:
                            # Nothing to be done for this node
                            add_new_channel = False
                        else:
                            # TODO: Wait for all calls to drain
                            channel_endpoints.channel.close()
                            add_new_channel = True

                    if add_new_channel:
                        # We have discovered a new node
                        new_channel = self._create_channel_from_server_endpoint_list(
                            newEndpoints
                        )
                        self._nodeChannels[node] = ChannelAndEndpoints(
                            new_channel, newEndpoints
                        )

                for node, channel_endpoints in self._nodeChannels.items():
                    if not temp_endpoints.get(node):
                        # TODO: Wait for all calls to drain
                        channel_endpoints.channel.close()
                        del self._nodeChannels[node]

        except Exception as e:
            logger.debug("failure tending: " + str(e))

        if not self._closed:
            # TODO: check tend interval.
            threading.Timer(1, self._tend).start()

    def _create_channel_from_host_port(self, host: types.HostPort) -> grpc.aio.Channel:
        return self._create_channel(host.host, host.port, host.isTls)

    def _create_channel_from_server_endpoint_list(
        self, endpoints: vector_db_pb2.ServerEndpointList
    ) -> grpc.aio.Channel:
        # TODO: Create channel with all endpoints
        for endpoint in endpoints.endpoints:
            if ":" in endpoint.address:
                # TODO: Ignoring IPv6 for now. Needs fix
                continue
            try:
                return self._create_channel(
                    endpoint.address, endpoint.port, endpoint.isTls
                )
            except Exception as e:
                logger.debug("failure creating channel: " + str(e))

    def _create_channel(self, host: str, port: int, isTls: bool) -> grpc.aio.Channel:
        # TODO: Take care of TLS
        host = re.sub(r"%.*", "", host)
        return grpc.aio.insecure_channel(f"{host}:{port}")