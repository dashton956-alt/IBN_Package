#!/bin/bash
# get_secret.sh
# Usage: get_secret.sh <secret_path> <field>
SECRET_PATH="$1"
FIELD="$2"
if [ -z "$SECRET_PATH" ] || [ -z "$FIELD" ]; then
  echo "Usage: $0 secret_path field"
  exit 2
fi
if [ -z "$VAULT_ADDR" ] || [ -z "$VAULT_TOKEN" ]; then
  echo "VAULT_ADDR and VAULT_TOKEN must be set in environment"
  exit 2
fi
curl -s --header "X-Vault-Token: $VAULT_TOKEN" "$VAULT_ADDR/v1/$SECRET_PATH" | jq -r ".data.data.$FIELD"
