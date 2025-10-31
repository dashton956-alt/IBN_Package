# AI Chat Agent - Full NetBox Integration

## What Was Added

I've completed your AI Chat agent workflow with **full NetBox integration**. Here's what's now available:

### ✅ NetBox Resources Added (11 new tools)

Your AI agent can now query these NetBox resources:

1. **Sites** - List all sites (already working)
2. **Devices** - List all network devices ✨ NEW (reconnected)
3. **Device Roles** - List device roles (router, switch, etc.) ✨ NEW (reconnected)
4. **Device Types** - List device models/types ✨ NEW
5. **Interfaces** - List all network interfaces ✨ NEW
6. **IP Addresses** - List all IP addresses in IPAM ✨ NEW
7. **Prefixes** - List all network prefixes/subnets ✨ NEW
8. **VLANs** - List all VLANs ✨ NEW
9. **Cables** - List all physical cables ✨ NEW
10. **Racks** - List all equipment racks ✨ NEW
11. **Virtual Machines** - List all VMs ✨ NEW
12. **Circuits** - List all WAN circuits ✨ NEW
13. **Providers** - List circuit providers ✨ NEW
14. **Tenants** - List all tenants ✨ NEW

### ✅ Other Integrations (Already Configured)

- **n8n API** - List workflows, execute workflows
- **Batfish** - List snapshots, run queries (when available)
- **Gluware** - Get devices (when available)

## Current Workflow Structure

```
┌─────────────────────────┐
│   Chat Trigger          │
│   (User messages)       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   AI Agent              │
│   (Google Gemini)       │
│   + Memory Buffer       │
└───────────┬─────────────┘
            │
            ├──────────────────────────────────────────┐
            │                                          │
            ▼                                          ▼
    ┌─────────────────┐                    ┌──────────────────┐
    │  NetBox Tools   │                    │  Other Tools     │
    │  (14 tools)     │                    │  (5 tools)       │
    ├─────────────────┤                    ├──────────────────┤
    │ • Sites         │                    │ • n8n Workflows  │
    │ • Devices       │                    │ • n8n Execute    │
    │ • Device Roles  │                    │ • Batfish Snaps  │
    │ • Device Types  │                    │ • Batfish Query  │
    │ • Interfaces    │                    │ • Gluware Devs   │
    │ • IP Addresses  │                    └──────────────────┘
    │ • Prefixes      │
    │ • VLANs         │
    │ • Cables        │
    │ • Racks         │
    │ • VMs           │
    │ • Circuits      │
    │ • Providers     │
    │ • Tenants       │
    └─────────────────┘
```

## How to Use

### Import the Updated Workflow

1. **Backup your current workflow** (export from n8n UI first!)
2. Open n8n UI: `http://localhost:5678`
3. Click **Workflows** → **Import from File**
4. Select: `/home/dan/ibnaas/n8n/Ai Chat agent.json`
5. It will update the existing workflow (ID: `IH9uGEhWQ2vyEjg5`)

### Test the Integration

Open the chat interface and try these queries:

#### NetBox Queries

```
"Show me all sites in NetBox"
"List all devices"
"What device roles do we have?"
"Show me all IP addresses"
"List all VLANs"
"What interfaces exist?"
"Show me all racks"
"List virtual machines"
"What circuits do we have?"
"Show me all cables"
"List device types"
"What tenants are configured?"
"Show me all prefixes"
"List circuit providers"
```

#### Combined Queries

```
"Show me all devices at the Fox-and-Goose site"
"How many active devices do we have?"
"List all IP addresses in the 10.0.0.0/8 range"
"Show me devices with the role 'router'"
"What VLANs are configured for site X?"
```

#### Cross-System Queries

```
"List all n8n workflows"
"Show me Batfish snapshots"
"Get devices from Gluware"
"Show me NetBox sites and n8n workflows"
```

## What the AI Agent Can Do Now

### 1. Network Inventory Management
- Query any NetBox resource
- Filter by attributes (site, role, status, etc.)
- Get device details and relationships

### 2. IP Address Management
- Check IP availability
- List prefixes and VLANs
- Find IP assignments

### 3. Circuit & Provider Management
- List WAN circuits
- Get provider information
- Check circuit status

### 4. Virtual Infrastructure
- List virtual machines
- Check VM assignments
- Get cluster information

