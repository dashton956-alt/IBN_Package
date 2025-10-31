NetBox MCP Docker image
=======================

This folder contains a Dockerfile to build a container image for the
`netbox-mcp-server` project. The container runs the MCP HTTP transport by
default and is configured using environment variables.

Build
-----

From this directory run:

```bash
docker build -t netbox-mcp-server:local .
```

Run (HTTP transport)
---------------------

Provide your NetBox endpoint and token. If you want AnythingLLM to access this
MCP server, make sure the container is reachable from AnythingLLM and point the
LLM at the server URL (e.g. http://host:8000/mcp).

```bash
docker run -d \
  --name netbox-mcp \
  -e NETBOX_URL="https://netbox.example.com/" \
  -e NETBOX_TOKEN="<your_token>" \
  -e TRANSPORT=http \
  -e HOST=0.0.0.0 \
  -e PORT=8002 \
  -p 8002:8002 \
  netbox-mcp-server:local
```

Then configure AnythingLLM (or your LLM client) to use the MCP server at
`http://<host>:8002/mcp`.

Notes
-----
- You can also run the server with `TRANSPORT=stdio` if you want to integrate
  it via stdio instead of HTTP (see the project's README for examples).
- Override `CMD` or pass different CLI args at runtime if you need custom
  behavior.
