#!/usr/bin/env bash
set -euo pipefail

# Initializes and unseals a Vault server and writes keys to vault/init/keys.json
# Usage: ./init_vault.sh

DATA_DIR="$(pwd)/data"
INIT_FILE="$(pwd)/init/keys.json"

if [ -f "$INIT_FILE" ]; then
  echo "Init file already exists at $INIT_FILE";
  cat "$INIT_FILE";
  exit 0
fi

export VAULT_ADDR='http://127.0.0.1:8200'

# Wait for Vault to be ready
for i in {1..30}; do
  if curl -s $VAULT_ADDR/v1/sys/health | grep -q 'initialized'; then
    break
  fi
  echo "Waiting for Vault to be ready... ($i)"
  sleep 1
done

# Initialize
echo "Initializing Vault..."
RESP=$(curl -s --request PUT --data '{"secret_shares":1,"secret_threshold":1}' $VAULT_ADDR/v1/sys/init)
echo "$RESP" > "$INIT_FILE"

# Extract keys and root token
ROOT_TOKEN=$(echo "$RESP" | jq -r '.root_token')
UNSEAL_KEY=$(echo "$RESP" | jq -r '.keys_base64[0]')

# Unseal
echo "Unsealing Vault..."
curl -s --request PUT --data "{\"key\": \"$UNSEAL_KEY\"}" $VAULT_ADDR/v1/sys/unseal >/dev/null

# Save two files: keys.json and env file
cat > "$INIT_FILE" <<EOF
{"root_token":"$ROOT_TOKEN","unseal_key":"$UNSEAL_KEY"}
EOF

cat > ./init/vault.env <<EOF
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='$ROOT_TOKEN'
EOF

echo "Vault initialized. Keys written to $INIT_FILE and vault.env"
