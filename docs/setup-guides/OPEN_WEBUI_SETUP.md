# Open WebUI + NetBox ChatOps Setup Guide

## ✅ Status: Open WebUI is Running!

Access your ChatOps interface at: **http://localhost:3001**

---

## Initial Setup Steps

### 1. **Access Open WebUI**
- Open your browser and go to: http://localhost:3001
- Since auth is disabled (`WEBUI_AUTH=false`), you'll be automatically logged in

### 2. **Verify LocalAI Connection**
- The UI should automatically detect LocalAI at `http://localai:8080/v1`
- Model `gpt-4o` should be available in the model selector
- If not visible, go to **Settings** → **Connections** → verify OpenAI API settings

### 3. **Add NetBox Function Tool**

The NetBox query function has been created at:
```
/home/dan/ibnaas/open-webui/functions/netbox_query.py
```

**To activate it in Open WebUI:**

1. Click your profile icon (top right) → **Admin Settings**
2. Go to **Functions** section in the sidebar
3. Click **+ Add Function** 
4. Upload the file: `/home/dan/ibnaas/open-webui/functions/netbox_query.py`
5. Enable the function and test it

**Available NetBox Functions:**
- `query_devices` - Find devices with filters (name, site, type, role)
- `query_interfaces` - List interfaces by device or name
- `query_vlans` - Query VLANs by ID, name, or site
- `query_ip_addresses` - Find IP addresses
- `query_prefixes` - List IP prefixes/subnets

### 4. **Test NetBox Integration**

Once the function is loaded, try these queries in chat:

```
Show me all devices in NetBox
```

```
Find devices with "spine" in the name
```

```
What VLANs are configured?
```

```
List interfaces on spine01
```

---

## Environment Variables

Open WebUI is configured with these NetBox settings:
```bash
NETBOX_URL=http://netbox-docker-netbox-1:8000
NETBOX_TOKEN=b6ec5fa9fb961fe932dc7a396058f93afbafad9e
```

These are automatically available to the NetBox function tool.

---

## Key Features vs AnythingLLM

✅ **Better function calling** - Native Python function support  
✅ **Simpler architecture** - No MCP complexity  
✅ **More stable streaming** - Fewer timeout errors  
✅ **Active development** - Regular updates and bug fixes  
✅ **Better UI** - Cleaner, more intuitive interface  

---

## Troubleshooting

### Function Not Working?
1. Check if function is enabled in Admin → Functions
2. Verify NetBox environment variables: 
   ```bash
   docker exec chatops-open-webui env | grep NETBOX
   ```
3. Test NetBox API manually:
   ```bash
   docker exec chatops-open-webui curl -H "Authorization: Token b6ec5fa9fb961fe932dc7a396058f93afbafad9e" http://netbox-docker-netbox-1:8000/api/dcim/devices/
   ```

### Model Not Showing?
1. Go to Settings → Connections
2. Verify OpenAI API Base URL: `http://localai:8080/v1`
3. Check LocalAI is running: `docker ps | grep localai`

### Container Issues?
```bash
# View logs
docker logs -f chatops-open-webui

# Restart container
docker compose -f docker-compose.chatops.yml restart open-webui
```

---

## Next Steps

1. ✅ Access http://localhost:3001
2. ⏳ Upload and enable NetBox function
3. ⏳ Test device queries
4. ⏳ Add more advanced functions (updates, VLAN creation, etc.)
5. ⏳ Integrate approval workflows with StackStorm

---

## Architecture

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────┐
│   Open WebUI    │─────▶│   LocalAI    │─────▶│   gpt-4o    │
│  (port 3001)    │      │ (port 8080)  │      │    Model    │
└────────┬────────┘      └──────────────┘      └─────────────┘
         │
         │ Function Calls
         │
         ▼
┌─────────────────┐
│  NetBox API     │
│  (REST API)     │
│  15 devices     │
└─────────────────┘
```

---

**Ready to test!** Open http://localhost:3001 and start querying your network inventory! 🚀
