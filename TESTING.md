# Testing and Verification Guide

This document provides detailed instructions for testing and verifying the KisanMitra AI application.

## Prerequisites

Before running tests, ensure:
1. Python 3.9+ is installed
2. Node.js 16+ is installed
3. pip is available
4. npm/yarn is available
5. You have an OpenAI API key

## Installation

### Method 1: Using Automated Script (Recommended)

**On Windows:**
```bash
cd d:\Farmer bot
setup.bat
```

**On Linux/Mac:**
```bash
cd /path/to/farmer bot
chmod +x setup.sh
./setup.sh
```

### Method 2: Manual Installation

**Backend Setup:**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env and add your OpenAI API key
```

**Frontend Setup:**
```bash
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Step 1: Start Backend (Terminal 1)

```bash
cd backend

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
...
```

The backend should initialize:
- Database (kisanmitra.db created)
- Vector store (Chroma)
- Knowledge base seeded
- API available at http://localhost:8000

### Step 2: Start Frontend (Terminal 2)

```bash
cd frontend

# Start development server
npm run dev
```

You should see output like:
```
Local:   http://localhost:5173/
Ready in 234ms.
```

### Step 3: Open Application in Browser

Navigate to: **http://localhost:5173**

You should see:
- KisanMitra logo and title
- Language selector (English, ಕನ್ನಡ)
- District dropdown
- Crop dropdown
- Quick action buttons
- Chat area

## Functional Testing

### Test 1: Health Check

**Method:** Check if backend is running
```bash
curl http://localhost:8000/api/health
```

**Expected Response:**
```json
{"status": "ok", "message": "KisanMitra API is running"}
```

### Test 2: Get Available Crops

```bash
curl http://localhost:8000/api/crops
```

**Expected Response:**
```json
[
  {"name": "Ragi (Finger Millet)", "kannada": "ರಾಗಿ"},
  {"name": "Tomato", "kannada": "ಟೊಮೆಟೊ"},
  ...
]
```

### Test 3: Get Available Districts

```bash
curl http://localhost:8000/api/districts
```

**Expected Response:**
```json
[
  {"name": "Mysuru", "kannada": "ಮೈಸೂರು"},
  {"name": "Bangalore", "kannada": "ಬೆಂಗಳೂರು"},
  ...
]
```

### Test 4: Get Weather

```bash
curl "http://localhost:8000/api/weather?district=Mysuru"
```

**Expected Response:**
```json
{
  "temperature": 28.5,
  "condition": "Clear sky",
  "humidity": 65,
  "rainfall": 0,
  "farming_advice": "Today is good for..."
}
```

### Test 5: Chat with AI (Requires API Key)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What should I grow in Mysuru?",
    "language": "en",
    "district": "Mysuru"
  }'
```

**Expected Response:**
```json
{
  "answer": "Based on Mysuru's climate and soil...",
  "sources": [...],
  "topic": "crop",
  "needs_expert": false,
  "conversation_id": 1,
  "message_id": 2
}
```

## UI Testing Checklist

### Language Selection
- [ ] Click English button - UI should be in English
- [ ] Click Kannada button - UI should be in Kannada
- [ ] Quick action texts should change

### District Selection
- [ ] Click district dropdown
- [ ] Select "Mysuru"
- [ ] Verify selected value displays

### Crop Selection
- [ ] Click crop dropdown
- [ ] Select "Tomato"
- [ ] Verify selected value displays

### Quick Actions
- [ ] Click "🌱 Crop Advice" button
- [ ] Should populate message input
- [ ] Message should be in selected language

### Send Message
- [ ] Type a question
- [ ] Click Send button
- [ ] Message should appear in chat window with "You" label
- [ ] AI response should appear with "Assistant" label
- [ ] Sources should be visible below response

### Clear Chat
- [ ] Click "Clear Chat" button
- [ ] Chat history should be cleared
- [ ] New conversation should start

### Message Features
- [ ] Links in responses should be clickable
- [ ] Sources should show title and URL
- [ ] Expert recommendation badge should appear for complex questions

## Performance Testing

### Response Time
- **Expected:** Chat responses in 5-15 seconds
- **Measurement:** Time from message send to response display

### Knowledge Base
- **Expected:** 8 documents seeded
- **Verification:** Check database file size (should be > 1MB)

### API Response
- **Expected:** < 200ms for non-LLM endpoints
- **Endpoints to test:**
  - GET /api/health
  - GET /api/crops
  - GET /api/districts
  - GET /api/weather

## Database Verification

### Check Database File
```bash
# Windows
dir backend\kisanmitra.db

# Linux/Mac
ls -lh backend/kisanmitra.db
```

Should exist and be > 1MB

### Check Database Schema
```bash
# Windows (using sqlite3 if installed)
sqlite3 backend\kisanmitra.db ".tables"

