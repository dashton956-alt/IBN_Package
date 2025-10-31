# Gluware API Endpoints - Quick Reference Card

## 🔌 All Endpoints at a Glance

| Endpoint | Methods | Primary Use | Key Parameters |
|----------|---------|-------------|----------------|
| `/devices` | GET, POST, PUT, DELETE | Device inventory management | deviceId, filters |
| `/sites` | GET, POST, PUT, DELETE | Site hierarchy & organization | siteId, includeDevices |
| `/audit` | GET | Compliance & activity tracking | startDate, endDate, action |
| `/lifecycle` | GET, POST, PUT, DELETE | Device lifecycle automation | lifecycleId, stage, status |
| `/topology` | GET | Network topology discovery | siteId, deviceId, depth |
| `/config-drift` | GET, POST, PUT | Config drift detection | deviceId, severity, status |
| `/cmdb` | GET, POST, PUT, DELETE | Configuration item mgmt | ciType, search, relationships |
| `/policy` | GET, POST, PUT, DELETE | Network policy automation | policyType, scope, validate |
| `/onboarding` | GET, POST, PUT, DELETE | Zero-touch provisioning | deviceIp, template, credentials |

## 📋 Parameter Reference

### Common Parameters
- `method` - HTTP method (GET/POST/PUT/DELETE)
- `body` - JSON body for write operations
- `filters` - Query string parameters

### Device Operations
```javascript
// Get all devices
{ method: "GET" }

// Get specific device
{ method: "GET", deviceId: "dev-123" }

// Filter devices
{ method: "GET", filters: "site=NYC&status=active" }

// Create device
{ method: "POST", body: "{...}" }

// Update device
{ method: "PUT", deviceId: "dev-123", body: "{...}" }

// Delete device
{ method: "DELETE", deviceId: "dev-123" }
```

### Site Operations
```javascript
// Get all sites with devices
{ method: "GET", includeDevices: "true" }

// Get specific site
{ method: "GET", siteId: "site-123" }

// Create site
{ method: "POST", body: "{\"name\":\"NYC Office\",\"region\":\"NA\"}" }
```

### Audit Queries
```javascript
// Last 7 days of changes
{ 
  method: "GET",
  startDate: "2025-01-24T00:00:00Z",
  endDate: "2025-01-31T23:59:59Z"
}

// User activity
{ method: "GET", userId: "admin", action: "UPDATE" }

// With pagination
{ method: "GET", limit: "50", offset: "100" }
```

### Lifecycle Management
```javascript
// Get lifecycle status
{ method: "GET", deviceId: "dev-123" }

// Start provisioning
{ 
  method: "POST",
  body: "{\"deviceId\":\"dev-123\",\"stage\":\"provisioning\"}"
}

// Update stage
{
  method: "PUT",
  lifecycleId: "lc-456",
  body: "{\"stage\":\"production\",\"status\":\"completed\"}"
}
```

### Topology Discovery
```javascript
// Full topology
{ method: "GET", depth: "3", includeLinks: "true" }

// Site topology
{ method: "GET", siteId: "site-123", format: "json" }

// Device-centric topology
{ method: "GET", deviceId: "dev-123", depth: "2" }
```

### Config Drift Detection
```javascript
// Get critical drifts
{ method: "GET", severity: "critical", status: "detected" }

// Trigger drift scan
{ method: "POST", body: "{\"deviceId\":\"dev-123\"}" }

// Acknowledge drift
{
  method: "PUT",
  driftId: "drift-789",
  body: "{\"status\":\"acknowledged\"}"
}
```

### CMDB Operations
```javascript
// Get all devices with relationships
{ method: "GET", ciType: "device", relationships: "true" }

// Search CIs
{ method: "GET", search: "router", ciType: "device" }

// Get specific attributes
{ method: "GET", attributes: "name,ipAddress,status" }
```

### Policy Management
```javascript
// Get active policies
{ method: "GET", status: "active" }

// Create & validate policy
{
  method: "POST",
  validate: "true",
  body: "{\"name\":\"QoS\",\"policyType\":\"qos\",\"scope\":\"global\"}"
}

// Get policies by type
{ method: "GET", policyType: "security", scope: "site" }
```

### Device Onboarding
```javascript
// Start onboarding
{
  method: "POST",
  autoApprove: "true",
  body: "{\"deviceIp\":\"10.0.1.50\",\"credentials\":{...},\"template\":\"cisco-ios\"}"
}

// Check status
{ method: "GET", onboardingId: "ob-123" }

// Approve step
{
  method: "PUT",
  onboardingId: "ob-123",
  body: "{\"action\":\"approve\"}"
}
```

## 🎯 Common Patterns

### Pattern: List → Filter → Update
```javascript
// 1. Get all items
{ method: "GET" }

// 2. Filter in code
const filtered = response.data.filter(...)

// 3. Update each
for (const item of filtered) {
  { method: "PUT", id: item.id, body: "{...}" }
}
```

### Pattern: Create → Validate → Execute
```javascript
// 1. Create with validation
{ method: "POST", validate: "true", body: "{...}" }

// 2. Check validation
if (response.success && response.validated) {
  // 3. Execute
  ...
}
```

### Pattern: Poll for Completion
```javascript
// 1. Start job
{ method: "POST", body: "{...}" }

// 2. Poll status
while (status !== "completed") {
  { method: "GET", jobId: id }
  await sleep(5000)
}
```

## 📊 Response Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process data |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Check input parameters |
| 401 | Unauthorized | Check API key |
| 404 | Not Found | Resource doesn't exist |
| 429 | Rate Limited | Implement backoff |
| 500 | Server Error | Retry or contact support |

## 🔒 Authentication

All endpoints require Bearer token authentication:

```
Authorization: Bearer YOUR_API_KEY
```

Set via environment variable:
```bash
export GLUWARE_API_KEY="your_key_here"
```

## ⚡ Rate Limiting

**Best Practices:**
- Batch operations: Use delays between calls
- Large datasets: Use pagination
- Long operations: Poll with exponential backoff
- Failed requests: Implement retry with backoff

**Example:**
```javascript
// Batch with delay
for (const item of items) {
  await executeWorkflow({...})
  await sleep(2000) // 2 second delay
}
```

## 🎓 Quick Lookup

**Need to...**
- Manage devices? → `/devices`
- Organize sites? → `/sites`
- Track changes? → `/audit`
- Automate lifecycle? → `/lifecycle`
- View topology? → `/topology`
- Check config compliance? → `/config-drift`
- Manage inventory? → `/cmdb`
- Apply policies? → `/policy`
- Add new devices? → `/onboarding`

## 📝 Notes

1. All workflows validate inputs before API calls
2. Responses are standardized across all endpoints
3. Error details include validation messages
4. Timestamps are ISO 8601 format
5. All dates require timezone (use UTC recommended)

## 🚀 Next Steps

1. Import workflows into n8n
2. Set environment variables
3. Test individual endpoints
4. Build orchestration workflows
5. Add monitoring & alerts

---

**For complete examples and detailed documentation, see README.md**
