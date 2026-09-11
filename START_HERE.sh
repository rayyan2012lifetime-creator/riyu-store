#!/bin/bash
# Pakistani AI Dropshipping Gateway - Auto-Start (Mac/Linux)
# Run: chmod +x START_HERE.sh && ./START_HERE.sh

echo ""
echo "======================================"
echo "🛍️  RIYU STORE"
echo "Pakistani AI Dropshipping Gateway"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Creating .env from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created!"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env and add your OPENAI_API_KEY"
        echo "Then run this script again."
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    echo "📥 Please install Python from https://www.python.org/"
    exit 1
fi

echo "🔍 Checking dependencies..."
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    python3 -m pip install -q -r requirements.txt
    echo "✅ Dependencies installed!"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "======================================"
echo "🚀 Starting Services..."
echo "======================================"
echo ""

# Create logs directory
mkdir -p logs

# Start API server in background
echo "📡 Starting API Server (http://localhost:8000)..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info > logs/api.log 2>&1 &
API_PID=$!

# Wait for API to start
sleep 3

# Start Streamlit app
echo "🎨 Starting Streamlit Dashboard (http://localhost:8501)..."
echo ""
echo "======================================"
echo "✅ SERVICES STARTING!"
echo "======================================"
echo ""
echo "Dashboard will open automatically in your browser..."
echo ""
echo "💡 You can now:"
echo "   • Access Store: http://localhost:8501"
echo "   • View API Docs: http://localhost:8000/docs"
echo "   • Press Ctrl+C to stop all services"
echo ""

# Open dashboard in browser (Mac/Linux)
sleep 2
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8501  # Linux
elif command -v open &> /dev/null; then
    open http://localhost:8501  # Mac
fi

# Run Streamlit (this blocks until stopped)
python3 -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --logger.level=warning

# Cleanup on exit
kill $API_PID 2>/dev/null
echo ""
echo "✅ Services stopped!"
echo "👋 Thank you for using RIYU STORE!"
echo ""