# Expected output:
# scheme_links   users           knowledge_documents  messages  farmer_context  conversations
```

### Count Seeded Documents
```bash
sqlite3 backend/kisanmitra.db "SELECT COUNT(*) FROM knowledge_documents;"
```

Expected: 8 or more

## Error Scenario Testing

### Test 1: Invalid API Key
**Setup:** Set `LLM_API_KEY=invalid_key` in .env
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "language": "en"}'
```
**Expected:** Error response mentioning invalid API key

### Test 2: Backend Offline
**Setup:** Stop the backend server
```bash
# From browser, try to send a message
```
**Expected:** Connection error in frontend

### Test 3: Empty Message
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "", "language": "en"}'
```
**Expected:** 422 Unprocessable Entity or validation error

### Test 4: Invalid Language
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "language": "hi"}'
```
**Expected:** 422 Validation error

## Bilingual Testing

### English Mode
1. Select "English" language
2. Select "Mysuru" district
3. Select "Tomato" crop
4. Click "🌱 Crop Advice"
5. Verify:
   - Button text is in English
   - Response is in English
   - District/crop names are in English

### Kannada Mode
1. Select "ಕನ್ನಡ" language
2. Select "ಮೈಸೂರು" district
3. Select "ಟೊಮೆಟೊ" crop
4. Click "🌱 ಸಸ್ಯ ಸಲಹೆ" (Kannada version)
5. Verify:
   - Button text is in Kannada
   - Response is in Kannada
   - District/crop names are in Kannada

## Conversation History Testing

1. Send message 1: "Which crops grow well here?"
2. Verify conversation appears with ID
3. Send message 2: "What about irrigation?"
4. Both messages should appear in history
5. Click another conversation (if exists)
6. Verify messages from first conversation are gone
7. Return to first conversation
8. Verify messages reappear

## Source Attribution Testing

1. Send a question: "How to manage tomato pests?"
2. In response, look for "Sources" section
3. Each source should have:
   - Document title
   - Source name/URL (if available)
   - Review date
4. Verify sources match knowledge base documents

## Build and Production Testing

### Build Frontend
```bash
cd frontend
npm run build
```

Expected output:
```
✓ 123 modules transformed.
dist/index.html  12.34 kB
dist/assets/...  34.56 kB
```

Verify `frontend/dist` folder exists with:
- `index.html`
- `assets/` folder with JS/CSS files

### Test Production Build Locally
```bash
# After building
cd frontend
npm run preview
```

Should serve on http://localhost:4173

## Troubleshooting Checklist

### Backend Won't Start
- [ ] Is Python 3.9+ installed?
- [ ] Is virtual environment activated?
- [ ] Are all dependencies installed? (`pip install -r requirements.txt`)
- [ ] Is .env file created with LLM_API_KEY?
- [ ] Is port 8000 available? (Check: `netstat -an | grep 8000`)

### Frontend Won't Start
- [ ] Is Node.js 16+ installed?
- [ ] Did you run `npm install`?
- [ ] Is port 5173 available?
- [ ] Check browser console for errors

### Chat Returns Errors
- [ ] Is backend running? (Test: `curl http://localhost:8000/api/health`)
- [ ] Is OpenAI API key valid?
- [ ] Do you have API credits?
- [ ] Check backend logs for error messages

### Knowledge Base Queries Return Nothing
- [ ] Is database file created? (`ls backend/kisanmitra.db`)
- [ ] Does database have documents? (Run SQL query above)
- [ ] Are you using correct keywords?
- [ ] Try simpler queries

### CORS Errors in Frontend
- [ ] Verify `FRONTEND_URL` in backend `.env` is correct
- [ ] Check browser console for specific CORS error
- [ ] Ensure backend is running on port 8000
- [ ] Verify frontend is on allowed origin

## Acceptance Criteria

The application is complete when:

✅ Backend starts without errors  
✅ Frontend starts without errors  
✅ All API endpoints respond  
✅ Chat endpoint works (with valid API key)  
✅ Knowledge base queries return results  
✅ UI renders properly in both languages  
✅ Conversation history persists  
✅ Sources are displayed correctly  
✅ Weather API integration works  
✅ All 4 reference endpoints work  

## Next Steps

If all tests pass:
1. Consider deploying to cloud platform
2. Set up domain/HTTPS
3. Monitor performance and errors
4. Collect user feedback
5. Plan enhancements (image upload, expert consultation, etc.)

If tests fail:
1. Check logs for error messages
2. Verify .env configuration
3. Ensure all dependencies are installed
4. Review troubleshooting section above
5. Check GitHub issues for similar problems