### 5. Physical Infrastructure
- List racks and cables
- Get device locations
- Check physical connections

### 6. Workflow Automation
- List n8n workflows
- Execute workflows
- Integrate with automation

### 7. Network Analysis (when Batfish is configured)
- List configuration snapshots
- Run BGP/OSPF queries
- Analyze routing tables

## Configuration Notes

### NetBox Credential
All NetBox tools use the same credential: **"NetBox account 2"** (ID: `iSGi9vEzxYq7DoOs`)

**Make sure this is configured with:**
- URL: `http://172.27.0.1:8443`
- Token: `${NETBOX_API_TOKEN}`

### Tool Behavior
Each NetBox tool:
- Has `returnAll` parameter controlled by AI
- Uses filters parameter for advanced queries
- Returns full JSON responses
- Supports pagination automatically

### AI Agent Settings
- **Model**: Google Gemini (PaLM API)
- **Memory**: Buffer Window (20 messages)
- **Mode**: Tools agent
- **All tools connected via `ai_tool` connection type**

## Advanced Usage

### The AI Can Handle Complex Requests

**Example 1: Multi-step query**
```
User: "Find all routers in the Fox-and-Goose site and show their IP addresses"

AI will:
1. List sites to find "Fox-and-Goose" 
2. List devices with site filter and role=router
3. List IP addresses for those devices
4. Format and present the results
```

**Example 2: Validation check**
```
User: "Are there any devices without IP addresses assigned?"

AI will:
1. Get all devices
2. Check which ones have no primary_ip
3. Report the findings
```

**Example 3: Inventory report**
```
User: "Give me a summary of our network infrastructure"

AI will:
1. Count sites, devices, IPs
2. List device roles and counts
3. Show VLAN counts
4. Present formatted summary
```

## Extending the Integration

### To Add More NetBox Operations

Currently all tools are `Get All` operations. You can add:
- **Get Single** - Get one device/site/IP by ID
- **Create** - Create new resources
- **Update** - Update existing resources
- **Delete** - Remove resources

### To Add More Filters

Modify the `filters` parameter in each node:
```json
"filters": {
  "site": "Fox-and-Goose",
  "status": "active",
  "device_type": "MX68CW-WW"
}
```

### To Add Custom Tools

Add new `n8n-nodes-netbox.netBoxTool` nodes:
1. Choose resource type
2. Choose operation
3. Set credentials
4. Connect to AI Agent via `ai_tool`

## Troubleshooting

### If Tools Don't Work

1. **Check NetBox credential**:
   - Settings → Credentials → "NetBox account 2"
   - URL must be `http://172.27.0.1:8443`
   - Token must be valid

2. **Test connection**:
   - Click "Test" in credential settings
   - Should return success

3. **Check workflow activation**:
   - Workflow must be active (green toggle)
   - All nodes should be connected (lines visible)

4. **Check logs**:
   ```bash
   docker logs n8n-n8n-1 --tail 50
   ```

### If AI Doesn't Use Tools

1. **Check tool connections**: All tools must be connected to "AI Agent1" via `ai_tool` connections
2. **Check AI model**: Google Gemini credential must be valid
3. **Try explicit requests**: "Use NetBox to show me all sites"

### If Results Are Wrong

1. **Check filters**: Some tools might have filters set
2. **Check returnAll**: Should be AI-controlled with `$fromAI()`
3. **Verify NetBox data**: Check data exists in NetBox UI

## Performance Considerations

- Each tool call makes an API request to NetBox
- Large datasets may take time (use filters)
- AI will automatically use appropriate tools
- Memory buffer keeps context of last 20 messages

## Security Notes

- API token is embedded in credential
- All tools use the same NetBox token
- No authentication required for chat (consider adding)
- Webhook ID is public but unpredictable

## Next Steps

1. ✅ Import the updated workflow
2. ✅ Test basic NetBox queries
3. ✅ Test cross-system queries
4. ✅ Train users on natural language queries
5. ⏳ Add more specific tools (get by ID, create, update)
6. ⏳ Add Gluware when available
7. ⏳ Configure Batfish REST API wrapper
8. ⏳ Add authentication to chat interface

---

**Updated**: October 30, 2025  
**Workflow ID**: `IH9uGEhWQ2vyEjg5`  
**Total Tools**: 19 (14 NetBox + 5 others)
