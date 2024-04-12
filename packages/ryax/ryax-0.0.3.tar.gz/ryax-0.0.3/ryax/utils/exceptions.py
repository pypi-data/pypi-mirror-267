from dataclasses import dataclass


class ActionNotFoundException(Exception):
    pass


class ActionBuildNotAllowedException(Exception):
    pass


class ActionUnauthorizedDelete(Exception):
    pass


class ActionInvalidSchemaException(Exception):
    message: str = "Invalid ryax_metadata.yaml file."


class ActionRunnerFileNotFoundException(Exception):
    pass


class RepositoryActionResourceRequestInvalidException(Exception):
    pass


class ActionHandleFunctionInvalidArgumentCountException(Exception):
    pass


class ActionHandleFunctionNotFoundException(Exception):
    pass


class ActionMetadataIsV1Exception(Exception):
    pass


class ActionDynamicOutputsNotPermittedException(Exception):
    pass


class ActionIOInvalidTypeException(Exception):
    pass


class UnableToOpenLogoFileException(Exception):
    pass


class ActionSurpassesDataLimitException(Exception):
    pass


class UnableToLoadActionFilesException(Exception):
    pass


class RepositoryActionInvalidKindException(Exception):
    pass


class RepositoryActionInvalidTypeException(Exception):
    pass


class RepositoryActionTechnicalNameInvalidException(Exception):
    pass


class LogoFileDoesNotExistException(Exception):
    pass


class LogoFileInvalidFileTypeException(Exception):
    pass


class LogoFileTooLargeException(Exception):
    pass


class RepositoryActionDuplicatedInputTechnicalNameException(Exception):
    pass


class RepositoryActionDuplicatedOutputTechnicalNameException(Exception):
    pass


@dataclass
class ActionScanErrors:
    """String representations for git_repo scan errors"""

    technical_name_is_invalid: str = (
        "Action 'id' is invalid, it should only contain lowercase letters,"
        " numbers or dots."
    )
    type_is_invalid: str = "Defined 'type' is invalid or missing."
    kind_is_invalid: str = "Defined 'kind' is invalid or missing."
    logo_file_not_found: str = "The logo file was not found."
    logo_file_invalid_format: str = "The logo file must be either .jpg or .png."
    logo_too_large: str = "The logo file must be a maximum of 250x250 pixels."
    read_metadata_fail: str = "Unable to read metadata file."
    parse_metadata_fail: str = "Unable to parse metadata file."
    handler_not_found: str = "File ryax_handler.py not found."
    duplicated_input_technical_name: str = "Two inputs (or more) have the same name."
    duplicated_output_technical_name: str = "Two outputs (or more) have the same name."
    size_too_big: str = "Action size is too big."
    runner_file_syntax_error: str = "Syntax Error in python handler file."
    runner_file_handle_function_error: str = (
        "Action must have a function 'handle' (or 'handler' for triggers)"
        " that takes exactly 1 argument."
    )
    runner_file_handle_function_invalid_argument_count: str = (
        "Handle function in the python code has an invalid number of arguments."
    )
    metadata_apiversion_is_v1: str = "Metadata apiVersion v1 no longer supported."
    non_trigger_action_has_dynamic_outputs: str = (
        "Only trigger actions may have dynamic outputs"
    )
    action_io_invalid_type: str = "An IO value in the metadata has an unsupported type."
    action_logo_file_could_not_be_opened: str = (
        "Action has logo defined but the file could not be opened."
    )
    action_files_exceed_data_limit: str = "Action files exceed data limit of 1GB."
    unable_to_open_action_files: str = (
        "Unable to open repository_action files in directory."
    )
    action_time_request_invalid: str = "Action time request is in valid. Must be a float followed by one of 's, m, h, d'"
