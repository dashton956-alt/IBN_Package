# Proxmox AI Agent Workflow Analysis & NetBox Adaptation

## 📊 Workflow Architecture Review

### **Current Proxmox Workflow Structure:**

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. INPUT TRIGGERS (Multiple Options)                           │
│    ├─ Chat Trigger (Primary)                                   │
│    ├─ Telegram Trigger                                         │
│    ├─ Gmail Trigger                                            │
│    └─ Webhook Trigger                                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. AI AGENT (Proxmox Command Generator)                        │
│    ├─ Model: Google Gemini 2.0 Flash                           │
│    ├─ Agent Type: ReAct Agent                                  │
│    ├─ Tools Available:                                         │
│    │   ├─ Proxmox API Documentation (Web scrape)               │
│    │   ├─ Proxmox API Wiki (Web scrape)                        │
│    │   └─ Proxmox Cluster Status (Live API call)               │
│    ├─ Output Parser: Structured JSON Parser                    │
│    └─ Auto-fixing Parser: Error correction                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. SWITCH (Route by HTTP Method)                               │
│    ├─ GET → Query Operations                                   │
│    ├─ POST → Create/Start Operations                           │
│    ├─ PUT → Update Operations                                  │
│    ├─ DELETE → Delete Operations                               │
│    └─ Invalid → Error Response                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. EXECUTION BRANCHES                                           │
│                                                                 │
│ GET Branch:                                                     │
│   HTTP Request → Structure Response → AI Agent (Summarize)     │
│                                                                 │
│ POST Branch:                                                    │
│   If (has details?) → HTTP Request → Merge → Parse Response    │
│                                                                 │
│ DELETE Branch:                                                  │
│   If (has details?) → HTTP Request → Merge → Parse Response    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. RESPONSE FORMATTING                                          │
│    ├─ Structure Response from Proxmox (Parse UPID)             │
│    ├─ Format Response and Hide Sensitive Data                  │
│    └─ Return formatted message to user                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Detailed Component Analysis

### **1. AI Agent Configuration:**

**Current Proxmox Prompt Structure:**
```
- System Identity: "Proxmox AI Agent expert"
- Objectives: 8 main sections
- Tools: 3 knowledge sources (API Doc, Wiki, Live cluster)
- Output Format: Strict JSON with response_type, url, details
- Validation: Required fields, optional fields, defaults
- Examples: 12 detailed examples
- Special Instructions: Always include all 3 JSON fields
```

**Key Prompt Features:**
- ✅ Node defaults (psb1, psb2, psb3)
- ✅ Auto-generate VMID by querying highest existing
- ✅ Exclude optional fields to use Proxmox defaults
- ✅ Missing parameter handling with helpful messages
- ✅ Invalid input detection
- ✅ Security: Don't include passwords/keys in output

---

### **2. Output Parsers:**

**Structured Output Parser:**
```json
{
  "response_type": "POST",
  "url": "/nodes/psb1/qemu",
  "details": {
    "vmid": 105,
    "cores": 4,
    "memory": 8192
  },
  "message": "Success message"
}
```

**Auto-fixing Output Parser:**
- Catches parsing errors
- Sends error back to AI
- Asks AI to regenerate valid JSON
- Ensures output matches schema

---

### **3. HTTP Request Routing:**

**GET Requests:**
```javascript
Method: GET
URL: https://10.11.12.101:8006/api2/json{{ $json.output.url }}
Auth: Header Auth
Options: allowUnauthorizedCerts: true
```

**POST Requests:**
```javascript
Method: POST
URL: https://10.11.12.101:8006/api2/json{{ $json.output.url }}
Body: {{ $json.output.details }}
Auth: Header Auth
```

**DELETE Requests:**
```javascript
Method: DELETE
URL: https://10.11.12.101:8006/api2/json{{ $json.output.url }}
Auth: Header Auth
```

**Conditional Logic:**
- If has `details` field → Send with body
- If no `details` field → Send without body

---

### **4. Response Processing:**

**For GET Operations:**
```
HTTP Response → Structure Response (combine fields) → 
AI Agent (summarize) → User-friendly output
```

