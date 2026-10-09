# Issue #11 hard-capacity session pressure closure — 2026-08-15

> **Point-in-time report — not current repository status.** Current
> classification lives in [`NATIVE_ENGINE_STATUS.md`](../../NATIVE_ENGINE_STATUS.md).

## Decision

Issue #11's remaining hard-pressure contract is complete. The production
candidate stays default-off. The result is positive for protected-state reuse
and recomputation, but mixed end to end; it is not a general speedup or vLLM
comparison claim.

## Production boundary

At the existing admission boundary, and only when no request can be planned
because all state slots are occupied, the new policy may select one safe idle
resident state. Leased states are never eligible. Control uses stable `StateKey`
order. Candidate uses the same eligible set and puts unprotected states first;
when every eligible state is protected it still chooses one, because session
protection is deliberately soft rather than a hard pin. The feature is disabled
by default, and `session_aware` fails validation unless session lifecycle
authority is also enabled.

Bounded telemetry records requests, applications, fallbacks, protected and
unprotected evictions, evicted token counts, and the latest decisions. The
public generate protocol and model execution semantics are unchanged.

## Frozen identity and gates

- official local image:
  `quay.io/ascend/vllm-ascend:v0.23.0rc1-openeuler`, image ID
  `sha256:f4c89c293e076453e9eef9edb5fb9669740dccbd3c48619a9f976d775fc29b81`;
- aggregate r3 identity: `e8dd29d35de9d0f171d450505b2a9686d038c60c15393677eecb7285d8d6b07d`;
- frozen Rust server: `9e6f69ab66a0a2425cf3ed57a15060e639c452a86f66caed862b011f0866e3fa`;
- frozen C++ worker: `cdda03cf1491f4e7e18296f966b89232bae64abb78bbd578cc5bfffd08524744`;
- workload SHA-256:
  `acab2ef22a997197a2fae7c94ea85519ed7b971c4a76a9174b5bda734c8a49c9`;
- state capacity 17, physical cache blocks 256, Qwen2.5-14B BF16, one fresh
  server/worker process per run.

All 237 Rust library tests and all-target build checks passed before hardware
execution. The reuse 1+1 passed token/lifecycle exactness: control observed the
pre-registered `409 StaleState` and recomputed four prompt tokens, while
candidate retained an exact hit and recomputed zero. Both arms made two
pressure decisions with zero fallback. The independent all-protected 1+1 also
passed: candidate made one protected eviction, continued serving, and exact
close reclaimed all 17 states. This proves protection cannot permanently block
admission.

## Repeated real-NPU result

The accepted NPU5 campaign completed three fresh processes per arm in the
pre-registered order. All six formal runs were exact and lifecycle-correct;
each arm made six pressure evictions with zero fallback. No run was removed.

| Metric | Control | Candidate | Interpretation |
|---|---:|---:|---|
| recomputed prompt tokens | 12 | 0 | 100% reduction; passes the 20% gate |
| protected-root state hits | 0 | 3 | candidate preserved each reusable root |
| logical request/s p50 | 8.8560 | 8.9009 | candidate +0.506% point estimate |
| TTFT p50 / p95 / p99 | 56.914 / 59.944 / 63.965 ms | 56.733 / 63.460 / 65.091 ms | mixed; p99 +1.76% |
| TPOT p50 / p95 / p99 | 40.680 / 42.358 / 43.688 ms | 40.676 / 41.141 / 41.273 ms | p99 -5.53%; passes the no-regression gate |
| sojourn p50 / p95 / p99 | 57.207 / 92.738 / 113.127 ms | 56.918 / 81.789 / 82.347 ms | tail directionally lower |
| peak HBM | 53,534 MiB | 53,534 MiB | unchanged at sampler resolution |
| throughput coefficient of variation | 0.823% | 0.683% | low within-arm dispersion |
| candidate close-to-reclaim p50 / p95 / max | n/a | 1.619 / 1.826 / 1.850 ms | five protected states reclaimed |

The frozen acceptance predicate passes because recomputation falls by 100% and
candidate TPOT p99 does not regress. The small logical-throughput point estimate
and slightly worse TTFT p99 do not establish statistical or broad serving
speedup.
The correct release classification is therefore: useful opt-in session-aware
soft protection with a positive recomputation result and mixed serving
performance.

## Evidence and failures

Accepted raw requests, per-run identities, HBM samples, summaries, status, and
cleanup are under `results/issue11-session-pressure-20260815-r3/`. Two failed
pre-release attempts remain separately preserved: one output-root preflight
rejection made no NPU request, and one candidate run exposed an incorrect probe
accounting expectation after the runtime itself had completed exact. Neither is
included in the 3+3 score.

Final review rejected the original `result.json` request/s fields because their
numerator counted the control-only expected `409 stale`, producing unmatched
20-versus-19 denominators. No raw timing changed. The identity-bound r3c
analysis uses 19 logical operations per arm and is authoritative for throughput:
control/candidate p50 is 8.8560/8.9009 logical request/s (+0.506%). The rejected
calculation remains append-only evidence. Corrected analysis identity is
`efc23629c45ad7c71f168361e26fc6d9f2fc08ff47f0543e170918f782f1c38c`.
