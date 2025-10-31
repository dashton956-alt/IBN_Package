# NetBox Modular Workflows

This folder contains modular, reusable NetBox workflows designed to be called from other workflows. Each workflow performs a specific operation with built-in validation and error handling.

## 📂 Workflow Catalog

### 🆕 Create Operations (with existence validation)

#### 1. **NetBox_Create_Device.json**
Creates a new device in NetBox after checking if it already exists.

**Input Parameters:**
- `device_name` (string, required) - Name of the device
- `device_type` (number, required) - Device type ID
- `site` (number, required) - Site ID
- `device_role` (number, required) - Device role ID
- `status` (string, optional) - Device status (defaults to "active")

**Output:**
```json
{
  "success": true,
  "action": "created",
  "device": { ... }
}
```
or
```json
{
  "success": false,
  "action": "already_exists",
  "message": "Device 'router01' already exists",
  "existing_device": { ... }
}
```

**Flow:**
1. Check if device exists by name
2. If not exists → Create device
3. If exists → Return existing device info

---

#### 2. **NetBox_Create_Site.json**
Creates a new site in NetBox with auto-slug generation.

**Input Parameters:**
- `site_name` (string, required) - Site name
- `site_slug` (string, optional) - URL slug (auto-generated if not provided)
- `status` (string, optional) - Site status (defaults to "active")
- `facility` (string, optional) - Facility name/code
- `description` (string, optional) - Site description

**Output:**
```json
{
  "success": true,
  "action": "created",
  "site": { ... }
}
```

**Features:**
- Auto-generates URL-friendly slug from site name
- Validates site doesn't already exist by slug
- Returns detailed error if site exists

**Flow:**
1. Prepare site data (auto-generate slug if needed)
2. Check if site exists by slug
3. If not exists → Create site
4. If exists → Return existing site info

---

#### 3. **NetBox_Create_IP_Address.json**
Creates an IP address in NetBox with optional interface assignment.

**Input Parameters:**
- `ip_address` (string, required) - IP in CIDR notation (e.g., "192.168.1.10/24")
- `vrf` (number, optional) - VRF ID
- `status` (string, optional) - IP status (defaults to "active")
- `dns_name` (string, optional) - DNS name
- `description` (string, optional) - Description
- `assigned_object_type` (string, optional) - Object type (e.g., "dcim.interface")
- `assigned_object_id` (number, optional) - Interface ID

**Output:**
```json
{
  "success": true,
  "action": "created",
  "ip_address": { ... }
}
```

**Features:**
- Validates IP doesn't exist in same VRF
- Supports interface assignment
- Handles optional fields dynamically

**Flow:**
1. Check if IP exists (with VRF filter if provided)
2. If not exists → Prepare body → Create IP
3. If exists → Return existing IP info

---

#### 4. **NetBox_Create_VLAN.json**
Creates a VLAN with validation for duplicates within scope.

**Input Parameters:**
- `vlan_id` (number, required) - VLAN ID (1-4094)
- `vlan_name` (string, required) - VLAN name
- `site` (number, optional) - Site ID
- `vlan_group` (number, optional) - VLAN group ID
- `status` (string, optional) - VLAN status (defaults to "active")
- `description` (string, optional) - Description

**Output:**
```json
{
  "success": true,
  "action": "created",
  "vlan": { ... }
}
```

**Features:**
- Checks for duplicate VLAN ID within site/group
- Handles scoped VLAN validation
- Returns existing VLAN if found

**Flow:**
1. Check if VLAN exists (filtered by VID, site, and group)
2. If not exists → Prepare body → Create VLAN
3. If exists → Return existing VLAN info

---

### ✏️ Update Operations

#### 5. **NetBox_Update_Object.json**
Universal PATCH workflow for updating any NetBox object.

**Input Parameters:**
- `object_type` (string, required) - Object API path (e.g., "dcim/devices", "ipam/ip-addresses")
- `object_id` (number, required) - Object ID to update
- `update_fields` (json, required) - JSON object with fields to update

**Example Input:**
```json
{
  "object_type": "dcim/devices",
  "object_id": 5,
  "update_fields": "{\"status\": \"active\", \"name\": \"router01-updated\"}"
}
```

**Output:**
```json
{
  "success": true,
  "action": "updated",
  "object_type": "dcim/devices",
  "object_id": 5,
  "previous": { ... },
  "updated": { ... }
}
```

**Features:**
- Retrieves current object first (GET before PATCH)
- Returns both previous and updated state
- Works with any NetBox object type
- Validates object exists before updating

**Flow:**
1. GET current object to verify it exists
2. If exists → Prepare update → PATCH object → Return comparison
3. If not found → Return error

---

## 🔧 How to Use These Workflows

### Method 1: From Another Workflow (Execute Workflow Node)

```
[Your Trigger] → [Execute Workflow] → [Process Response]
```

