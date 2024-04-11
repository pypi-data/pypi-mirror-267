from typing import List, Type

from sqlfluff.core.config import ConfigLoader
from sqlfluff.core.plugin import hookimpl
from sqlfluff.core.rules import BaseRule


@hookimpl
def get_rules() -> List[Type[BaseRule]]:
    """Get plugin rules."""
    from sqlfluff_common_conventions.CC01 import Rule_CC01
    from sqlfluff_common_conventions.CC02 import Rule_CC02
    from sqlfluff_common_conventions.CC03 import Rule_CC03

    return [Rule_CC01, Rule_CC02, Rule_CC03]
