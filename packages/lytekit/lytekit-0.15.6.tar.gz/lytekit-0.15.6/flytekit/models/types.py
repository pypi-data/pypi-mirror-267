import json as _json
import typing

from flyteidl.core import types_pb2 as _types_pb2
from google.protobuf import json_format as _json_format
from google.protobuf import struct_pb2 as _struct

from flytekit.models import common as _common
from flytekit.models.annotation import TypeAnnotation as TypeAnnotationModel
from flytekit.models.core import types as _core_types


class SimpleType(object):
    NONE = _types_pb2.NONE
    INTEGER = _types_pb2.INTEGER
    FLOAT = _types_pb2.FLOAT
    STRING = _types_pb2.STRING
    BOOLEAN = _types_pb2.BOOLEAN
    DATETIME = _types_pb2.DATETIME
    DURATION = _types_pb2.DURATION
    BINARY = _types_pb2.BINARY
    ERROR = _types_pb2.ERROR
    STRUCT = _types_pb2.STRUCT


class UnionType(_common.FlyteIdlEntity):
    """
    Models _types_pb2.UnionType
    """

    def __init__(self, variants: typing.List["LiteralType"]):
        self._variants = variants

    @property
    def variants(self) -> typing.List["LiteralType"]:
        return self._variants

    def to_flyte_idl(self) -> _types_pb2.UnionType:
        return _types_pb2.UnionType(
            variants=[val.to_flyte_idl() if val else None for val in self._variants],
        )

    @classmethod
    def from_flyte_idl(cls, proto: _types_pb2.UnionType):
        return cls(variants=[LiteralType.from_flyte_idl(v) for v in proto.variants])


class RecordFieldType(_common.FlyteIdlEntity):
    def __init__(self, key: str, literal_type: "LiteralType"):
        self._key = key
        self._literal_type = literal_type

    @property
    def key(self):
        return self._key

    @property
    def literal_type(self):
        return self._literal_type

    def to_flyte_idl(self) -> _types_pb2.RecordFieldType:
        return _types_pb2.RecordFieldType(key=self.key, type=self.literal_type.to_flyte_idl())

    @classmethod
    def from_flyte_idl(cls, proto: _types_pb2.RecordFieldType):
        return cls(key=proto.key, literal_type=LiteralType.from_flyte_idl(proto.type))


class RecordType(_common.FlyteIdlEntity):
    def __init__(self, fields: typing.List[RecordFieldType]):
        self._fields = fields

    @property
    def fields(self):
        return self._fields

    def to_flyte_idl(self) -> _types_pb2.RecordType:
        return _types_pb2.RecordType(fields=[x.to_flyte_idl() for x in self.fields])

    @classmethod
    def from_flyte_idl(cls, proto: _types_pb2.RecordType):
        return cls(fields=[RecordFieldType.from_flyte_idl(x) for x in proto.fields])


class TypeStructure(_common.FlyteIdlEntity):
    """
    Models _types_pb2.TypeStructure
    """

    def __init__(self, tag: str):
        self._tag = tag

    @property
    def tag(self) -> str:
        return self._tag

    def to_flyte_idl(self) -> _types_pb2.TypeStructure:
        return _types_pb2.TypeStructure(
            tag=self._tag,
        )

    @classmethod
    def from_flyte_idl(cls, proto: _types_pb2.TypeStructure):
        return cls(tag=proto.tag)


