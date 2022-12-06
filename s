#!/usr/bin/env sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

if [ -f .env ]; then
  # Load Environment Variables
  export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
  echo "Missing .env file"
  exit 0
fi

echo "Syncing to host: $HOST"
rsync -avh "$SCRIPT_DIR" "$HOST":~/
