KisanMitra AI
Beginner-Level AI Farmer Chatbot for Karnataka
Complete Project Specification — MVP / Student Project

1. Project Summary
KisanMitra AI is a simple AI-powered chatbot designed to help farmers in Karnataka with common agricultural questions. The first version is intentionally beginner-friendly: one main AI agent, a small agriculture knowledge base, farmer location/crop context, and optional weather information. The system should answer in simple Kannada or English.
The project is NOT intended to be an official Government of Karnataka service. It is an independent educational/software project that provides informational assistance.
2. Important Permission / Government Website Decision
For the beginner MVP, do NOT build direct integrations with FRUITS, RaithaMitra, K-KISAN, PM-KISAN, or other government systems. Do not automate login, submit applications, access private farmer records, or scrape government websites.
Instead, store a small set of manually reviewed agricultural information in your own database and show links to official government pages when a farmer needs to apply or verify current information.
•	No government permission is required merely to build a student/demo chatbot that gives general information and links to official public pages.
•	Do not claim that the chatbot is an official government service.
•	Do not use government logos or branding in a way that implies official endorsement.
•	Do not copy large amounts of website content or continuously scrape pages.
•	If you later request API access, use a government dataset/API according to its published terms and access requirements.
•	Do not collect Aadhaar numbers, bank details, land records, or other sensitive farmer information in the MVP.
For current market prices, a later version may use an appropriate open-data/API source. India's Open Government Data platform currently exposes agricultural datasets and APIs, including daily mandi price datasets generated through AGMARKNET. Use the published API/data terms rather than scraping. The MVP can simply omit live market prices to keep the project easy.
3. Project Goal
Build a working web chatbot where a farmer selects Kannada or English, optionally provides a district and crop, and asks an agriculture-related question. The AI uses a small trusted knowledge base and the farmer's context to produce a simple, useful response.
4. Target Users
•	Farmers in Karnataka
•	Agriculture students
•	Students building an AI/agent project
•	Demonstration users and project evaluators
5. MVP Scope
The MVP must contain only the following core features:
•	Chat interface
•	Kannada and English responses
•	District selection
•	Crop selection or crop mentioned in chat
•	One main AI agent / orchestrator
•	Agriculture knowledge base using RAG
•	Basic conversation memory
•	Simple safety disclaimer
•	Optional weather API integration
•	Official-source links for government schemes
•	Chat history for the current user/session
The following are explicitly OUT OF SCOPE for Version 1:
•	Government portal login
•	FRUITS integration
•	Aadhaar verification
•	Government scheme application submission
•	Live mandi/market trading
•	Image disease diagnosis
•	Payment system
•	SMS/WhatsApp integration
•	Multi-agent swarm
•	Complex IoT/sensor integration
•	Mobile application
•	Fine-tuning an LLM
6. Example Questions
•	Which crops are suitable for Mysuru?
•	How often should I water tomato plants?
•	What are common pests in ragi?
•	My tomato leaves are turning yellow. What could be the reason?
•	What is the best season for growing ragi?
•	What should I consider before selecting a crop?
•	Which government scheme should I check for farmers?
•	What documents are generally required for a government scheme?
•	What is today's weather? (only if weather integration is enabled)
7. Simple AI Architecture
Use a single-agent architecture for the first version:
User → React Chat UI → FastAPI Backend → Farmer Context → RAG Retrieval → AI Agent/LLM → Safety Check → Response → Chat UI
The AI agent should use tools only when necessary:
•	Knowledge search tool — searches the agriculture knowledge base.
•	Weather tool — calls a weather API if live weather is requested.
•	Official-link lookup — returns stored official links for schemes/services.
This is enough to demonstrate an AI agent without making the system unnecessarily complex.
8. AI Agent Responsibilities
•	Understand the farmer's question.
•	Identify the topic: crop, soil, irrigation, pest/disease, weather, scheme, or general agriculture.
•	Use district/crop context when available.
•	Retrieve relevant knowledge before answering agriculture questions.
•	Ask one or two clarification questions when important information is missing.
•	Avoid inventing facts, scheme names, prices, or application requirements.
•	Answer in the selected language.
•	State uncertainty when the available information is insufficient.
9. RAG Knowledge Base
Create a small local knowledge base rather than trying to cover all agriculture in Karnataka at first. Start with 10–20 reviewed documents or structured records covering common crops and basic practices.
•	Ragi
•	Rice
•	Maize
•	Tomato
•	Onion
•	Groundnut
•	Sugarcane
•	Pulses
•	Basic soil and irrigation guidance
•	Basic government agriculture information
Each knowledge record should contain: title, topic, crop, district/region if applicable, content, source name, source URL, last-reviewed date, and language.
10. Government Information Strategy
Government information should be treated as reference information, not as a live government service. For the MVP, manually add a small number of scheme records and link the farmer to the official page.
Example record:
•	Scheme: PM-KISAN
•	Purpose: short description
•	Eligibility: short, verified summary
•	Official URL: official government page
•	Last reviewed: date
When the farmer asks about a scheme, the bot should say that eligibility and requirements can change and the farmer should verify the current details on the linked official page.
11. Weather Integration
Weather is optional in the MVP. If enabled, use a normal weather API with a free/developer tier where available. This does not require permission from the Government of India or Government of Karnataka merely because the user is a farmer. You will need to follow the chosen weather provider's API terms and protect the API key.
Weather inputs:
•	District/location
•	Current temperature
•	Rain probability/forecast
•	Humidity, if available
•	Basic weather-based farming guidance
Do not present a weather forecast as guaranteed.
12. User Flow
1.	Open the website.
2.	Select Kannada or English.
3.	Select district (optional but recommended).
4.	Select crop (optional).
5.	Enter a question.
6.	Backend sends the question and context to the AI agent.
7.	Agent retrieves relevant knowledge.
8.	Agent optionally calls weather.
9.	Agent generates a simple answer.
10.	UI displays the answer and source information.
11.	User can continue the conversation.
13. UI Requirements
•	Clean, mobile-friendly chat screen
•	Language selector: Kannada / English
•	District dropdown
•	Crop dropdown
•	Chat message area
•	Text input
•	Send button
•	Clear chat button
•	Source/reference area under answers when applicable
•	Simple disclaimer in the footer
Suggested quick buttons:
•	🌱 Crop Advice
•	💧 Irrigation
•	🐛 Pest/Disease
•	🌦️ Weather
•	🏛️ Schemes
14. Recommended Technology Stack
•	Frontend: React + Vite
•	Styling: CSS or Tailwind CSS
•	Backend: Python + FastAPI
•	AI: LLM API
•	RAG: Chroma or FAISS for a beginner prototype
•	Embeddings: an embedding model/API
•	Database: SQLite for MVP
•	ORM: SQLAlchemy (optional)
•	HTTP client: requests/httpx
•	Environment variables: .env
•	Version control: Git + GitHub
Do not add PostgreSQL, Redis, Kubernetes, microservices, LangGraph, multiple agents, or cloud infrastructure unless the basic MVP is already working. They can be added later.
15. Database Design
SQLite tables:
•	users — id, name (optional), language, district, created_at
•	conversations — id, user_id, title, created_at
•	messages — id, conversation_id, role, content, created_at
•	farmer_context — conversation_id, district, taluk (optional), crop, soil_type (optional)
•	knowledge_documents — id, title, topic, crop, content, source_name, source_url, reviewed_date
•	scheme_links — id, scheme_name, description, official_url, reviewed_date
16. API Endpoints
•	POST /api/chat — send a question and receive an AI response
•	GET /api/conversations — list conversations
•	GET /api/conversations/{id} — get messages
•	DELETE /api/conversations/{id} — delete conversation
•	GET /api/crops — list supported crops
•	GET /api/districts — list Karnataka districts
•	GET /api/schemes — list stored government scheme references
•	GET /api/health — backend health check
•	GET /api/weather — optional weather endpoint
17. Chat Request Example
POST /api/chat request JSON:
{"message":"My tomato leaves are turning yellow","language":"en","district":"Mysuru","crop":"Tomato","conversation_id":1}
Response JSON:
{"answer":"...","sources":[{"title":"...","url":"..."}],"topic":"crop_disease","needs_expert":false}
18. Prompt Rules
System prompt should instruct the AI to:
•	Act as a farmer-support assistant for Karnataka.
•	Use retrieved knowledge whenever available.
•	Never fabricate sources.
•	Never claim to be a government official.
•	Keep answers simple and practical.
•	Use Kannada when Kannada is selected.
•	Ask for district/crop when the answer depends on them.
•	Avoid unsafe or overly specific chemical recommendations when reliable information is unavailable.
•	For important treatment decisions, recommend verification with a qualified agriculture expert.
•	Clearly distinguish known facts from suggestions.
19. Safety and Responsible AI
•	The chatbot is an informational assistant, not an agricultural authority.
•	Disease identification should be phrased as possible causes, not guaranteed diagnosis.
•	Do not recommend banned or illegal products.
•	Do not invent pesticide doses or mixing instructions.
•	Do not provide false government eligibility claims.
•	Do not expose private user data.
•	Show source and last-reviewed date where practical.
•	Allow users to report an incorrect answer.
20. Error Handling
•	AI API unavailable → show a friendly retry message.
•	Knowledge search fails → provide a cautious general response or ask the user to retry.
•	Weather API fails → tell the user live weather is temporarily unavailable.
•	Unknown crop → ask the user to specify the crop.
•	Unknown district → ask the user to choose a district.
•	Empty message → do not send the request.
•	Invalid uploaded file → reject it (image upload is out of MVP scope).
21. Project Folder Structure
kisanmitra-ai/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── Message.jsx
│   │   │   ├── LanguageSelector.jsx
│   │   │   ├── DistrictSelector.jsx
│   │   │   └── QuickActions.jsx
│   │   ├── pages/
│   │   │   └── ChatPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── App.jsx
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   ├── weather.py
│   │   │   └── schemes.py
│   │   ├── agents/
│   │   │   └── farmer_agent.py
│   │   ├── rag/
│   │   │   ├── ingest.py
│   │   │   └── retriever.py
│   │   ├── services/
│   │   │   ├── llm_service.py
│   │   │   └── weather_service.py
│   │   ├── database/
│   │   │   ├── models.py
│   │   │   └── db.py
│   │   └── prompts/
│   │       └── farmer_prompt.txt
│   ├── data/
│   │   └── agriculture/
│   ├── .env
│   └── requirements.txt
│
├── README.md
└── .gitignore
22. Environment Variables
LLM_API_KEY=your_key
WEATHER_API_KEY=your_key_if_used
DATABASE_URL=sqlite:///./kisanmitra.db
Never commit .env to GitHub.
23. Development Phases
12.	Create React frontend and simple chat UI.
13.	Create FastAPI backend and /api/health.
14.	Connect frontend to backend.
15.	Connect the LLM.
16.	Add Kannada/English selection.
17.	Add district and crop context.
18.	Create agriculture knowledge documents.
19.	Implement embeddings and vector search.
20.	Connect RAG to the AI agent.
21.	Add official scheme links.
22.	Optionally add weather.
23.	Add error handling and safety instructions.
24.	Test with 30–50 sample farmer questions.
25.	Deploy only after the local version works.
24. Testing Requirements
Test at least these categories:
•	Normal agriculture questions
•	Kannada questions
•	English questions
•	Mixed Kannada-English questions
•	Unknown questions
•	Missing district
•	Missing crop
•	Government scheme questions
•	Weather questions
•	Prompt injection attempts
•	Empty/very long messages
•	API failure
•	Incorrect or missing knowledge-base information
25. Acceptance Criteria
•	A farmer can open the website and send a message.
•	The chatbot responds successfully.
•	The user can choose Kannada or English.
•	The selected district and crop are included in the AI context.
•	The chatbot retrieves relevant agriculture information before answering supported topics.
•	The chatbot can provide source references for knowledge-base answers.
•	Government questions link to official sources rather than pretending to perform government services.
•	No payment system exists.
•	No government login or private government database integration exists.
•	The application works locally using documented setup commands.
•	The application handles API failures without crashing.
26. Future Enhancements — NOT Required for MVP
•	Voice input/output
•	Crop image analysis
•	Disease detection
•	Live mandi prices using an approved/open API
•	More agricultural universities and knowledge sources
•	Personalized farmer profiles
•	SMS/WhatsApp
•	Mobile application
•	Multiple specialized agents
•	Expert escalation
•	Notifications and weather alerts
•	Advanced analytics
27. Recommended Beginner Project Boundary
For a first implementation, the best version is: React + FastAPI + one LLM + Chroma/FAISS + SQLite + a small agriculture knowledge base + Kannada/English + district/crop context. This is enough to demonstrate AI agent behavior, RAG, backend APIs, frontend development, and a real agricultural use case without creating government-integration or compliance complexity.
28. Source / Reference Policy
Use official public government pages as references for government-related information. The current official Indian government portals identify AGMARKNET as a Ministry of Agriculture and Farmers Welfare initiative and provide agricultural market information. Karnataka government/NIC pages also describe services such as RaithaMitra, FRUITS, K-KISAN and Krishi Marata Vahini. These should be linked as references rather than directly integrated into the beginner MVP.
Project rule: whenever a source is used, store its name, URL and last-reviewed date in the knowledge base.
29. Final Project Definition
KisanMitra AI is a beginner-friendly, AI-agent-based farmer chatbot for Karnataka. It provides general agricultural guidance using a trusted local knowledge base and optional weather information. It uses farmer context such as language, district and crop to make responses more relevant. It does not perform government transactions, access private government records, process payments, or represent itself as an official government service.
30. Implementation Principle
Keep the first version simple. Build a reliable chatbot first, then add features one at a time. The project should demonstrate working functionality rather than a large number of complicated integrations.
