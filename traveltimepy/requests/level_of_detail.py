from enum import Enum
from typing import Union, Dict, Any

from pydantic import BaseModel, Field, model_serializer


class Level(str, Enum):
    LOWEST = "lowest"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    HIGHEST = "highest"


class SimpleLevelOfDetail(BaseModel):
    """Simple level of detail configuration.

    Attributes:
        level: Specifies the detail level of the returned shape.
            Available levels:
                - LOWEST - Minimal detail, maximum performance
                - LOW - Reduced detail, improved performance
                - MEDIUM - Balanced detail and performance
                - HIGH - Enhanced detail, reduced performance
                - HIGHEST - Maximum detail, minimum performance
    """

    level: Level

    def get_type_name(self) -> str:
        return "simple"


class SimpleNumericLevelOfDetail(BaseModel):
    """Numeric level of detail configuration.

    Provides fine-grained control over rendering detail using numeric values
    instead of predefined enum levels.

    Attributes:
        level (int): The numeric level of detail value. Allows to pick less
            details compared to SimpleLevelOfDetail.

            Valid range: -20 (least detailed) to 2 (most detailed)

            Mapping to simple levels:

            - -20 to -3: Progressively less detailed than LOWEST
            - -2: Equivalent to LOWEST
            - -1: Equivalent to LOW
            - 0: Equivalent to MEDIUM
            - 1: Equivalent to HIGH
            - 2: Equivalent to HIGHEST
    """

    level: int = Field(ge=-20, le=2)

    def get_type_name(self) -> str:
        return "simple_numeric"


class CoarseGridLevelOfDetail(BaseModel):
    """Grid configuration for shape construction.

    Attributes:
        square_size (int): Specifies the grid cell size (in metres) used to construct the shape.
            This parameter controls the level of detail in the resulting shape.

            A smaller value creates a finer grid with more detail but requires more processing power.
            A larger value creates a coarser grid with less detail and improved performance.

            Examples:

            Small value (higher detail):    Large value (lower detail):
            +--+--+--+--+--+--+            +--------+--------+
            |  |  |  |  |  |  |            |        |        |
            +--+--+--+--+--+--+            |        |        |
            |  |  |  |  |  |  |            +--------+--------+
            +--+--+--+--+--+--+            |        |        |
            |  |  |  |  |  |  |            |        |        |
            +--+--+--+--+--+--+            +--------+--------+

            Minimum value: 600 metres
    """

    square_size: int = Field(ge=600)

    def get_type_name(self) -> str:
        return "coarse_grid"


class LevelOfDetail(BaseModel):
    scale_type: Union[
        SimpleLevelOfDetail, SimpleNumericLevelOfDetail, CoarseGridLevelOfDetail
    ] = SimpleLevelOfDetail(level=Level.LOWEST)

    @model_serializer
    def serialize_model(self) -> Dict[str, Any]:
        result = {"scale_type": self.scale_type.get_type_name()}
        result.update(self.scale_type.model_dump())
        return result
