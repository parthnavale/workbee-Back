#!/bin/bash

# Base URL of your API
BASE_URL="https://myworkbee.duckdns.org"

# If your API requires authentication, set your token here:
# AUTH_HEADER="Authorization: Bearer <your_token>"
AUTH_HEADER="Content-Type: application/json"

# Function to delete all items from a given endpoint
# Usage: delete_all "endpoint_name"
delete_all() {
  endpoint=$1
  echo "Fetching all $endpoint..."
  # Fetch all items and extract their IDs
  ids=$(curl -s -H "$AUTH_HEADER" "$BASE_URL/$endpoint/" | grep -o '"id":[0-9]*' | cut -d: -f2)
  for id in $ids; do
    url="$BASE_URL/$endpoint/$id"
    echo "-----------------------------"
    echo "[REQUEST] DELETE $url"
    echo "Request body: (none)"
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X DELETE -H "$AUTH_HEADER" "$url")
    body=$(echo "$response" | sed -e '/HTTP_STATUS:/d')
    status=$(echo "$response" | grep HTTP_STATUS | cut -d':' -f2)
    echo "[RESPONSE] Status code: $status"
    echo "[RESPONSE] Body: $body"
    echo "-----------------------------"
  done
}

echo "Starting data deletion process..."

delete_all "applications"
delete_all "jobs"
delete_all "business-owners"
delete_all "workers"
delete_all "users"

echo "Data deletion complete." 