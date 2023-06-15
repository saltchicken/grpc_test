from __future__ import print_function

import logging

import grpc
import proto_pb2
import proto_pb2_grpc


def run():
    with open('../roots.pem', 'rb') as f:
        creds = grpc.ssl_channel_credentials(f.read())
    with grpc.secure_channel('192.168.1.100:50051', creds) as channel:
    # with grpc.insecure_channel('192.168.1.5:50051') as channel:
    # with grpc.insecure_channel('127.0.0.1:50051') as channel:
        stub = proto_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(proto_pb2.HelloRequest(name='you'))
        print(response.message)
        response = stub.SayHelloAgain(proto_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
