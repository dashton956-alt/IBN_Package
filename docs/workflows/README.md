n8n prototype for aichatops

Files:
- docker-compose.yml  -> n8n service on port 5678
- flow-aichatops.json -> workflow to import: webhook -> LocalAI + NetBox -> aggregate -> respond

Usage:
1) Configure env in `docker-compose.yml` or override when running (set `N8N_LOCALAI_URL`, `N8N_NETBOX_URL`, `N8N_NETBOX_TOKEN`).

2) Start n8n:

```bash
cd /home/dan/ibnaas/n8n
docker compose up -d
```

3) Import the flow (the automation will also be copied and imported by the helper script we provide):

```bash
# copy and import into running container
docker cp flow-aichatops.json st2-docker-st2api-1:/tmp || true
# (we provide the import command below which the agent will run)
```

4) Call the webhook to test (example):

```bash
curl -s -X POST http://localhost:5678/webhook/aichatops \
  -H "Content-Type: application/json" \
  -d '{"question":"show me 5 devices"}' | jq
```

Notes:
- LocalAI API paths vary by model; set `N8N_LOCALAI_URL` so the flow posts to the correct endpoint. The flow sends JSON body {"input": "<question>"} by default — adjust `bodyParametersJson` in `flow-aichatops.json` for your LocalAI installation.
- For production, enable auth on n8n UI and secure webhooks.
