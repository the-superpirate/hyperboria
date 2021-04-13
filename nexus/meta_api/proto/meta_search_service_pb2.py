# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nexus/meta_api/proto/meta_search_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nexus.models.proto import \
    typed_document_pb2 as nexus_dot_models_dot_proto_dot_typed__document__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
  name='nexus/meta_api/proto/meta_search_service.proto',
  package='nexus.meta_api.proto',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n.nexus/meta_api/proto/meta_search_service.proto\x12\x14nexus.meta_api.proto\x1a\'nexus/models/proto/typed_document.proto\"l\n\x0eScoredDocument\x12\x39\n\x0etyped_document\x18\x01 \x01(\x0b\x32!.nexus.models.proto.TypedDocument\x12\r\n\x05score\x18\x02 \x01(\x02\x12\x10\n\x08position\x18\x03 \x01(\r\"b\n\x0eSearchResponse\x12>\n\x10scored_documents\x18\x01 \x03(\x0b\x32$.nexus.meta_api.proto.ScoredDocument\x12\x10\n\x08has_next\x18\x02 \x01(\x08\"\x87\x01\n\rSearchRequest\x12\x0f\n\x07schemas\x18\x01 \x03(\t\x12\r\n\x05query\x18\x02 \x01(\t\x12\x0c\n\x04page\x18\x03 \x01(\r\x12\x11\n\tpage_size\x18\x04 \x01(\r\x12\x10\n\x08language\x18\x05 \x01(\t\x12\x0f\n\x07user_id\x18\x06 \x01(\x03\x12\x12\n\nsession_id\x18\x07 \x01(\t2c\n\nMetaSearch\x12U\n\x06search\x12#.nexus.meta_api.proto.SearchRequest\x1a$.nexus.meta_api.proto.SearchResponse\"\x00\x62\x06proto3'
  ,
  dependencies=[nexus_dot_models_dot_proto_dot_typed__document__pb2.DESCRIPTOR,])




_SCOREDDOCUMENT = _descriptor.Descriptor(
  name='ScoredDocument',
  full_name='nexus.meta_api.proto.ScoredDocument',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='typed_document', full_name='nexus.meta_api.proto.ScoredDocument.typed_document', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='score', full_name='nexus.meta_api.proto.ScoredDocument.score', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='position', full_name='nexus.meta_api.proto.ScoredDocument.position', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=221,
)


_SEARCHRESPONSE = _descriptor.Descriptor(
  name='SearchResponse',
  full_name='nexus.meta_api.proto.SearchResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scored_documents', full_name='nexus.meta_api.proto.SearchResponse.scored_documents', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='has_next', full_name='nexus.meta_api.proto.SearchResponse.has_next', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=223,
  serialized_end=321,
)


_SEARCHREQUEST = _descriptor.Descriptor(
  name='SearchRequest',
  full_name='nexus.meta_api.proto.SearchRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='schemas', full_name='nexus.meta_api.proto.SearchRequest.schemas', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='nexus.meta_api.proto.SearchRequest.query', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page', full_name='nexus.meta_api.proto.SearchRequest.page', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='nexus.meta_api.proto.SearchRequest.page_size', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='language', full_name='nexus.meta_api.proto.SearchRequest.language', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='nexus.meta_api.proto.SearchRequest.user_id', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='nexus.meta_api.proto.SearchRequest.session_id', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=324,
  serialized_end=459,
)

_SCOREDDOCUMENT.fields_by_name['typed_document'].message_type = nexus_dot_models_dot_proto_dot_typed__document__pb2._TYPEDDOCUMENT
_SEARCHRESPONSE.fields_by_name['scored_documents'].message_type = _SCOREDDOCUMENT
DESCRIPTOR.message_types_by_name['ScoredDocument'] = _SCOREDDOCUMENT
DESCRIPTOR.message_types_by_name['SearchResponse'] = _SEARCHRESPONSE
DESCRIPTOR.message_types_by_name['SearchRequest'] = _SEARCHREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ScoredDocument = _reflection.GeneratedProtocolMessageType('ScoredDocument', (_message.Message,), {
  'DESCRIPTOR' : _SCOREDDOCUMENT,
  '__module__' : 'nexus.meta_api.proto.meta_search_service_pb2'
  # @@protoc_insertion_point(class_scope:nexus.meta_api.proto.ScoredDocument)
  })
_sym_db.RegisterMessage(ScoredDocument)

SearchResponse = _reflection.GeneratedProtocolMessageType('SearchResponse', (_message.Message,), {
  'DESCRIPTOR' : _SEARCHRESPONSE,
  '__module__' : 'nexus.meta_api.proto.meta_search_service_pb2'
  # @@protoc_insertion_point(class_scope:nexus.meta_api.proto.SearchResponse)
  })
_sym_db.RegisterMessage(SearchResponse)

SearchRequest = _reflection.GeneratedProtocolMessageType('SearchRequest', (_message.Message,), {
  'DESCRIPTOR' : _SEARCHREQUEST,
  '__module__' : 'nexus.meta_api.proto.meta_search_service_pb2'
  # @@protoc_insertion_point(class_scope:nexus.meta_api.proto.SearchRequest)
  })
_sym_db.RegisterMessage(SearchRequest)



_METASEARCH = _descriptor.ServiceDescriptor(
  name='MetaSearch',
  full_name='nexus.meta_api.proto.MetaSearch',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=461,
  serialized_end=560,
  methods=[
  _descriptor.MethodDescriptor(
    name='search',
    full_name='nexus.meta_api.proto.MetaSearch.search',
    index=0,
    containing_service=None,
    input_type=_SEARCHREQUEST,
    output_type=_SEARCHRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_METASEARCH)

DESCRIPTOR.services_by_name['MetaSearch'] = _METASEARCH

# @@protoc_insertion_point(module_scope)
