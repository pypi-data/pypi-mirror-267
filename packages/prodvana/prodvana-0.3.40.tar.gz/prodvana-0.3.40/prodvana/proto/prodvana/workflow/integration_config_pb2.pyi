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

class AlertingConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class PagerDuty(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        SERVICE_FIELD_NUMBER: builtins.int
        service: builtins.str
        def __init__(
            self,
            *,
            service: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["service", b"service"]) -> None: ...

    PAGERDUTY_FIELD_NUMBER: builtins.int
    @property
    def pagerduty(self) -> global___AlertingConfig.PagerDuty: ...
    def __init__(
        self,
        *,
        pagerduty: global___AlertingConfig.PagerDuty | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["pagerduty", b"pagerduty"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["pagerduty", b"pagerduty"]) -> None: ...

global___AlertingConfig = AlertingConfig

class AnnotationsConfig(google.protobuf.message.Message):
    """this is currently used only on the Release Channel level because
    Honeycomb's model means we map environment to a Release Channel

    Last9's model is configured at the Application level because it does not
    have a similar concept.

    It doesn't make sense to put Last9 config at the RC level or Honeycomb config
    at the Application level, so these are separate AnnotationConfig messages.
    See prodvana.proto.prodvana.application.AnnotationsConfig for Last9 config.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Honeycomb(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        ENVIRONMENT_FIELD_NUMBER: builtins.int
        DATASET_FIELD_NUMBER: builtins.int
        environment: builtins.str
        dataset: builtins.str
        def __init__(
            self,
            *,
            environment: builtins.str = ...,
            dataset: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["dataset", b"dataset", "environment", b"environment"]) -> None: ...

    HONEYCOMB_FIELD_NUMBER: builtins.int
    @property
    def honeycomb(self) -> global___AnnotationsConfig.Honeycomb: ...
    def __init__(
        self,
        *,
        honeycomb: global___AnnotationsConfig.Honeycomb | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["honeycomb", b"honeycomb"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["honeycomb", b"honeycomb"]) -> None: ...

global___AnnotationsConfig = AnnotationsConfig

class TokenConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TOKEN_SECRET_KEY_FIELD_NUMBER: builtins.int
    TOKEN_SECRET_VERSION_FIELD_NUMBER: builtins.int
    token_secret_key: builtins.str
    token_secret_version: builtins.str
    def __init__(
        self,
        *,
        token_secret_key: builtins.str = ...,
        token_secret_version: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["token_secret_key", b"token_secret_key", "token_secret_version", b"token_secret_version"]) -> None: ...

global___TokenConfig = TokenConfig

class IntegrationConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SLACK_CONFIG_FIELD_NUMBER: builtins.int
    PAGERDUTY_CONFIG_FIELD_NUMBER: builtins.int
    @property
    def slack_config(self) -> global___TokenConfig: ...
    @property
    def pagerduty_config(self) -> global___TokenConfig: ...
    def __init__(
        self,
        *,
        slack_config: global___TokenConfig | None = ...,
        pagerduty_config: global___TokenConfig | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["config_oneof", b"config_oneof", "pagerduty_config", b"pagerduty_config", "slack_config", b"slack_config"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["config_oneof", b"config_oneof", "pagerduty_config", b"pagerduty_config", "slack_config", b"slack_config"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["config_oneof", b"config_oneof"]) -> typing_extensions.Literal["slack_config", "pagerduty_config"] | None: ...

global___IntegrationConfig = IntegrationConfig
