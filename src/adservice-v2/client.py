#!/usr/bin/python

import sys
import grpc

from logger import getJSONLogger
logger = getJSONLogger('adservice-v2-server')
import demo_pb2_grpc
import demo_pb2
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

if __name__ == "__main__":

    # set up server stub
    # ensure the service is listening to port 9556
    channel = grpc.insecure_channel('localhost:9556')
    # stub = demo_pb2_grpc.AdServiceV2Stub(channel)
    # stub = health_pb2_grpc.HealthStub(channel)
    # stub = demo_pb2_grpc.ProductCatalogServiceStub(channel)
    
    request = demo_pb2.AdRequest(context_keys=["1", "2"])
    # request = health_pb2.HealthCheckRequest()
    # request = demo_pb2.Empty()
    
    # make a call to server and return a response
    response = stub.GetAds(request)
    # response = stub.ListProducts(request)
    # response = stub.Check(request)
    logger.info(response)
