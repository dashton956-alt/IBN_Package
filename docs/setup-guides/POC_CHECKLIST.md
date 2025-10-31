# Intent-based Network Automation + AIOps POC Checklist

This file is a single-source checklist and quick-reference for the POC described in the diagram. Use it to track progress and run quick validation commands.

## Summary
- Goal: Build a minimal, secure POC to demonstrate intent-based network automation with AIOps using StackStorm (automation), NetBox (source-of-truth), Gluware (device config), and AnythingLLM (intent parsing / AI ops).
- Scope: Get secure API access, build 3 canonical playbooks (intent → NetBox → Gluware → verify), and add a basic telemetry pipeline for anomaly detection.

## Environment snapshot (as of 2025-10-07)
- NetBox: running and healthy, publishing host port 8000 -> container 8080
- StackStorm: core services running; `st2web` started and exposed on host port 8001 (remapped to avoid NetBox conflict)
- Vault: `vault-dev` is running; `vault-prod` is restarting and requires investigation if you need prod-mode Vault
- Secrets: one-off `vault-init` produced `/vault/secrets/netbox.json` in external volume `st2-docker_st2-vault-secrets` (contains NetBox secret JSON)
- Notes: StackStorm images are present locally; previous Vault Agent sidecar approach was deferred due to compose/permission complexities

## Checklist (tick boxes reflect current status)
| # | Task | Description | Status | Owner | ETA |
|---|------|-------------|:------:|:-----:|:---:|
| 1 | Review diagram & inventory | Inspect running services and diagram; produce gap analysis | ✅ Completed | Dan | - |
| 2 | Map required integrations | NetBox API, Gluware API, Telemetry collectors, Secrets store, Observability | ✅ Completed | Dan / Team | - |
| 3 | Identify missing infra/components | Vault, telemetry pipeline, sandbox, RBAC, dashboards | ✅ In-progress (partial) | Dan | 1 day |
| 4 | Recommend POC architecture & components | Minimal architecture, tradeoffs, network/data flows | 🔲 Not started | Dan | 1 day |
| 5 | Deliver POC plan & quick wins | Step-by-step tasks, commands, and example playbooks | 🔲 Not started | Dan | 2 days |
| 6 | Create service accounts + API tokens | NetBox service token, Gluware API token | 🔲 Not started | Dan | 0.5 day |
| 7 | Secure tokens (Vault or ST2 K/V) | One-off Vault write succeeded; consider Vault Agent or ST2 startup fetch for automation | 🔲 In-progress (manual done) | Dan | 0.5 day |
| 8 | Configure ST2 pack configs | `st2 pack config set` for `netbox` and `gluware` | 🔲 Not started | Dan | 0.5 day |
| 9 | Test connectivity | `st2 run` smoke tests for NetBox and Gluware actions | 🔲 Not started (st2web smoke test in progress) | Dan | 0.5 day |
| 10 | Implement 3 canonical playbooks | Intent-driven PoE/config change, anomaly remediation, daily drift audit | 🔲 Not started | Dan | 2 days |
| 11 | Basic telemetry pipeline | Syslog/SNMP → Loki/Prometheus (or ELK) → alerting | 🔲 Not started | Dan | 2–3 days |
| 12 | Integrate AnythingLLM | Intent interpretation endpoint + ST2 adapter | 🔲 Not started | Dan | 2 days |
| 13 | ChatOps approvals & notifications | Slack/MS Teams integration for approvals | 🔲 Not started | Dan | 1 day |
| 14 | Safe sandbox testing | Device emulator or a single spare device for tests | 🔲 Not started | Dan | ongoing |

---

## Gap analysis (concise)
- Secrets/credentials: no central secrets store (Vault recommended). ST2 K/V can be used for quick POC.
- Telemetry: no centralized telemetry ingestion (logs/metrics/traces) for AIOps.
- Sandbox/testbed: missing a non-production device group for safe testing.
- Observability: dashboards and correlation not yet defined.
- Pack configuration: `netbox` and `gluware` packs require secure tokens and host configuration inside ST2.

## Concrete integration checklist (commands + examples)
Below are commands you can run from the host. Replace tokens/hosts with real values.

1) Create NetBox API token (via NetBox UI):
- Log into NetBox → your user → Tokens → Add Token (create `st2-service-token`)

2) Configure NetBox pack in StackStorm (example):
```bash
# Run from host, adjust container name if different
docker exec st2-docker-st2client-1 st2 pack config netbox set '
{"hostname":"https://172.30.133.89","api_token":"<NETBOX_TOKEN>","use_https":true,"ssl_verify":false}'
```

