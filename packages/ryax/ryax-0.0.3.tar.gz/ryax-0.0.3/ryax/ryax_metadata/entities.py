from enum import Enum
from typing import Optional, Union
from dataclasses import dataclass

from ryax.utils.exceptions import (
    RepositoryActionInvalidTypeException,
    RepositoryActionInvalidKindException,
    RepositoryActionResourceRequestInvalidException,
)


class RepositoryActionKind(Enum):
    PROCESSOR = "Processor"
    SOURCE = "Source"
    PUBLISHER = "Publisher"
    UNDEFINED = "Undefined"

    @classmethod
    def string_to_enum(cls, value: str) -> "RepositoryActionKind":
        for name in cls:
            if name.value == value:
                return name
        else:
            raise RepositoryActionInvalidKindException

    @classmethod
    def has_value(cls, value: str) -> bool:
        return any(value == var.value for var in cls)


class RepositoryActionType(Enum):
    PYTHON3 = "python3"
    PYTHON3_CUDA = "python3-cuda"
    CSHARP_DOTNET6 = "csharp-dotnet6"
    NODEJS = "nodejs"
    INTERNAL = "internal"
    UNDEFINED = "Undefined"

    @classmethod
    def string_to_enum(cls, value: str) -> "RepositoryActionType":
        for name in cls:
            if name.value == value:
                return name
        else:
            raise RepositoryActionInvalidTypeException


class RepositoryActionStatus(Enum):
    SCANNING = "Scanning"
    SCANNED = "Scanned"
    SCAN_ERROR = "Scan Error"
    BUILD_PENDING = "Build Pending"
    BUILDING = "Building"
    BUILD_ERROR = "Build Error"
    BUILT = "Built"


class RepositoryActionIOType(Enum):
    BYTES = "bytes"
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    FILE = "file"
    DIRECTORY = "directory"
    LONGSTRING = "longstring"
    PASSWORD = "password"
    ENUM = "enum"
    TABLE = "table"

    @classmethod
    def has_value(cls, value: Optional[str]) -> bool:
        return any(value == var.value for var in cls)


class RepositoryActionIOKind(Enum):
    INPUT = "input"
    OUTPUT = "output"


class RyaxMetadataSchemaV2:
    schema: dict = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "apiVersion": {"type": "string", "const": "ryax.tech/v2.0"},
            "kind": {
                "type": "string",
                "enum": [item.value for item in RepositoryActionKind],
            },
            "spec": {
                "additionalProperties": False,
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "minLength": 3,
                        "maxLength": 24,
                    },
                    "human_name": {
                        "type": "string",
                        "minLength": 3,
                        "maxLength": 128,
                    },
                    "type": {
                        "type": "string",
                        "enum": [item.value for item in RepositoryActionType],
                    },
                    "dependencies": {
                        "type": "array",
                        "maxItems": 64,
                        "items": {
                            "type": "string",
                            "maxLength": 1024,
                        },
                    },
                    "version": {"type": "string", "minLength": 3, "maxLength": 128},
                    "logo": {"type": "string"},
                    "addons": {
                        "type": "object",
                        "description": "The addons as key-values, with the values being an object containing parametrisation of the addon",
                    },
                    "options": {
                        "type": "object",
                        "description": "Key values to give options to Ryax",
                    },
                    "inputs": {
                        "type": "array",
                        "description": "The list of action's inputs.",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "human_name": {
                                    "type": "string",
                                    "minLength": 0,
                                    "maxLength": 128,
                                },
                                "help": {
                                    "type": "string",
                                    "minLength": 0,
                                    "maxLength": 10_000,
                                },
                                "name": {
                                    "type": "string",
                                    "minLength": 1,
                                    "maxLength": 64,
                                },
                                "type": {
                                    "type": "string",
                                    "enum": [
                                        item.value for item in RepositoryActionIOType
                                    ],
                                },
                                "enum_values": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "minLength": 1,
                                        "maxLength": 10_000,
                                    },
                                    "maxItems": 64,
                                },
                                "default_value": {
                                    "type": ["string", "number", "boolean"],
                                },
                                "optional": {
                                    "type": ["boolean"],
                                },
                            },
                            "required": [
                                "human_name",
                                "help",
                                "name",
                                "type",
                            ],
                        },
                    },
                    "outputs": {
                        "type": "array",
                        "description": "The list of action's outputs.",
                        "maxItems": 64,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "human_name": {
                                    "type": "string",
                                    "minLength": 0,
                                    "maxLength": 128,
                                },
                                "help": {
                                    "type": "string",
                                    "minLength": 0,
                                    "maxLength": 10_000,
                                },
                                "name": {
                                    "type": "string",
                                    "minLength": 1,
                                    "maxLength": 64,
                                },
                                "type": {
                                    "type": "string",
                                    "enum": [
                                        item.value for item in RepositoryActionIOType
                                    ],
                                },
                                "enum_values": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "minLength": 1,
                                        "maxLength": 10_000,
                                    },
                                    "maxItems": 64,
                                },
                                "optional": {
                                    "type": ["boolean"],
                                },
                            },
                            "required": [
                                "human_name",
                                "help",
                                "name",
                                "type",
                            ],
                        },
                    },
                    "dynamic_outputs": {
                        "description": "If True, this action has dynamic outputs. Which means that the outputs of this action will be defined independently for each instance.",
                        "type": "boolean",
                    },
                    "description": {"type": "string"},
                    "categories": {
                        "type": "array",
                        "description": "Categories of the actions.",
                        "maxItems": 32,
                        "items": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 32,
                        },
                    },
                    "resources": {
                        "additionalProperties": False,
                        "type": "object",
                        "properties": {
                            "cpu": {"type": "number", "minimum": 0.1},
                            "memory": {
                                "anyOf": [
                                    {"type": "string", "minLength": 2, "maxLength": 24},
                                    {"type": "number", "minimum": 1_000_000},
                                ]
                            },
                            "time": {
                                "anyOf": [
                                    {"type": "string", "minLength": 2, "maxLength": 32},
                                    {"type": "number", "minimum": 1},
                                ]
                            },
                            "gpu": {"type": "number", "minimum": 1},
                        },
                    },
                },
                "required": ["id", "human_name", "type"],
            },
        },
        "required": ["apiVersion", "kind", "spec"],
    }


