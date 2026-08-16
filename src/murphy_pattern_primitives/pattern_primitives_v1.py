"""Murphy 0013-0020 shared primitive interfaces.

NON-PRODUCTION / GOVERNANCE IMPLEMENTATION.
These primitives intentionally refuse to invent tolerances or filters.
They return NOT_EVALUABLE until an approved deterministic project contract
exists. They do not modify canonical Murphy semantics or generate direction.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Status(str, Enum):
    AVAILABLE = "AVAILABLE"
    NOT_EVALUABLE = "NOT_EVALUABLE"
    CONFIRMED = "CONFIRMED"
    NOT_CONFIRMED = "NOT_CONFIRMED"


@dataclass(frozen=True)
class HorizontalLevel:
    level_id: str
    level_price: float
    role: str
    availability_timestamp: str
    status: Status


@dataclass(frozen=True)
class BoundaryRelationship:
    upper_boundary_id: str
    lower_boundary_id: str
    relationship: str
    availability_timestamp: str


@dataclass(frozen=True)
class BreakoutConfirmation:
    boundary_id: str
    direction: str
    breakout_timestamp: Optional[str]
    confirmation_timestamp: Optional[str]
    availability_timestamp: str
    status: Status


@dataclass(frozen=True)
class FlagpoleRelation:
    pole_start_timestamp: Optional[str]
    pole_end_timestamp: Optional[str]
    direction: Optional[str]
    relation_to_formation: str
    availability_timestamp: str
    status: Status


def horizontal_level_without_approved_tolerance(*, level_id: str,
                                                  level_price: float,
                                                  role: str,
                                                  availability_timestamp: str) -> HorizontalLevel:
    """Do not invent a horizontal-level tolerance."""
    return HorizontalLevel(level_id, level_price, role, availability_timestamp,
                           Status.NOT_EVALUABLE)


def boundary_relationship_without_approved_tolerance(*, upper_boundary_id: str,
                                                       lower_boundary_id: str,
                                                       availability_timestamp: str) -> BoundaryRelationship:
    """Do not invent convergence/parallelism thresholds."""
    return BoundaryRelationship(upper_boundary_id, lower_boundary_id,
                                "NOT_EVALUABLE", availability_timestamp)


def breakout_without_approved_filter(*, boundary_id: str, direction: str,
                                      availability_timestamp: str) -> BreakoutConfirmation:
    """Do not convert Murphy's examples into mandatory project filters."""
    return BreakoutConfirmation(boundary_id, direction, None, None,
                                availability_timestamp, Status.NOT_EVALUABLE)


def flagpole_without_approved_sharpness(*, availability_timestamp: str) -> FlagpoleRelation:
    """Keep source-descriptive 'sharp' separate until a contract is approved."""
    return FlagpoleRelation(None, None, None, "PRECEDES", availability_timestamp,
                            Status.NOT_EVALUABLE)
