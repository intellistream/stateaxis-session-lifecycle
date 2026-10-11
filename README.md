# stateaxis-session-lifecycle

Extension ID: `org.vllm-hust.stateaxis-session-lifecycle`

Session-qualified reuse and soft-protected state eviction.

This repository is the independent MOD boundary for StateAxis issue
[#11](https://github.com/Qixin-Gaoke/stateaxis/issues/11). Version `0.2.0` is an
active Manifest 0.3 contract for the existing StateAxis generation-safe session
lifecycle mechanism. It remains default-off and may only be enabled by Extension
Manager/ECPA with the exact research-manifest digest.

## Evidence boundary

Status: **historical mixed, active experimental, not performance-qualified**.

In the preserved Qwen2.5-14B capacity-pressure cell, recomputed prompt tokens fell
from 12 to 0 and logical throughput improved by 0.506%, while TTFT tails were mixed.
That result predates this active revision and is not a general performance claim.

The copied evidence and its SHA-256 are recorded in `PROVENANCE.json`. Negative,
failed, and inconclusive results are retained. Microbenchmarks and component results
must not be restated as online end-to-end gains.

## Install and inspect

```bash
python -m pip install .
vllm-hust-ext extension inspect org.vllm-hust.stateaxis-session-lifecycle
vllm-hust-ext extension check org.vllm-hust.stateaxis-session-lifecycle
```

Discovery alone does not enable the MOD. The admitted ON contract fixes the session
and holder bounds, generation binding, transactional holder updates, idle-close
rules, shared-state lifetime, deterministic soft-protection policy, leased-state
exclusion, and fail-closed behavior. StateAxis rejects direct activation that lacks
the pinned MOD identity.

## Activate through Extension Manager

```bash
export VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json
vllm-hust-ext extension check org.vllm-hust.stateaxis-session-lifecycle
vllm-hust-ext extension plan org.vllm-hust.stateaxis-session-lifecycle
vllm-hust-ext run --dry-run -- /path/to/native_state_engine ...
```

Rollback is omission: remove the MOD from the Manager plan. The StateAxis default
then allocates no session tables and uses no session-aware pressure authority.

## Validate

```bash
python -m pip install -e '.[test]'
pytest -q
```

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.
