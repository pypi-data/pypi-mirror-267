# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: prodvana/protection/attachments.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from prodvana.proto.prodvana.protection import protection_reference_pb2 as prodvana_dot_protection_dot_protection__reference__pb2
from prodvana.proto.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%prodvana/protection/attachments.proto\x12\x13prodvana.protection\x1a.prodvana/protection/protection_reference.proto\x1a\x17validate/validate.proto\"\xe5\x01\n\x1aProtectionAttachmentConfig\x12:\n\x04name\x18\x01 \x01(\tB,\xfa\x42)r\'\x10\x00\x18?2!^[a-z]?([a-z0-9-]*[a-z0-9]){0,1}$\x12?\n\x03ref\x18\x02 \x01(\x0b\x32(.prodvana.protection.ProtectionReferenceB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01\x12J\n\tlifecycle\x18\x03 \x03(\x0b\x32(.prodvana.protection.ProtectionLifecycleB\r\xfa\x42\n\x92\x01\x07\"\x05\x8a\x01\x02\x10\x01*Y\n\x0e\x41ttachmentType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x13\n\x0fRELEASE_CHANNEL\x10\x01\x12\x14\n\x10SERVICE_INSTANCE\x10\x02\x12\x0f\n\x0b\x43ONVERGENCE\x10\x03\x42OZMgithub.com/prodvana/prodvana-public/go/prodvana-sdk/proto/prodvana/protectionb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'prodvana.protection.attachments_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZMgithub.com/prodvana/prodvana-public/go/prodvana-sdk/proto/prodvana/protection'
  _PROTECTIONATTACHMENTCONFIG.fields_by_name['name']._options = None
  _PROTECTIONATTACHMENTCONFIG.fields_by_name['name']._serialized_options = b'\372B)r\'\020\000\030?2!^[a-z]?([a-z0-9-]*[a-z0-9]){0,1}$'
  _PROTECTIONATTACHMENTCONFIG.fields_by_name['ref']._options = None
  _PROTECTIONATTACHMENTCONFIG.fields_by_name['ref']._serialized_options = b'\372B\005\212\001\002\020\001'
  _PROTECTIONATTACHMENTCONFIG.fields_by_name['lifecycle']._options = None
  _PROTECTIONATTACHMENTCONFIG.fields_by_name['lifecycle']._serialized_options = b'\372B\n\222\001\007\"\005\212\001\002\020\001'
  _globals['_ATTACHMENTTYPE']._serialized_start=367
  _globals['_ATTACHMENTTYPE']._serialized_end=456
  _globals['_PROTECTIONATTACHMENTCONFIG']._serialized_start=136
  _globals['_PROTECTIONATTACHMENTCONFIG']._serialized_end=365
# @@protoc_insertion_point(module_scope)
