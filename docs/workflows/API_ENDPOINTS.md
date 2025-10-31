# API Endpoints Reference

This document contains all API endpoints configured for your IBNaaS environment with the correct URLs for accessing them from n8n and other containerized services.

## Network Configuration

- **Docker Host IP (from containers)**: `172.27.0.1`
- **Localhost (from host machine)**: `localhost` or `127.0.0.1`

## NetBox API

### Base Configuration
- **External URL (from host)**: `http://localhost:8443` or `http://localhost:8000`
- **Internal URL (from n8n/containers)**: `http://172.27.0.1:8443`
- **API Token**: `${NETBOX_API_TOKEN}`
- **Authentication Header**: `Authorization: Token ${NETBOX_API_TOKEN}`

### Root Endpoint
```
GET http://172.27.0.1:8443/api/
```

### Main API Categories

#### DCIM (Data Center Infrastructure Management)
```
GET http://172.27.0.1:8443/api/dcim/

# Devices
GET http://172.27.0.1:8443/api/dcim/devices/
GET http://172.27.0.1:8443/api/dcim/devices/{id}/
GET http://172.27.0.1:8443/api/dcim/devices/?limit=50
GET http://172.27.0.1:8443/api/dcim/devices/?name=<device_name>
GET http://172.27.0.1:8443/api/dcim/devices/?site=<site_name>

# Device Types
GET http://172.27.0.1:8443/api/dcim/device-types/
GET http://172.27.0.1:8443/api/dcim/device-types/{id}/

# Device Roles
GET http://172.27.0.1:8443/api/dcim/device-roles/
GET http://172.27.0.1:8443/api/dcim/device-roles/{id}/

# Sites
GET http://172.27.0.1:8443/api/dcim/sites/
GET http://172.27.0.1:8443/api/dcim/sites/{id}/
GET http://172.27.0.1:8443/api/dcim/sites/?limit=50

# Racks
GET http://172.27.0.1:8443/api/dcim/racks/
GET http://172.27.0.1:8443/api/dcim/racks/{id}/

# Interfaces
GET http://172.27.0.1:8443/api/dcim/interfaces/
GET http://172.27.0.1:8443/api/dcim/interfaces/{id}/
GET http://172.27.0.1:8443/api/dcim/interfaces/?device=<device_name>

# Cables
GET http://172.27.0.1:8443/api/dcim/cables/
GET http://172.27.0.1:8443/api/dcim/cables/{id}/

# Manufacturers
GET http://172.27.0.1:8443/api/dcim/manufacturers/
GET http://172.27.0.1:8443/api/dcim/manufacturers/{id}/

# Platforms
GET http://172.27.0.1:8443/api/dcim/platforms/
GET http://172.27.0.1:8443/api/dcim/platforms/{id}/
```

#### IPAM (IP Address Management)
```
GET http://172.27.0.1:8443/api/ipam/

# IP Addresses
GET http://172.27.0.1:8443/api/ipam/ip-addresses/
GET http://172.27.0.1:8443/api/ipam/ip-addresses/{id}/
GET http://172.27.0.1:8443/api/ipam/ip-addresses/?limit=50
GET http://172.27.0.1:8443/api/ipam/ip-addresses/?address=<ip_address>

# Prefixes
GET http://172.27.0.1:8443/api/ipam/prefixes/
GET http://172.27.0.1:8443/api/ipam/prefixes/{id}/

# VLANs
GET http://172.27.0.1:8443/api/ipam/vlans/
GET http://172.27.0.1:8443/api/ipam/vlans/{id}/

# VRFs
GET http://172.27.0.1:8443/api/ipam/vrfs/
GET http://172.27.0.1:8443/api/ipam/vrfs/{id}/

# Aggregates
GET http://172.27.0.1:8443/api/ipam/aggregates/
GET http://172.27.0.1:8443/api/ipam/aggregates/{id}/
```

#### Circuits
```
GET http://172.27.0.1:8443/api/circuits/

# Circuits
GET http://172.27.0.1:8443/api/circuits/circuits/
GET http://172.27.0.1:8443/api/circuits/circuits/{id}/

# Providers
GET http://172.27.0.1:8443/api/circuits/providers/
GET http://172.27.0.1:8443/api/circuits/providers/{id}/

# Circuit Types
GET http://172.27.0.1:8443/api/circuits/circuit-types/
GET http://172.27.0.1:8443/api/circuits/circuit-types/{id}/
```

