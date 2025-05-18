from typing import Annotated

from pydantic import Field, StringConstraints


type NoWhitespaceString = Annotated[str, StringConstraints(strip_whitespace=True)]
type PositiveInt = Annotated[int, Field(gt=0)]
type PositiveFloat = Annotated[float, Field(gt=0)]
