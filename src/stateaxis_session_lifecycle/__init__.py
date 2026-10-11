"""Exact activation contract for bounded StateAxis session lifecycle authority."""

from __future__ import annotations

from dataclasses import dataclass

MOD_ID = "org.vllm-hust.stateaxis-session-lifecycle"


@dataclass(frozen=True, slots=True)
class SessionLifecycleConfig:
    """The only session lifecycle and pressure policy admitted by StateAxis."""

    enabled: bool = True
    max_session_ids: int = 64
    max_holder_edges: int = 256
    pressure_policy: str = "session_aware"
    generation_bound: bool = True
    transactional_holder_edges: bool = True
    idle_close_required: bool = True
    exclusive_state_reclaimed_on_close: bool = True
    shared_state_survives_until_last_holder: bool = True
    soft_protection: bool = True
    leased_states_ineligible: bool = True
    deterministic_candidate_order: bool = True
    fail_closed: bool = True

    def __post_init__(self) -> None:
        if self != SessionLifecycleConfig.__new_default():
            raise ValueError("session lifecycle requires the reviewed bounded contract")

    @classmethod
    def __new_default(cls) -> SessionLifecycleConfig:
        instance = object.__new__(cls)
        for field, value in (
            ("enabled", True),
            ("max_session_ids", 64),
            ("max_holder_edges", 256),
            ("pressure_policy", "session_aware"),
            ("generation_bound", True),
            ("transactional_holder_edges", True),
            ("idle_close_required", True),
            ("exclusive_state_reclaimed_on_close", True),
            ("shared_state_survives_until_last_holder", True),
            ("soft_protection", True),
            ("leased_states_ineligible", True),
            ("deterministic_candidate_order", True),
            ("fail_closed", True),
        ):
            object.__setattr__(instance, field, value)
        return instance


def session_lifecycle() -> SessionLifecycleConfig:
    """Return the default-off candidate's admitted ON configuration."""

    return SessionLifecycleConfig()


__all__ = ["MOD_ID", "SessionLifecycleConfig", "session_lifecycle"]
