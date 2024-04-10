# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: prodvana/deployment/manager.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from prodvana.proto.prodvana.object import meta_pb2 as prodvana_dot_object_dot_meta__pb2
from prodvana.proto.prodvana.deployment.model import object_pb2 as prodvana_dot_deployment_dot_model_dot_object__pb2
from prodvana.proto.prodvana.service import service_config_pb2 as prodvana_dot_service_dot_service__config__pb2
from prodvana.proto.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!prodvana/deployment/manager.proto\x12\x13prodvana.deployment\x1a\x1cgoogle/api/annotations.proto\x1a\x1aprodvana/object/meta.proto\x1a&prodvana/deployment/model/object.proto\x1a%prodvana/service/service_config.proto\x1a\x17validate/validate.proto\"m\n\x13RecordDeploymentReq\x12\x45\n\x06\x63onfig\x18\x01 \x01(\x0b\x32+.prodvana.deployment.model.DeploymentConfigB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01\x12\x0f\n\x07pending\x18\x02 \x01(\x08\"A\n\x14RecordDeploymentResp\x12)\n\x04meta\x18\x01 \x01(\x0b\x32\x1b.prodvana.object.ObjectMeta\"o\n\x19UpdateDeploymentStatusReq\x12\x15\n\rdeployment_id\x18\x01 \x01(\t\x12;\n\x06status\x18\x02 \x01(\x0e\x32+.prodvana.deployment.model.DeploymentStatus\"Y\n\x1aUpdateDeploymentStatusResp\x12;\n\x06status\x18\x01 \x01(\x0e\x32+.prodvana.deployment.model.DeploymentStatus\"\x81\x01\n\x10\x44\x65ploymentFilter\x12\x10\n\x08services\x18\x01 \x03(\t\x12\x18\n\x10release_channels\x18\x02 \x03(\t\x12\x13\n\x0b\x61pplication\x18\x03 \x01(\t\x12\x18\n\x10\x64\x65sired_state_id\x18\x04 \x01(\t\x12\x12\n\nrelease_id\x18\x05 \x01(\t\"\xe8\x01\n\x12ListDeploymentsReq\x12\x36\n\x07\x66ilters\x18\x01 \x03(\x0b\x32%.prodvana.deployment.DeploymentFilter\x12\x35\n\x06\x66ilter\x18\x02 \x01(\x0b\x32%.prodvana.deployment.DeploymentFilter\x12\x1e\n\x16starting_deployment_id\x18\x03 \x01(\t\x12\x1c\n\x14\x65nding_deployment_id\x18\x04 \x01(\t\x12\x12\n\npage_token\x18\x05 \x01(\t\x12\x11\n\tpage_size\x18\x06 \x01(\x05\"j\n\x13ListDeploymentsResp\x12:\n\x0b\x64\x65ployments\x18\x01 \x03(\x0b\x32%.prodvana.deployment.model.Deployment\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\xbd\x02\n\rDeploymentRef\x12\x17\n\rdeployment_id\x18\x01 \x01(\tH\x00\x12=\n\x06\x63onfig\x18\x02 \x01(\x0b\x32+.prodvana.deployment.model.DeploymentConfigH\x00\x12[\n\x17service_instance_config\x18\x03 \x01(\x0b\x32\x38.prodvana.deployment.DeploymentRef.ServiceInstanceConfigH\x00\x1ak\n\x15ServiceInstanceConfig\x12R\n\x0f\x63ompiled_config\x18\x01 \x01(\x0b\x32/.prodvana.service.CompiledServiceInstanceConfigB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01\x42\n\n\x03ref\x12\x03\xf8\x42\x01\"\x99\x01\n\x14\x43ompareDeploymentReq\x12\x44\n\x0enew_deployment\x18\x01 \x01(\x0b\x32\".prodvana.deployment.DeploymentRefB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01\x12;\n\x0fprev_deployment\x18\x02 \x01(\x0b\x32\".prodvana.deployment.DeploymentRef\"\\\n\x15\x43ompareDeploymentResp\x12\x43\n\ncomparison\x18\x01 \x01(\x0b\x32/.prodvana.deployment.model.DeploymentComparison\"\x9a\x01\n\x14PreviewDeploymentReq\x12\x45\n\x06\x63onfig\x18\x01 \x01(\x0b\x32+.prodvana.deployment.model.DeploymentConfigB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01\x12;\n\x0fprev_deployment\x18\x02 \x01(\x0b\x32\".prodvana.deployment.DeploymentRef\"R\n\x15PreviewDeploymentResp\x12\x39\n\ndeployment\x18\x01 \x01(\x0b\x32%.prodvana.deployment.model.Deployment\"\xec\x01\n\x17GetLatestDeploymentsReq\x12\x36\n\x07\x66ilters\x18\x01 \x03(\x0b\x32%.prodvana.deployment.DeploymentFilter\x12\x35\n\x06\x66ilter\x18\x02 \x01(\x0b\x32%.prodvana.deployment.DeploymentFilter\x12;\n\x06status\x18\x03 \x01(\x0e\x32+.prodvana.deployment.model.DeploymentStatus\x12\x12\n\npage_token\x18\x04 \x01(\t\x12\x11\n\tpage_size\x18\x05 \x01(\x05\"o\n\x18GetLatestDeploymentsResp\x12:\n\x0b\x64\x65ployments\x18\x01 \x03(\x0b\x32%.prodvana.deployment.model.Deployment\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"u\n\x19\x44\x65ploymentServiceInstance\x12\x1c\n\x0b\x61pplication\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x12\x18\n\x07service\x18\x02 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x12 \n\x0frelease_channel\x18\x03 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\"\xee\x01\n\x1a\x43heckCommitInDeploymentReq\x12 \n\rdeployment_id\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01H\x00\x12_\n\x1b\x64\x65ployment_service_instance\x18\x02 \x01(\x0b\x32..prodvana.deployment.DeploymentServiceInstanceB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00\x12\x1b\n\nrepository\x18\x03 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x12\x17\n\x06\x63ommit\x18\x04 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x42\x17\n\x10\x64\x65ployment_oneof\x12\x03\xf8\x42\x01\"\xae\x01\n\x1b\x43heckCommitInDeploymentResp\x12G\n\x06result\x18\x01 \x01(\x0e\x32\x37.prodvana.deployment.CheckCommitInDeploymentResp.Result\"F\n\x06Result\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0c\n\x08INCLUDED\x10\x01\x12\x0f\n\x0bNO_RELATION\x10\x02\x12\x10\n\x0cNOT_INCLUDED\x10\x03\x32\x96\t\n\x11\x44\x65ploymentManager\x12\x83\x01\n\x10RecordDeployment\x12(.prodvana.deployment.RecordDeploymentReq\x1a).prodvana.deployment.RecordDeploymentResp\"\x1a\x82\xd3\xe4\x93\x02\x14\"\x0f/v1/deployments:\x01*\x12\xae\x01\n\x16UpdateDeploymentStatus\x12..prodvana.deployment.UpdateDeploymentStatusReq\x1a/.prodvana.deployment.UpdateDeploymentStatusResp\"3\x82\xd3\xe4\x93\x02-\"(/v1/deployments/{deployment_id=*}/status:\x01*\x12}\n\x0fListDeployments\x12\'.prodvana.deployment.ListDeploymentsReq\x1a(.prodvana.deployment.ListDeploymentsResp\"\x17\x82\xd3\xe4\x93\x02\x11\x12\x0f/v1/deployments\x12n\n\x15ListDeploymentsStream\x12\'.prodvana.deployment.ListDeploymentsReq\x1a(.prodvana.deployment.ListDeploymentsResp\"\x00\x30\x01\x12\x8e\x01\n\x11\x43ompareDeployment\x12).prodvana.deployment.CompareDeploymentReq\x1a*.prodvana.deployment.CompareDeploymentResp\"\"\x82\xd3\xe4\x93\x02\x1c\"\x17/v1/deployments/compare:\x01*\x12\x8e\x01\n\x11PreviewDeployment\x12).prodvana.deployment.PreviewDeploymentReq\x1a*.prodvana.deployment.PreviewDeploymentResp\"\"\x82\xd3\xe4\x93\x02\x1c\"\x17/v1/deployments/preview:\x01*\x12\x93\x01\n\x14GetLatestDeployments\x12,.prodvana.deployment.GetLatestDeploymentsReq\x1a-.prodvana.deployment.GetLatestDeploymentsResp\"\x1e\x82\xd3\xe4\x93\x02\x18\x12\x16/v1/deployments/latest\x12\xa2\x01\n\x17\x43heckCommitInDeployment\x12/.prodvana.deployment.CheckCommitInDeploymentReq\x1a\x30.prodvana.deployment.CheckCommitInDeploymentResp\"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/v1/deployments/check_commitBOZMgithub.com/prodvana/prodvana-public/go/prodvana-sdk/proto/prodvana/deploymentb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'prodvana.deployment.manager_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZMgithub.com/prodvana/prodvana-public/go/prodvana-sdk/proto/prodvana/deployment'
  _RECORDDEPLOYMENTREQ.fields_by_name['config']._options = None
  _RECORDDEPLOYMENTREQ.fields_by_name['config']._serialized_options = b'\372B\005\212\001\002\020\001'
  _DEPLOYMENTREF_SERVICEINSTANCECONFIG.fields_by_name['compiled_config']._options = None
  _DEPLOYMENTREF_SERVICEINSTANCECONFIG.fields_by_name['compiled_config']._serialized_options = b'\372B\005\212\001\002\020\001'
  _DEPLOYMENTREF.oneofs_by_name['ref']._options = None
  _DEPLOYMENTREF.oneofs_by_name['ref']._serialized_options = b'\370B\001'
  _COMPAREDEPLOYMENTREQ.fields_by_name['new_deployment']._options = None
  _COMPAREDEPLOYMENTREQ.fields_by_name['new_deployment']._serialized_options = b'\372B\005\212\001\002\020\001'
  _PREVIEWDEPLOYMENTREQ.fields_by_name['config']._options = None
  _PREVIEWDEPLOYMENTREQ.fields_by_name['config']._serialized_options = b'\372B\005\212\001\002\020\001'
  _DEPLOYMENTSERVICEINSTANCE.fields_by_name['application']._options = None
  _DEPLOYMENTSERVICEINSTANCE.fields_by_name['application']._serialized_options = b'\372B\004r\002\020\001'
  _DEPLOYMENTSERVICEINSTANCE.fields_by_name['service']._options = None
  _DEPLOYMENTSERVICEINSTANCE.fields_by_name['service']._serialized_options = b'\372B\004r\002\020\001'
  _DEPLOYMENTSERVICEINSTANCE.fields_by_name['release_channel']._options = None
  _DEPLOYMENTSERVICEINSTANCE.fields_by_name['release_channel']._serialized_options = b'\372B\004r\002\020\001'
  _CHECKCOMMITINDEPLOYMENTREQ.oneofs_by_name['deployment_oneof']._options = None
  _CHECKCOMMITINDEPLOYMENTREQ.oneofs_by_name['deployment_oneof']._serialized_options = b'\370B\001'
  _CHECKCOMMITINDEPLOYMENTREQ.fields_by_name['deployment_id']._options = None
  _CHECKCOMMITINDEPLOYMENTREQ.fields_by_name['deployment_id']._serialized_options = b'\372B\004r\002\020\001'
  _CHECKCOMMITINDEPLOYMENTREQ.fields_by_name['deployment_service_instance']._options = None
  _CHECKCOMMITINDEPLOYMENTREQ.fields_by_name['deployment_service_instance']._serialized_options = b'\372B\005\212\001\002\020\001'
  _CHECKCOMMITINDEPLOYMENTREQ.fields_by_name['repository']._options = None
  _CHECKCOMMITINDEPLOYMENTREQ.fields_by_name['repository']._serialized_options = b'\372B\004r\002\020\001'
  _CHECKCOMMITINDEPLOYMENTREQ.fields_by_name['commit']._options = None
  _CHECKCOMMITINDEPLOYMENTREQ.fields_by_name['commit']._serialized_options = b'\372B\004r\002\020\001'
  _DEPLOYMENTMANAGER.methods_by_name['RecordDeployment']._options = None
  _DEPLOYMENTMANAGER.methods_by_name['RecordDeployment']._serialized_options = b'\202\323\344\223\002\024\"\017/v1/deployments:\001*'
  _DEPLOYMENTMANAGER.methods_by_name['UpdateDeploymentStatus']._options = None
  _DEPLOYMENTMANAGER.methods_by_name['UpdateDeploymentStatus']._serialized_options = b'\202\323\344\223\002-\"(/v1/deployments/{deployment_id=*}/status:\001*'
  _DEPLOYMENTMANAGER.methods_by_name['ListDeployments']._options = None
  _DEPLOYMENTMANAGER.methods_by_name['ListDeployments']._serialized_options = b'\202\323\344\223\002\021\022\017/v1/deployments'
  _DEPLOYMENTMANAGER.methods_by_name['CompareDeployment']._options = None
  _DEPLOYMENTMANAGER.methods_by_name['CompareDeployment']._serialized_options = b'\202\323\344\223\002\034\"\027/v1/deployments/compare:\001*'
  _DEPLOYMENTMANAGER.methods_by_name['PreviewDeployment']._options = None
  _DEPLOYMENTMANAGER.methods_by_name['PreviewDeployment']._serialized_options = b'\202\323\344\223\002\034\"\027/v1/deployments/preview:\001*'
  _DEPLOYMENTMANAGER.methods_by_name['GetLatestDeployments']._options = None
  _DEPLOYMENTMANAGER.methods_by_name['GetLatestDeployments']._serialized_options = b'\202\323\344\223\002\030\022\026/v1/deployments/latest'
  _DEPLOYMENTMANAGER.methods_by_name['CheckCommitInDeployment']._options = None
  _DEPLOYMENTMANAGER.methods_by_name['CheckCommitInDeployment']._serialized_options = b'\202\323\344\223\002\036\022\034/v1/deployments/check_commit'
  _globals['_RECORDDEPLOYMENTREQ']._serialized_start=220
  _globals['_RECORDDEPLOYMENTREQ']._serialized_end=329
  _globals['_RECORDDEPLOYMENTRESP']._serialized_start=331
  _globals['_RECORDDEPLOYMENTRESP']._serialized_end=396
  _globals['_UPDATEDEPLOYMENTSTATUSREQ']._serialized_start=398
  _globals['_UPDATEDEPLOYMENTSTATUSREQ']._serialized_end=509
  _globals['_UPDATEDEPLOYMENTSTATUSRESP']._serialized_start=511
  _globals['_UPDATEDEPLOYMENTSTATUSRESP']._serialized_end=600
  _globals['_DEPLOYMENTFILTER']._serialized_start=603
  _globals['_DEPLOYMENTFILTER']._serialized_end=732
  _globals['_LISTDEPLOYMENTSREQ']._serialized_start=735
  _globals['_LISTDEPLOYMENTSREQ']._serialized_end=967
  _globals['_LISTDEPLOYMENTSRESP']._serialized_start=969
  _globals['_LISTDEPLOYMENTSRESP']._serialized_end=1075
  _globals['_DEPLOYMENTREF']._serialized_start=1078
  _globals['_DEPLOYMENTREF']._serialized_end=1395
  _globals['_DEPLOYMENTREF_SERVICEINSTANCECONFIG']._serialized_start=1276
  _globals['_DEPLOYMENTREF_SERVICEINSTANCECONFIG']._serialized_end=1383
  _globals['_COMPAREDEPLOYMENTREQ']._serialized_start=1398
  _globals['_COMPAREDEPLOYMENTREQ']._serialized_end=1551
  _globals['_COMPAREDEPLOYMENTRESP']._serialized_start=1553
  _globals['_COMPAREDEPLOYMENTRESP']._serialized_end=1645
  _globals['_PREVIEWDEPLOYMENTREQ']._serialized_start=1648
  _globals['_PREVIEWDEPLOYMENTREQ']._serialized_end=1802
  _globals['_PREVIEWDEPLOYMENTRESP']._serialized_start=1804
  _globals['_PREVIEWDEPLOYMENTRESP']._serialized_end=1886
  _globals['_GETLATESTDEPLOYMENTSREQ']._serialized_start=1889
  _globals['_GETLATESTDEPLOYMENTSREQ']._serialized_end=2125
  _globals['_GETLATESTDEPLOYMENTSRESP']._serialized_start=2127
  _globals['_GETLATESTDEPLOYMENTSRESP']._serialized_end=2238
  _globals['_DEPLOYMENTSERVICEINSTANCE']._serialized_start=2240
  _globals['_DEPLOYMENTSERVICEINSTANCE']._serialized_end=2357
  _globals['_CHECKCOMMITINDEPLOYMENTREQ']._serialized_start=2360
  _globals['_CHECKCOMMITINDEPLOYMENTREQ']._serialized_end=2598
  _globals['_CHECKCOMMITINDEPLOYMENTRESP']._serialized_start=2601
  _globals['_CHECKCOMMITINDEPLOYMENTRESP']._serialized_end=2775
  _globals['_CHECKCOMMITINDEPLOYMENTRESP_RESULT']._serialized_start=2705
  _globals['_CHECKCOMMITINDEPLOYMENTRESP_RESULT']._serialized_end=2775
  _globals['_DEPLOYMENTMANAGER']._serialized_start=2778
  _globals['_DEPLOYMENTMANAGER']._serialized_end=3952
# @@protoc_insertion_point(module_scope)
