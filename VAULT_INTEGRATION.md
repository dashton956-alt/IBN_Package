# HashiCorp Vault integration for ST2 (POC)

This document explains how to run a small Vault instance for the POC and how to fetch secrets from Vault within StackStorm workflows/actions so pack configs do not contain plaintext tokens.

WARNING: For production, use a proper HA Vault cluster with storage backend and secure unseal. The instructions below are POC-friendly.

## 1) Quick Vault (dev) startup (POC only)
Run Vault in dev mode (single-process) — good for POC but not secure for production.

```bash
# Run Vault dev server (bind to 127.0.0.1 or internal network)
docker run --name vault-dev -e 'VAULT_DEV_ROOT_TOKEN_ID=devroot' -p 8200:8200 --cap-add=IPC_LOCK -d hashicorp/vault:1.13.3

# Export token locally
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='devroot'
```

## 2) Store NetBox token in Vault

```bash
vault kv put secret/netbox api_token=0039616ab84275a19fbca20ee3985bcc1ade9728
```

## 3) Example: Fetch secret from Vault in a shell action
Create a StackStorm action that calls Vault HTTP API to retrieve the secret at runtime.

Example curl call (inside a container with `VAULT_ADDR` and `VAULT_TOKEN` exported):

```bash
curl -s --header "X-Vault-Token: $VAULT_TOKEN" $VAULT_ADDR/v1/secret/data/netbox | jq -r '.data.data.api_token'
```

## 4) Example ST2 action (shell) to fetch secret
- Create a pack `packs.dev/vault` with a simple shell action `get_secret.sh` that accepts a `key` parameter and prints the secret value.
- Example action will call the Vault HTTP API as above and echo the token.

## 5) Integrating into NetBox pack workflows
- Replace pack config plaintext token usage by adding a small wrapper action that obtains token from Vault and injects into subsequent actions' parameters.
- Alternatively, implement an ST2 sensor that pulls secrets as needed and caches them in memory with a short TTL.

## 6) Secure notes
- Never use Vault dev mode beyond a local POC.
- For production: use TLS, secure storage backend, auto-unseal (KMS), and RBAC policies limiting access.

## 7) Next: example pack scaffold
I created a small example pack under `packs.dev/vault` showing how to fetch secrets from Vault. Use it as a template to wire secret fetching into the `netbox` and `gluware` packs.
