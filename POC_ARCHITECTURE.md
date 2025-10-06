# Recommended POC Architecture

This document describes a minimal, secure architecture for the intent-based network automation + AIOps POC, trade-offs, and component placement.

## Components
- StackStorm (control plane)
  - Hosts: existing `st2-docker` cluster
  - Role: Orchestrate workflows, run actions, integrate ChatOps
- NetBox (source-of-truth)
  - Hosts: existing `netbox-docker`
  - Role: Inventory, device metadata, authoritative mapping
- Gluware (device orchestration)
  - Hosts: existing Gluware controller or simulated one for POC
- AnythingLLM (intent parser)
  - Hosts: local container or cloud LLM endpoint
  - Role: Convert natural language into structured tasks or call ST2 webhook
- Vault (secrets) — recommended
  - Role: Centralized secrets store, rotate tokens
- Telemetry: Loki + Promtail, Prometheus + exporters, Grafana
  - Role: Central log/metric collection and alerting
- ChatOps (Slack/MS Teams)
  - Role: User approvals, notifications, and interactive workflows
- Sandbox (EVE-NG or spare devices)
  - Role: Safe testing before production

## Network layout (minimal)
- Management VLAN: ST2, NetBox, Gluware API endpoints, Vault
- Telemetry VLAN: Prometheus, Loki, exporters
- Device VLAN(s): Devices under test and production (use VLAN tagging for isolation)

## Data flow
1. User sends an intent via ChatOps or AnythingLLM.
2. LLM sends structured intent to ST2 webhook or ST2 sensor picks it up.
3. ST2 queries NetBox for device/port metadata.
4. ST2 calls Gluware API to generate and push config.
5. Telemetry system verifies the change, sends alerts back to ST2 if anomalies found.
6. ST2 updates NetBox and sends ChatOps notification.

## Security considerations
- Use Vault for storing tokens. ST2 should fetch tokens dynamically rather than storing secrets in files.
- Use mTLS or at minimum TLS with CA-signed certs for all APIs in production.
- Limit ST2 action runner permissions and use just-in-time approvals for risky actions.

## Trade-offs
- Simplicity vs Security: For quick POC, self-signed certs and ST2 K/V are acceptable. For production, Vault + signed certs are required.
- Observability completeness vs time: Start with logs (Loki) and 2–3 critical metrics in Prometheus, expand later.

## Minimal BOM (POC)
- StackStorm (existing)
- NetBox (existing)
- Gluware controller (existing or simulator)
- Loki + Promtail (lightweight logs)
- Grafana (dashboarding)
- HashiCorp Vault (optional for rapid secure token storage)


## Example ST2 pack config (templates)
NetBox:
```json
{
  "hostname": "https://172.30.133.89",
  "api_token": "<NETBOX_TOKEN>",
  "use_https": true,
  "ssl_verify": false
}
```
Gluware:
```json
{
  "gluware_api": { "url": "https://gluware.example", "token": "<GLUWARE_TOKEN>" }
}
```

## Next steps
- Create service tokens for NetBox & Gluware and store them in Vault or ST2 K/V.
- Add 3 sample workflows to `packs.dev` and validate with the smoke tests.
- Deploy Loki + Grafana and wire a single alert to ST2.
