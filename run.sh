#!/bin/bash

# Navigate to FastAPI backend and run it
cd app
pip install -r requirements.txt
echo "Starting FastAPI backend..."
uvicorn main:app --reload --port 8000 & 
FASTAPI_PID=$!

# Navigate to Vue frontend and run it
cd ../vue
echo "Starting Vue frontend..."
npm install
npm run dev &
VUE_PID=$!

# Function to stop both on script exit
trap "kill $VUE_PID $FASTAPI_PID" EXIT

# Wait for both processes
wait
