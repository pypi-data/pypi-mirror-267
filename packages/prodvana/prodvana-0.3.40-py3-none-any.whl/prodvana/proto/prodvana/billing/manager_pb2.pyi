"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class UsageMetrics(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NUM_USERS_FIELD_NUMBER: builtins.int
    NUM_RUNTIMES_FIELD_NUMBER: builtins.int
    NUM_APPLICATIONS_FIELD_NUMBER: builtins.int
    num_users: builtins.int
    num_runtimes: builtins.int
    num_applications: builtins.int
    def __init__(
        self,
        *,
        num_users: builtins.int = ...,
        num_runtimes: builtins.int = ...,
        num_applications: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["num_applications", b"num_applications", "num_runtimes", b"num_runtimes", "num_users", b"num_users"]) -> None: ...

global___UsageMetrics = UsageMetrics

class GetUsageMetricsReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___GetUsageMetricsReq = GetUsageMetricsReq

class GetUsageMetricsResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    USAGE_METRICS_FIELD_NUMBER: builtins.int
    @property
    def usage_metrics(self) -> global___UsageMetrics: ...
    def __init__(
        self,
        *,
        usage_metrics: global___UsageMetrics | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["usage_metrics", b"usage_metrics"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["usage_metrics", b"usage_metrics"]) -> None: ...

global___GetUsageMetricsResp = GetUsageMetricsResp