#### Virtualization
```
GET http://172.27.0.1:8443/api/virtualization/

# Virtual Machines
GET http://172.27.0.1:8443/api/virtualization/virtual-machines/
GET http://172.27.0.1:8443/api/virtualization/virtual-machines/{id}/

# Clusters
GET http://172.27.0.1:8443/api/virtualization/clusters/
GET http://172.27.0.1:8443/api/virtualization/clusters/{id}/

# Cluster Types
GET http://172.27.0.1:8443/api/virtualization/cluster-types/
GET http://172.27.0.1:8443/api/virtualization/cluster-types/{id}/
```

#### Tenancy
```
GET http://172.27.0.1:8443/api/tenancy/

# Tenants
GET http://172.27.0.1:8443/api/tenancy/tenants/
GET http://172.27.0.1:8443/api/tenancy/tenants/{id}/

# Tenant Groups
GET http://172.27.0.1:8443/api/tenancy/tenant-groups/
GET http://172.27.0.1:8443/api/tenancy/tenant-groups/{id}/
```

#### Extras
```
GET http://172.27.0.1:8443/api/extras/

# Custom Fields
GET http://172.27.0.1:8443/api/extras/custom-fields/
GET http://172.27.0.1:8443/api/extras/custom-fields/{id}/

# Tags
GET http://172.27.0.1:8443/api/extras/tags/
GET http://172.27.0.1:8443/api/extras/tags/{id}/

# Config Contexts
GET http://172.27.0.1:8443/api/extras/config-contexts/
GET http://172.27.0.1:8443/api/extras/config-contexts/{id}/
```

#### Status
```
GET http://172.27.0.1:8443/api/status/
```

---

## n8n API

### Base Configuration
- **External URL (from host)**: `http://localhost:5678`
- **Internal URL (from containers)**: `http://172.27.0.1:5678` or `http://n8n-n8n-1:5678` (within n8n network)
- **For self-referencing**: `http://localhost:5678` (from within n8n container)
- **Authentication**: API Key (configure in Settings → API)

### Workflows
```
# List all workflows
GET http://localhost:5678/api/v1/workflows

# Get specific workflow
GET http://localhost:5678/api/v1/workflows/{id}

# Create workflow
POST http://localhost:5678/api/v1/workflows

# Update workflow
PATCH http://localhost:5678/api/v1/workflows/{id}

# Delete workflow
DELETE http://localhost:5678/api/v1/workflows/{id}

# Activate workflow
POST http://localhost:5678/api/v1/workflows/{id}/activate

# Deactivate workflow
POST http://localhost:5678/api/v1/workflows/{id}/deactivate
```

### Executions
```
# List executions
GET http://localhost:5678/api/v1/executions

# Get execution
GET http://localhost:5678/api/v1/executions/{id}

# Delete execution
DELETE http://localhost:5678/api/v1/executions/{id}
```

### Credentials
```
# List credentials
GET http://localhost:5678/api/v1/credentials

# Get credential
GET http://localhost:5678/api/v1/credentials/{id}
```

### Webhooks
```
# Webhook endpoint (production)
POST http://localhost:5678/webhook/{path}

# Webhook endpoint (test)
POST http://localhost:5678/webhook-test/{path}
```

---

## Batfish API

### Base Configuration
- **External URL (from host)**: `http://localhost:9997`
- **Internal URL (from containers)**: `http://172.27.0.1:9997` or `http://batfish:9997` (if on same network)
- **Dashboard**: `http://localhost:8050`
- **Jupyter**: `http://localhost:8888` (token: `aa9bf5625f98ed49ddc68e434dedd61ff343275bb17eff85`)
- **Authentication**: None (default installation)

**Note**: The Batfish API appears to be a Jupyter notebook interface. The REST API (port 9996) is not exposed. You'll need to use the Pybatfish Python library through Jupyter or implement a REST wrapper.

### Available Ports
```
9997 - Batfish service port (exposed)
8050 - Batfish dashboard
8888 - Jupyter notebook interface
9996 - Batfish API (internal only, not exposed to host)
```

