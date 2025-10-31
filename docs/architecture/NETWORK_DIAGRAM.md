# POC Network Diagram — review

This is a reviewable network diagram and mapping for the Intent-based Network Automation + AIOps POC. It shows the recommended zones, example CIDRs, where services live (Docker vs VM), and required flows/ports. Use it to review and tell me any changes and I will update the PlantUML or produce a PNG.

---

## ASCII overview (quick)

+-----------------------------+        +-------------------+
|         ChatOps / DMZ       |        |   Documentation    |
|  (Slack webhook reverse     |        |   GitHub (external)|
|   proxy)                    |        +-------------------+
+------------+----------------+
             | webhook
             v
+-----------------------------+          +---------------------+
|        MGMT (st2_mgmt)      |<-------->|   TELEM (telemetry_net)
|  - StackStorm (ST2)         |  alerts  |  - Loki / Prometheus
|  - NetBox (SOoT)            | <------+ |  - Alertmanager
|  - Vault (secrets)          |  metrics |  - Fluentbit/Promtail
|  - AnythingLLM (intent)     |          +---------------------+
|  - GitHub runner / CI       |                 ^
+----+----------------+-------+                 |
     |                |                         | telemetry
     |                |                         |
     |                v                         v
     |           +-----------+           +-------------------+
     |           |  Host /  |           |     DATA (Devices)|
     |           |  Host IP |<----------| - Meraki, Catalyst|
     |           |  (exposed|   mgmt     | - FortiManager    |
     |           |   ports) |  flows     | - Mist            |
     |           +-----------+           +-------------------+
     |                    ^                    |
     |                    |                    | telemetry / mgmt
     |                    |                    v
     |                    +-------------+  +-----------+
     |                                  |  | Gluware VM|
     |                                  |  | (separate)|
     |                                  |  +-----------+
     +----------------------------------+


Legend:
- Everything inside `MGMT` and `TELEM` is recommended to run on Docker user networks.
- `Gluware VM` and physical devices are on the DATA network (not Docker); they communicate with MGMT via the host network (or macvlan if configured).

---

## PlantUML (renderable)
- Source available in `network_diagram.puml` (open in VS Code with PlantUML to preview).

---

## Suggested networks / CIDRs
- MGMT (st2_mgmt): 172.24.0.0/24 (Docker user network)
- TELEM (telemetry_net): 172.25.0.0/24
- SANDBOX (sandbox_net): 172.26.0.0/24
- DMZ (optional): 172.27.0.0/28
- DATA (physical devices and Gluware VM): your existing device VLANs (example 10.20.0.0/22)


## Mapping: components → networks
- st2_mgmt (Docker): StackStorm containers, NetBox, Vault, AnythingLLM, CI runner
- telemetry_net (Docker or host-exposed): Loki, Prometheus, Fluentbit/Promtail
- sandbox_net: emulators and test containers
- DATA (physical): Gluware VM and network devices


## Required flows & ports (short version)
- ST2 -> NetBox: TCP 443 (HTTPS)
- ST2 -> Vault: TCP 8200 (or 8201 in our dev) (HTTPS)
- ST2 -> Gluware VM: TCP 443 (HTTPS)
- Devices -> Telemetry: UDP/TCP 514 (syslog), gNMI, NetFlow ports as needed
- Telemetry -> ST2: HTTPS webhook (443) or Alertmanager integration
- Admin clients -> MGMT UIs: HTTPS (443) via VPN or management network


## Practical recommendations
- Create Docker user networks `st2_mgmt` and `telemetry_net` and attach the appropriate containers.
- Use host port publishing for telemetry (UDP 514) if devices cannot reach containers directly.
- Use AppRole for Vault (do not store tokens in files). Keep Vault in MGMT.
- Use internal DNS names for services and signed certs (internal CA) if possible.


## Next actions
- If this mapping looks right, I can:
  - (A) Create the Docker networks and attach existing containers (safe). 
  - (B) Produce a rendered PNG from the PlantUML source and push it here for visual review.
  - (C) Scaffold ST2 Orquesta workflow to fetch secrets from Vault and call NetBox (requires only Vault URL).

Tell me which of A/B/C (or other changes) you want next and I will proceed.

---

_File: `NETWORK_DIAGRAM.md` created at repository root._
