# NetBox ChatOps - Intent-Based Network Management

AI-powered ChatOps interface for intent-based networking using AnythingLLM, NetBox MCP, Batfish validation, and StackStorm/Glueware execution.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         ChatOps Stack                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐       ┌──────────────┐      ┌──────────────┐ │
│  │ AnythingLLM  │◄─────►│   LocalAI    │      │  NetBox MCP  │ │
│  │  (ChatOps)   │       │  (LLM/Claude)│      │ (Source of   │ │
│  │   Port 3001  │       │  Port 8080   │      │   Truth)     │ │
│  └──────┬───────┘       └──────────────┘      └──────┬───────┘ │
│         │                                              │         │
│         │  Agent Orchestration                         │         │
│         │                                              │         │
│         ├──────────────────────────────────────────────┘         │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Intent-Based Workflow Engine                 │  │
│  │  1. Parse Intent → 2. Discover → 3. Plan → 4. Validate  │  │
│  │  5. Approve → 6. Execute → 7. Update NetBox             │  │
│  └──────────────────────────────────────────────────────────┘  │
│         │                                                        │
└─────────┼────────────────────────────────────────────────────────┘
          │
          ├────────► Batfish (Validation)      Port 9997
          ├────────► StackStorm (Execution)    Port 9101
          └────────► Glueware (Config Push)    Port 8000
```

## Components

### 1. AnythingLLM (ChatOps Interface)
- **Purpose**: Natural language chat interface for network operations
- **Port**: 3001
- **Features**:
  - Agent-based workflow orchestration
  - Multi-approver approval policies
  - Dry-run mode for safe testing
  - Integration with NetBox MCP, Batfish, StackStorm

### 2. LocalAI (LLM Engine)
- **Purpose**: Claude Sonnet 4.5-compatible LLM inference
- **Port**: 8080
- **Models**: gpt-4o, text-embedding-ada-002
- **Resources**: 4 CPUs, 8GB RAM

### 3. NetBox MCP Server
- **Purpose**: Source of truth for network inventory
- **Port**: 8002
- **Capabilities**:
  - Query devices, interfaces, IPs, VLANs, circuits
  - Update network state
  - MCP-compliant tool interface

## Quick Start

### 1. Prerequisites
```bash
# Set environment variables
export NETBOX_TOKEN="your-netbox-api-token"
export JWT_SECRET="your-jwt-secret-for-anythingllm"
export ST2_API_KEY="your-stackstorm-api-key"
```

### 2. Start the ChatOps Stack
```bash
cd /home/dan/ibnaas
docker compose -f docker-compose.chatops.yml up -d
```

### 3. Verify Services
```bash
# Check all services are healthy
docker compose -f docker-compose.chatops.yml ps

# Test LocalAI
curl http://localhost:8080/v1/models

# Test NetBox MCP
curl http://localhost:8002/mcp

# Test AnythingLLM
curl http://localhost:3001/api/ping
```

### 4. Access ChatOps Interface
Open browser to: `http://localhost:3001`

## Usage Examples

### Example 1: Add VLAN to Switches
**User input (chat):**
```
Add VLAN 100 (name: Guest-WiFi) to all access switches in the NYC site
```

**Agent workflow:**
1. **Parse Intent**: Extract VLAN 100, name "Guest-WiFi", site "NYC", device role "access"
2. **Discover**: Query NetBox for access switches at NYC site
3. **Generate Plan**: Create config snippets for each switch
4. **Validate**: Run Batfish to verify VLAN doesn't conflict with routing
5. **Request Approval**: Send approval request to network-admin and network-engineer roles (requires 2 approvals)
6. **Execute** (after approval): Push configs via StackStorm
7. **Update NetBox**: Record VLAN assignment in NetBox

### Example 2: Troubleshoot Connectivity
**User input:**
```
Why can't server 10.1.50.10 reach 10.2.100.20?
```

**Agent workflow:**
1. **Analyze**: Identify source and destination IPs
2. **Discover**: Query NetBox for device attachments, VLANs, routing
3. **Validate**: Run Batfish reachability analysis
4. **Diagnose**: Correlate NetBox state with Batfish results, identify missing route or ACL block
5. **Suggest Fix**: Propose configuration change with approval

### Example 3: Dry-Run Mode
**User input:**
```
[DRY-RUN] Add BGP peer 198.51.100.1 to border routers in DC1
```

