# Syslog Observability Stack - Complete Deployment Package

## 📦 Package Contents

This complete deployment package provides everything needed to run a production-grade, event-driven syslog observability and automation platform.

### Core Infrastructure (1 file)
- **docker-compose.yml** (9.5 KB) - Complete Docker Compose stack with 10 services

### Configuration Files

#### Syslog-NG (2 files)
- `syslog-ng/Dockerfile` - Custom syslog-ng image with Kafka support
- `syslog-ng/syslog-ng.conf` - Log parsing, classification, and Kafka routing

#### Loki (1 file)
- `loki/loki-config.yaml` - Log storage and retention configuration

#### Promtail (1 file)
- `promtail/promtail-config.yaml` - Log scraping and shipping configuration

#### Grafana (3 files)
- `grafana/provisioning/datasources/loki.yaml` - Loki datasource auto-provisioning
- `grafana/provisioning/dashboards/dashboards.yaml` - Dashboard provisioning config
- `grafana/dashboards/syslog-overview.json` - Pre-built syslog dashboard

#### n8n Workflows (2 files)
- `n8n/workflows/error-alert-workflow.json` - Error detection and alerting
- `n8n/workflows/config-change-workflow.json` - Config change tracking

### Documentation (3 files)
- **SYSLOG_STACK_README.md** - Complete documentation
- **QUICK_START_GUIDE.md** - 5-minute deployment guide
- **DEPLOYMENT_PACKAGE.md** - This file

---

## 🏗️ Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    Network Devices / Servers                 │
│                  (Cisco, Linux, Windows, etc.)              │
└───────────────────────┬─────────────────────────────────────┘
                        │ Syslog UDP/TCP 514
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                      Syslog-NG Server                        │
│  • Receives logs on UDP/TCP 514                             │
│  • Parses and enriches messages                             │
│  • Classifies by severity and type                          │
│  • Routes to Kafka topics                                    │
└───┬───────────────┬──────────────┬──────────────────────────┘
    │               │              │
    │ JSON/Kafka    │              │ File Logs
    ↓               ↓              ↓
┌─────────┐   ┌──────────┐   ┌──────────┐
│ Kafka   │   │ Kafka    │   │ Promtail │
│ Topics  │   │ UI       │   │ Scraper  │
│ (7x)    │   │ (Monitor)│   │          │
└────┬────┘   └──────────┘   └─────┬────┘
     │                              │
     │                              ↓
     │                         ┌─────────┐
     │                         │  Loki   │
     │                         │ Storage │
     │                         └────┬────┘
     ↓                              ↓
┌──────────┐                  ┌──────────┐
│   n8n    │                  │ Grafana  │
│ Workflows│                  │  Dashboards
│          │                  │  Explorer│
│ • Errors │                  │  Alerts  │
│ • Config │                  └──────────┘
│ • Events │
└──────────┘
```

---

## 🎯 Deployment Options

### Option 1: Quick Deploy (Recommended)
```bash
# Extract package
tar -xzf syslog-stack.tar.gz
cd syslog-stack

# Deploy
docker-compose up -d

# Verify
docker-compose ps

# Access
# - Grafana: http://localhost:3000 (admin/admin)
# - n8n: http://localhost:5678 (admin/admin)
# - Kafka UI: http://localhost:8080
```

### Option 2: Production Deploy
```bash
# 1. Review and customize configurations
vi docker-compose.yml
vi syslog-ng/syslog-ng.conf
vi loki/loki-config.yaml

# 2. Set production passwords
export GRAFANA_ADMIN_PASSWORD="your-secure-password"
export N8N_PASSWORD="your-secure-password"
export POSTGRES_PASSWORD="your-secure-password"

# 3. Deploy
docker-compose up -d

