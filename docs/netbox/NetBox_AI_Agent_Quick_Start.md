# NetBox AI Agent - Quick Start Guide

## 📋 Overview
This is a fully functional AI-powered NetBox workflow that converts natural language requests into NetBox API commands.

## 🚀 Import & Setup

### 1. Import Workflow to n8n
```bash
# File location:
/home/dan/ibnaas/n8n/chat ops/NetBox AI Agent with n8n and Generative AI Integration.json

# In n8n UI:
1. Go to Workflows
2. Click "Import from File"
3. Select the workflow JSON file
4. Click "Import"
```

### 2. Verify Credentials
The workflow uses **Header Auth** credential with ID: `zUcs6TpKWgVP6mF0`

**Format:**
- Header Name: `Authorization`
- Header Value: `Token ${NETBOX_API_TOKEN}`

**To check/create:**
```
1. In n8n: Go to Credentials
2. Search for "Header Auth account"
3. Verify it has:
   - Name: Authorization
   - Value: Token ${NETBOX_API_TOKEN}
```

### 3. Test NetBox Connection
```bash
# Test API access:
curl -H "Authorization: Token ${NETBOX_API_TOKEN}" \
     http://172.27.0.1:8443/api/status/

# Should return NetBox version and status
```

## 🎯 Test Queries

### GET Operations (List/Query)
```
"Show me all devices"
"List all sites"
"Get device with ID 5"
"List all IP addresses in prefix 10.0.0.0/24"
"Show me all active devices at site 2"
"Search for devices with 'router' in the name"
```

### POST Operations (Create)
```
"Create a device named router01 with device type 1, site 2, and device role 3"
"Create a site called Data Center 3 with status planned"
"Create IP address 192.168.1.10/24 with status active"
"Create VLAN 100 named Management at site 1"
"Create interface eth0 on device 5 with type 1000base-t"
```

### PATCH Operations (Update)
```
"Update device 5 status to active"
"Update device 5 to set status active, name router01-updated, and description Updated router"
"Update VLAN 100 status to active"
```

### DELETE Operations
```
"Delete device with ID 10"
"Delete IP address with ID 50"
```

### Invalid Input (Should return "Invalid")
```
"Tell me a joke"
"What's the weather?"
```

## 🔧 Workflow Architecture

```
┌─────────────────┐
│  Triggers       │  Chat, Telegram, Gmail, Webhook
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   AI Agent      │  Gemini 2.0 with ReAct
│   (Prompt)      │  405-line NetBox expert prompt
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Output Parsers  │  Structured + Auto-fixing
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Switch Node    │  Routes by HTTP method
└────┬─┬─┬─┬──────┘
     │ │ │ │
     │ │ │ └─────► DELETE → HTTP Request3/4
     │ │ └───────► PATCH  → HTTP Request1 (dynamic)
     │ └─────────► POST   → HTTP Request1 (dynamic)
     └───────────► GET    → HTTP Request
```

## 🛠️ Tools Available to AI Agent

1. **NetBox API Documentation**
   - URL: http://172.27.0.1:8443/api/docs/
   - Provides interactive API documentation

2. **NetBox API Schema**
   - URL: http://172.27.0.1:8443/api/schema/
   - OpenAPI schema with field details

3. **NetBox Status**
   - URL: http://172.27.0.1:8443/api/status/
   - System status and version info

## 📊 Supported NetBox Objects

### DCIM (Data Center Infrastructure)
- Devices, Device Types, Device Roles
- Interfaces, Cables
- Sites, Locations, Racks
- Manufacturers, Platforms
- Power Ports, Console Ports

### IPAM (IP Address Management)
- IP Addresses, Prefixes
- VLANs, VLAN Groups
- VRFs, Aggregates, ASNs
- Services

### Circuits
- Circuits, Providers, Circuit Types

### Virtualization
- Virtual Machines, Clusters, VM Interfaces

### Tenancy & Wireless
- Tenants, Wireless LANs

## 🔍 AI Agent Capabilities

### Understands:
- Natural language requests
- NetBox object relationships
- Required vs optional fields
- CIDR notation for IP addresses
- VLAN ID ranges (1-4094)
- Slug auto-generation

### Validates:
- Required fields for each object type
- Status values (active, planned, staged, etc.)
- IP address format (CIDR)
- VLAN ID ranges

### Generates:
- Complete API URLs
- Proper HTTP methods
- JSON payloads with correct fields
- Helpful error messages for missing data

## ⚙️ HTTP Method Handling

| Method | Purpose | Body | AI Agent Output |
|--------|---------|------|-----------------|
| GET | List/query | No | `{ "response_type": "GET", "url": "..." }` |
| POST | Create | Yes | `{ "response_type": "POST", "url": "...", "details": {...} }` |
| PATCH | Update | Yes | `{ "response_type": "PATCH", "url": "...", "details": {...} }` |
| DELETE | Remove | No | `{ "response_type": "DELETE", "url": "..." }` |