### Common Pybatfish Operations
(These would be used within Python/Jupyter, not as REST endpoints)
```python
from pybatfish.client.commands import *
from pybatfish.question import bfq

# Initialize session
bf_session.host = "batfish"

# List snapshots
bf_list_snapshots()

# Load network and snapshot
bf_set_network("network_name")
bf_init_snapshot("path/to/configs")

# Run questions
result = bfq.nodeProperties().answer()
result = bfq.routes().answer()
result = bfq.bgpSessionStatus().answer()
result = bfq.ospfSessionStatus().answer()
```

---

## Gluware API

### Status
⚠️ **Gluware container is not currently running in your environment**

### Expected Configuration (when running)
- **Typical URL**: `http://gluware-server:8080` or `https://gluware-server:443`
- **Authentication**: API Token or Basic Auth
- **From containers**: `http://172.27.0.1:<port>` (when exposed)

### Common Endpoints (reference - adjust based on your Gluware deployment)
```
# Authentication
POST http://gluware-server:8080/api/auth/login

# Devices
GET http://gluware-server:8080/api/devices
GET http://gluware-server:8080/api/devices/{id}

# Jobs
GET http://gluware-server:8080/api/jobs
POST http://gluware-server:8080/api/jobs

# Templates
GET http://gluware-server:8080/api/templates
```

---

## Testing Examples

### Test NetBox from n8n container
```bash
docker exec -i n8n-n8n-1 sh -c "wget -q -O- --header='Authorization: Token ${NETBOX_API_TOKEN}' http://172.27.0.1:8443/api/dcim/devices/?limit=1"
```

### Test NetBox from host
```bash
curl -H "Authorization: Token ${NETBOX_API_TOKEN}" http://localhost:8443/api/dcim/devices/?limit=1
```

### Test n8n API from host
```bash
curl http://localhost:5678/api/v1/workflows
```

### Test Batfish connection
```bash
curl http://localhost:9997
curl http://localhost:8050  # Dashboard
```

---

## n8n Credential Configuration

### NetBox Credential
```yaml
Name: NetBox API
Type: NetBox API (from n8n-nodes-netbox plugin)
URL: http://172.27.0.1:8443
API Token: ${NETBOX_API_TOKEN}
```

### Gluware Credential (when available)
```yaml
Name: Gluware API
Type: HTTP Request / Generic Credential
URL: http://172.27.0.1:PORT
Authentication: Header Auth
Header Name: Authorization
Header Value: Bearer YOUR_GLUWARE_TOKEN
```

### n8n Self-Reference Credential
```yaml
Name: n8n API
Type: HTTP Request
URL: http://localhost:5678
Authentication: Header Auth
Header Name: X-N8N-API-KEY
Header Value: YOUR_N8N_API_KEY
```

---

## Important Notes

1. **Always use `172.27.0.1` when accessing host-published ports from containers** (like n8n accessing NetBox)
2. **Use `localhost` when accessing from the host machine**
3. **NetBox has two ports exposed**: 8000 and 8443 (both map to container port 8080)
4. **Batfish REST API (9996) is not exposed** - you'll need to use Pybatfish library or wrap it
5. **No trailing slashes** in base URLs for n8n credentials
6. **Always include the `Authorization: Token` header** for NetBox API calls

---

## Quick Reference Table

| Service | From Host | From n8n Container | Default Port |
|---------|-----------|-------------------|--------------|
| NetBox API | `http://localhost:8443` | `http://172.27.0.1:8443` | 8443 |
| NetBox Alt | `http://localhost:8000` | `http://172.27.0.1:8000` | 8000 |
| n8n UI | `http://localhost:5678` | `http://localhost:5678` | 5678 |
| n8n API | `http://localhost:5678/api/v1` | `http://localhost:5678/api/v1` | 5678 |
| Batfish Service | `http://localhost:9997` | `http://172.27.0.1:9997` | 9997 |
| Batfish Dashboard | `http://localhost:8050` | `http://172.27.0.1:8050` | 8050 |
| Batfish Jupyter | `http://localhost:8888` | `http://172.27.0.1:8888` | 8888 |
| Gluware | N/A (not running) | N/A | - |

---

## How to Use These APIs in n8n

### Step 1: Configure Credentials

#### NetBox Credential Setup

