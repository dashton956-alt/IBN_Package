# Syslog Stack - 5 Minute Quick Start

## Prerequisites
- Docker & Docker Compose installed
- 8GB RAM minimum
- Ports available: 514, 3000, 5678, 8080, 9092

## Step 1: Deploy (2 minutes)

```bash
# Navigate to stack directory
cd syslog-stack

# Start all services
docker-compose up -d

# Wait for services to be ready (check every 10 seconds)
docker-compose ps
```

Expected output: All services should show "Up" status.

## Step 2: Verify Services (1 minute)

```bash
# Check all containers are running
docker-compose ps | grep Up | wc -l
# Should show: 10

# Check Kafka topics were created
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
# Should show: 7 topics

# Test syslog port
nc -zv localhost 514
# Should show: Connection succeeded
```

## Step 3: Access UIs (30 seconds)

Open in your browser:

1. **Grafana**: http://localhost:3000
   - Username: `admin`
   - Password: `admin`
   
2. **n8n**: http://localhost:5678
   - Username: `admin`
   - Password: `admin`

3. **Kafka UI**: http://localhost:8080
   - No authentication required

## Step 4: Send Test Log (30 seconds)

```bash
# Send a test error message
echo "<134>$(date '+%b %d %H:%M:%S') test-host myapp: Test ERROR message for syslog stack" | nc -u localhost 514

# Send a test config change
echo "<134>$(date '+%b %d %H:%M:%S') router-01 CONFIG: User admin modified interface GigabitEthernet0/1" | nc -u localhost 514

# Send a security event
echo "<134>$(date '+%b %d %H:%M:%S') firewall-01 SECURITY: Unauthorized access attempt from 192.168.1.100" | nc -u localhost 514
```

## Step 5: Verify Logs (1 minute)

### In Grafana:
1. Navigate to "Explore" (compass icon)
2. Select "Loki" datasource
3. Enter query: `{job="syslog-ng"}`
4. Click "Run query"
5. You should see your test messages!

### In Kafka UI:
1. Go to http://localhost:8080
2. Click "Topics"
3. Click "syslog-raw"
4. Click "Messages"
5. View your messages in JSON format

### In n8n:
1. Go to http://localhost:5678
2. Click "Workflows"
3. Import `n8n/workflows/error-alert-workflow.json`
4. Activate the workflow
5. Send another error log (see Step 4)
6. Check "Executions" tab

## Common Commands

### View Logs
```bash
docker logs syslog-ng
docker logs kafka
docker logs loki
docker logs n8n
```

### Restart Service
```bash
docker-compose restart syslog-ng
```

### Stop Stack
```bash
docker-compose down
```

### Stop and Remove All Data
```bash
docker-compose down -v
```

## Troubleshooting

### Logs not appearing?
```bash
# Check syslog-ng is receiving
docker exec syslog-ng syslog-ng-ctl stats

# Check Kafka has messages
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic syslog-raw \
  --from-beginning \
  --max-messages 1
```

### Can't connect to Grafana?
```bash
# Check Grafana is healthy
curl -f http://localhost:3000/api/health
docker logs grafana
```

### Kafka errors?
```bash
# Verify Kafka is ready
docker exec kafka kafka-broker-api-versions \
  --bootstrap-server localhost:9092
```

## Next Steps

### 1. Configure Your Devices
Point your network devices to send syslog to your Docker host:

**Cisco:**
```
conf t
logging host <docker-host-ip>
logging trap informational
logging facility local0
end
```

**Linux:**
```bash
# Add to /etc/rsyslog.conf
*.* @<docker-host-ip>:514
```

### 2. Customize n8n Workflows
1. Open n8n UI
2. Import workflows from `n8n/workflows/`
3. Configure Slack/Jira credentials
4. Activate workflows

### 3. Explore Dashboards
1. Open Grafana
2. Go to "Dashboards"
3. Browse "Syslog Overview Dashboard"
4. Customize as needed

### 4. Set Up Alerts
1. In n8n, customize alert thresholds
2. Configure notification channels
3. Test with sample logs

## Configuration Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Service definitions |
| `syslog-ng/syslog-ng.conf` | Log parsing & routing |
| `loki/loki-config.yaml` | Log storage config |
| `grafana/dashboards/*.json` | Pre-built dashboards |
| `n8n/workflows/*.json` | Automation workflows |

## Help & Documentation

- **Full README**: See `SYSLOG_STACK_README.md`
- **Config Details**: Check individual service config files
- **Logs**: `docker-compose logs <service-name>`
- **Status**: `docker-compose ps`

## Success Checklist

- [ ] All services running (`docker-compose ps`)
- [ ] Kafka topics created (7 topics)
- [ ] Grafana accessible (port 3000)
- [ ] n8n accessible (port 5678)
- [ ] Test logs sent successfully
- [ ] Logs visible in Grafana
- [ ] Messages in Kafka (check Kafka UI)

**If all checked: You're ready to go! 🎉**

## Production Checklist

Before going to production:

- [ ] Change all default passwords
- [ ] Configure firewall rules
- [ ] Set up SSL/TLS
- [ ] Configure backups
- [ ] Set retention policies
- [ ] Test failover scenarios
- [ ] Monitor resource usage
- [ ] Document your setup

---

**Time taken**: ~5 minutes  
**Status**: Stack is ready for log ingestion!  
**Next**: Configure your syslog sources and customize workflows
