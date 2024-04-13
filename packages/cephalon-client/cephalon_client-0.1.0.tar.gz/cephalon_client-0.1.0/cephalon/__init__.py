import warnings
from typing import Optional, Any
from cephalon.core import Config, Client, client
from cephalon import path

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="Accessing `.value` on Result type is deprecated, please use `.ok_value` or `.err_value` instead",
)