1. Open n8n UI: `http://localhost:5678`
2. Click **Settings** (gear icon) → **Credentials**
3. Click **+ Add Credential**
4. Search for **"NetBox API"** (from n8n-nodes-netbox plugin)
5. Configure:
   - **Credential Name**: `NetBox Production`
   - **NetBox URL**: `http://172.27.0.1:8443` (⚠️ NO trailing slash!)
   - **API Token**: `${NETBOX_API_TOKEN}`
6. Click **Test** to verify connection
7. Click **Save**

#### Alternative: HTTP Request Credential (for custom API calls)

1. Click **+ Add Credential** → **HTTP Request**
2. Configure:
   - **Credential Name**: `NetBox HTTP`
   - **Authentication**: `Generic Credential Type`
   - **Generic Auth Type**: `Header Auth`
   - **Header Name**: `Authorization`
   - **Header Value**: `Token ${NETBOX_API_TOKEN}`
3. Click **Save**

### Step 2: Create a Workflow

#### Method 1: Using NetBox Plugin Nodes (Recommended)

**Example: Get Devices from NetBox**

1. Create new workflow: **+ Add workflow**
2. Add **Manual Trigger** node
3. Add **NetBox** node:
   - Click **+** → Search "NetBox"
   - **Credential**: Select `NetBox Production`
   - **Resource**: `Device`
   - **Operation**: `Get All`
   - **Limit**: `50`
   - **Filters** (optional):
     - Site: `999123-Fox-and-Goose`
     - Status: `active`
4. Add **Set** node (optional - to format output)
5. Execute workflow to test

#### Method 2: Using HTTP Request Node (More Flexible)

**Example: Get NetBox Devices with Custom Query**

```
1. Add Manual Trigger
2. Add HTTP Request node:
   - Method: GET
   - URL: http://172.27.0.1:8443/api/dcim/devices/
   - Authentication: Predefined Credential
   - Credential: NetBox HTTP (or create header)
   - Query Parameters:
     - limit: 50
     - site: 999123-Fox-and-Goose
```

**Example: Get NetBox IP Addresses**

```
1. Add HTTP Request node:
   - Method: GET
   - URL: http://172.27.0.1:8443/api/ipam/ip-addresses/
   - Headers:
     - Name: Authorization
     - Value: Token ${NETBOX_API_TOKEN}
   - Query Parameters:
     - limit: 100
```

### Step 3: Common n8n Workflow Patterns

#### Pattern 1: Query NetBox → Process → Take Action

```
[Manual/Schedule Trigger] 
  → [NetBox: Get Devices] 
  → [Filter: Active devices only]
  → [IF Node: Check status]
  → [Send Notification/Update Device]
```

#### Pattern 2: Webhook → Validate in NetBox → Respond

```
[Webhook Trigger] 
  → [HTTP Request: Check NetBox IP]
  → [IF: IP exists?]
    → YES: [Return success]
    → NO: [Create in NetBox]
```

#### Pattern 3: Multi-Source Data Aggregation

```
[Schedule Trigger]
  → [NetBox: Get Devices]
  → [Batfish: Analyze Configs]
  → [Merge Data]
  → [Store Results]
```

### Step 4: Working with NetBox Data in n8n

#### Accessing Response Data

NetBox responses come in this format:
```json
{
  "count": 13,
  "next": "http://...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "999123-Fox-and-Goose-RT-01",
      "device_type": {...},
      "site": {...},
      "status": {"value": "active"}
    }
  ]
}
```

**In n8n expressions:**
- Get all devices: `{{ $json.results }}`
- Get first device name: `{{ $json.results[0].name }}`
- Get device count: `{{ $json.count }}`
- Loop through devices: Use **Split In Batches** or **Loop** node

#### Example: Filter Active Devices

```javascript
// In Function node or expression
const devices = $input.item.json.results;
const activeDevices = devices.filter(d => d.status.value === 'active');
return activeDevices;
```

### Step 5: Real-World n8n Examples

#### Example 1: Daily Device Report

**Workflow:**
```
[Schedule: Daily 8am]
  → [NetBox: Get All Devices]
  → [Code: Format data]
  → [Email: Send report]
```

**NetBox Node Config:**
- Resource: `Device`
- Operation: `Get All`
- Return All: `true`

#### Example 2: IP Address Availability Check

