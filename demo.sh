#!/usr/bin/env bash
# Hit the Service many times and count how often each pod answered.
# A roughly even split across the three pod names is round-robin balancing.
#
# Usage: ./demo.sh [url] [count]   (default: http://localhost:30080 , 30 requests)
set -euo pipefail

URL="${1:-http://localhost:30080}"
COUNT="${2:-30}"

echo "Sending $COUNT requests to $URL"
for _ in $(seq "$COUNT"); do
  # Extract just the "pod" field from the JSON response.
  curl -s "$URL" | sed -n 's/.*"pod":"\([^"]*\)".*/\1/p'
done | sort | uniq -c | sort -rn
