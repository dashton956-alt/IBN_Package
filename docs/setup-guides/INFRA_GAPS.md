# Infrastructure Gaps

This document lists missing or weak areas in the current environment for the POC and recommended remediation steps.

## High-priority gaps
1. Secrets management
   - Current state: Pack configs and tokens may be stored in plaintext or local env files.
   - Recommendation: Deploy HashiCorp Vault (or use cloud KMS) and integrate with ST2 actions to fetch secrets at runtime.
2. Telemetry ingestion & correlation
   - Current state: No centralized telemetry collector configured for device metrics and logs.
   - Recommendation: Start with Loki + Promtail for logs and Prometheus for metrics. Add Grafana for dashboards and alerting. For deeper analysis, consider an ELK or OpenSearch deployment.
3. Sandbox/testbed
   - Current state: No dedicated test/dev device group.
   - Recommendation: Use device emulators (EVE-NG, VIRL) or a spare device VLAN for safe testing.

## Medium-priority gaps
4. RBAC & Audit
   - Current state: No formal RBAC for ST2 or NetBox beyond default user accounts.
   - Recommendation: Configure ST2 roles and NetBox user groups; ensure audit logging is enabled and retained.
5. Observability playbooks
   - Current state: No defined detection rules that trigger ST2 workflows.
   - Recommendation: Define 3-5 rules (interface error spike, BGP flap, sudden CPU) and map them to ST2 workflows for automated response.

## Low-priority / add-on
6. Model training and AIOps pipelines
   - Recommendation: Capture labeled events and outcomes to train models; use a small ML pipeline (Jupyter, scikit, or cloud ML) for anomaly scoring.
7. CI/CD for packs
   - Recommendation: Add a pipeline (GitHub Actions) that lints packs, runs unit tests, and publishes to pack repos.

## Quick remediation steps (POC-friendly)
- Short-term (days):
  - Use ST2 encrypted K/V for tokens (quick). Deploy Loki + Grafana as a lightweight logs pipeline.
  - Create a single test device group in NetBox and tag devices as `poctest`.
- Mid-term (weeks):
  - Deploy Vault; integrate ST2 packs with a secrets fetch action.
  - Implement Prometheus exporters and a basic Grafana dashboard for device health.

## Impact if not addressed
- Secrets leakage risk and difficulty rotating keys.
- Harder to validate automation effects without telemetry.
- Risk of running destructive playbooks against production devices.
