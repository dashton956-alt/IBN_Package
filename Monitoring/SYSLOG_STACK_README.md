# Event-Driven Syslog Observability Stack

A production-ready, Docker-based syslog server architecture with event-driven automation using Kafka, Loki, Grafana, and n8n.

## 🏗️ Architecture

```
Network Devices → Syslog-NG → Kafka → n8n Workflows
                              ↓
                         Promtail → Loki → Grafana
```

## 📦 What's Included

### Services (10)
- **Syslog-NG**: Log collection (ports 514 UDP/TCP)
- **Apache Kafka**: Event streaming (port 9092)
- **Zookeeper**: Kafka coordination (port 2181)
- **Grafana Loki**: Log storage (port 3100)
- **Promtail**: Log shipper
- **Grafana**: Visualization (port 3000)
- **n8n**: Workflow automation (port 5678)
- **PostgreSQL**: n8n database
- **Kafka UI**: Management interface (port 8080)
- **Kafka Connect**: Integration framework (port 8083)

### Configuration Files
- `docker-compose.yml` - Complete stack definition
- `syslog-ng/syslog-ng.conf` - Syslog parsing & Kafka routing
- `loki/loki-config.yaml` - Log storage configuration
- `promtail/promtail-config.yaml` - Log scraping configuration
- `grafana/dashboards/` - Pre-built dashboards
- `n8n/workflows/` - Event-driven automation workflows

### Kafka Topics (7)
- `syslog-raw`, `syslog-error`, `syslog-warning`, `syslog-info`
- `device-events`, `network-events`, `security-events`

## 🚀 Quick Start

### 1. Deploy Stack
```bash
docker-compose up -d
```

### 2. Access Services
- Grafana: http://localhost:3000 (admin/admin)
- n8n: http://localhost:5678 (admin/admin)
- Kafka UI: http://localhost:8080

### 3. Configure Syslog Sources
Point your devices to send logs to Docker host port 514.

**Cisco Example:**
```
logging host <docker-host-ip>
logging trap informational
```

### 4. Import n8n Workflows
1. Access n8n UI
2. Import `n8n/workflows/error-alert-workflow.json`
3. Import `n8n/workflows/config-change-workflow.json`

## 📊 Features

### Automated Log Processing
- **Parse & Enrich**: Extract fields, classify severity
- **Route to Kafka**: Topic-based distribution by log type
- **Store in Loki**: Compressed, indexed log storage
- **Visualize in Grafana**: Real-time dashboards

### Event-Driven Automation
- **Error Alerts**: Slack notifications for critical errors
- **Config Change Tracking**: Detect & audit device changes
- **Compliance Checks**: Trigger workflows for ACL changes
- **Ticket Creation**: Auto-create Jira tickets

### Monitoring & Analytics
- Log volume by severity
- Top hosts by activity
- Error rate tracking
- Config change audit trail

## 🔧 Configuration

### Syslog-NG Highlights
```conf
# Receives on UDP/TCP 514
source s_network_udp { network(transport("udp") port(514)); };

# Routes to Kafka by severity
filter f_error { level(err, crit, alert, emerg); };
destination d_kafka_error { kafka(...); };

# Enriches with metadata
rewrite r_add_metadata { ... };
```

### n8n Workflow: Error Alerts
1. **Kafka Consumer** → Reads from `syslog-error`
2. **Parse Message** → Extract fields
3. **Check Severity** → Route critical vs. error
4. **Alert** → Slack notification
5. **Ticket** → Create Jira issue (critical only)
6. **Log** → Record in Loki

### n8n Workflow: Config Changes
1. **Kafka Consumer** → Reads from `device-events`
2. **Parse Event** → Extract user, section, type
3. **Check Criticality** → Identify risky changes
4. **Alert** → Notify team
5. **Audit** → Log to CMDB & Google Sheets
6. **Compliance** → Trigger checks if ACL change

## 🔍 Querying Logs

