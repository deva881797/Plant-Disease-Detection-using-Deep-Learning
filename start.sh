#!/bin/bash
# Start nginx reverse proxy with Streamlit and FastAPI backends

# Create nginx log directory
mkdir -p /var/log/nginx

# Start FastAPI in background (internal port 8000)
uvicorn api:app --host 127.0.0.1 --port 8000 &

# Start Streamlit in background (internal port 8502)
streamlit run app.py --server.port=8502 --server.address=127.0.0.1 --server.headless=true &

# Wait for services to start
sleep 3

# Start nginx in foreground (exposed port 8501)
nginx -g "daemon off;"
