import ast
import itertools
import random
import re
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from ryax.utils.exceptions import (
    ActionScanErrors,
    ActionSurpassesDataLimitException,
    ActionInvalidSchemaException,
    ActionRunnerFileNotFoundException,
    ActionMetadataIsV1Exception,
    RepositoryActionTechnicalNameInvalidException,
    ActionDynamicOutputsNotPermittedException,
    ActionIOInvalidTypeException,
    RepositoryActionDuplicatedInputTechnicalNameException,
    RepositoryActionDuplicatedOutputTechnicalNameException,
    ActionHandleFunctionNotFoundException,
    ActionHandleFunctionInvalidArgumentCountException,
    LogoFileDoesNotExistException,
    LogoFileInvalidFileTypeException,
    LogoFileTooLargeException,
    UnableToOpenLogoFileException,
    UnableToLoadActionFilesException,
    RepositoryActionInvalidTypeException,
    RepositoryActionInvalidKindException,
    RepositoryActionResourceRequestInvalidException,
)
from ryax.ryax_metadata.entities import (
    RyaxMetadataSchemaV2,
    RepositoryActionResources,
    RepositoryActionType,
    RepositoryActionKind,
    RepositoryActionIOType,
)
import yaml
from jsonschema import ValidationError, validate
from PIL import Image


