# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from prodvana.proto.prodvana.organization import organization_manager_pb2 as prodvana_dot_organization_dot_organization__manager__pb2


class OrganizationManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetOrganization = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/GetOrganization',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationResp.FromString,
                )
        self.GetOrganizationMetrics = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/GetOrganizationMetrics',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetricsReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetricsResp.FromString,
                )
        self.GetOrganizationInsights = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/GetOrganizationInsights',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationInsightsReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationInsightsResp.FromString,
                )
        self.SnoozeOrganizationInsight = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/SnoozeOrganizationInsight',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.SnoozeOrganizationInsightReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.SnoozeOrganizationInsightResp.FromString,
                )
        self.GetOrganizationMetadata = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/GetOrganizationMetadata',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetadataReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetadataResp.FromString,
                )
        self.SetOrganizationMetadata = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/SetOrganizationMetadata',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationMetadataReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationMetadataResp.FromString,
                )
        self.GetUser = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/GetUser',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetUserReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetUserResp.FromString,
                )
        self.GetOrganizationSubscriptionStatus = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/GetOrganizationSubscriptionStatus',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSubscriptionStatusReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSubscriptionStatusResp.FromString,
                )
        self.GetOrganizationSettings = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/GetOrganizationSettings',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSettingsReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSettingsResp.FromString,
                )
        self.SetOrganizationSettings = channel.unary_unary(
                '/prodvana.organization.OrganizationManager/SetOrganizationSettings',
                request_serializer=prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationSettingsReq.SerializeToString,
                response_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationSettingsResp.FromString,
                )


class OrganizationManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetOrganization(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrganizationMetrics(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrganizationInsights(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SnoozeOrganizationInsight(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrganizationMetadata(self, request, context):
        """Get org metadata, useful for constructing edit workflows for metadata
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetOrganizationMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUser(self, request, context):
        """Get a user in an organization, will return NOT_FOUND if the user is eitehr missing or not in an organization
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrganizationSubscriptionStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrganizationSettings(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetOrganizationSettings(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrganizationManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetOrganization': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrganization,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationResp.SerializeToString,
            ),
            'GetOrganizationMetrics': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrganizationMetrics,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetricsReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetricsResp.SerializeToString,
            ),
            'GetOrganizationInsights': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrganizationInsights,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationInsightsReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationInsightsResp.SerializeToString,
            ),
            'SnoozeOrganizationInsight': grpc.unary_unary_rpc_method_handler(
                    servicer.SnoozeOrganizationInsight,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.SnoozeOrganizationInsightReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.SnoozeOrganizationInsightResp.SerializeToString,
            ),
            'GetOrganizationMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrganizationMetadata,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetadataReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetadataResp.SerializeToString,
            ),
            'SetOrganizationMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.SetOrganizationMetadata,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationMetadataReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationMetadataResp.SerializeToString,
            ),
            'GetUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUser,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetUserReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetUserResp.SerializeToString,
            ),
            'GetOrganizationSubscriptionStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrganizationSubscriptionStatus,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSubscriptionStatusReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSubscriptionStatusResp.SerializeToString,
            ),
            'GetOrganizationSettings': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrganizationSettings,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSettingsReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSettingsResp.SerializeToString,
            ),
            'SetOrganizationSettings': grpc.unary_unary_rpc_method_handler(
                    servicer.SetOrganizationSettings,
                    request_deserializer=prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationSettingsReq.FromString,
                    response_serializer=prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationSettingsResp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'prodvana.organization.OrganizationManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrganizationManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetOrganization(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/GetOrganization',
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOrganizationMetrics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/GetOrganizationMetrics',
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetricsReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetricsResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOrganizationInsights(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/GetOrganizationInsights',
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationInsightsReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationInsightsResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SnoozeOrganizationInsight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/SnoozeOrganizationInsight',
            prodvana_dot_organization_dot_organization__manager__pb2.SnoozeOrganizationInsightReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.SnoozeOrganizationInsightResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOrganizationMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/GetOrganizationMetadata',
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetadataReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationMetadataResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetOrganizationMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/SetOrganizationMetadata',
            prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationMetadataReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationMetadataResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/GetUser',
            prodvana_dot_organization_dot_organization__manager__pb2.GetUserReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.GetUserResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOrganizationSubscriptionStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/GetOrganizationSubscriptionStatus',
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSubscriptionStatusReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSubscriptionStatusResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOrganizationSettings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/GetOrganizationSettings',
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSettingsReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.GetOrganizationSettingsResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetOrganizationSettings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/prodvana.organization.OrganizationManager/SetOrganizationSettings',
            prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationSettingsReq.SerializeToString,
            prodvana_dot_organization_dot_organization__manager__pb2.SetOrganizationSettingsResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