# 4. Configure SSL/TLS (see documentation)
# 5. Set up backups (see documentation)
# 6. Configure monitoring (see documentation)
```

---

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] Docker Engine 20.10+ installed
- [ ] Docker Compose 2.0+ installed
- [ ] Minimum 8GB RAM available
- [ ] 20GB+ disk space available
- [ ] Ports 514, 3000, 5678, 8080, 9092 available
- [ ] Network access to syslog sources configured

### Deployment
- [ ] Extract deployment package
- [ ] Review configurations
- [ ] Update passwords (production)
- [ ] Run `docker-compose up -d`
- [ ] Verify all containers running
- [ ] Check Kafka topics created (7 topics)

### Post-Deployment
- [ ] Access Grafana (port 3000)
- [ ] Access n8n (port 5678)
- [ ] Access Kafka UI (port 8080)
- [ ] Send test syslog messages
- [ ] Verify logs in Grafana
- [ ] Import n8n workflows
- [ ] Configure notification channels (Slack, etc.)
- [ ] Set up backups
- [ ] Configure firewall rules

### Production Hardening
- [ ] Change all default passwords
- [ ] Enable TLS/SSL
- [ ] Configure authentication
- [ ] Set up monitoring
- [ ] Configure retention policies
- [ ] Test backup/restore
- [ ] Document setup
- [ ] Train operations team

---

## 📊 Services Overview

| Service | Container | Ports | Purpose | Data Volume |
|---------|-----------|-------|---------|-------------|
| Syslog-NG | `syslog-ng` | 514 | Log collection | `syslog-logs` |
| Kafka | `kafka` | 9092, 9093 | Event streaming | `kafka-data` |
| Zookeeper | `zookeeper` | 2181 | Kafka coordination | `zookeeper-data` |
| Loki | `loki` | 3100 | Log storage | `loki-data` |
| Promtail | `promtail` | 9080 | Log shipping | None |
| Grafana | `grafana` | 3000 | Visualization | `grafana-data` |
| n8n | `n8n` | 5678 | Automation | `n8n-data` |
| PostgreSQL | `postgres` | 5432 | n8n DB | `postgres-data` |
| Kafka UI | `kafka-ui` | 8080 | Management UI | None |
| Kafka Connect | `kafka-connect` | 8083 | Integrations | None |

---

## 🔧 Configuration Highlights

### Syslog-NG
- **Input**: UDP/TCP port 514
- **Parsing**: Syslog RFC 3164/5424
- **Classification**: By severity, facility, content patterns
- **Output**: 7 Kafka topics + file logs
- **Features**: Message enrichment, JSON formatting, filtering

### Kafka Topics
1. **syslog-raw** - All raw logs
2. **syslog-error** - Error-level logs
3. **syslog-warning** - Warning logs
4. **syslog-info** - Info logs
5. **device-events** - Device-specific events
6. **network-events** - Network events
7. **security-events** - Security-related logs

### Loki
- **Storage**: Filesystem-based
- **Retention**: 720 hours (30 days)
- **Indexing**: BoltDB
- **Compression**: Snappy
- **Query**: LogQL

### Grafana
- **Datasource**: Loki (auto-provisioned)
- **Dashboards**: Pre-configured syslog overview
- **Features**: Log explorer, alerting, annotations

### n8n Workflows

#### Error Alert Workflow
- Triggers: Kafka error topic
- Actions:
  - Parse and classify errors
  - Send Slack notifications
  - Create Jira tickets (critical)
  - Log to Loki (audit trail)

#### Config Change Workflow
- Triggers: Kafka device-events topic
- Actions:
  - Extract user and change details
  - Classify criticality
  - Alert on critical changes
  - Log to CMDB
  - Audit trail (Google Sheets)
  - Trigger compliance checks

---

## 💾 Resource Requirements

### Minimum (Development/Testing)
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Disk**: 20 GB
- **Throughput**: ~1,000 logs/sec

### Recommended (Production - Small)
- **CPU**: 8 cores
- **RAM**: 16 GB
- **Disk**: 100 GB SSD
- **Throughput**: ~10,000 logs/sec

### Recommended (Production - Large)
- **CPU**: 16+ cores
- **RAM**: 32+ GB
- **Disk**: 500+ GB SSD
- **Throughput**: ~50,000+ logs/sec

---

## 🔐 Security Considerations

### Default Credentials (MUST CHANGE FOR PRODUCTION)
- Grafana: admin/admin
- n8n: admin/admin
- PostgreSQL: n8n/n8n

### Production Security Checklist
- [ ] Change all default passwords
- [ ] Enable Kafka SASL/SSL
- [ ] Configure Grafana OAuth
- [ ] Enable n8n authentication
- [ ] Use Docker secrets for credentials
- [ ] Enable TLS for syslog (port 6514)
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Set up log rotation
- [ ] Regular security updates

---

## 📈 Scaling Guide

### Horizontal Scaling

**Kafka:**
```yaml
# Add in docker-compose.yml
kafka-2:
  image: confluentinc/cp-kafka:7.5.0
  environment:
    KAFKA_BROKER_ID: 2
    # ... (same config with different ID)
