from __future__ import annotations

from dataclasses import dataclass, make_dataclass
from enum import Enum
from typing import List, Optional, Type, TypedDict, cast

from rest_framework.request import Request
from rest_framework.views import APIView

from drf_error_handler.settings import DEFAULTS, IMPORT_STRINGS, PackageSettings

package_settings = PackageSettings(DEFAULTS, IMPORT_STRINGS)


class ExceptionHandlerContext(TypedDict):
    view: APIView
    args: tuple
    kwargs: dict
    request: Optional[Request]


BUSINESS_CODE_NAME = cast(str, package_settings.EXCEPTION_RESPONSE_BUSINESS_ATTRIBUTE)


class ErrorType(str, Enum):
    VALIDATION_ERROR = "validation_error"
    CLIENT_ERROR = "client_error"
    SERVER_ERROR = "server_error"


Error = make_dataclass("Error", [("detail", str), ("attr", Type[Optional[str]]), (BUSINESS_CODE_NAME, int)])

@dataclass
class ErrorResponse:
    type: ErrorType
    errors: List[Error] # type: ignore[reportInvalidTypeForm]


class SetValidationErrorsKwargs(TypedDict):
    error_codes: List[str]
    field_name: Optional[str]
    actions: Optional[List[str]]
    methods: Optional[List[str]]
    versions: Optional[List[str]]
