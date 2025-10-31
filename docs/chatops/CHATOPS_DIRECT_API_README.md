# ChatOps with Direct NetBox API Integration

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AnythingLLM ChatOps                     │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Agent    │──│  LocalAI LLM │──│  NetBox API      │   │
│  │   Skills   │  │  (gpt-4o)    │  │  Skills (Direct) │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │                    │                   │
         ▼                    ▼                   ▼
    ┌─────────┐          ┌─────────┐        ┌──────────┐
    │Batfish  │          │StackStorm│       │  NetBox  │
    │Validate │          │ Execute  │       │   API    │
    └─────────┘          └─────────┘        └──────────┘
```

## Setup Changes (Option A - Direct API)

### Removed:
- ❌ NetBox MCP Server container
- ❌ HTTP-to-stdio bridge wrapper
- ❌ MCP protocol overhead

### Added:
- ✅ Direct NetBox API skills (`/app/server/storage/plugins/agent-skills/`)
- ✅ Native JavaScript functions for NetBox queries
- ✅ Environment variables: `NETBOX_URL`, `NETBOX_TOKEN`

## Available Agent Skills

### Query Functions (Read-Only)
1. **query_netbox_devices** - Find devices by site, name, role, status
2. **query_netbox_interfaces** - Find interfaces by device, name, type
3. **query_netbox_vlans** - Find VLANs by ID, name, site
4. **query_netbox_ip_addresses** - Find IP assignments
5. **query_netbox_prefixes** - Find IP prefixes/subnets

### Update Functions (Require Approval)
6. **update_netbox_device** - Update device attributes
7. **update_netbox_interface** - Update interface configuration
8. **create_netbox_vlan** - Create new VLANs
9. **assign_vlan_to_interface** - Assign VLANs to ports (access/trunk)

## Quick Start

### 1. Set NetBox API Token

```bash
export NETBOX_TOKEN="your-netbox-api-token-here"
```

### 2. Start the Stack

```bash
cd /home/dan/ibnaas
docker compose -f docker-compose.chatops.yml up -d
```

### 3. Access AnythingLLM

Open http://localhost:3001

### 4. Configure Workspace

1. **Create Workspace**: "Intent-Based Networking"
2. **Enable Agent Mode**: Workspace Settings → Enable Agent
3. **Select LLM**: LocalAI / gpt-4o
4. **Agent Skills**: Skills should auto-load from `/app/server/storage/plugins/agent-skills/`

### 5. Test NetBox Integration

Try these queries in the chat:

**Read-Only Queries:**
```
Show me all devices in the NYC site
List interfaces on border-router-nyc-01
What VLANs are defined?
```

**Dry-Run Mode:**
```
[DRY-RUN] Add VLAN 100 named Guest-WiFi to switches in NYC
[DRY-RUN] Configure GigabitEthernet0/1 as access port on VLAN 50
```

**Production Changes (Require Approval):**
```
Add VLAN 200 Management to all core switches
Configure trunk port GigabitEthernet0/24 with VLANs 10,20,30,40
```

## Agent Workflow

1. **Parse Intent** - Understand user's network goal
2. **Query NetBox** - Discover current state using API skills
3. **Generate Plan** - Determine required changes
4. **Validate** - Simulate with Batfish (if configured)
5. **Request Approval** - Multi-approver workflow for production
6. **Execute** - Push changes via StackStorm/Glueware
7. **Update NetBox** - Reflect changes in source of truth

## NetBox API Examples

The skills use the NetBox REST API directly:

```javascript
// Query devices at NYC site
await queryDevices({ filters: { site: 'nyc' } });

// Find interface on specific device
await queryInterfaces({ filters: { device: 'border-router-nyc-01', name: 'GigabitEthernet0/1' } });

// Get VLAN 100
await queryVLANs({ filters: { vid: 100 } });

// Update interface to trunk mode with VLANs
await updateInterface(123, {
  mode: 'tagged',
  tagged_vlans: [10, 20, 30]
});
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NETBOX_URL` | `http://host.docker.internal:8000` | NetBox instance URL |
| `NETBOX_TOKEN` | (required) | NetBox API authentication token |
| `LLM_PROVIDER` | `localai` | LLM provider |
| `LOCALAI_BASE_PATH` | `http://localai:8080` | LocalAI endpoint |
| `LOCALAI_MODEL_PREF` | `gpt-4o` | Model to use |

## Troubleshooting

### Skills Not Loading

```bash
# Check if skills are present
docker exec chatops-anythingllm ls -la /app/server/storage/plugins/agent-skills/

# Restart container
docker compose -f docker-compose.chatops.yml restart anythingllm
```

### NetBox API Connection Failed

```bash
# Test from container
docker exec chatops-anythingllm curl -H "Authorization: Token $NETBOX_TOKEN" \
  http://host.docker.internal:8000/api/dcim/devices/ | jq .

# Check environment
docker exec chatops-anythingllm printenv | grep NETBOX
```

### Agent Not Using Skills

- Ensure workspace has Agent Mode enabled
- Check LLM model supports function calling (gpt-4o does)
- Skills appear in "Agent Skills" tab in UI
- Try more explicit instructions: "Use the query_netbox_devices skill to find..."

## Benefits of Direct API vs MCP

✅ **Simpler** - No protocol bridge, no MCP server container
✅ **Faster** - Direct HTTP calls, no stdio/session overhead  
✅ **More Reliable** - Fewer failure points
✅ **Easier Debugging** - Standard REST API calls
✅ **Better Error Handling** - Direct HTTP status codes
✅ **Flexible** - Easy to add/modify functions

## Next Steps

1. Set `NETBOX_TOKEN` environment variable
2. Open http://localhost:3001 and create workspace
3. Enable agent mode
4. Test with read-only queries
5. Try dry-run mode for changes
6. Configure approval workflow for production
7. Integrate with Batfish/StackStorm for execution

## Files

- `/home/dan/ibnaas/docker-compose.chatops.yml` - Stack configuration
- `/home/dan/ibnaas/anythingllm/storage/plugins/agent-skills/netbox-api.js` - NetBox API functions
- `/home/dan/ibnaas/anythingllm/storage/plugins/agent-skills/plugin.json` - Skill definitions
