# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: prodvana/settings/organization/users.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from prodvana.proto.prodvana.users import users_pb2 as prodvana_dot_users_dot_users__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*prodvana/settings/organization/users.proto\x12\x1eprodvana.settings.organization\x1a\x1cgoogle/api/annotations.proto\x1a\x1aprodvana/users/users.proto\"A\n\x0cSettingsUser\x12\"\n\x04user\x18\x01 \x01(\x0b\x32\x14.prodvana.users.User\x12\r\n\x05roles\x18\x02 \x03(\t\"\x1d\n\nGetUserReq\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"I\n\x0bGetUserResp\x12:\n\x04user\x18\x01 \x01(\x0b\x32,.prodvana.settings.organization.SettingsUser\"\x0e\n\x0cListRolesReq\"3\n\x0eRoleDefinition\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\"N\n\rListRolesResp\x12=\n\x05roles\x18\x01 \x03(\x0b\x32..prodvana.settings.organization.RoleDefinition\"5\n\x0cListUsersReq\x12\x12\n\npage_token\x18\x01 \x01(\t\x12\x11\n\tpage_size\x18\x02 \x01(\x05\"e\n\rListUsersResp\x12;\n\x05users\x18\x01 \x03(\x0b\x32,.prodvana.settings.organization.SettingsUser\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"-\n\x0bSetRolesReq\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\r\n\x05roles\x18\x02 \x03(\t\"\x0e\n\x0cSetRolesResp\"*\n\nUserInvite\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\r\n\x05roles\x18\x02 \x03(\t\"K\n\x0eInviteUsersReq\x12\x39\n\x05users\x18\x01 \x03(\x0b\x32*.prodvana.settings.organization.UserInvite\"\x11\n\x0fInviteUsersResp\" \n\x1eOrganizationSupportsInvitesReq\";\n\x1fOrganizationSupportsInvitesResp\x12\x18\n\x10supports_invites\x18\x01 \x01(\x08\" \n\rRemoveUserReq\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"\x10\n\x0eRemoveUserResp2\x91\t\n\x14UsersSettingsManager\x12\x95\x01\n\x07GetUser\x12*.prodvana.settings.organization.GetUserReq\x1a+.prodvana.settings.organization.GetUserResp\"1\x82\xd3\xe4\x93\x02+\x12)/v1/settings/organization/users/{user_id}\x12\x91\x01\n\tListUsers\x12,.prodvana.settings.organization.ListUsersReq\x1a-.prodvana.settings.organization.ListUsersResp\"\'\x82\xd3\xe4\x93\x02!\x12\x1f/v1/settings/organization/users\x12\x91\x01\n\tListRoles\x12,.prodvana.settings.organization.ListRolesReq\x1a-.prodvana.settings.organization.ListRolesResp\"\'\x82\xd3\xe4\x93\x02!\x12\x1f/v1/settings/organization/roles\x12\x9e\x01\n\x08SetRoles\x12+.prodvana.settings.organization.SetRolesReq\x1a,.prodvana.settings.organization.SetRolesResp\"7\x82\xd3\xe4\x93\x02\x31\"//v1/settings/organization/users/{user_id}/roles\x12\xa1\x01\n\x0bInviteUsers\x12..prodvana.settings.organization.InviteUsersReq\x1a/.prodvana.settings.organization.InviteUsersResp\"1\x82\xd3\xe4\x93\x02+\"&/v1/settings/organization/users/invite:\x01*\x12\xd2\x01\n\x1bOrganizationSupportsInvites\x12>.prodvana.settings.organization.OrganizationSupportsInvitesReq\x1a?.prodvana.settings.organization.OrganizationSupportsInvitesResp\"2\x82\xd3\xe4\x93\x02,\x12*/v1/settings/organization/users/can_invite\x12\x9e\x01\n\nRemoveUser\x12-.prodvana.settings.organization.RemoveUserReq\x1a..prodvana.settings.organization.RemoveUserResp\"1\x82\xd3\xe4\x93\x02+*)/v1/settings/organization/users/{user_id}BZZXgithub.com/prodvana/prodvana-public/go/prodvana-sdk/proto/prodvana/settings/organizationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'prodvana.settings.organization.users_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZXgithub.com/prodvana/prodvana-public/go/prodvana-sdk/proto/prodvana/settings/organization'
  _USERSSETTINGSMANAGER.methods_by_name['GetUser']._options = None
  _USERSSETTINGSMANAGER.methods_by_name['GetUser']._serialized_options = b'\202\323\344\223\002+\022)/v1/settings/organization/users/{user_id}'
  _USERSSETTINGSMANAGER.methods_by_name['ListUsers']._options = None
  _USERSSETTINGSMANAGER.methods_by_name['ListUsers']._serialized_options = b'\202\323\344\223\002!\022\037/v1/settings/organization/users'
  _USERSSETTINGSMANAGER.methods_by_name['ListRoles']._options = None
  _USERSSETTINGSMANAGER.methods_by_name['ListRoles']._serialized_options = b'\202\323\344\223\002!\022\037/v1/settings/organization/roles'
  _USERSSETTINGSMANAGER.methods_by_name['SetRoles']._options = None
  _USERSSETTINGSMANAGER.methods_by_name['SetRoles']._serialized_options = b'\202\323\344\223\0021\"//v1/settings/organization/users/{user_id}/roles'
  _USERSSETTINGSMANAGER.methods_by_name['InviteUsers']._options = None
  _USERSSETTINGSMANAGER.methods_by_name['InviteUsers']._serialized_options = b'\202\323\344\223\002+\"&/v1/settings/organization/users/invite:\001*'
  _USERSSETTINGSMANAGER.methods_by_name['OrganizationSupportsInvites']._options = None
  _USERSSETTINGSMANAGER.methods_by_name['OrganizationSupportsInvites']._serialized_options = b'\202\323\344\223\002,\022*/v1/settings/organization/users/can_invite'
  _USERSSETTINGSMANAGER.methods_by_name['RemoveUser']._options = None
  _USERSSETTINGSMANAGER.methods_by_name['RemoveUser']._serialized_options = b'\202\323\344\223\002+*)/v1/settings/organization/users/{user_id}'
  _globals['_SETTINGSUSER']._serialized_start=136
  _globals['_SETTINGSUSER']._serialized_end=201
  _globals['_GETUSERREQ']._serialized_start=203
  _globals['_GETUSERREQ']._serialized_end=232
  _globals['_GETUSERRESP']._serialized_start=234
  _globals['_GETUSERRESP']._serialized_end=307
  _globals['_LISTROLESREQ']._serialized_start=309
  _globals['_LISTROLESREQ']._serialized_end=323
  _globals['_ROLEDEFINITION']._serialized_start=325
  _globals['_ROLEDEFINITION']._serialized_end=376
  _globals['_LISTROLESRESP']._serialized_start=378
  _globals['_LISTROLESRESP']._serialized_end=456
  _globals['_LISTUSERSREQ']._serialized_start=458
  _globals['_LISTUSERSREQ']._serialized_end=511
  _globals['_LISTUSERSRESP']._serialized_start=513
  _globals['_LISTUSERSRESP']._serialized_end=614
  _globals['_SETROLESREQ']._serialized_start=616
  _globals['_SETROLESREQ']._serialized_end=661
  _globals['_SETROLESRESP']._serialized_start=663
  _globals['_SETROLESRESP']._serialized_end=677
  _globals['_USERINVITE']._serialized_start=679
  _globals['_USERINVITE']._serialized_end=721
  _globals['_INVITEUSERSREQ']._serialized_start=723
  _globals['_INVITEUSERSREQ']._serialized_end=798
  _globals['_INVITEUSERSRESP']._serialized_start=800
  _globals['_INVITEUSERSRESP']._serialized_end=817
  _globals['_ORGANIZATIONSUPPORTSINVITESREQ']._serialized_start=819
  _globals['_ORGANIZATIONSUPPORTSINVITESREQ']._serialized_end=851
  _globals['_ORGANIZATIONSUPPORTSINVITESRESP']._serialized_start=853
  _globals['_ORGANIZATIONSUPPORTSINVITESRESP']._serialized_end=912
  _globals['_REMOVEUSERREQ']._serialized_start=914
  _globals['_REMOVEUSERREQ']._serialized_end=946
  _globals['_REMOVEUSERRESP']._serialized_start=948
  _globals['_REMOVEUSERRESP']._serialized_end=964
  _globals['_USERSSETTINGSMANAGER']._serialized_start=967
  _globals['_USERSSETTINGSMANAGER']._serialized_end=2136
# @@protoc_insertion_point(module_scope)
