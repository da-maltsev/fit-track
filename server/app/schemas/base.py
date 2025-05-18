from typing import Annotated

from pydantic import StringConstraints


type NoWhitespaceString = Annotated[str, StringConstraints(strip_whitespace=True)]