**For POST/DELETE Operations:**
```
HTTP Response → Parse UPID string → 
Extract: node, operation, user, timestamp → 
Format message hiding sensitive data → 
Return simple success message
```

**UPID Parsing Example:**
```
Input: "UPID:psb1:00001234:00000123:65ABC123:aptupdate::root@pam!n8n:"
Output: {
  upid: "UPID",
  node: "psb1",
  processID: "00001234",
  operation: "aptupdate",
  user: "root@pam!n8n",
  timestamp: "65ABC123" → converted to readable date
}
```

---

## 🔄 NetBox Adaptation Requirements

### **Changes Needed for NetBox:**

#### **1. Remove Node Concept:**
```diff
- Proxmox has nodes (psb1, psb2, psb3)
+ NetBox has no nodes - single API endpoint
- URL: /nodes/{node}/qemu/
+ URL: /dcim/devices/ or /ipam/ip-addresses/
```

#### **2. Update Base URL:**
```diff
- https://10.11.12.101:8006/api2/json
+ http://172.27.0.1:8443/api
```

#### **3. Change Authentication:**
```diff
- Proxmox: PVEAPIToken=root@pam!n8n=1234
+ NetBox: Token ${NETBOX_API_TOKEN}
```

#### **4. Update AI Tools:**
```diff
- Proxmox API Documentation
- Proxmox API Wiki
- Proxmox Cluster Status (Live)
+
+ NetBox API Schema (http://172.27.0.1:8443/api/schema/)
+ NetBox Documentation
+ NetBox Live Query (http://172.27.0.1:8443/api/status/)
```

#### **5. Modify Output Schema:**
```json
// Proxmox Schema
{
  "response_type": "POST",
  "url": "/nodes/psb1/qemu",
  "details": { "vmid": 105 }
}

// NetBox Schema
{
  "response_type": "POST",
  "url": "/dcim/devices/",
  "details": { 
    "name": "router01",
    "device_type": 1,
    "site": 1,
    "device_role": 1
  }
}
```

#### **6. Update Response Parsing:**
```diff
- Parse Proxmox UPID (task tracking)
+ Parse NetBox response (direct object data)
- Extract: node, operation, user, timestamp
+ Extract: id, name, status, created, last_updated
```

#### **7. HTTP Methods Difference:**
```diff
- Proxmox uses PUT for updates
+ NetBox uses PATCH for partial updates
- Proxmox: PUT /nodes/node1/qemu/105/config
+ NetBox: PATCH /dcim/devices/5/
```

#### **8. Add NetBox-Specific Validation:**
```diff
+ IP addresses must be in CIDR format (192.168.1.1/24)
+ VLAN IDs must be 1-4094
+ Slugs must be URL-friendly (auto-generate)
+ Status values: active, planned, staged, failed, etc.
+ Required vs optional fields vary by object type
```

---

## 📝 NetBox Workflow Modifications

### **Detailed Changes by Node:**

#### **Node 1: AI Agent Prompt**
```diff
- "You are a Proxmox AI Agent expert..."
+ "You are a NetBox AI Agent expert..."

- "My proxmox nodes are named as psb1, psb2 and psb3"
+ [Remove - NetBox has no nodes]

- "Default to psb1 if node not specified"
+ [Remove - not applicable]

- Examples: VM operations (create, start, stop, clone)
+ Examples: Device/IP/VLAN operations (create, list, update)

- Special: Auto-generate VMID
+ Special: Query for existing IDs, validate uniqueness
```

#### **Node 2: Tools**
```diff
Tool 1: Proxmox API Documentation
- URL: https://pve.proxmox.com/pve-docs/api-viewer/
+ URL: http://172.27.0.1:8443/api/docs/
+ Description: "NetBox API schema and documentation"

Tool 2: Proxmox API Wiki
- URL: https://pve.proxmox.com/wiki/Proxmox_VE_API
+ URL: http://172.27.0.1:8443/api/schema/
+ Description: "NetBox API schema definition"

Tool 3: Proxmox Cluster Status
- URL: https://10.11.12.101:8006/api2/json/cluster/status
+ URL: http://172.27.0.1:8443/api/status/
+ Description: "NetBox system status and version info"
```

