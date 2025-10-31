# Gluware API n8n Workflows

Modular n8n workflow collection for interacting with the Gluware API. Each workflow is designed as a reusable sub-workflow that can be called from other workflows using the Execute Workflow node.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Available Workflows](#available-workflows)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Common Patterns](#common-patterns)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This collection provides standardized, production-ready workflows for all major Gluware API endpoints:

- **Devices Management** - CRUD operations for network devices
- **Sites Management** - Organization and site hierarchy management
- **Audit Logs** - Compliance and activity tracking
- **Lifecycle Management** - Device lifecycle automation
- **Network Topology** - Topology discovery and visualization
- **Config Drift Detection** - Configuration compliance monitoring
- **CMDB Integration** - Configuration item management
- **Policy Management** - Network policy automation
- **Device Onboarding** - Zero-touch provisioning workflows

## ✅ Prerequisites

### Required

- n8n version 1.0.0 or higher
- Gluware API access with valid API key
- Network connectivity to Gluware instance

### Environment Variables

Set these in your n8n environment:

```bash
GLUWARE_API_URL=https://your-gluware-instance.com/api/v1
GLUWARE_API_KEY=your_api_key_here
```

## 📦 Installation

### Option 1: Import Individual Workflows

1. Open n8n interface
2. Click "Add Workflow" > "Import from File"
3. Select the desired workflow JSON file
4. Save the workflow

### Option 2: Bulk Import

Import all workflows at once using n8n CLI:

```bash
# Import all workflows
for workflow in gluware_*.json; do
  n8n import:workflow --input="$workflow"
done
```

### Option 3: API Import

Use the n8n API to programmatically import workflows:

```bash
curl -X POST http://localhost:5678/rest/workflows \
  -H "Content-Type: application/json" \
  -d @gluware_devices_workflow.json
```

## 🔧 Available Workflows

### 1. Devices API (`gluware_devices_workflow.json`)

**Purpose:** Manage network device inventory

**Input Parameters:**
- `method` (string): HTTP method - GET, POST, PUT, DELETE
- `deviceId` (string): Specific device ID for single device operations
- `filters` (string): Query parameters (e.g., "site=NYC&status=active")
- `body` (string): JSON body for POST/PUT operations

**Example Usage:**
```json
{
  "method": "GET",
  "filters": "site=NYC&vendor=Cisco"
}
```

### 2. Sites API (`gluware_sites_workflow.json`)

**Purpose:** Manage site hierarchy and organization

**Input Parameters:**
- `method` (string): GET, POST, PUT, DELETE
- `siteId` (string): Specific site identifier
- `filters` (string): Query filters
- `includeDevices` (string): "true" or "false" - include device list
- `body` (string): JSON body for modifications

**Example Usage:**
```json
{
  "method": "POST",
  "body": "{\"name\": \"NYC-Office\", \"region\": \"NA-EAST\", \"address\": \"123 Main St\"}"
}
```

### 3. Audit API (`gluware_audit_workflow.json`)

**Purpose:** Query audit logs for compliance and tracking

**Input Parameters:**
- `method` (string): GET (read-only)
- `auditId` (string): Specific audit entry ID
- `startDate` (string): ISO 8601 date (e.g., "2025-01-01T00:00:00Z")
- `endDate` (string): ISO 8601 date
- `userId` (string): Filter by user
- `action` (string): Filter by action (CREATE, UPDATE, DELETE)
- `resource` (string): Filter by resource type
- `limit` (string): Pagination limit (default: "100")
- `offset` (string): Pagination offset (default: "0")

**Example Usage:**
```json
{
  "method": "GET",
  "startDate": "2025-01-01T00:00:00Z",
  "endDate": "2025-01-31T23:59:59Z",
  "action": "UPDATE",
  "limit": "50"
}
```

### 4. Lifecycle API (`gluware_lifecycle_workflow.json`)

**Purpose:** Manage device lifecycle stages

**Input Parameters:**
- `method` (string): GET, POST, PUT, DELETE
- `lifecycleId` (string): Specific lifecycle record ID
- `deviceId` (string): Filter by device
- `status` (string): pending, in-progress, completed, failed, cancelled
- `stage` (string): discovery, provisioning, deployment, configuration, testing, production, decommission
- `body` (string): JSON body for operations

**Example Usage:**
```json
{
  "method": "POST",
  "body": "{\"deviceId\": \"dev-123\", \"stage\": \"provisioning\", \"autoProgress\": true}"
}
```

### 5. Topology API (`gluware_topology_workflow.json`)

**Purpose:** Query and visualize network topology

**Input Parameters:**
- `method` (string): GET (read-only)
- `topologyId` (string): Specific topology snapshot ID
- `siteId` (string): Filter topology by site
- `deviceId` (string): Center topology on device
- `depth` (string): Topology depth 1-5 (default: "2")
- `includeLinks` (string): "true" or "false"
- `format` (string): json, graphml, cytoscape

**Example Usage:**
```json
{
  "method": "GET",
  "siteId": "site-nyc",
  "depth": "3",
  "includeLinks": "true",
  "format": "json"
}
```

### 6. Config Drift API (`gluware_config_drift_workflow.json`)

**Purpose:** Detect and manage configuration drift

**Input Parameters:**
- `method` (string): GET, POST, PUT
- `driftId` (string): Specific drift record ID
- `deviceId` (string): Filter by device
- `severity` (string): critical, high, medium, low, info
- `status` (string): detected, acknowledged, resolved, ignored
- `startDate` (string): ISO 8601 date
- `endDate` (string): ISO 8601 date
- `body` (string): JSON body for POST/PUT

**Example Usage:**
```json
{
  "method": "GET",
  "severity": "critical",
  "status": "detected",
  "startDate": "2025-01-01T00:00:00Z"
}
```

### 7. CMDB API (`gluware_cmdb_workflow.json`)

**Purpose:** Configuration Management Database operations

**Input Parameters:**
- `method` (string): GET, POST, PUT, DELETE
- `ciId` (string): Configuration Item ID
- `ciType` (string): device, interface, service, application, server, database, network, storage
- `search` (string): Search query
- `attributes` (string): Comma-separated attribute list
- `relationships` (string): "true" or "false"
- `body` (string): JSON body for modifications

**Example Usage:**
```json
{
  "method": "GET",
  "ciType": "device",
  "relationships": "true",
  "attributes": "name,ipAddress,status"
}
```

### 8. Policy API (`gluware_policy_workflow.json`)

**Purpose:** Network policy automation and management

**Input Parameters:**
- `method` (string): GET, POST, PUT, DELETE
- `policyId` (string): Specific policy ID
- `policyType` (string): security, qos, routing, access, compliance, backup, monitoring
- `scope` (string): global, site, device, interface
- `status` (string): active, inactive, draft, deprecated, scheduled
- `validate` (string): "true" or "false" - validate before applying
- `body` (string): JSON body with policy rules

**Example Usage:**
```json
{
  "method": "POST",
  "validate": "true",
  "body": "{\"name\": \"QoS-Voice\", \"policyType\": \"qos\", \"scope\": \"global\", \"rules\": [{\"match\": \"dscp ef\", \"action\": \"priority-queue\"}]}"
}
```

### 9. Onboarding API (`gluware_onboarding_workflow.json`)

**Purpose:** Automate device onboarding workflows

**Input Parameters:**
- `method` (string): GET, POST, PUT, DELETE
- `onboardingId` (string): Specific onboarding job ID
- `deviceId` (string): Target device
- `status` (string): pending, in-progress, completed, failed, cancelled, awaiting-approval
- `template` (string): Onboarding template name
- `autoApprove` (string): "true" or "false"
- `body` (string): JSON body with device details

**Example Usage:**
```json
{
  "method": "POST",
  "autoApprove": "true",
  "body": "{\"deviceIp\": \"10.0.1.50\", \"credentials\": {\"username\": \"admin\", \"password\": \"secret\"}, \"template\": \"cisco-ios-standard\"}"
}
```

## ⚙️ Configuration

### Setting Up Credentials

1. Navigate to Settings > Credentials in n8n
2. Create new credential of type "Header Auth" or "API Key"
3. Configure as follows:
   - **Name:** Gluware API
   - **Auth Type:** Bearer Token
   - **Token:** Your Gluware API key

### Environment Variables

Add to your n8n environment configuration:

```bash
# .env file or environment configuration
GLUWARE_API_URL=https://api.gluware.com/v1
GLUWARE_API_KEY=glu_xxxxxxxxxxxxxxxxxxxxxxxx
```

## 💡 Usage Examples

### Example 1: List All Devices

```javascript
// In your parent workflow, use Execute Workflow node
{
  "workflowName": "Gluware - Devices API",
  "data": {
    "method": "GET"
  }
}
```

### Example 2: Create New Site with Error Handling

```javascript
// Parent workflow with error handling
{
  "workflowName": "Gluware - Sites API",
  "data": {
    "method": "POST",
    "body": JSON.stringify({
      "name": "London Office",
      "region": "EMEA",
      "address": "10 Downing Street",
      "timezone": "Europe/London"
    })
  }
}

// Check response
if (response.success) {
  console.log("Site created:", response.data);
} else {
  console.error("Failed:", response.error.message);
}
```

### Example 3: Audit Log Query for Security Events

```javascript
{
  "workflowName": "Gluware - Audit API",
  "data": {
    "method": "GET",
    "startDate": new Date(Date.now() - 7*24*60*60*1000).toISOString(),
    "endDate": new Date().toISOString(),
    "action": "DELETE",
    "limit": "100"
  }
}
```

### Example 4: Detect Critical Config Drift

```javascript
{
  "workflowName": "Gluware - Config Drift API",
  "data": {
    "method": "GET",
    "severity": "critical",
    "status": "detected"
  }
}

// Process results
const criticalDrifts = response.data.filter(d => d.severity === 'critical');
if (criticalDrifts.length > 0) {
  // Send alert
  // Trigger remediation workflow
}
```

### Example 5: Onboard Multiple Devices

```javascript
const devices = [
  { ip: "10.0.1.10", template: "cisco-ios" },
  { ip: "10.0.1.11", template: "cisco-ios" },
  { ip: "10.0.1.12", template: "juniper-junos" }
];

for (const device of devices) {
  await executeWorkflow({
    "workflowName": "Gluware - Onboarding API",
    "data": {
      "method": "POST",
      "autoApprove": "true",
      "body": JSON.stringify({
        "deviceIp": device.ip,
        "credentials": {
          "username": "admin",
          "password": process.env.DEVICE_PASSWORD
        },
        "template": device.template
      })
    }
  });
}
```

## 🔄 Common Patterns

### Pattern 1: Poll for Job Completion

```javascript
// Start onboarding job
const startResponse = await executeWorkflow({
  workflowName: "Gluware - Onboarding API",
  data: {
    method: "POST",
    body: JSON.stringify({...})
  }
});

const jobId = startResponse.data.id;

// Poll for completion
let completed = false;
while (!completed) {
  await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
  
  const statusResponse = await executeWorkflow({
    workflowName: "Gluware - Onboarding API",
    data: {
      method: "GET",
      onboardingId: jobId
    }
  });
  
  if (['completed', 'failed'].includes(statusResponse.data.status)) {
    completed = true;
  }
}
```

### Pattern 2: Batch Operations with Error Handling

```javascript
const deviceIds = ['dev-1', 'dev-2', 'dev-3'];
const results = [];

for (const deviceId of deviceIds) {
  try {
    const response = await executeWorkflow({
      workflowName: "Gluware - Devices API",
      data: {
        method: "PUT",
        deviceId: deviceId,
        body: JSON.stringify({
          status: "maintenance"
        })
      }
    });
    
    results.push({
      deviceId,
      success: response.success,
      data: response.data
    });
  } catch (error) {
    results.push({
      deviceId,
      success: false,
      error: error.message
    });
  }
}

return results;
```

### Pattern 3: Cascading Operations

```javascript
// 1. Create site
const siteResponse = await executeWorkflow({
  workflowName: "Gluware - Sites API",
  data: {
    method: "POST",
    body: JSON.stringify({ name: "New Site" })
  }
});

const siteId = siteResponse.data.id;

// 2. Onboard devices to site
const devicesResponse = await executeWorkflow({
  workflowName: "Gluware - Onboarding API",
  data: {
    method: "POST",
    body: JSON.stringify({
      deviceIp: "10.0.1.50",
      siteId: siteId,
      ...
    })
  }
});

// 3. Apply policy to site
const policyResponse = await executeWorkflow({
  workflowName: "Gluware - Policy API",
  data: {
    method: "POST",
    body: JSON.stringify({
      name: "Site Security Policy",
      scope: "site",
      siteId: siteId,
      ...
    })
  }
});
```

## ⚠️ Error Handling

All workflows return a standardized response format:

### Success Response
```json
{
  "success": true,
  "method": "GET",
  "statusCode": 200,
  "data": { ... },
  "timestamp": "2025-01-31T12:00:00.000Z",
  "endpoint": "devices"
}
```

### Error Response
```json
{
  "success": false,
  "method": "POST",
  "error": {
    "message": "Device not found",
    "statusCode": 404,
    "details": "Device with ID 'dev-999' does not exist"
  },
  "timestamp": "2025-01-31T12:00:00.000Z",
  "endpoint": "devices"
}
```

### Handling Errors in Parent Workflow

```javascript
const response = await executeWorkflow({...});

if (!response.success) {
  // Log error
  console.error(`Error: ${response.error.message}`);
  
  // Send notification
  await sendAlert({
    severity: 'error',
    message: response.error.message,
    endpoint: response.endpoint
  });
  
  // Optionally retry or compensate
  if (response.error.statusCode === 429) { // Rate limit
    await new Promise(resolve => setTimeout(resolve, 60000));
    // Retry...
  }
}
```

## 🔍 Troubleshooting

### Issue: "Workflow not found"
**Solution:** Ensure the workflow is imported and the name matches exactly (including case)

### Issue: "Authentication failed"
**Solution:** 
- Check `GLUWARE_API_KEY` environment variable
- Verify API key is valid and not expired
- Ensure Bearer token format is correct

### Issue: "Connection timeout"
**Solution:**
- Check `GLUWARE_API_URL` is accessible
- Verify network connectivity
- Check firewall rules
- Increase timeout in HTTP Request node settings

### Issue: "Validation failed"
**Solution:** 
- Check input parameters match expected format
- Review validation error details in response
- Ensure required fields are provided

### Issue: "Rate limit exceeded"
**Solution:**
- Implement exponential backoff
- Add delays between batch operations
- Use pagination for large datasets

## 📚 Additional Resources

- [Gluware API Documentation](https://docs.gluware.com/api)
- [n8n Documentation](https://docs.n8n.io)
- [n8n Community Forum](https://community.n8n.io)

## 🤝 Contributing

To add new endpoints or improve existing workflows:

1. Follow the existing workflow structure
2. Include comprehensive validation
3. Standardize response formatting
4. Add detailed node descriptions
5. Update this README

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

For issues or questions:
- Open an issue in this repository
- Contact Gluware support for API-specific questions
- Visit n8n community for workflow-related questions