**Example Configuration:**
```json
{
  "workflowId": "NetBox_Create_Device",
  "workflowInputs": {
    "device_name": "router01",
    "device_type": 1,
    "site": 2,
    "device_role": 3,
    "status": "active"
  }
}
```

### Method 2: From n8n AI Agent (Tool Workflow)

Add these as tools in your AI agent:

```json
{
  "type": "@n8n/n8n-nodes-langchain.toolWorkflow",
  "parameters": {
    "description": "Create a new device in NetBox",
    "workflowId": "NetBox_Create_Device",
    "workflowInputs": { ... }
  }
}
```

### Method 3: Via HTTP Webhook (if you add webhook trigger)

You can extend any workflow by adding a webhook trigger alongside the workflow trigger.

---

## 🎯 Design Patterns

### ✅ Validation First
All create workflows check for existence before creating to prevent duplicates.

### 📊 Consistent Response Format
All workflows return standardized responses:
- `success`: boolean
- `action`: string ("created", "updated", "already_exists", "not_found")
- `message`: string (for errors)
- `[object_name]`: object data

### 🔄 GET Before PATCH
Update workflow always retrieves current state before applying changes.

### 🛡️ Error Handling
Workflows gracefully handle:
- Object already exists
- Object not found
- Invalid parameters
- API errors

### 📦 Modular Design
Each workflow does ONE thing well and can be composed with others.

---

## 🚀 Common Usage Patterns

### Pattern 1: Create with Validation
```
Check Exists → If Not Exists → Create → Return Success
                ↓ If Exists
                Return Existing
```

### Pattern 2: Update with Safety
```
Get Current → If Exists → Apply Changes → Return Comparison
              ↓ If Not Found
              Return Error
```

### Pattern 3: Chaining Operations
```
Create Site → Create Device → Create Interface → Assign IP
```

---

## 🔐 Authentication

All workflows use the **Header Auth credential** (ID: `zUcs6TpKWgVP6mF0`) for NetBox API authentication.

**NetBox API Endpoint:** `http://172.27.0.1:8443/api/`

To update credentials:
1. Open any workflow
2. Click on HTTP Request nodes
3. Update credentials reference if needed

---

## 📋 Workflow IDs

When calling these workflows from other workflows, use these IDs:

| Workflow | ID |
|----------|-----|
| NetBox_Create_Device | `netbox-create-device` |
| NetBox_Create_Site | `netbox-create-site` |
| NetBox_Create_IP_Address | `netbox-create-ip` |
| NetBox_Create_VLAN | `netbox-create-vlan` |
| NetBox_Update_Object | `netbox-update-object` |

---

## 🧪 Testing

### Test NetBox_Create_Site:
```json
{
  "site_name": "Test Data Center",
  "status": "planned",
  "description": "Test site for validation"
}
```

### Test NetBox_Create_Device:
```json
{
  "device_name": "test-router01",
  "device_type": 1,
  "site": 1,
  "device_role": 1
}
```

### Test NetBox_Create_IP_Address:
```json
{
  "ip_address": "10.0.0.1/24",
  "status": "active",
  "dns_name": "test.example.com"
}
```

### Test NetBox_Create_VLAN:
```json
{
  "vlan_id": 100,
  "vlan_name": "Management",
  "status": "active"
}
```

### Test NetBox_Update_Object:
```json
{
  "object_type": "dcim/devices",
  "object_id": 5,
  "update_fields": "{\"status\": \"active\"}"
}
```

---

## 📈 Future Enhancements

Potential additions:
- NetBox_Delete_Object (with confirmation)
- NetBox_Create_Interface
- NetBox_Create_Prefix
- NetBox_Assign_IP_To_Interface
- NetBox_Bulk_Create (batch operations)
- NetBox_Query (search/filter)
- Error logging and notifications
- Rollback capabilities

---

## 🤝 Integration Examples

### Example 1: AI Agent Creating Infrastructure
```
User: "Create a new site called DC3 and add router01"

AI Agent:
1. Calls NetBox_Create_Site with site_name="DC3"
2. Calls NetBox_Create_Device with device_name="router01", site=[new site ID]
3. Returns success message with both object IDs
```

### Example 2: Automation Workflow
```
[Schedule Trigger]
   ↓
[Loop Through CSV]
   ↓
[Execute NetBox_Create_Device for each row]
   ↓
[Send Summary Email]
```

### Example 3: Self-Service Portal
```
[Webhook: User Request]
   ↓
[Validate Request]
   ↓
[Execute NetBox_Create_VLAN]
   ↓
[Update Ticket System]
   ↓
[Notify User]
```

---

## 📚 Related Documentation

- NetBox API Docs: https://netbox.readthedocs.io/
- n8n Execute Workflow: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/
- n8n HTTP Request: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/

---

**Status:** ✅ All workflows validated and ready for import  
**Last Updated:** October 31, 2025  
**NetBox Version:** 4.4.4  
**n8n Version:** 1.117.3
