# KisanMitra AI

🌾 **An AI-powered Agricultural Assistant Chatbot for Karnataka Farmers**

KisanMitra AI is a beginner-friendly chatbot that helps farmers in Karnataka with agricultural guidance on crops, irrigation, pest management, diseases, soil health, and government schemes.

## Features

✅ **Multi-language Support**: English and Kannada  
✅ **Context-Aware Responses**: Uses farmer's district and crop information  
✅ **RAG (Retrieval-Augmented Generation)**: Searches verified agricultural knowledge base  
✅ **AI Agent**: Intelligent assistant that understands agricultural topics  
✅ **Weather Integration**: Real-time weather data and farming advice  
✅ **Government Schemes**: Links to official government resources  
✅ **Conversation History**: Keep track of past discussions  
✅ **Beginner-Friendly**: Simple, clean interface designed for farmers  

## Project Structure

```
kisanmitra-ai/
├── backend/                          # Python FastAPI backend
│   ├── app/
│   │   ├── main.py                  # FastAPI application
│   │   ├── routes/
│   │   │   ├── chat.py             # Chat endpoints
│   │   │   └── reference.py        # Crops, districts, schemes endpoints
│   │   ├── agents/
│   │   │   └── farmer_agent.py     # AI agent orchestrator
│   │   ├── rag/
│   │   │   ├── retriever.py        # Chroma vector store
│   │   │   └── ingest.py           # Knowledge base ingestion
│   │   ├── services/
│   │   │   ├── llm_service.py      # OpenAI API client
│   │   │   └── weather_service.py  # Weather API integration
│   │   ├── database/
│   │   │   ├── models.py           # SQLAlchemy models
│   │   │   └── db.py               # Database configuration
│   │   └── prompts/
│   ├── data/
│   │   └── agriculture/            # Knowledge base documents
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                # Environment variables template
│   └── README.md
│
├── frontend/                         # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx      # Main chat interface
│   │   │   ├── Message.jsx         # Message display
│   │   │   ├── LanguageSelector.jsx
│   │   │   ├── DistrictSelector.jsx
│   │   │   ├── CropSelector.jsx
│   │   │   └── QuickActions.jsx
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   ├── App.jsx                 # Main App component
│   │   └── main.jsx                # Entry point
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── .gitignore
├── README.md
└── Spec.md                          # Complete specification
```

## Technology Stack

- **Frontend**: React 18 + Vite + CSS3
- **Backend**: Python 3.9+ + FastAPI
- **Database**: SQLite
- **RAG**: Chroma with Sentence Transformers
- **LLM**: OpenAI API (GPT-3.5-turbo or GPT-4)
- **Weather API**: Open-Meteo (free, no key needed)
- **HTTP**: Axios + HTTPX

## Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- OpenAI API key

## Installation & Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Edit .env and add your OpenAI API key
# LLM_API_KEY=your_openai_api_key_here
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file if needed
echo "VITE_API_BASE_URL=http://localhost:8000/api" > .env.local
```

## Running the Application

### Option 1: Run both services in separate terminals (Recommended for development)

**Terminal 1 - Backend:**
```bash
cd backend

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# The backend will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

**Terminal 2 - Frontend:**
```bash
cd frontend

# Run development server
npm run dev

# The frontend will be available at http://localhost:5173
```

### Option 2: Run backend only (for API testing)

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload --port 8000
```

Then open http://localhost:8000/docs in your browser to test API endpoints.

## API Endpoints

### Chat
- `POST /api/chat` - Send a message and get AI response
- `GET /api/conversations` - List all conversations
- `GET /api/conversations/{id}` - Get messages in a conversation
- `DELETE /api/conversations/{id}` - Delete a conversation

### Reference Data
- `GET /api/crops` - List crops
- `GET /api/districts` - List districts
- `GET /api/schemes` - List government schemes
- `GET /api/weather?district=Mysuru` - Get weather
- `GET /api/supported-districts-weather` - Supported weather districts

### Health & Info
- `GET /api/health` - Health check
- `GET /` - API info

## Environment Configuration

Create a `.env` file in the `backend` directory:

```env
# LLM Configuration
LLM_API_KEY=your_openai_api_key
LLM_MODEL=gpt-3.5-turbo

# Database
DATABASE_URL=sqlite:///./kisanmitra.db

