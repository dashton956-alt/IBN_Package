# Open WebUI Tools Troubleshooting Guide

## Current Issue
The NetBox function is uploaded and loaded by Open WebUI, but it's not being called when you ask questions. The logs show `'tool_ids': None`, which means **the tool is not enabled for your chat session**.

## Solution: Enable Tools in Open WebUI

### Method 1: Enable Tools in Chat Interface (RECOMMENDED)

1. **Open your chat in Open WebUI** (http://localhost:3001)

2. **Look at the top of the chat window** - you should see:
   - Model selector showing "gpt-4o"
   - A settings/gear icon or tools icon

3. **Click the model dropdown or gear icon**

4. **Look for "Tools" or "Functions" section** and:
   - ✅ Check/Enable "NetBox Network Query Tool"
   - ✅ Make sure it's toggled ON (blue/green toggle)

5. **Start a NEW chat** after enabling (important!)

### Method 2: Check Admin Settings

1. Go to **Settings** (gear icon in bottom left)
2. Navigate to **Admin Panel** → **Tools** (or **Functions**)
3. Find **"NetBox Network Query Tool"**
4. Make sure it's:
   - ✅ **Active/Enabled** (toggle ON)
   - ✅ **Global** (if you want it available for all chats)
5. Click **Save**

### Method 3: Enable in Model Configuration

1. Go to **Settings** → **Models**
2. Find **"gpt-4o"** model
3. Click to edit/configure
4. Look for **"Tools"** or **"Function Calling"** section
5. Enable **"NetBox Network Query Tool"**
6. Save changes

## Verification Steps

### Step 1: Check if Tool is Loaded
Run this command to verify the function is active:
```bash
docker logs chatops-open-webui 2>&1 | grep -i "function_netbox" | tail -5
```

You should see: `inlet:function_netbox_fuction2`

### Step 2: Test with a New Chat
1. **Start a completely NEW chat** (important!)
2. **Before typing**, verify the tool is enabled (should show a checkmark or badge)
3. Type: **"Show me all devices in NetBox"**
4. Watch the response - it should:
   - Show a loading indicator
   - Call the function (you might see "Using NetBox Network Query Tool")
   - Return actual device data (15 devices)

### Step 3: Check Logs During Test
In another terminal, watch the logs:
```bash
docker logs -f chatops-open-webui 2>&1 | grep -E "tool_ids|function|netbox"
```

**BEFORE enabling tools**, you'll see:
```
'tool_ids': None
```

**AFTER enabling tools**, you should see:
```
'tool_ids': ['function_netbox_fuction2']
```

## Common Issues

### Issue 1: "Tool not showing in UI"
**Solution:** The function might need to be re-uploaded or reactivated:
1. Go to Admin → Functions
2. Find "NetBox Network Query Tool"
3. Click Edit
4. Click Save (even without changes)
5. Toggle it OFF then ON again

### Issue 2: "Tool is enabled but still not being called"
**Solution:** Add a system prompt to guide the AI:
1. Go to **Settings** → **Interface** → **System Prompt**
2. Add this:
```
You are a network operations assistant with access to NetBox inventory tools.

When users ask about devices, interfaces, VLANs, IP addresses, or network information, you MUST use the available NetBox query tools to retrieve accurate data.

Available tools:
- query_devices: Get device information
- query_interfaces: Get interface details
- query_vlans: Get VLAN information
- query_ip_addresses: Get IP address details
- query_prefixes: Get IP prefix information

Always use these tools instead of making assumptions or explaining how to query the API manually.
```

### Issue 3: "Getting 'Not authenticated' errors"
Even though `WEBUI_AUTH=false` is set, you might need to:
1. Create an admin account on first access
2. Log in once
3. Then the tools should work

### Issue 4: "Function returns errors"
Check environment variables:
```bash
docker exec chatops-open-webui env | grep NETBOX
```

Should show:
```
NETBOX_URL=http://netbox-docker-netbox-1:8000
NETBOX_TOKEN=b6ec5fa9fb961fe932dc7a396058f93afbafad9e
```

### Issue 5: "Can't find Tools section in UI"
Open WebUI version might be different. Try:
- Click the **+ button** next to the message input
- Look for **"Tools"**, **"Functions"**, or **"Plugins"**
- Check the **hamburger menu** (three lines) in the top left

## Test Queries

Once tools are enabled, try these:

1. **Basic query:**
   ```
   Show me all devices in NetBox
   ```
   Expected: List of 15 devices with details

2. **Filtered query:**
   ```
   Find devices with "spine" in the name
   ```
   Expected: Arista spine switches

3. **Interface query:**
   ```
   Show me interfaces on spine01
   ```
   Expected: List of interfaces on spine01

4. **VLAN query:**
   ```
   List all VLANs
   ```
   Expected: VLAN inventory

## Success Indicators

✅ **Tool is working when you see:**
- Function name appears in chat (e.g., "Using NetBox Network Query Tool")
- Actual device data returned (not explanations)
- Logs show `'tool_ids': ['function_netbox_fuction2']`
- Response includes formatted device information

❌ **Tool is NOT working when you see:**
- AI explains how to use the API
- Response shows Python code examples
- Logs show `'tool_ids': None`
- Generic explanations instead of actual data

## Next Steps After Tool Works

1. ✅ Test all 6 NetBox query functions
2. ✅ Upload StackStorm function (stackstorm_function.py)
3. ✅ Create and upload Batfish function
4. ✅ Move to Phase 2: Glueware Integration

## Need More Help?

If you still can't find where to enable tools:
1. Take a screenshot of your Open WebUI interface
2. Share the output of: `docker logs chatops-open-webui --tail=20`
3. Check if Open WebUI needs to be updated: `docker pull ghcr.io/open-webui/open-webui:main`
