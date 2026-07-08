#!/bin/bash
curl --request POST http://127.0.0.1:5000/api/timeline_post -d 'name=Test&email=test@mlh.io&content=This is a test!'
response=$(curl http://127.0.0.1:5000/api/timeline_post)

if echo "$response" | grep -q "This is a test!"; then
  echo "POST request successful"
else
  echo "POST request failed"
  exit 1
fi