```

**n8n:**
```yaml
n8n-worker-1:
  image: n8nio/n8n:latest
  environment:
    - EXECUTIONS_MODE=queue
```

**Loki (Distributed Mode):**
- Deploy Loki in microservices mode
- Separate ingester, distributor, querier
- Use object storage (S3, GCS)

### Vertical Scaling
- Increase memory limits in docker-compose.yml
- Add more Kafka partitions
- Increase Loki chunk cache size

---

## 🛠️ Operations

### Daily Operations
```bash
# Check service health
docker-compose ps

# View logs
docker-compose logs -f --tail=100

# Restart service
docker-compose restart <service-name>
```

### Monitoring
```bash
# Check Kafka consumer lag
docker exec kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --describe --group n8n-error-alerts

# Check Loki metrics
curl http://localhost:3100/metrics

# Check syslog-ng stats
docker exec syslog-ng syslog-ng-ctl stats
```

### Maintenance
```bash
# Backup volumes
docker run --rm -v syslog-stack_loki-data:/data \
  -v $(pwd)/backup:/backup alpine \
  tar czf /backup/loki-$(date +%Y%m%d).tar.gz /data

# Clean old logs (Kafka)
docker exec kafka kafka-configs \
  --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name syslog-raw \
  --alter --add-config retention.ms=604800000

# Compact Loki chunks
docker exec loki /usr/bin/loki-cli compact
```

---

## 📞 Support & Troubleshooting

### Common Issues

**Issue**: Logs not appearing in Grafana
- Check syslog-ng is receiving: `docker exec syslog-ng syslog-ng-ctl stats`
- Check Kafka has messages: `docker exec kafka kafka-console-consumer ...`
- Check Promtail is scraping: `docker logs promtail`
- Check Loki is ingesting: `curl http://localhost:3100/metrics`

**Issue**: n8n workflow not triggering
- Check Kafka consumer connection in n8n UI
- Verify topic has messages in Kafka UI
- Check n8n execution logs
- Verify workflow is activated

**Issue**: High resource usage
- Review Kafka retention settings
- Check Loki compaction is running
- Monitor container stats: `docker stats`
- Review log volume and rates

### Getting Help
1. Check service logs: `docker logs <container>`
2. Review configuration files
3. Check health endpoints
4. Review documentation
5. Check GitHub issues (if applicable)

---

## 🎓 Training Resources

### Quick Start
- **QUICK_START_GUIDE.md** - 5-minute setup guide

### Full Documentation
- **SYSLOG_STACK_README.md** - Complete reference

### External Resources
- Syslog-NG: https://www.syslog-ng.com/technical-documents
- Kafka: https://kafka.apache.org/documentation/
- Loki: https://grafana.com/docs/loki/latest/
- n8n: https://docs.n8n.io/
- LogQL: https://grafana.com/docs/loki/latest/logql/

---

## ✅ Deployment Summary

**What you get:**
- ✅ Complete syslog collection infrastructure
- ✅ Real-time event streaming (Kafka)
- ✅ Centralized log storage (Loki)
- ✅ Beautiful visualizations (Grafana)
- ✅ Event-driven automation (n8n)
- ✅ Pre-built workflows and dashboards
- ✅ Production-ready configuration
- ✅ Comprehensive documentation

**Deployment time:**
- Quick deploy: 5 minutes
- Full production setup: 1-2 hours

**Skills required:**
- Basic: Docker, Linux, networking
- Advanced: Kafka, LogQL, n8n workflows

**Use cases:**
- Network monitoring and alerting
- Security event detection
- Compliance and audit logging
- Incident response automation
- Configuration change tracking

---

**Ready to deploy? Start with QUICK_START_GUIDE.md!**
