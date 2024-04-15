"""Waylay Function Registry: apis."""

# import apis into api package
from .about_api import AboutApi
from .jobs_api import JobsApi
from .model_functions_api import ModelFunctionsApi
from .plug_functions_api import PlugFunctionsApi
from .runtimes_api import RuntimesApi
from .schemas_api import SchemasApi
from .webscript_functions_api import WebscriptFunctionsApi

__all__ = [
    "AboutApi",
    "JobsApi",
    "ModelFunctionsApi",
    "PlugFunctionsApi",
    "RuntimesApi",
    "SchemasApi",
    "WebscriptFunctionsApi",
]
