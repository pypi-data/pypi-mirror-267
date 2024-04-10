# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: prodvana/common_config/helm.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from prodvana.proto.validate import validate_pb2 as validate_dot_validate__pb2
from prodvana.proto.prodvana.common_config import kubernetes_config_pb2 as prodvana_dot_common__config_dot_kubernetes__config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!prodvana/common_config/helm.proto\x12\x16prodvana.common_config\x1a\x17validate/validate.proto\x1a.prodvana/common_config/kubernetes_config.proto\"l\n\x0fRemoteHelmChart\x12\x0e\n\x04repo\x18\x01 \x01(\tH\x00\x12\x16\n\x05\x63hart\x18\x02 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x12\x1e\n\rchart_version\x18\x03 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x42\x11\n\nrepo_oneof\x12\x03\xf8\x42\x01\"\xc1\x01\n\x13HelmValuesOverrides\x12\x1a\n\x07inlined\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01H\x00\x12\x34\n\x05local\x18\x02 \x01(\x0b\x32#.prodvana.common_config.LocalConfigH\x00\x12\x36\n\x06remote\x18\x04 \x01(\x0b\x32$.prodvana.common_config.RemoteConfigH\x00\x42\x15\n\x0eoverride_oneof\x12\x03\xf8\x42\x01J\x04\x08\x03\x10\x04R\x03map\"\xd0\x02\n\nHelmConfig\x12\x39\n\x06remote\x18\x01 \x01(\x0b\x32\'.prodvana.common_config.RemoteHelmChartH\x00\x12\x34\n\x05local\x18\x05 \x01(\x0b\x32#.prodvana.common_config.LocalConfigH\x00\x12\x1e\n\x14helm_tarball_blob_id\x18\x06 \x01(\tH\x00\x12\x45\n\x10values_overrides\x18\x02 \x03(\x0b\x32+.prodvana.common_config.HelmValuesOverrides\x12\x14\n\x0crelease_name\x18\x03 \x01(\t\x12\x1a\n\tnamespace\x18\x04 \x01(\tB\x07\xfa\x42\x04r\x02\x18\x00\x12\x17\n\x0f\x66ixup_ownership\x18\x08 \x01(\x08\x42\x12\n\x0b\x63hart_oneof\x12\x03\xf8\x42\x01J\x04\x08\x07\x10\x08R\x05\x66orceBRZPgithub.com/prodvana/prodvana-public/go/prodvana-sdk/proto/prodvana/common_configb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'prodvana.common_config.helm_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZPgithub.com/prodvana/prodvana-public/go/prodvana-sdk/proto/prodvana/common_config'
  _REMOTEHELMCHART.oneofs_by_name['repo_oneof']._options = None
  _REMOTEHELMCHART.oneofs_by_name['repo_oneof']._serialized_options = b'\370B\001'
  _REMOTEHELMCHART.fields_by_name['chart']._options = None
  _REMOTEHELMCHART.fields_by_name['chart']._serialized_options = b'\372B\004r\002\020\001'
  _REMOTEHELMCHART.fields_by_name['chart_version']._options = None
  _REMOTEHELMCHART.fields_by_name['chart_version']._serialized_options = b'\372B\004r\002\020\001'
  _HELMVALUESOVERRIDES.oneofs_by_name['override_oneof']._options = None
  _HELMVALUESOVERRIDES.oneofs_by_name['override_oneof']._serialized_options = b'\370B\001'
  _HELMVALUESOVERRIDES.fields_by_name['inlined']._options = None
  _HELMVALUESOVERRIDES.fields_by_name['inlined']._serialized_options = b'\372B\004r\002\020\001'
  _HELMCONFIG.oneofs_by_name['chart_oneof']._options = None
  _HELMCONFIG.oneofs_by_name['chart_oneof']._serialized_options = b'\370B\001'
  _HELMCONFIG.fields_by_name['namespace']._options = None
  _HELMCONFIG.fields_by_name['namespace']._serialized_options = b'\372B\004r\002\030\000'
  _globals['_REMOTEHELMCHART']._serialized_start=134
  _globals['_REMOTEHELMCHART']._serialized_end=242
  _globals['_HELMVALUESOVERRIDES']._serialized_start=245
  _globals['_HELMVALUESOVERRIDES']._serialized_end=438
  _globals['_HELMCONFIG']._serialized_start=441
  _globals['_HELMCONFIG']._serialized_end=777
# @@protoc_insertion_point(module_scope)
