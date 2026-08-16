"""Executable evidence for the Murphy 0030 gate.

These tests prove implementation properties only; they do not certify
source-faithful box-size governance or grant Freeze authority.
"""

from src.murphy_0030_0032.pnf_3box_reference import PNF3BoxReference, PNFBar


def _bars():
    return [
        PNFBar("2024-01-01", 100, 101, 99, 101),
        PNFBar("2024-01-02", 101, 104, 100, 103),
        PNFBar("2024-01-03", 103, 104, 99, 100),
        PNFBar("2024-01-04", 100, 100, 94, 95),
        PNFBar("2024-01-05", 95, 99, 95, 98),
    ]


def _signature(columns):
    return [(column.kind, tuple(column.boxes)) for column in columns]


def test_c3_prefix_state_is_immune_to_future_suffix():
    data = _bars()
    prefix = data[:3]
    suffix = data[3:]
    prefix_state = PNF3BoxReference(1.0).build_snapshots(prefix)[-1]
    full_states = PNF3BoxReference(1.0).build_snapshots(prefix + suffix)
    assert _signature(prefix_state) == _signature(full_states[len(prefix) - 1])


def test_c4_replay_is_deterministic():
    data = _bars()
    first = PNF3BoxReference(1.0).build(data)
    second = PNF3BoxReference(1.0).build(data)
    assert _signature(first) == _signature(second)


def test_gate_fixture_is_pre_oos_2025():
    assert all(bar.timestamp[:4] != "2025" for bar in _bars())
