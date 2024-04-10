"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import prodvana.proto.prodvana.secrets.secrets_manager_pb2

class SecretsManagerStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    ListSecrets: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.ListSecretsReq,
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.ListSecretsResp,
    ]
    ListSecretVersions: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.ListSecretVersionsReq,
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.ListSecretVersionsResp,
    ]
    SetSecret: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.SetSecretReq,
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.SetSecretResp,
    ]
    DeleteSecret: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.DeleteSecretReq,
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.DeleteSecretResp,
    ]
    DeleteSecretVersion: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.DeleteSecretVersionReq,
        prodvana.proto.prodvana.secrets.secrets_manager_pb2.DeleteSecretVersionResp,
    ]

class SecretsManagerServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ListSecrets(
        self,
        request: prodvana.proto.prodvana.secrets.secrets_manager_pb2.ListSecretsReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.secrets.secrets_manager_pb2.ListSecretsResp: ...
    @abc.abstractmethod
    def ListSecretVersions(
        self,
        request: prodvana.proto.prodvana.secrets.secrets_manager_pb2.ListSecretVersionsReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.secrets.secrets_manager_pb2.ListSecretVersionsResp: ...
    @abc.abstractmethod
    def SetSecret(
        self,
        request: prodvana.proto.prodvana.secrets.secrets_manager_pb2.SetSecretReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.secrets.secrets_manager_pb2.SetSecretResp: ...
    @abc.abstractmethod
    def DeleteSecret(
        self,
        request: prodvana.proto.prodvana.secrets.secrets_manager_pb2.DeleteSecretReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.secrets.secrets_manager_pb2.DeleteSecretResp: ...
    @abc.abstractmethod
    def DeleteSecretVersion(
        self,
        request: prodvana.proto.prodvana.secrets.secrets_manager_pb2.DeleteSecretVersionReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.secrets.secrets_manager_pb2.DeleteSecretVersionResp: ...

def add_SecretsManagerServicer_to_server(servicer: SecretsManagerServicer, server: grpc.Server) -> None: ...