@dataclass
class RyaxMetadata:
    metadata_file_content: dict
    action_dir: Path
    is_a_trigger: bool
    generated_metadata: bool
    scan_errors: list

    @classmethod
    def from_handler_file(cls, action_dir: Path) -> "RyaxMetadata":
        handler_file = (
            action_dir / "ryax_handler.py"
            if Path(action_dir / "ryax_handler.py").is_file()
            else action_dir / "ryax_run.py"
        )
        is_trigger = bool(handler_file.name != "ryax_handler.py")
        metadata_template: dict = {
            "apiVersion": "ryax.tech/v2.0",
            "kind": "Source" if is_trigger else "Processor",
            "spec": {
                "id": cls.gen_action_id(),
                "human_name": action_dir.name,
                "type": "python3",
                "version": "1.0",
                "description": "Action Description",
                "dependencies": [],
                "categories": [],
                "resources": {},
                "inputs": [
                    {
                        "help": "IO Help",
                        "human_name": "IO Display Name",
                        "name": "io_name",
                        "type": "integer",
                        "optional": False,
                    },
                ],
                "outputs": [
                    {
                        "help": "IO Help",
                        "human_name": "IO Display Name",
                        "name": "io_name",
                        "type": "integer",
                        "optional": False,
                    },
                ],
            },
        }
        return RyaxMetadata(
            metadata_file_content=metadata_template,
            action_dir=action_dir,
            is_a_trigger=is_trigger,
            generated_metadata=True,
            scan_errors=[],
        )

    @staticmethod
    def gen_action_id() -> str:
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=16))

    @classmethod
    def from_metadata_and_handler_file(cls, action_dir: Path) -> "RyaxMetadata":
        handler_file = (
            action_dir / "ryax_handler.py"
            if Path(action_dir / "ryax_handler.py").is_file()
            else action_dir / "ryax_run.py"
        )
        metadata_file = action_dir / "ryax_metadata.yaml"
        action_dir = handler_file.absolute().parent
        is_trigger = bool(handler_file.name != "ryax_handler.py")
        with open(metadata_file, "r") as f:
            ryax_metadata_content = yaml.safe_load(f)
        return RyaxMetadata(
            metadata_file_content=ryax_metadata_content,
            action_dir=action_dir,
            is_a_trigger=is_trigger,
            generated_metadata=False,
            scan_errors=[],
        )

    def write_metadata(self) -> None:
        metadata_loc: Path = self.action_dir / "ryax_metadata.yaml"
        with open(metadata_loc, "w") as f:
            yaml.dump(self.metadata_file_content, f)

    def add_io(self, add_input: bool = True) -> None:
        io_spec = (
            {
                "help": "IO Help",
                "human_name": "IO Display Name",
                "name": "io_name",
                "type": "integer",
                "optional": False,
            },
        )
        if add_input:
            self.metadata_file_content["spec"]["inputs"].append(io_spec)
        else:
            self.metadata_file_content["spec"]["outputs"].append(io_spec)

    def check_schema_validity(self) -> None:
        # Api Version
        if self.metadata_file_content.get("apiVersion") == "ryax.tech/v1":
            raise ActionMetadataIsV1Exception
        # Schema Validation
        try:
            validate(
                instance=self.metadata_file_content, schema=RyaxMetadataSchemaV2.schema
            )
        except ValidationError as err:
            message = "Invalid ryax_metadata.yaml file"
            if (
                len(err.message) <= 255
            ):  # err.message copies the data set in input, and it can be very long
                message += f": {err.message}"
            if len(err.path) > 0:
                path = "[%s]" % "][".join(repr(index) for index in err.path)
                message += f" in {path}."
            else:
                message += "."
            raise ActionInvalidSchemaException(message)
        # ID
        if not self.metadata_file_content.get("id", None):
            self.metadata_file_content["id"] = self.gen_action_id()
        if re.match("^[a-z0-9-.]+$", self.metadata_file_content["id"]) is None:
            raise RepositoryActionTechnicalNameInvalidException
        # Kind & Dynamic Outputs
        if (
            RepositoryActionKind.string_to_enum(self.metadata_file_content["kind"])
            != RepositoryActionKind.SOURCE
            and self.metadata_file_content["spec"].get("dynamic_outputs", False) is True
        ):
            raise ActionDynamicOutputsNotPermittedException()
        # Resources
        RepositoryActionResources.from_metadata(
            cpu=self.metadata_file_content["spec"]["resources"].get("cpu"),
            memory=self.metadata_file_content["spec"]["resources"].get("memory"),
            time=self.metadata_file_content["spec"]["resources"].get("time"),
            gpu=self.metadata_file_content["spec"]["resources"].get("gpu"),
        ) if self.metadata_file_content["spec"].get("resources") is not None else None
        # IOs
        inputs = self.metadata_file_content["spec"].get("inputs", [])
        for metadata_input in inputs:
            if not RepositoryActionIOType.has_value(metadata_input["type"]):
                raise ActionIOInvalidTypeException
        for input_a, input_b in itertools.combinations(inputs, 2):
            if input_a["name"] == input_b["name"]:
                raise RepositoryActionDuplicatedInputTechnicalNameException
        outputs = self.metadata_file_content["spec"].get("outputs", [])
        for metadata_output in outputs:
            if not RepositoryActionIOType.has_value(metadata_output["type"]):
                raise ActionIOInvalidTypeException
        for output_a, output_b in itertools.combinations(outputs, 2):
            if output_a["name"] == output_b["name"]:
                raise RepositoryActionDuplicatedOutputTechnicalNameException
        # Logo
        metadata_logo: str = self.metadata_file_content["spec"].get("logo", None)
        if metadata_logo is not None:
            logo_path = Path(metadata_logo)
            logo_complete_path = Path(self.action_dir / logo_path).absolute()
            self.check_logo_file(logo_complete_path)
            self.load_logo_file(logo_complete_path)

    @staticmethod
    def _load_runner_file_contents(runner_file_path: Path) -> str:
        """Loads the runner file as a raw string"""
        with open(runner_file_path, "r") as f:
            return f.read()

    @staticmethod
    def _confirm_has_handler_function(
        parsed_runner_file_contents: ast.AST, kind: str
    ) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
        """Checks that the user has defined a handler/run function"""
        generator = ast.walk(parsed_runner_file_contents)
        if kind == RepositoryActionKind.SOURCE.value:
            for node in generator:
                if isinstance(node, ast.AsyncFunctionDef) and (node.name == "run"):
                    return node
        else:
            for node in generator:
                if isinstance(node, ast.FunctionDef) and node.name == "handle":
                    return node
        raise ActionHandleFunctionNotFoundException()

    @staticmethod
    def _check_handler_args(
        handler_node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        kind: RepositoryActionKind,
        has_addons: bool,
    ) -> None:
        """Checks that the handler method in the user code takes the correct amount of arguments"""
        action_args = 2 if has_addons else 1
        trigger_args = 3 if has_addons else 2

        handler_args = next(
            len(node.args)
            for node in ast.walk(handler_node)
            if isinstance(node, ast.arguments)
        )
        if not (
            (handler_args == action_args and kind != RepositoryActionKind.SOURCE)
            or (handler_args == trigger_args and kind == RepositoryActionKind.SOURCE)
        ):
            raise ActionHandleFunctionInvalidArgumentCountException()

    def check_runner_file_validity(
        self,
    ) -> None:
        """
        Checking the python code of the runner file:
        1. Locate the existing file and load its contents
        2. Parse the contents and check for a handle(r) function that takes 1 argument
        """
        if (
            self.metadata_file_content["spec"]["type"]
            == RepositoryActionType.PYTHON3.value
        ):
            trigger_runner = "ryax_run.py"
            action_runner = "ryax_handler.py"

            runner_path = (
                self.action_dir / trigger_runner
                if self.metadata_file_content["kind"]
                == RepositoryActionKind.SOURCE.value
                else self.action_dir / action_runner
            )
            if not runner_path.is_file():
                raise ActionRunnerFileNotFoundException()

            runner_file_contents = self._load_runner_file_contents(runner_path)
            parsed_contents = ast.parse(runner_file_contents)
            _ = self._confirm_has_handler_function(
                parsed_contents, self.metadata_file_content["kind"]
            )
            # TODO decide if this check is needed after addons are supported
            # self._check_handler_args(handler_node, kind, has_addons)
        if type == RepositoryActionType.CSHARP_DOTNET6:
            # TODO Do some validation using something like https://github.com/pan-unit42/dotnetfile
            pass

    @staticmethod
    def _load_file_content_as_bytes(file_path: Path) -> bytes:
        """Reads a file in binary mode and returns the content"""
        with open(file_path, "rb") as file:
            content = file.read()
        return content

    @staticmethod
    def check_logo_file(logo_path: Path) -> None:
        if not logo_path.is_file():
            raise LogoFileDoesNotExistException
        elif logo_path.suffix not in [".png", ".jpg", ".jpeg"]:
            raise LogoFileInvalidFileTypeException
        else:
            with Image.open(str(logo_path)) as img:
                width, height = img.size
            if width > 250 or height > 250:
                raise LogoFileTooLargeException

    def load_logo_file(self, logo_path: Path) -> bytes:
        """Loads the repository_action logo"""
        try:
            logo_content = self._load_file_content_as_bytes(logo_path)
            return logo_content
        except Exception:
            raise UnableToOpenLogoFileException

    def check_action_data(
        self,
    ) -> None:
        """
        Principal method used for creating a RepositoryAction from user code.
        Checks all the user files and catches any possible exceptions
        """
        try:
            self.check_schema_validity()
            self.check_runner_file_validity()
        except (IOError, FileNotFoundError):
            self.scan_errors.append(ActionScanErrors.read_metadata_fail)
        except ActionIOInvalidTypeException:
            self.scan_errors.append(ActionScanErrors.action_io_invalid_type)
        except ActionMetadataIsV1Exception:
            self.scan_errors.append(ActionScanErrors.metadata_apiversion_is_v1)
        except ActionInvalidSchemaException as err:
            self.scan_errors.append(str(err))
        except yaml.YAMLError:
            self.scan_errors.append(ActionScanErrors.parse_metadata_fail)
        except ActionRunnerFileNotFoundException:
            self.scan_errors.append(ActionScanErrors.handler_not_found)
        except SyntaxError:
            self.scan_errors.append(ActionScanErrors.runner_file_syntax_error)
        except ActionHandleFunctionNotFoundException:
            self.scan_errors.append(ActionScanErrors.runner_file_handle_function_error)
        except ActionHandleFunctionInvalidArgumentCountException:
            self.scan_errors.append(
                ActionScanErrors.runner_file_handle_function_invalid_argument_count
            )
        except ActionDynamicOutputsNotPermittedException:
            self.scan_errors.append(
                ActionScanErrors.non_trigger_action_has_dynamic_outputs
            )
        except UnableToOpenLogoFileException:
            self.scan_errors.append(
                ActionScanErrors.action_logo_file_could_not_be_opened
            )
        except ActionSurpassesDataLimitException:
            self.scan_errors.append(ActionScanErrors.action_files_exceed_data_limit)
        except UnableToLoadActionFilesException:
            self.scan_errors.append(ActionScanErrors.unable_to_open_action_files)
        except RepositoryActionInvalidKindException:
            self.scan_errors.append(ActionScanErrors.kind_is_invalid)
        except RepositoryActionInvalidTypeException:
            self.scan_errors.append(ActionScanErrors.type_is_invalid)
        except RepositoryActionTechnicalNameInvalidException:
            self.scan_errors.append(ActionScanErrors.technical_name_is_invalid)
        except LogoFileDoesNotExistException:
            self.scan_errors.append(ActionScanErrors.logo_file_not_found)
        except LogoFileInvalidFileTypeException:
            self.scan_errors.append(ActionScanErrors.logo_file_invalid_format)
        except LogoFileTooLargeException:
            self.scan_errors.append(ActionScanErrors.logo_too_large)
        except RepositoryActionDuplicatedInputTechnicalNameException:
            self.scan_errors.append(ActionScanErrors.duplicated_input_technical_name)
        except RepositoryActionDuplicatedOutputTechnicalNameException:
            self.scan_errors.append(ActionScanErrors.duplicated_output_technical_name)
        except RepositoryActionResourceRequestInvalidException as err:
            self.scan_errors.append(str(err))
