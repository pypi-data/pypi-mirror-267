"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import prodvana.proto.prodvana.service.service_manager_pb2

class ServiceManagerStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    ConfigureService: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.ConfigureServiceReq,
        prodvana.proto.prodvana.service.service_manager_pb2.ConfigureServiceResp,
    ]
    ValidateConfigureService: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.ConfigureServiceReq,
        prodvana.proto.prodvana.service.service_manager_pb2.ValidateConfigureServiceResp,
    ]
    ListServiceConfigVersions: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.ListServiceConfigVersionsReq,
        prodvana.proto.prodvana.service.service_manager_pb2.ListServiceConfigVersionsResp,
    ]
    GetServiceConfig: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceConfigReq,
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceConfigResp,
    ]
    """unparametrized configs"""
    GenerateVersionName: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.GenerateVersionNameReq,
        prodvana.proto.prodvana.service.service_manager_pb2.GenerateVersionNameResp,
    ]
    ApplyParameters: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.ApplyParametersReq,
        prodvana.proto.prodvana.service.service_manager_pb2.ApplyParametersResp,
    ]
    ValidateApplyParameters: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.ApplyParametersReq,
        prodvana.proto.prodvana.service.service_manager_pb2.ValidateApplyParametersResp,
    ]
    GetMaterializedConfig: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.GetMaterializedConfigReq,
        prodvana.proto.prodvana.service.service_manager_pb2.GetMaterializedConfigResp,
    ]
    ListMaterializedConfigVersions: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.ListMaterializedConfigVersionsReq,
        prodvana.proto.prodvana.service.service_manager_pb2.ListMaterializedConfigVersionsResp,
    ]
    DeleteService: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.DeleteServiceReq,
        prodvana.proto.prodvana.service.service_manager_pb2.DeleteServiceResp,
    ]
    ListServices: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.ListServicesReq,
        prodvana.proto.prodvana.service.service_manager_pb2.ListServicesResp,
    ]
    ListCommits: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.ListCommitsReq,
        prodvana.proto.prodvana.service.service_manager_pb2.ListCommitsResp,
    ]
    GetService: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceReq,
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceResp,
    ]
    ListServiceInstances: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.ListServiceInstancesReq,
        prodvana.proto.prodvana.service.service_manager_pb2.ListServiceInstancesResp,
    ]
    GetServiceInstance: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceInstanceReq,
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceInstanceResp,
    ]
    GetServiceMetrics: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceMetricsReq,
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceMetricsResp,
    ]
    GetServiceInsights: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceInsightsReq,
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceInsightsResp,
    ]
    SnoozeServiceInsight: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.SnoozeServiceInsightReq,
        prodvana.proto.prodvana.service.service_manager_pb2.SnoozeServiceInsightResp,
    ]
    GetServiceMetadata: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceMetadataReq,
        prodvana.proto.prodvana.service.service_manager_pb2.GetServiceMetadataResp,
    ]
    SetServiceMetadata: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.SetServiceMetadataReq,
        prodvana.proto.prodvana.service.service_manager_pb2.SetServiceMetadataResp,
    ]
    SetServiceConvergenceMode: grpc.UnaryUnaryMultiCallable[
        prodvana.proto.prodvana.service.service_manager_pb2.SetServiceConvergenceModeReq,
        prodvana.proto.prodvana.service.service_manager_pb2.SetServiceConvergenceModeResp,
    ]

class ServiceManagerServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ConfigureService(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.ConfigureServiceReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.ConfigureServiceResp: ...
    @abc.abstractmethod
    def ValidateConfigureService(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.ConfigureServiceReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.ValidateConfigureServiceResp: ...
    @abc.abstractmethod
    def ListServiceConfigVersions(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.ListServiceConfigVersionsReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.ListServiceConfigVersionsResp: ...
    @abc.abstractmethod
    def GetServiceConfig(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.GetServiceConfigReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.GetServiceConfigResp:
        """unparametrized configs"""
    @abc.abstractmethod
    def GenerateVersionName(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.GenerateVersionNameReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.GenerateVersionNameResp: ...
    @abc.abstractmethod
    def ApplyParameters(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.ApplyParametersReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.ApplyParametersResp: ...
    @abc.abstractmethod
    def ValidateApplyParameters(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.ApplyParametersReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.ValidateApplyParametersResp: ...
    @abc.abstractmethod
    def GetMaterializedConfig(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.GetMaterializedConfigReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.GetMaterializedConfigResp: ...
    @abc.abstractmethod
    def ListMaterializedConfigVersions(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.ListMaterializedConfigVersionsReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.ListMaterializedConfigVersionsResp: ...
    @abc.abstractmethod
    def DeleteService(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.DeleteServiceReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.DeleteServiceResp: ...
    @abc.abstractmethod
    def ListServices(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.ListServicesReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.ListServicesResp: ...
    @abc.abstractmethod
    def ListCommits(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.ListCommitsReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.ListCommitsResp: ...
    @abc.abstractmethod
    def GetService(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.GetServiceReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.GetServiceResp: ...
    @abc.abstractmethod
    def ListServiceInstances(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.ListServiceInstancesReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.ListServiceInstancesResp: ...
    @abc.abstractmethod
    def GetServiceInstance(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.GetServiceInstanceReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.GetServiceInstanceResp: ...
    @abc.abstractmethod
    def GetServiceMetrics(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.GetServiceMetricsReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.GetServiceMetricsResp: ...
    @abc.abstractmethod
    def GetServiceInsights(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.GetServiceInsightsReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.GetServiceInsightsResp: ...
    @abc.abstractmethod
    def SnoozeServiceInsight(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.SnoozeServiceInsightReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.SnoozeServiceInsightResp: ...
    @abc.abstractmethod
    def GetServiceMetadata(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.GetServiceMetadataReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.GetServiceMetadataResp: ...
    @abc.abstractmethod
    def SetServiceMetadata(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.SetServiceMetadataReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.SetServiceMetadataResp: ...
    @abc.abstractmethod
    def SetServiceConvergenceMode(
        self,
        request: prodvana.proto.prodvana.service.service_manager_pb2.SetServiceConvergenceModeReq,
        context: grpc.ServicerContext,
    ) -> prodvana.proto.prodvana.service.service_manager_pb2.SetServiceConvergenceModeResp: ...

def add_ServiceManagerServicer_to_server(servicer: ServiceManagerServicer, server: grpc.Server) -> None: ...