## 🎨 Example AI Agent Outputs

### Example 1: Create Device
**Input:** "Create a device named router01 with device type 1, site 2, and device role 3"

**AI Output:**
```json
{
  "response_type": "POST",
  "url": "http://172.27.0.1:8443/api/dcim/devices/",
  "details": {
    "name": "router01",
    "device_type": 1,
    "site": 2,
    "device_role": 3,
    "status": "active"
  }
}
```

### Example 2: Update Device
**Input:** "Update device 5 status to active"

**AI Output:**
```json
{
  "response_type": "PATCH",
  "url": "http://172.27.0.1:8443/api/dcim/devices/5/",
  "details": {
    "status": "active"
  }
}
```

### Example 3: Query Devices
**Input:** "Show me all active devices at site 2"

**AI Output:**
```json
{
  "response_type": "GET",
  "url": "http://172.27.0.1:8443/api/dcim/devices/?site_id=2&status=active"
}
```

## 🚨 Troubleshooting

### Issue: "Missing required parameters"
**Cause:** AI detected missing fields for the operation
**Solution:** The AI will tell you which fields are required. Query for IDs first:
```
"Show me all device types"  # Get device_type ID
"Show me all sites"         # Get site ID
"Show me all device roles"  # Get device_role ID
```

### Issue: HTTP 401 Unauthorized
**Cause:** Invalid or missing API token
**Solution:** 
1. Check credential in n8n (ID: zUcs6TpKWgVP6mF0)
2. Verify token format: `Token <token-value>`
3. Test token in terminal:
```bash
curl -H "Authorization: Token ${NETBOX_API_TOKEN}" \
     http://172.27.0.1:8443/api/status/
```

### Issue: HTTP 400 Bad Request
**Cause:** Invalid data format (e.g., missing CIDR notation)
**Solution:** Check AI agent output:
- IP addresses need CIDR: `192.168.1.10/24` not `192.168.1.10`
- VLAN IDs must be 1-4094
- Required fields must be present

### Issue: "Invalid" response
**Cause:** Request not related to NetBox
**Solution:** Rephrase request with NetBox terminology:
- ❌ "Show me servers"
- ✅ "Show me all devices"

## 📈 Performance Tips

1. **Query IDs First:** Before creating objects, get IDs of related objects
2. **Use Filters:** Instead of listing all, filter: `?site_id=2&status=active`
3. **PATCH Not PUT:** For updates, AI uses PATCH (NetBox best practice)
4. **Check Before Create:** Use modular workflows for existence validation

## 🔗 Related Workflows

The following modular workflows complement this AI agent:

1. **NetBox_Create_Device.json** - Validates existence before creating devices
2. **NetBox_Create_Site.json** - Auto-generates slugs for sites
3. **NetBox_Create_IP_Address.json** - CIDR validation and VRF support
4. **NetBox_Create_VLAN.json** - VLAN ID validation (1-4094)
5. **NetBox_Update_Object.json** - Universal PATCH workflow with GET-before-update

Location: `/home/dan/ibnaas/n8n/netbox flows/`

## 📚 Additional Resources

- **Full Conversion Summary:** `/home/dan/ibnaas/n8n/chat ops/NetBox_AI_Agent_Conversion_Summary.md`
- **AI Agent Prompt:** `/home/dan/ibnaas/n8n/netbox flows/NetBox_AI_Agent_Prompt.txt`
- **Conversion Guide:** `/home/dan/ibnaas/n8n/netbox flows/Proxmox_to_NetBox_Conversion_Guide.md`
- **Modular Workflows README:** `/home/dan/ibnaas/n8n/netbox flows/README.md`

## 🎯 Quick Test Checklist

After import, test these in order:

- [ ] **Basic GET:** "Show me all devices"
- [ ] **Filtered GET:** "List devices at site 1"
- [ ] **Simple POST:** "Create a site called Test Site"
- [ ] **Complex POST:** "Create a device named test-router with device type 1, site 1, and device role 1"
- [ ] **PATCH:** "Update device 1 status to active"
- [ ] **DELETE:** "Delete device 999" (non-existent to test error handling)
- [ ] **Invalid:** "What's the weather?" (should return Invalid)

## ✅ Success Indicators

You'll know it's working correctly when:
1. AI agent returns properly formatted JSON
2. HTTP requests execute without errors
3. NetBox objects are created/updated/deleted as expected
4. Response parser formats data readably
5. Invalid inputs return `{ "response_type": "Invalid" }`

---

**Ready to go!** 🚀 Start with simple GET queries and work up to complex operations.

For support, refer to the full conversion summary or NetBox API docs.