#### **Node 3: Structured Output Parser**
```diff
{
-  "response_type": "POST",
-  "url": "/nodes/psb1/qemu",
-  "details": {
-    "vmid": 105,
-    "cores": 4,
-    "memory": 8192,
-    "net0": "virtio,bridge=vmbr0"
-  }
+  "response_type": "POST",
+  "url": "/dcim/devices/",
+  "details": {
+    "name": "router01",
+    "device_type": 1,
+    "site": 1,
+    "device_role": 1,
+    "status": "active"
+  }
}
```

#### **Node 4: HTTP Requests**
```diff
GET Request:
- URL: https://10.11.12.101:8006/api2/json{{ url }}
+ URL: http://172.27.0.1:8443/api{{ url }}

POST Request:
- URL: https://10.11.12.101:8006/api2/json{{ url }}
+ URL: http://172.27.0.1:8443/api{{ url }}

DELETE Request:
- URL: https://10.11.12.101:8006/api2/json{{ url }}
+ URL: http://172.27.0.1:8443/api{{ url }}

- Method: PUT for updates
+ Method: PATCH for updates (add new branch)
```

#### **Node 5: Response Parsing**
```diff
- Parse UPID string (Proxmox task tracking)
+ Parse NetBox object response

Proxmox Response:
- { "data": "UPID:psb1:..." }
+ 

NetBox Response:
+ { 
+   "id": 5, 
+   "name": "router01",
+   "status": { "value": "active" },
+   "created": "2025-10-31",
+   "last_updated": "2025-10-31T10:30:00Z"
+ }
```

#### **Node 6: Success Message Format**
```diff
Proxmox:
- "Operation 'aptupdate' executed on node 'psb1' by 'root@pam'"

NetBox:
+ "Device 'router01' created successfully with ID 5"
+ "IP address '10.0.0.1/24' assigned to interface eth0"
+ "VLAN 100 'Management' created at site DC1"
```

---

## 🎯 Key Differences Summary

| Feature | Proxmox | NetBox |
|---------|---------|--------|
| **Nodes** | psb1, psb2, psb3 | N/A (single instance) |
| **Base URL** | `/api2/json` | `/api` |
| **Auth Header** | `PVEAPIToken=user!token=key` | `Authorization: Token <key>` |
| **Update Method** | PUT | PATCH |
| **ID Generation** | Auto-query highest VMID | User provides or queries |
| **Response** | UPID task string | Direct object JSON |
| **Object Types** | VMs, nodes, storage | Devices, IPs, VLANs, sites |
| **Required Fields** | vmid, cores, memory | Varies by object (device needs type/site/role) |
| **Status Values** | running, stopped | active, planned, staged, failed |
| **Slug Fields** | N/A | Required for many objects |
| **CIDR Notation** | N/A | Required for IPs/prefixes |

---

## 🚀 Implementation Checklist for NetBox

- [ ] Replace AI Agent prompt with NetBox version
- [ ] Update all 3 tool URLs to NetBox endpoints
- [ ] Change authentication header format
- [ ] Update base URL in all HTTP Request nodes
- [ ] Add PATCH method branch in Switch node
- [ ] Remove node-specific logic from prompt
- [ ] Update Structured Output Parser schema
- [ ] Replace UPID parsing with NetBox object parsing
- [ ] Update success message formatting
- [ ] Add NetBox-specific validation (CIDR, slugs, VLAN IDs)
- [ ] Update sticky note documentation
- [ ] Test with NetBox API examples (create device, IP, VLAN)
- [ ] Add error handling for NetBox-specific errors

---

## 📋 Next Steps

1. **Create NetBox AI Agent workflow** based on Proxmox template
2. **Use the NetBox prompt** from `NetBox_AI_Agent_Prompt.txt`
3. **Update all HTTP nodes** with NetBox URLs and auth
4. **Test with sample queries:**
   - "List all devices"
   - "Create device router01 with type 1, site 2, role 3"
   - "Create IP 10.0.0.1/24"
   - "Update device 5 status to active"
5. **Integrate with modular workflows** from `netbox flows/` folder

---

This analysis provides a complete roadmap for converting the Proxmox AI Agent workflow to work with NetBox!
