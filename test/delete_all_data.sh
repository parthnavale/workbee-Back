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
    echo "Deleting $endpoint/$id"
    curl -s -X DELETE -H "$AUTH_HEADER" "$BASE_URL/$endpoint/$id"
  done
}

echo "Starting data deletion process..."

# 1. Delete all job applications
delete_all "applications"

# 2. Delete all jobs
delete_all "jobs"

# 3. Delete all business owners
delete_all "business-owners"

# 4. Delete all workers
delete_all "workers"

# 5. Delete all users
delete_all "users"

echo "Data deletion complete." 