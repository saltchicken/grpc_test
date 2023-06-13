from concurrent import futures
import logging, time

import grpc
import proto_pb2
import proto_pb2_grpc


class Greeter(proto_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        tic = time.time()
        time.sleep(2)
        toc = time.time()
        return proto_pb2.HelloReply(message=f'{toc-tic}')
    def SayHelloAgain(self, request, context):
        return proto_pb2.HelloReply(message=f'Hello again, {request.name}!')


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
