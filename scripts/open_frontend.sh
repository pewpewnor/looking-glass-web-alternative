#!/bin/bash

# Open the application in the default browser
echo "Opening Looking Glass Web Alternative in the browser..."
echo ""
echo "Make sure Flask backend is running! Use start_server.sh first"
echo ""

APP_URL="http://localhost:5001"

# Try to open with default browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$APP_URL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$APP_URL"
else
    # Windows (Git Bash)
    start "$APP_URL"
fi

echo "Frontend opened at: $APP_URL"
echo "Backend should be running on: http://localhost:5001"
