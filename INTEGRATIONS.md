# Integrations Map

This document lists the concrete integrations required for the Intent-based Network Automation + AIOps POC, where they connect, required protocols, and quick validation commands.

## Core systems
- StackStorm (ST2)
  - Role: Orchestration engine, workflows, sensors, and pack execution.
  - Integrations:
    - NetBox pack (source-of-truth lookup, inventory)
      - Protocol: HTTPS REST API
      - Auth: API token
      - Example ST2 config keys: `hostname`, `api_token`, `use_https`, `ssl_verify`
      - Smoke test: `st2 run netbox.get.dcim.devices limit=1`
    - Gluware pack (device configuration via Gluware controller)
      - Protocol: HTTPS REST API (Gluware API)
      - Auth: API token
      - Example ST2 config keys: `gluware_api.url`, `gluware_api.token`
      - Smoke test: `st2 run gluware.gluware.get_device serial="..."`
    - AnythingLLM adapter (optional)
      - Role: Intent parsing & prompt-to-action translation
      - Protocol: HTTP(S) to LLM service or local container
      - Auth: depends on LLM service

- NetBox
  - Role: Source-of-truth (inventory, interfaces, roles)
  - Exposed via HTTPS endpoint for ST2 and other consumers
  - Required: service account token for ST2; secure cert or validated TLS

- Gluware
  - Role: Device configuration and orchestration interface
  - Exposed via API to ST2 to push configs and run diagnostics

- Telemetry & Observability
  - Syslog/Netflow/Telemetry collectors → Loki/Promtail or ELK
  - Prometheus node exporters or exporters on devices (if supported)
  - Alertmanager or Grafana alerting to trigger ST2 webhooks

- Secrets store
  - Short-term: StackStorm encrypted K/V for POC
  - Long-term: HashiCorp Vault + ST2 integration plugin

- Event bus / messaging
  - StackStorm uses RabbitMQ already for internal messaging
  - Consider Kafka or RabbitMQ topics for telemetry ingestion if scaling

## Integration flows (high level)
1. ChatOps/AnythingLLM receives natural language intent.
2. ST2 sensor receives parsed intent (or LLM directly calls ST2 webhook).
3. ST2 workflow queries NetBox for device/port metadata.
4. ST2 executes Gluware pack actions to apply device changes.
5. Telemetry collectors validate changes; alerts feed back into ST2.
6. ST2 updates NetBox / ticketing system and notifies ChatOps.

## Quick validation commands
Run these from the host (adjust container name if different):

```bash
# List installed packs in ST2
docker exec st2-docker-st2client-1 st2 pack list

# NetBox smoke test
docker exec st2-docker-st2client-1 st2 run netbox.get.dcim.devices limit=1

# Gluware smoke test
docker exec st2-docker-st2client-1 st2 run gluware.gluware.get_device serial="SOME-SERIAL"
```


## Notes & assumptions
- All ST2 pack configs will be provided via `st2 pack config set` or a secrets manager.
- TLS verification can be disabled initially (`ssl_verify:false`) for self-signed certs, but should be enabled in production.
- For the POC we assume a small device set and single Gluware controller.
