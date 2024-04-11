"""State store actions.

Actions can be passed to the ActionDispatcher, where they will trigger
reactions in objects that subscribe to the pipeline, like the StateStore.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from opentrons.protocols.models import LabwareDefinition
from opentrons.hardware_control.types import DoorState
from opentrons.hardware_control.modules import LiveData

from opentrons_shared_data.errors import EnumeratedError

from ..commands import Command, CommandCreate, CommandPrivateResult
from ..types import (
    LabwareOffsetCreate,
    ModuleDefinition,
    Liquid,
    DeckConfigurationType,
    AddressableAreaLocation,
)


@dataclass(frozen=True)
class PlayAction:
    """Start or resume processing commands in the engine."""

    requested_at: datetime
    deck_configuration: Optional[DeckConfigurationType]


class PauseSource(str, Enum):
    """The source of a PauseAction.

    Attributes:
        CLIENT: the pause came externally, from the engine client.
        PROTOCOL: the pause came from the protocol itself.
    """

    CLIENT = "client"
    PROTOCOL = "protocol"


@dataclass(frozen=True)
class PauseAction:
    """Pause processing commands in the engine."""

    source: PauseSource


@dataclass(frozen=True)
class StopAction:
    """Stop the current engine execution.

    After a StopAction, the engine status will be marked as stopped.
    """

    from_estop: bool = False


@dataclass(frozen=True)
class FinishErrorDetails:
    """Error details for the payload of a FinishAction or HardwareStoppedAction."""

    error: Exception
    error_id: str
    created_at: datetime


@dataclass(frozen=True)
class FinishAction:
    """Gracefully stop processing commands in the engine."""

    set_run_status: bool = True
    """Whether to set the engine status depending on `error_details`.

    If True, the engine status will be marked `succeeded` or `failed`, depending on `error_details`.
    If False, the engine status will be marked `stopped`.
    """

    error_details: Optional[FinishErrorDetails] = None
    """The fatal error that caused the run to fail."""


@dataclass(frozen=True)
class HardwareStoppedAction:
    """An action dispatched after hardware has been stopped for good, for this engine instance."""

    completed_at: datetime

    finish_error_details: Optional[FinishErrorDetails]
    """The error that happened while doing post-run finish steps (homing and dropping tips)."""


@dataclass(frozen=True)
class DoorChangeAction:
    """Handle events coming in from hardware control."""

    door_state: DoorState


@dataclass(frozen=True)
class QueueCommandAction:
    """Add a command request to the queue."""

    command_id: str
    created_at: datetime
    request: CommandCreate
    request_hash: Optional[str]


@dataclass(frozen=True)
class UpdateCommandAction:
    """Update a given command."""

    command: Command
    private_result: CommandPrivateResult


@dataclass(frozen=True)
class FailCommandAction:
    """Mark a given command as failed.

    The given command and all currently queued commands will be marked
    as failed due to the given error.
    """

    # TODO(mc, 2021-11-12): we'll likely need to add the command params
    # to this payload for state reaction purposes
    command_id: str
    error_id: str
    failed_at: datetime
    error: EnumeratedError


@dataclass(frozen=True)
class AddLabwareOffsetAction:
    """Add a labware offset, to apply to subsequent `LoadLabwareCommand`s."""

    labware_offset_id: str
    created_at: datetime
    request: LabwareOffsetCreate


@dataclass(frozen=True)
class AddLabwareDefinitionAction:
    """Add a labware definition, to apply to subsequent `LoadLabwareCommand`s."""

    definition: LabwareDefinition


@dataclass(frozen=True)
class AddLiquidAction:
    """Add a liquid, to apply to subsequent `LoadLiquid`s."""

    liquid: Liquid


@dataclass(frozen=True)
class AddAddressableAreaAction:
    """Add a single addressable area to state.

    This differs from the deck configuration in PlayAction which sends over a mapping of cutout fixtures.
    This action will only load one addressable area and that should be pre-validated before being sent via
    the action.
    """

    addressable_area: AddressableAreaLocation


@dataclass(frozen=True)
class AddModuleAction:
    """Add an attached module directly to state without a location."""

    module_id: str
    serial_number: str
    definition: ModuleDefinition
    module_live_data: LiveData


@dataclass(frozen=True)
class ResetTipsAction:
    """Reset the tip tracking state of a given tip rack."""

    labware_id: str


@dataclass(frozen=True)
class SetPipetteMovementSpeedAction:
    """Set the speed of a pipette's X/Y/Z movements. Does not affect plunger speed.

    None will use the hardware API's default.
    """

    pipette_id: str
    speed: Optional[float]


Action = Union[
    PlayAction,
    PauseAction,
    StopAction,
    FinishAction,
    HardwareStoppedAction,
    DoorChangeAction,
    QueueCommandAction,
    UpdateCommandAction,
    FailCommandAction,
    AddLabwareOffsetAction,
    AddLabwareDefinitionAction,
    AddModuleAction,
    AddAddressableAreaAction,
    AddLiquidAction,
    ResetTipsAction,
    SetPipetteMovementSpeedAction,
]