class LiteralType(_common.FlyteIdlEntity):
    def __init__(
        self,
        simple=None,
        schema=None,
        collection_type=None,
        map_value_type=None,
        record_type=None,
        blob=None,
        enum_type=None,
        union_type=None,
        metadata=None,
        structure=None,
        annotation=None,
    ):
        """
        This is a oneof message, only one of the kwargs may be set, representing one of the Flyte types.

        :param int simple: Enum type from SimpleType
        :param LiteralType collection_type: For list-like objects, this is the type of each entry in the list.
        :param LiteralType map_value_type: For map objects, this is the type of the value.  The key must always be a
            string.
        :param flytekit.models.core.types.BlobType blob: For blob objects, this describes the type.
        :param flytekit.models.core.types.EnumType enum_type: For enum objects, describes an enum
        :param flytekit.models.core.types.UnionType union_type: For union objects, describes an python union type.
        :param flytekit.models.core.types.TypeStructure structure: Type matching hints
        :param dict[Text, T] metadata: Additional data describing the type
        :param flytekit.models.annotation.TypeAnnotation annotation: Additional data
            describing the type _intended to be saturated by the client_
        """
        self._simple = simple
        self._schema = schema
        self._collection_type = collection_type
        self._map_value_type = map_value_type
        self._record_type = record_type
        self._blob = blob
        self._enum_type = enum_type
        self._union_type = union_type
        self._metadata = metadata
        self._structure = structure
        self._metadata = metadata
        self._annotation = annotation

    @property
    def simple(self) -> SimpleType:
        return self._simple

    @property
    def collection_type(self) -> "LiteralType":
        """
        The collection value type
        """
        return self._collection_type

    @property
    def map_value_type(self) -> "LiteralType":
        """
        The Value for a dictionary. Key is always string
        """
        return self._map_value_type

    @property
    def record_type(self):
        return self._record_type

    @property
    def blob(self) -> _core_types.BlobType:
        return self._blob

    @property
    def enum_type(self) -> _core_types.EnumType:
        return self._enum_type

    @property
    def union_type(self) -> UnionType:
        return self._union_type

    @property
    def structure(self) -> TypeStructure:
        return self._structure

    @property
    def metadata(self):
        """
        :rtype: dict[Text, T]
        """
        return self._metadata

    @property
    def annotation(self) -> TypeAnnotationModel:
        """
        :rtype: flytekit.models.annotation.TypeAnnotation
        """
        return self._annotation

    @metadata.setter
    def metadata(self, value):
        self._metadata = value

    @annotation.setter
    def annotation(self, value):
        self.annotation = value

    @structure.setter
    def structure(self, value):
        self._structure = value

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.core.types_pb2.LiteralType
        """

        if self.metadata is not None:
            metadata = _json_format.Parse(_json.dumps(self.metadata), _struct.Struct())
        else:
            metadata = None

        t = _types_pb2.LiteralType(
            simple=self.simple if self.simple is not None else None,
            collection_type=self.collection_type.to_flyte_idl() if self.collection_type is not None else None,
            map_value_type=self.map_value_type.to_flyte_idl() if self.map_value_type is not None else None,
            record_type=self.record_type.to_flyte_idl() if self.record_type is not None else None,
            blob=self.blob.to_flyte_idl() if self.blob is not None else None,
            enum_type=self.enum_type.to_flyte_idl() if self.enum_type else None,
            union_type=self.union_type.to_flyte_idl() if self.union_type else None,
            metadata=metadata,
            annotation=self.annotation.to_flyte_idl() if self.annotation else None,
            structure=self.structure.to_flyte_idl() if self.structure else None,
        )
        return t

    @classmethod
    def from_flyte_idl(cls, proto):
        """
        :param flyteidl.core.types_pb2.LiteralType proto:
        :rtype: LiteralType
        """
        collection_type = None
        map_value_type = None
        if proto.HasField("collection_type"):
            collection_type = LiteralType.from_flyte_idl(proto.collection_type)
        if proto.HasField("map_value_type"):
            map_value_type = LiteralType.from_flyte_idl(proto.map_value_type)
        return cls(
            simple=proto.simple if proto.HasField("simple") else None,
            collection_type=collection_type,
            map_value_type=map_value_type,
            record_type=RecordType.from_flyte_idl(proto.record_type) if proto.HasField("record_type") else None,
            blob=_core_types.BlobType.from_flyte_idl(proto.blob) if proto.HasField("blob") else None,
            enum_type=_core_types.EnumType.from_flyte_idl(proto.enum_type) if proto.HasField("enum_type") else None,
            union_type=UnionType.from_flyte_idl(proto.union_type) if proto.HasField("union_type") else None,
            metadata=_json_format.MessageToDict(proto.metadata) or None,
            structure=TypeStructure.from_flyte_idl(proto.structure) if proto.HasField("structure") else None,
            annotation=TypeAnnotationModel.from_flyte_idl(proto.annotation) if proto.HasField("annotation") else None,
        )


class OutputReference(_common.FlyteIdlEntity):
    def __init__(self, node_id, var):
        """
        A reference to an output produced by a node. The type can be retrieved -and validated- from
            the underlying interface of the node.

        :param Text node_id: Node id must exist at the graph layer.
        :param Text var: Variable name must refer to an output variable for the node.
        """
        self._node_id = node_id
        self._var = var

    @property
    def node_id(self):
        """
        Node id must exist at the graph layer.
        :rtype: Text
        """
        return self._node_id

    @property
    def var(self):
        """
        Variable name must refer to an output variable for the node.
        :rtype: Text
        """
        return self._var

    @var.setter
    def var(self, var_name):
        self._var = var_name

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.core.types.OutputReference
        """
        return _types_pb2.OutputReference(node_id=self.node_id, var=self.var)

    @classmethod
    def from_flyte_idl(cls, pb2_object):
        """
        :param flyteidl.core.types.OutputReference pb2_object:
        :rtype: OutputReference
        """
        return cls(node_id=pb2_object.node_id, var=pb2_object.var)


class Error(_common.FlyteIdlEntity):
    def __init__(self, failed_node_id: str, message: str):
        self._message = message
        self._failed_node_id = failed_node_id

    def to_flyte_idl(self) -> _types_pb2.Error:
        return _types_pb2.Error(
            message=self._message,
            failed_node_id=self._failed_node_id,
        )

    @classmethod
    def from_flyte_idl(cls, pb2_object: _types_pb2.Error) -> "Error":
        """
        :param flyteidl.core.types.OutputReference pb2_object:
        :rtype: OutputReference
        """
        return cls(failed_node_id=pb2_object.failed_node_id, message=pb2_object.message)
