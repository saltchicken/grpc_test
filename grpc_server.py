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
    with open('../csr.pem', 'rb') as f:
        server_crt_data = f.read()
    with open('../certificate.pem', 'rb') as f:
        server_key_data = f.read()
    credentials = grpc.ssl_server_credentials(
        [(server_key_data, server_crt_data)],
        root_certificates=None,
        require_client_auth=True  # Enable client authentication
    )
    # server.add_insecure_port('[::]:' + port)
    server.add_secure_port('[::]:' + port, credentials)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
