# Historical R3/R3c matched real-NPU result

This is the accepted issue #11 capacity-pressure campaign: Qwen2.5-14B BF16,
capacity 17, 256 physical blocks, physical Ascend 910B2 NPU5, and three fresh
processes per arm.

| Metric | Control | Candidate | Interpretation |
|---|---:|---:|---|
| Recomputed prompt tokens | 12 | 0 | -100%; passes 20% gate |
| Protected-root state hits | 0 | 3 | candidate preserved each reusable root |
| Logical request/s p50 | 8.8560 | 8.9009 | +0.506% point estimate |
| TTFT P99 | 63.965 ms | 65.091 ms | +1.76% |
| TPOT P99 | 43.688 ms | 41.273 ms | -5.53% |
| Sojourn P99 | 113.127 ms | 82.347 ms | directionally lower |
| Peak HBM | 53,534 MiB | 53,534 MiB | unchanged |

All six formal runs were exact and lifecycle-correct. Each arm made six pressure
evictions with zero fallback. The independent all-protected gate also showed soft
protection cannot permanently block admission, and exact close reclaimed all states.

The registered acceptance predicate passed because recomputation fell by 100% and
candidate TPOT P99 did not regress. Serving performance is still mixed: the throughput
gain is small and TTFT P99 is worse. This is therefore a useful historical component
result, not a general end-to-end speedup or qualification of active v0.2.0.

`rejected-unmatched-result.json` is intentionally retained. Its request/s numerator
counted the control-only expected stale request and compared 20 control attempts with
19 candidate operations. `result_corrected_r3c.json` uses 19 logical operations per
arm without changing any raw timing and is authoritative for throughput.
