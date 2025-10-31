#!/bin/bash
# Test NetBox API connectivity from AnythingLLM container

echo "=== Testing NetBox API Connectivity ==="
echo ""

# Check environment variables
echo "1. Environment Variables:"
docker exec chatops-anythingllm bash -c 'echo "NETBOX_URL=$NETBOX_URL"; echo "NETBOX_TOKEN=${NETBOX_TOKEN:0:20}..."'
echo ""

# Test API connectivity
echo "2. Testing API Connection:"
docker exec chatops-anythingllm curl -s -w "\nHTTP Status: %{http_code}\n" \
  -H "Authorization: Token $NETBOX_TOKEN" \
  -H "Accept: application/json" \
  http://host.docker.internal:8000/api/dcim/devices/ \
  | jq -r 'if .results then "✅ SUCCESS - Found \(.count) devices" else "❌ FAILED - \(.detail // "Unknown error")" end' 2>/dev/null || echo "❌ FAILED - Could not parse response"
echo ""

# Test skills are loaded
echo "3. Agent Skills Files:"
docker exec chatops-anythingllm ls -lh /app/server/storage/plugins/agent-skills/ | grep -E "(netbox|plugin)"
echo ""

# Test LocalAI connectivity
echo "4. LocalAI Connection:"
docker exec chatops-anythingllm curl -s http://localai:8080/v1/models | jq -r '.data[] | select(.id=="gpt-4o") | "✅ Model \(.id) available"' 2>/dev/null || echo "❌ gpt-4o not found"
echo ""

echo "=== Test Complete ==="
echo ""
echo "Next steps:"
echo "1. Open http://localhost:3001"
echo "2. Create workspace 'Intent-Based Networking'"
echo "3. Enable Agent Mode in workspace settings"
echo "4. Test with: 'Show me all devices in NetBox'"
