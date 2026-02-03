#!/usr/bin/env bash
# Trigger a manual deploy on Render via the Render REST API.
# Usage:
#   export RENDER_API_KEY=\"<your_render_api_key>\"
#   export RENDER_SERVICE_ID=\"<your_service_id>\"
#   ./render_trigger.sh

if [ -z "$RENDER_API_KEY" ] || [ -z "$RENDER_SERVICE_ID" ]; then
  echo "RENDER_API_KEY and RENDER_SERVICE_ID environment variables must be set"
  exit 1
fi

echo "Triggering Render deploy for service: $RENDER_SERVICE_ID"

curl -s -X POST \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
  -d '{"clearCache": true}' \
  | jq '.'

exit 0