**Workflow:**
```
[Webhook: POST /check-ip]
  → [HTTP Request: Query NetBox IP]
  → [IF: Response count > 0]
    → YES: Return "IP in use"
    → NO: Return "IP available"
```

**HTTP Request Config:**
```
URL: http://172.27.0.1:8443/api/ipam/ip-addresses/
Method: GET
Query Parameters:
  - address: {{ $json.body.ip }}
Headers:
  - Authorization: Token ${NETBOX_API_TOKEN}
```

#### Example 3: Create Device in NetBox

**Workflow:**
```
[Webhook Trigger]
  → [NetBox: Create Device]
  → [Response: Return device ID]
```

**NetBox Node Config:**
```
Resource: Device
Operation: Create
Fields:
  - Name: {{ $json.body.device_name }}
  - Device Type: {{ $json.body.device_type_id }}
  - Site: {{ $json.body.site_id }}
  - Status: active
```

#### Example 4: Sync NetBox with External System

**Workflow:**
```
[Schedule: Every hour]
  → [NetBox: Get Devices updated in last hour]
  → [Split In Batches: 10]
  → [Loop Start]
    → [External API: Update device]
    → [NetBox: Update custom field with sync timestamp]
  → [Loop End]
```

### Step 6: Advanced Techniques

#### Using Pagination

NetBox returns paginated results. To get ALL data:

```
[HTTP Request to NetBox]
  → [Function: Extract 'next' URL]
  → [IF: 'next' exists?]
    → YES: [HTTP Request with 'next' URL] → Loop back
    → NO: [Continue to next node]
```

Or use the NetBox node's **Return All** option (it handles pagination automatically).

#### Error Handling

Add **Error Trigger** node:
```
[Try this workflow]
→ [On Error: Error Trigger]
  → [Log to file/database]
  → [Send alert]
  → [Retry or stop]
```

#### Using Expressions for Dynamic URLs

```javascript
// Build URL dynamically
URL: http://172.27.0.1:8443/api/dcim/devices/{{ $json.device_id }}/

// Conditional parameters
Query: limit={{ $json.limit || 50 }}
```

### Step 7: Testing Your Setup

#### Test 1: Simple Device Query

1. Create workflow with Manual Trigger + HTTP Request
2. Configure:
   ```
   Method: GET
   URL: http://172.27.0.1:8443/api/dcim/devices/?limit=1
   Headers:
     Authorization: Token ${NETBOX_API_TOKEN}
   ```
3. Execute and verify you get device data

#### Test 2: NetBox Plugin Test

1. Add NetBox node
2. Select credential
3. Resource: `Site`, Operation: `Get All`
4. Execute - should return your sites

#### Test 3: Create Operation

1. Use NetBox node with Operation: `Create`
2. Create a test tag or custom field
3. Verify it appears in NetBox UI

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ECONNREFUSED ::1:8443` | URL is `localhost` - change to `172.27.0.1:8443` |
| `403 Forbidden` | Check token is correct and formatted as `Token <token>` |
| `404 Not Found` | Verify endpoint path (e.g., `/api/dcim/devices/` not `/api/devices/`) |
| Plugin not found | Ensure n8n-nodes-netbox is installed in Settings → Community Nodes |
| Timeout errors | Increase timeout in HTTP Request node settings |
| Pagination issues | Use NetBox node's "Return All" or implement pagination loop |

### Useful n8n Expressions

```javascript
// Get current timestamp for NetBox custom fields
{{ $now.toISO() }}

// Format device name
{{ $json.name.toLowerCase().replace(/\s/g, '-') }}

// Check if field exists
{{ $json.primary_ip4 ? $json.primary_ip4.address : 'No IP' }}

// Build NetBox URL
{{ 'http://172.27.0.1:8443/api/dcim/devices/' + $json.id + '/' }}

// Extract ID from NetBox URL
{{ $json.url.split('/').slice(-2, -1)[0] }}
```

### Next Steps

1. ✅ Configure NetBox credential with `http://172.27.0.1:8443`
2. ✅ Test basic GET request to `/api/dcim/devices/`
3. ✅ Create simple workflow (Manual → NetBox → Display)
4. ✅ Add error handling
5. ✅ Build your first automation workflow
6. ✅ Integrate with AI Chat Agent (see Ai Chat agent.json)

---

**Generated**: October 30, 2025  
**Environment**: IBNaaS Docker Compose Stack