@dataclass
class RepositoryActionResources:
    id: str
    cpu: Optional[float] = None
    memory: Optional[int] = None
    time: Optional[float] = None
    gpu: Optional[int] = None

    @staticmethod
    def from_metadata(
        cpu: Optional[float] = None,
        memory: Optional[Union[int, str]] = None,
        time: Optional[Union[float, str]] = None,
        gpu: Optional[int] = None,
        minimum_memory_allocation: int = 32 * 1024**2,  # 32MB
    ) -> None:
        times_to_seconds = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        time_units = ",".join(times_to_seconds.keys())
        float_time: Optional[float] = None
        if isinstance(time, float) or isinstance(time, int):
            float_time = float(time)
        elif time is not None and float_time is None:
            try:
                if time[-1] not in times_to_seconds:
                    raise RepositoryActionResourceRequestInvalidException(
                        f"Time value must end with one of these units: {time_units}"
                    )
            except (TypeError, IndexError):
                raise RepositoryActionResourceRequestInvalidException(
                    f"Time value must end with one of these units: {time_units}"
                )
            try:
                float_time = float(time[:-1]) * times_to_seconds[time[-1]]
            except ValueError:
                raise RepositoryActionResourceRequestInvalidException(
                    f"Time value must be a float that end with one of these units: {time_units}"
                )

        if float_time is not None and float_time <= 0:
            raise RepositoryActionResourceRequestInvalidException(
                "Time value must not be zero or negative"
            )

        memory_in_bytes = {"K": 1024, "M": 1024**2, "G": 1024**3}
        memory_units = ",".join(memory_in_bytes.keys())
        int_memory: Optional[int] = None
        if isinstance(memory, int):
            int_memory = memory
        elif memory is not None and int_memory is None:
            try:
                if memory[-1] not in memory_units:
                    raise RepositoryActionResourceRequestInvalidException(
                        f"Memory value must end with one of these units: {memory_units}"
                    )
            except (TypeError, IndexError):
                raise RepositoryActionResourceRequestInvalidException(
                    f"Memory value must end with one of these units: {memory_units}"
                )
            try:
                int_memory = int(memory[:-1]) * memory_in_bytes[memory[-1]]
            except ValueError:
                raise RepositoryActionResourceRequestInvalidException(
                    f"Memory value must be a float that end with one of these units: {memory_units}"
                )

        if int_memory is not None and int_memory <= minimum_memory_allocation:
            raise RepositoryActionResourceRequestInvalidException(
                f"Memory value must not be less then {minimum_memory_allocation} bytes to be able to start the action runtime"
            )
