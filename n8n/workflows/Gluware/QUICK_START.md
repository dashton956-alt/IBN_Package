# Gluware API n8n Workflows - Quick Start Guide

## 🚀 What You Got

This package includes **10 production-ready n8n workflows** for the Gluware API:

### Core API Workflows (9)
1. **gluware_devices_workflow.json** - Device inventory management
2. **gluware_sites_workflow.json** - Site hierarchy management
3. **gluware_audit_workflow.json** - Audit log queries
4. **gluware_lifecycle_workflow.json** - Device lifecycle automation
5. **gluware_topology_workflow.json** - Network topology discovery
6. **gluware_config_drift_workflow.json** - Configuration drift detection
7. **gluware_cmdb_workflow.json** - CMDB operations
8. **gluware_policy_workflow.json** - Policy management
9. **gluware_onboarding_workflow.json** - Device onboarding

### Example Orchestrator (1)
10. **gluware_orchestrator_example.json** - Complete working example showing how to use the sub-workflows

## ⚡ Quick Setup (5 Minutes)

### Step 1: Set Environment Variables
```bash
export GLUWARE_API_URL="https://your-gluware-instance.com/api/v1"
export GLUWARE_API_KEY="your_api_key_here"
```

### Step 2: Import Workflows
In n8n interface:
1. Go to Workflows
2. Click "Add Workflow" → "Import from File"
3. Import all 10 JSON files
4. Save each workflow

### Step 3: Test Individual Workflow
1. Open "Gluware - Devices API"
2. Click "Execute Workflow"
3. Check the output

### Step 4: Use in Your Workflows
Add "Execute Workflow" node in your workflow:
```javascript
{
  "workflowName": "Gluware - Devices API",
  "data": {
    "method": "GET"
  }
}
```

## 📦 What's Included

### Each Workflow Has:
✅ Input validation
✅ Error handling
✅ Standardized response format
✅ Detailed node descriptions
✅ Authentication setup
✅ Query parameter building
✅ Response formatting

### Features:
- **Modular Design** - Each endpoint is a separate, reusable workflow
- **Error Handling** - Automatic validation and error responses
- **Standardized** - Consistent input/output format across all workflows
- **Documented** - Every node has clear descriptions
- **Production Ready** - Battle-tested patterns and best practices

## 🎯 Common Use Cases

### 1. Daily Drift Check (see orchestrator example)
- Get all devices
- Check config drift on each
- Alert on any drift detected
- Log to audit system

### 2. Mass Device Update
```javascript
const devices = ['dev-1', 'dev-2', 'dev-3'];
for (const id of devices) {
  await executeWorkflow({
    workflowName: "Gluware - Devices API",
    data: {
      method: "PUT",
      deviceId: id,
      body: JSON.stringify({ status: "maintenance" })
    }
  });
}
```

### 3. Site Creation & Device Onboarding
```javascript
// Create site
const site = await executeWorkflow({
  workflowName: "Gluware - Sites API",
  data: {
    method: "POST",
    body: JSON.stringify({ name: "New Office" })
  }
});

// Onboard device to site
await executeWorkflow({
  workflowName: "Gluware - Onboarding API",
  data: {
    method: "POST",
    body: JSON.stringify({
      deviceIp: "10.0.1.50",
      siteId: site.data.id,
      credentials: {...}
    })
  }
});
```

## 📊 Response Format

All workflows return standardized responses:

**Success:**
```json
{
  "success": true,
  "method": "GET",
  "statusCode": 200,
  "data": { ... },
  "timestamp": "2025-01-31T12:00:00.000Z"
}
```

**Error:**
```json
{
  "success": false,
  "error": {
    "message": "Device not found",
    "statusCode": 404,
    "details": "..."
  },
  "timestamp": "2025-01-31T12:00:00.000Z"
}
```

## 🔧 Customization

### Change Base URL
Update environment variable:
```bash
GLUWARE_API_URL=https://your-instance.com/api/v1
```

### Add Custom Headers
Edit HTTP Request nodes to add headers:
```json
{
  "name": "X-Custom-Header",
  "value": "custom-value"
}
```

### Adjust Timeouts
In HTTP Request nodes, under Options → Timeout:
- Default: 30000ms (30 seconds)
- Increase for long-running operations

## 🐛 Troubleshooting

### "Workflow not found"
→ Ensure workflow is imported and name matches exactly

### "Authentication failed"
→ Check GLUWARE_API_KEY environment variable

### "Connection timeout"
→ Verify GLUWARE_API_URL is accessible

### "Validation failed"
→ Check input parameters match expected format (see README.md)

## 📚 Documentation Files

- **README.md** - Complete documentation with all endpoints, parameters, and examples
- **QUICK_START.md** - This file
- **gluware_orchestrator_example.json** - Working example of orchestration

## 🎓 Learning Path

1. **Start Here**: Import all workflows
2. **Test Individual**: Try "Gluware - Devices API" with GET method
3. **Study Example**: Review the orchestrator example
4. **Build Your Own**: Create a workflow that calls multiple sub-workflows
5. **Production**: Add error handling, notifications, and logging

## 💡 Pro Tips

1. **Batch Operations**: Use Split In Batches node to avoid rate limits
2. **Error Handling**: Always check `response.success` before using data
3. **Logging**: Add Function nodes to log important operations
4. **Testing**: Test each workflow individually before orchestrating
5. **Monitoring**: Set up notifications for failed workflows

## 🆘 Need Help?

- Check **README.md** for detailed documentation
- Review **gluware_orchestrator_example.json** for working example
- Open workflow and read node descriptions
- Contact Gluware support for API questions
- Visit n8n community for workflow questions

## 🚦 Next Steps

1. ✅ Import all workflows
2. ✅ Set environment variables
3. ✅ Test Devices API workflow
4. ✅ Review orchestrator example
5. ✅ Build your first orchestration workflow

**You're ready to go! Start with the orchestrator example and customize it for your needs.**

---

**Note**: These workflows are designed to be production-ready, but always test thoroughly in a non-production environment first.
