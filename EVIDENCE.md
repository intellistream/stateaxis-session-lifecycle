# Evidence index

## Current independent revision

- Version: `0.2.0`
- Status: active, default-off, experimental, not performance-qualified.
- The Manifest 0.3 contract activates bounded generation-safe session lifecycle
  and session-aware soft protection through Extension Manager/ECPA.
- `evidence/ecpa-contract-20261011/`
  - Manager inspection, admission, planning, and dry-run evidence
  - labelled `manager_contract_non_performance`; no accelerator claim

## Preserved historical evidence

- `evidence/ISSUE11_SESSION_PRESSURE_CLOSURE_20260815.md`
  - matched Qwen2.5-14B real-NPU 3+3 campaign in the frozen capacity-17 cell
  - recomputed prompt tokens: 12 OFF versus 0 ON
  - logical request/s p50: 8.8560 OFF versus 8.9009 ON (+0.506%)
  - serving latency was mixed, so no general speedup claim is made
- `evidence/on-off-preflight-20261010/`
  - preserved pre-activation result; ON was not runnable at version `0.1.0.dev0`

Historical evidence does not automatically qualify version `0.2.0`. Failed,
negative, corrected, and preflight results remain part of the record.
