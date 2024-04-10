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

class ConfigWritebackPath(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DISPLAY_NAME_FIELD_NUMBER: builtins.int
    DISPLAY_PATH_FIELD_NUMBER: builtins.int
    display_name: builtins.str
    """short, user-readable name of what this config is. May contain spaces."""
    display_path: builtins.str
    """will be HTTP if apiserver is configured with a http display path, otherwise will be a git ssh/local path"""
    def __init__(
        self,
        *,
        display_name: builtins.str = ...,
        display_path: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["display_name", b"display_name", "display_path", b"display_path"]) -> None: ...

global___ConfigWritebackPath = ConfigWritebackPath
