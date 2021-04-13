#!/usr/bin/python

import os
import random
import time
import traceback
from concurrent import futures

import grpc

from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
import demo_pb2_grpc
import demo_pb2

from logger import getJSONLogger
logger = getJSONLogger('adservice-v2-server')


class AdServiceV2(demo_pb2_grpc.AdServiceV2Servicer, health_pb2_grpc.HealthServicer):
    def __init__(self):
        self.channel = grpc.insecure_channel(os.environ["PRODUCT_CATALOG_SERVICE_ADDR"])
        self.stub = demo_pb2_grpc.ProductCatalogServiceStub(self.channel)

    def GetAds(self, request, context):
        request = demo_pb2.Empty()
        products = self.stub.ListProducts(request).products
        ads = [demo_pb2.Ad(redirect_url=random.choice(products).id, text="AdV2 - Items with 25% discount!")]
        return demo_pb2.AdResponse(ads=ads)

    # Uncomment to enable the HealthChecks for the Ad service
    # Note: These are needed for the liveness and readiness probes
    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING)
    
    def Watch(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.UNIMPLEMENTED)


if __name__ == "__main__":
    logger.info("initializing adservice-v2")

    # create gRPC server, add the Ad-v2 service and start it
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    service = AdServiceV2()
    demo_pb2_grpc.add_AdServiceV2Servicer_to_server(service, server)
    health_pb2_grpc.add_HealthServicer_to_server(service, server)
    server.add_insecure_port('[::]:9556')
    server.start()
    server.wait_for_termination()
