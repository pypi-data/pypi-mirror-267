"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import prodvana.proto.prodvana.protection.protection_manager_pb2

class ProtectionManagerStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    ConfigureProtection: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.protection.protection_manager_pb2.ConfigureProtectionReq,
        prodvana.proto.prodvana.protection.protection_manager_pb2.ConfigureProtectionResp,
    ]
    ValidateConfigureProtection: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.protection.protection_manager_pb2.ConfigureProtectionReq,
        prodvana.proto.prodvana.protection.protection_manager_pb2.ValidateConfigureProtectionResp,
    ]
    ListProtections: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.protection.protection_manager_pb2.ListProtectionsReq,
        prodvana.proto.prodvana.protection.protection_manager_pb2.ListProtectionsResp,
    ]
    GetProtection: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionReq,
        prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionResp,
    ]
    GetProtectionConfig: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionConfigReq,
        prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionConfigResp,
    ]
    GetProtectionAttachmentConfig: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionAttachmentConfigReq,
        prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionAttachmentConfigResp,
    ]

class ProtectionManagerServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ConfigureProtection(
        self,
        request: prodvana.proto.prodvana.protection.protection_manager_pb2.ConfigureProtectionReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.protection.protection_manager_pb2.ConfigureProtectionResp: ...
    @abc.abstractmethod
    def ValidateConfigureProtection(
        self,
        request: prodvana.proto.prodvana.protection.protection_manager_pb2.ConfigureProtectionReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.protection.protection_manager_pb2.ValidateConfigureProtectionResp: ...
    @abc.abstractmethod
    def ListProtections(
        self,
        request: prodvana.proto.prodvana.protection.protection_manager_pb2.ListProtectionsReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.protection.protection_manager_pb2.ListProtectionsResp: ...
    @abc.abstractmethod
    def GetProtection(
        self,
        request: prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionResp: ...
    @abc.abstractmethod
    def GetProtectionConfig(
        self,
        request: prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionConfigReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionConfigResp: ...
    @abc.abstractmethod
    def GetProtectionAttachmentConfig(
        self,
        request: prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionAttachmentConfigReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.protection.protection_manager_pb2.GetProtectionAttachmentConfigResp: ...

def add_ProtectionManagerServicer_to_server(servicer: ProtectionManagerServicer, server: grpc.Server) -> None: ...