3) Configure Gluware pack in StackStorm (example):
```bash
docker exec st2-docker-st2client-1 st2 pack config gluware set '
{"gluware_api":{"url":"https://gluware.example","token":"<GLUWARE_TOKEN>"}}'
```

4) Quick smoke tests:
```bash
# NetBox smoke test
docker exec st2-docker-st2client-1 st2 run netbox.get.dcim.devices limit=1

# Gluware smoke test
docker exec st2-docker-st2client-1 st2 run gluware.gluware.get_device serial="SOME-SERIAL"
```

5) Store secrets in StackStorm K/V (quick POC, not recommended for prod):
```bash
# Example: store a secret (key=netbox_token)
docker exec st2-docker-st2client-1 st2 key set netbox_token --value='<NETBOX_TOKEN>'
```

6) (Optional) Use HashiCorp Vault: deploy Vault and create an ST2 action to fetch secrets in playbooks.


## Minimal canonical playbooks (brief)
- Playbook A — Intent: Disable PoE on port:
  1. Parse intent (AnythingLLM or ChatOps) → extract device & port
  2. Verify device in NetBox (inventory lookup)
  3. Generate change plan & dry-run (Gluware) if available
  4. Execute config change via Gluware action
  5. Verify via telemetry/API and update a ticket

- Playbook B — Anomaly remediation:
  1. Telemetry pipeline generates alert (e.g., interface error spike)
  2. Trigger ST2 workflow: fetch device info from NetBox
  3. Run diagnostics (ping, show counters via Gluware)
  4. If fixable, apply non-invasive change; otherwise, create ticket and notify ChatOps

- Playbook C — Daily drift detection:
  1. Snapshot device config via Gluware
  2. Compare snapshot against NetBox expected config
  3. Report drift and optionally remediate or stub a ticket


## Observability & telemetry (POC recommendation)
- Start small:
  - Syslog → Loki (promtail) → Grafana (dashboards + alerting)
  - Export a few key metrics (interface errors, CPU, memory) to Prometheus
- For logs use Fluentd/Fluentbit or Filebeat to ship logs to an ELK stack or Loki
- Build 2-3 detection rules (thresholds & anomaly) that trigger ST2 workflows


## Next immediate steps (pick one)
1. I can create the `st2 pack config` commands for you and run them here if you paste the NetBox and Gluware tokens (or give me temporary placeholder tokens).
2. I can add a Vault-based secrets example and a sample ST2 action to fetch secrets from Vault.
3. I can scaffold the 3 canonical playbooks into `packs.dev` and register them with StackStorm.

Tell me which one you want me to do now and I'll start it, and I will mark the corresponding checklist items as in-progress and update the file accordingly.

## Next actions (recommended, prioritized)
1) Quick smoke-tests (recommended now)
  - Verify st2web UI is reachable and API responds (I already checked HTTP 200 on port 8001).
  - Run an ST2 NetBox smoke action (example commands below). Expected outcome: ST2 can query NetBox via configured pack or via direct curl when testing.

  Commands (run on host):
  ```bash
  # Check st2web HTTP
  curl -I http://localhost:8001

  # If you have the st2 client container available, run a NetBox lookup (adjust container name if different):
  docker exec -it st2-docker-st2client-1 st2 run netbox.get.dcim.devices limit=1 || true
  ```

2) Configure pack configs (next, low friction)
  - Create NetBox and Gluware service tokens and set them with `st2 pack config`.
  - If you prefer not to expose tokens here, I can scaffold the commands and you can paste tokens to run locally.

3) Automate secrets (follow-up)
  - Decide between: keep the one-off `vault-init` approach (simple) or rework a Vault Agent sidecar with corrected permissions and compose wiring (longer).
  - If you want automation now, I recommend the one-off approach integrated into a small startup script for ST2 that reads `/vault/secrets/netbox.json` on boot.

4) Vault-prod & Agent (deferred)
  - Investigate why `vault-prod` is restarting (check logs) only if you plan to use prod-mode Vault. Otherwise keep `vault-dev` for POC.

If you tell me which of (1)-(3) to run now, I'll mark the corresponding checklist items as in-progress and execute them.

---

*File: `POC_CHECKLIST.md` created at repository root.*

## Related documents
- `INTEGRATIONS.md` — Detailed integrations map (created)
- `INFRA_GAPS.md` — Infrastructure gaps and remediation (created)
- `POC_ARCHITECTURE.md` — Recommended minimal architecture (created)

If you'd like this file in a different name or path, tell me and I will move/rename it. 