### LogQL Examples (Grafana Explore)
```logql
# All error logs
{job="syslog-ng"} |~ "error|critical"

# Config changes on specific device
{job="syslog-ng", host="router-01"} |~ "config"

# Security events
{job="syslog-ng"} |~ "security|unauthorized|denied"

# Count errors per minute
sum(count_over_time({job="syslog-ng"} |~ "error" [1m]))
```

## 🛠️ Operations

### View Kafka Messages
```bash
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic syslog-error \
  --from-beginning
```

### Check Service Health
```bash
docker-compose ps
docker logs syslog-ng
docker logs kafka
```

### Send Test Log
```bash
echo "<134>Oct 31 12:00:00 test-host app: Test error" | \
  nc -u localhost 514
```

### Backup Data
```bash
# Loki
docker run --rm -v syslog-stack_loki-data:/data \
  -v $(pwd)/backup:/backup alpine \
  tar czf /backup/loki.tar.gz /data

# n8n workflows
docker exec n8n n8n export:workflow --all \
  --output=/workflows/backup.json
```

## 🔐 Security (Production)

1. **Change passwords** in docker-compose.yml
2. **Enable TLS** for Kafka, Grafana, syslog
3. **Restrict firewall** to trusted syslog sources
4. **Enable authentication** on all services
5. **Use secrets management** for credentials

## 📈 Scaling

### Increase Kafka Partitions
```bash
docker exec kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --alter --topic syslog-raw --partitions 6
```

### Add n8n Workers
```yaml
n8n-worker:
  image: n8nio/n8n:latest
  environment:
    - EXECUTIONS_MODE=queue
```

## 🐛 Troubleshooting

### Logs Not Appearing
```bash
# Check syslog-ng
docker exec syslog-ng syslog-ng-ctl stats

# Check Kafka
docker exec kafka kafka-topics --list \
  --bootstrap-server localhost:9092

# Check Loki
curl http://localhost:3100/ready
```

### n8n Workflow Not Triggering
1. Check execution history in n8n UI
2. Verify Kafka topic has messages (Kafka UI)
3. Check n8n logs: `docker logs n8n`

## 📚 File Structure

```
.
├── docker-compose.yml          # Main deployment
├── syslog-ng/
│   ├── Dockerfile             # Custom image
│   └── syslog-ng.conf         # Parsing & routing
├── loki/
│   └── loki-config.yaml       # Storage config
├── promtail/
│   └── promtail-config.yaml   # Log scraping
├── grafana/
│   ├── provisioning/          # Auto-config
│   └── dashboards/            # Pre-built dashboards
└── n8n/
    └── workflows/             # Automation workflows
        ├── error-alert-workflow.json
        └── config-change-workflow.json
```

## 🎯 Use Cases

- **Network Operations**: Monitor device status, config changes
- **Security**: Detect unauthorized access, policy violations
- **Compliance**: Audit trail, change tracking
- **Incident Response**: Auto-create tickets, alert teams
- **Capacity Planning**: Analyze log volume, patterns

## 💡 Next Steps

1. ✅ Deploy stack
2. ✅ Configure syslog sources
3. ✅ Import dashboards
4. ✅ Import n8n workflows
5. ✅ Customize alerts
6. ✅ Add integrations (Slack, Jira, etc.)
7. ✅ Set up backups
8. ✅ Configure monitoring

## 📖 Documentation

- Full docs: See individual config files
- LogQL: https://grafana.com/docs/loki/latest/logql/
- n8n: https://docs.n8n.io/
- Kafka: https://kafka.apache.org/documentation/

## ✨ Key Features

✅ **Modular Architecture** - Replace/extend components  
✅ **Event-Driven** - React to logs in real-time  
✅ **Scalable** - Handle thousands of logs/sec  
✅ **Observable** - Full visibility into log pipeline  
✅ **Automated** - Reduce manual intervention  
✅ **Production-Ready** - Health checks, persistence  

---

**Need help?** Check service logs, review config files, or consult component documentation.
