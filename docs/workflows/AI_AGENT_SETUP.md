# AI Chat Agent Setup Guide

## Overview
Your AI Chat agent now has access to:
- **NetBox DCIM/IPAM** - Query network devices and IP addresses
- **Gluware API** - Access network automation platform
- **Batfish** - Network configuration analysis and validation
- **n8n Workflows** - List and execute automation workflows

## Credentials Setup

Before the agent can access these APIs, you need to configure credentials in n8n:

### 1. NetBox API Token
1. Go to n8n UI: http://localhost:5678
2. Navigate to: **Settings → Credentials → Add Credential**
3. Select: **Header Auth**
4. Configure:
   - **Name**: `NetBox API Token`
   - **Credential ID**: `netbox-api-token` (must match workflow)
   - **Header Name**: `Authorization`
   - **Header Value**: `Token YOUR_NETBOX_TOKEN_HERE`

To get your NetBox token:
```bash
# Access NetBox on host port 8443
# Login at: https://localhost:8443/
# Go to: Profile → API Tokens → Add Token
# Copy token value
```

### 2. Gluware API Token
1. In n8n UI: **Settings → Credentials → Add Credential**
2. Select: **Header Auth**
3. Configure:
   - **Name**: `Gluware API Token`
   - **Credential ID**: `gluware-api-token`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer YOUR_GLUWARE_TOKEN_HERE`

### 3. Import Updated Workflow
```bash
# Import the updated AI Chat agent workflow
docker cp "/home/dan/ibnaas/n8n/Ai Chat agent.json" n8n-n8n-1:/home/node/ai-chat-agent.json

# Delete old workflow and import new one
docker exec -i n8n-n8n-1 sh -c "n8n execute --id=IH9uGEhWQ2vyEjg5 --workflow-deactivate || true"
docker exec -i n8n-n8n-1 sh -c "n8n import:workflow --input=/home/node/ai-chat-agent.json"
```

## Agent Capabilities

The AI agent can now:

### NetBox Queries
- "Show me all network devices"
- "List devices in site XYZ"
- "What IP addresses are allocated?"
- "Search for device spine1"

### Gluware Operations
- "List devices in Gluware"
- "What devices are managed by Gluware?"

### Batfish Analysis
- "List available Batfish snapshots"
- "Run reachability analysis on snapshot production"
- "Check BGP session status"
- "Validate routing policies"

### n8n Workflow Automation
- "What workflows are available?"
- "List all n8n workflows"
- "Execute workflow XYZ"

## API Endpoints (for reference)

The tools are configured to call:
- NetBox: `http://netbox-docker-netbox-1:8080/api/`
- Gluware: `http://gluware-api:8080/api/`
- Batfish: `http://batfish:9996/v2/`
- n8n: `http://localhost:5678/api/v1/`

Update URLs in the workflow JSON if your services use different hostnames/ports.

## Testing

1. Activate the workflow in n8n UI
2. Open the chat interface
3. Try queries like:
   - "Show me 5 devices from NetBox"
   - "What Batfish snapshots are available?"
   - "List n8n workflows"

## Troubleshooting

**"Tool execution failed"**
- Check credentials are configured correctly
- Verify API endpoints are reachable from n8n container
- Check service logs for errors

**"Unauthorized" errors**
- Verify API tokens are valid
- Check token format (Token vs Bearer prefix)

**Services unreachable**
- Ensure all containers are on same network or can resolve hostnames
- Test connectivity: `docker exec n8n-n8n-1 wget -O- http://netbox-docker-netbox-1:8080/api/`

## Next Steps

- Add more NetBox tools (sites, racks, cables, circuits)
- Add Gluware workflow execution tools
- Add more Batfish question types
- Implement dry-run/confirmation for destructive operations