**Agent workflow:**
- Runs full workflow (discover → plan → validate → execute)
- **No real changes applied** (StackStorm/Glueware run with `dryRun: true`)
- Returns simulation results and proposed configs for review

## Approval Policy

### Multi-Approver Configuration
- **Minimum Approvals**: 2
- **Eligible Approvers**: network-admin, network-engineer, ops-lead
- **Timeout**: 1 hour (3600 seconds)
- **Scope**: All production changes (dry-run bypasses approval)

### Approval Workflow
1. Agent generates change plan and validation results
2. System sends approval request to eligible users
3. 2+ approvers must review and approve
4. Once threshold met, execution proceeds
5. If timeout expires, change is rejected

## Safety Features

| Feature | Description | Default |
|---------|-------------|---------|
| **Dry-Run Default** | New users start in dry-run mode | Enabled |
| **Pre-Execution Validation** | Batfish validation required before execution | Enabled |
| **Multi-Approver** | 2+ approvals for production changes | Enabled |
| **Max Devices Per Change** | Limit blast radius | 10 devices |
| **Change Window Enforcement** | Respect maintenance windows | Enabled |
| **Rollback Support** | Generate rollback configs | Enabled |

## Configuration Files

| File | Purpose |
|------|---------|
| `docker-compose.chatops.yml` | Unified compose stack |
| `anythingllm/storage/agents/netbox-chatops-intent/agent.json` | Agent configuration |
| `anythingllm/storage/plugins/anythingllm_mcp_servers.json` | MCP server registry |

## Monitoring & Logs

### View Logs
```bash
# All services
docker compose -f docker-compose.chatops.yml logs -f

# Specific service
docker compose -f docker-compose.chatops.yml logs -f anythingllm
docker compose -f docker-compose.chatops.yml logs -f localai
docker compose -f docker-compose.chatops.yml logs -f netbox-mcp
```

### Health Checks
```bash
# Check service health
docker compose -f docker-compose.chatops.yml ps
```

## Integration Details

### NetBox MCP Tools
- `query_devices` - List devices with filters
- `query_interfaces` - Get interface details
- `query_ip_addresses` - IP inventory
- `query_vlans` - VLAN database
- `update_device` - Modify device attributes (requires approval)

### Batfish Validation
- **Endpoint**: `http://batfish:9997/v2/analysis`
- **Questions**:
  - Reachability analysis
  - BGP session status
  - Route table verification
  - ACL policy validation

### StackStorm Execution
- **Endpoint**: `http://st2-docker-st2api-1:9101/v1/executions`
- **Actions**:
  - `network.deploy_config` - Push configuration
  - `network.provision_service` - Provision L2/L3 services
  - `network.run_workflow` - Execute custom workflows

### Glueware Config Push
- **Endpoint**: `http://glueware:8000/api/push`
- **Methods**:
  - Direct SSH config push
  - Pre-validation with dry-run
  - Rollback generation

## Troubleshooting

### Agent Not Starting
```bash
# Check AnythingLLM logs
docker logs chatops-anythingllm | grep -i agent

# Verify MCP server connectivity
docker exec -it chatops-anythingllm curl http://netbox-mcp:8002/mcp
```

### LocalAI Not Responding
```bash
# Check model loading
docker logs chatops-localai | grep -i model

# List loaded models
curl http://localhost:8080/v1/models
```

### Approval Requests Not Received
- Verify user roles match `approverRoles` in agent.json
- Check approval timeout (default 1 hour)
- Review AnythingLLM user permissions

## Security Considerations

1. **API Keys**: Store in environment variables, not in compose file
2. **Network Isolation**: Use Docker networks to segment traffic
3. **Approval Audit**: All approvals logged with timestamp and approver
4. **Dry-Run First**: Test changes in dry-run before production
5. **Role-Based Access**: Limit approver roles to authorized personnel

## Next Steps

1. **Customize Agent**: Edit `agent.json` to add custom workflows
2. **Add Tools**: Extend MCP server with additional NetBox queries
3. **Integrate Monitoring**: Add Prometheus/Grafana for observability
4. **Create Runbooks**: Document common ChatOps procedures
5. **Training**: Onboard team with dry-run scenarios

## Support

- Documentation: [NETBOX_MCP_CHATOPS.md](./NETBOX_MCP_CHATOPS.md)
- Issues: GitHub Issues
- Architecture: See diagram above