# Server
DEBUG=true
PORT=8000
FRONTEND_URL=http://localhost:5173

# Weather API (optional - Open-Meteo is free and requires no key)
WEATHER_API_KEY=
```

## Chat Request Example

```json
POST /api/chat
{
  "message": "My tomato plants have yellow leaves. What could be the reason?",
  "language": "en",
  "district": "Mysuru",
  "crop": "Tomato",
  "conversation_id": 1
}
```

Response:
```json
{
  "answer": "Yellow leaves on tomato plants can be caused by several factors...",
  "sources": [
    {
      "title": "Tomato Cultivation Best Practices",
      "url": "https://agriculture.karnataka.gov.in",
      "relevance": "95%"
    }
  ],
  "topic": "disease",
  "needs_expert": true,
  "conversation_id": 1,
  "message_id": 2
}
```

## Seeding the Knowledge Base

The knowledge base is automatically seeded on first run with agricultural documents about:
- Common crops (Ragi, Tomato, Onion, Rice, Groundnut, etc.)
- Irrigation and water management
- Pest and disease management
- Soil health
- Government schemes

To add more documents, edit `backend/app/rag/ingest.py` and add them to the `initial_documents` list.

## Testing

### Test the Backend API
```bash
# Start the backend
cd backend && python -m uvicorn app.main:app

# In another terminal, test endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/crops
curl http://localhost:8000/api/districts

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Which crops should I grow?",
    "language": "en",
    "district": "Mysuru"
  }'
```

### Test the Frontend
- Open http://localhost:5173 in your browser
- Select language and district
- Ask a question
- Verify the AI response and sources are displayed

## Important Notes

1. **API Key Required**: You need an OpenAI API key. Get one at https://platform.openai.com/api-keys

2. **Knowledge Base**: The MVP includes basic agricultural information. You can extend it by adding more documents to the `KnowledgeDocument` table.

3. **Government Schemes**: Links to official government pages are stored in the `SchemeLink` table. This is not an official government service.

4. **Weather API**: Uses free Open-Meteo API (no key required). Covers 20+ districts in Karnataka.

5. **Database**: SQLite is used for MVP simplicity. For production, consider PostgreSQL.

6. **Safety**: The chatbot is designed to give guidance but recommends expert consultation for serious issues.

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (3.9+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check if port 8000 is available
- Make sure .env file exists with LLM_API_KEY

### Frontend won't connect to backend
- Check backend is running on http://localhost:8000
- Verify CORS is enabled in FastAPI (should be by default)
- Check browser console for errors
- Try accessing http://localhost:8000/api/health

### LLM API errors
- Verify your OpenAI API key is correct
- Check you have API credits
- Ensure the model (gpt-3.5-turbo) is available in your account

### No responses from AI
- Check backend logs for errors
- Verify knowledge base was seeded (check database file size)
- Test LLM service directly in backend logs

## Performance Notes

- First run will initialize vector store and database (takes 30-60 seconds)
- Each chat message queries the knowledge base (2-3 seconds typical)
- OpenAI API calls take 5-10 seconds
- Weather API responses are instant

## Deployment

### Local Deployment
```bash
# Build frontend
cd frontend
npm run build

# Move dist folder to backend/static (if needed)
cp -r dist ../backend/static

# Run backend in production
cd ../backend
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### Cloud Deployment
For production deployment on cloud platforms (AWS, Azure, Heroku):
1. Use PostgreSQL instead of SQLite
2. Set up environment variables securely
3. Use production-grade ASGI server (gunicorn, uvicorn with multiple workers)
4. Enable HTTPS/SSL
5. Set up proper logging and monitoring

See individual platform documentation for detailed steps.

## Future Enhancements

- [ ] Image-based crop disease detection
- [ ] Voice input/output
- [ ] Multi-agent specialized for different topics
- [ ] Live market prices using approved APIs
- [ ] SMS/WhatsApp integration
- [ ] Mobile app
- [ ] Expert consultation booking
- [ ] Personalized recommendations based on history
- [ ] Integration with government open data APIs

## License

This is an educational/demonstration project.

## Support

For issues, questions, or suggestions, please check the specification file (`Spec.md`) for detailed requirements and architecture.

---

**Note**: KisanMitra AI is an independent educational project, not an official Government of Karnataka service. Always verify information on official government websites for government schemes and regulations.
