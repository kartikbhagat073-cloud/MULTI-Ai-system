# AI Model Arena

> Compare multiple AI models on the same task, review their responses side-by-side, and choose the output you want to continue with.

AI Model Arena is an AI orchestration application designed to help users compare responses from different AI systems using a single prompt. Instead of switching between multiple AI tools manually, users can select models, submit one task, receive multiple responses, compare them, and select the response they want to use.

---

## ✨ Core Idea

```text
                    User
                      │
                      ▼
              Select AI Models
                      │
                      ▼
                 Enter Task
                      │
                      ▼
              AI Orchestrator
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
         GPT       Gemini       Ollama
          │           │           │
          └───────────┼───────────┘
                      ▼
              Compare Responses
                      │
                      ▼
                Select Output
                      │
                      ▼
             Continue / Edit / Use
```

The same task is sent to the selected AI systems. Their outputs are returned in a normalized format so the frontend can display them together.

---

## 🚀 Current MVP

The current version focuses on validating the core orchestration workflow.

### Available

- Select multiple AI models
- Enter a single task/prompt
- Send the same task to selected models
- Receive normalized responses
- Display responses for comparison
- Select a preferred response
- React + Vite frontend
- FastAPI backend
- Model adapter architecture
- Mock model adapters for local development
- Health-check API
- Compare API

### Coming Next

- Real OpenAI integration
- Real Gemini integration
- Ollama/local model integration
- Continue with selected response
- Conversation/context management
- Persistent task history
- Database
- AI-powered response evaluation
- Quality, latency, and cost comparison
- Authentication
- Production deployment

> **Note:** The current MVP uses mock AI adapters. You do not need API keys to run the current version.

---

# 🏗️ Architecture

```text
┌─────────────────────────────┐
│       React Frontend        │
│                             │
│  Model Selection            │
│  Prompt Input               │
│  Response Comparison        │
│  Output Selection           │
└──────────────┬──────────────┘
               │
               │ HTTP
               ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
│                             │
│  API Routes                 │
│  Request Validation         │
│  Orchestrator               │
│  Response Normalization     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Model Adapter Layer   │
│                             │
│  OpenAI Adapter             │
│  Gemini Adapter             │
│  Ollama Adapter             │
│  Claude Adapter             │
│  ...                        │
└─────────────────────────────┘
```

## Why use an adapter layer?

The application should not depend directly on one AI provider.

Instead of putting provider-specific logic throughout the application, every provider implements a common interface.

Conceptually:

```python
class ModelAdapter:
    def generate(self, prompt):
        ...
```

This makes it easier to add or replace models without changing the core orchestration logic.

---

# 🛠️ Tech Stack

## Frontend

- React
- Vite
- CSS

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

## AI Layer

The architecture is designed to support:

- OpenAI models
- Google Gemini
- Anthropic Claude
- Ollama/local LLMs
- Other compatible AI providers

## Future Data Layer

The application can later use:

- PostgreSQL
- SQLite for local development
- Redis for caching/queues if required

---

# 📁 Project Structure

```text
ai-model-arena/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   └── services/
│   │       ├── model_adapter.py
│   │       ├── mock_adapter.py
│   │       └── orchestrator.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── styles.css
│   │
│   ├── index.html
│   └── package.json
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── TASK_BOARD.md
│
└── README.md
```

---

# 💻 Local Installation

## Prerequisites

Install:

- Python 3.10+
- Node.js LTS
- npm
- Git

Check your versions:

```bash
python --version
node --version
npm --version
git --version
```

---

# 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-model-arena.git
cd ai-model-arena
```

Replace `YOUR_USERNAME` with your GitHub username.

---

# 2. Setup the Backend

Open a terminal and navigate to the backend:

```bash
cd backend
```

## Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

For PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/api/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# 5. Open FastAPI Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

You can test the available endpoints directly from the Swagger UI.

---

# 6. Setup the Frontend

Open a **new terminal**.

From the project root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

---

# 7. Start the Frontend

```bash
npm run dev
```

Vite will display the local development URL, normally:

```text
http://localhost:5173
```

Open that URL in your browser.

---

# ▶️ Running the Application

You need **two terminals** running at the same time.

### Terminal 1 — Backend

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

# 🧪 Testing the MVP

1. Open the frontend.
2. Select two or more available models.
3. Enter a task.

Example:

```text
Write a short product description for a kids water bottle.
```

4. Click **Compare Responses**.
5. The backend sends the task to the selected adapters.
6. The responses are returned to the frontend.
7. Review the outputs.
8. Select the preferred response.

The current adapters are mock implementations, so the application can be tested without external API keys.

---

# 🔌 API

## Health Check

### Request

```http
GET /api/health
```

### Response

```json
{
  "status": "ok"
}
```

---

## Compare Models

### Request

```http
POST /api/compare
```

Example request:

```json
{
  "prompt": "Write a short product description for a kids water bottle.",
  "models": [
    "GPT",
    "Gemini"
  ]
}
```

The backend sends the prompt to the selected model adapters and returns normalized responses.

---

# 🔐 Environment Variables

The current MVP does not require external AI API keys.

When real providers are added, environment variables should be stored in a local `.env` file.

Example:

```env
OPENAI_API_KEY=your_api_key_here
GEMINI_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_api_key_here
```

### Important

Never commit API keys to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
node_modules/
```

---

# 🧠 Model Adapter Design

The long-term goal is to make every AI provider interchangeable.

Example:

```text
                 Orchestrator
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
  OpenAI Adapter  Gemini Adapter  Ollama Adapter
        │             │             │
        ▼             ▼             ▼
     OpenAI         Gemini         Local LLM
```

The orchestrator should only care about:

```text
Model name
Prompt
Response
Metadata
```

It should not need to know the implementation details of each provider.

---

# 🎯 Product Roadmap

## Phase 1 — MVP

- [x] Project setup
- [x] React frontend
- [x] FastAPI backend
- [x] Model adapter architecture
- [x] Mock adapters
- [x] Prompt submission
- [x] Multi-model orchestration
- [x] Response comparison
- [x] Response selection

## Phase 2 — Real AI Models

- [ ] OpenAI adapter
- [ ] Gemini adapter
- [ ] Ollama adapter
- [ ] Claude adapter
- [ ] Provider error handling
- [ ] Timeout handling
- [ ] Retry handling

## Phase 3 — Continue Workflow

- [ ] Continue with selected response
- [ ] Edit selected response
- [ ] Use response as context
- [ ] Follow-up prompts
- [ ] Conversation history

## Phase 4 — Evaluation

- [ ] Response scoring
- [ ] Relevance evaluation
- [ ] Accuracy evaluation
- [ ] Creativity evaluation
- [ ] Completeness evaluation
- [ ] AI judge
- [ ] Human feedback

## Phase 5 — Data & Accounts

- [ ] Database
- [ ] User accounts
- [ ] Task history
- [ ] Saved responses
- [ ] Favorite models
- [ ] Usage tracking

## Phase 6 — Analytics

- [ ] Response latency
- [ ] Token usage
- [ ] Estimated cost
- [ ] Model performance
- [ ] User preference analytics

## Phase 7 — Production

- [ ] Authentication
- [ ] Secure API key management
- [ ] Rate limiting
- [ ] Logging
- [ ] Monitoring
- [ ] Docker
- [ ] CI/CD
- [ ] Production deployment

---

# 🔮 Future Vision

The final product can evolve from a simple comparison tool into an intelligent **AI decision and orchestration platform**.

For example:

```text
User Task
    │
    ▼
Select Models
    │
    ▼
Run Same Task
    │
    ▼
┌───────────────────────────┐
│ GPT       → Response A    │
│ Gemini    → Response B    │
│ Claude    → Response C    │
│ Ollama    → Response D    │
└───────────────────────────┘
    │
    ▼
AI Evaluation
    │
    ├── Accuracy
    ├── Relevance
    ├── Quality
    ├── Cost
    └── Latency
    │
    ▼
Recommended Response
    │
    ▼
User Approval
    │
    ▼
Continue / Refine / Export
```

---

# 🤝 Contributing

Contributions are welcome.

### Fork the repository

```bash
git fork
```

### Create a feature branch

```bash
git checkout -b feature/your-feature
```

### Commit changes

```bash
git add .
git commit -m "Add your feature"
```

### Push the branch

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 🐛 Troubleshooting

## Backend does not start

Make sure the virtual environment is activated:

```bash
venv\Scripts\activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

Start again:

```bash
uvicorn app.main:app --reload
```

## Frontend does not start

Delete `node_modules` and reinstall:

```bash
npm install
```

Then:

```bash
npm run dev
```

## Port 8000 is already in use

Start FastAPI on another port:

```bash
uvicorn app.main:app --reload --port 8001
```

If you change the backend port, update the frontend API configuration accordingly.

---

# 📌 Project Status

**Status:** 🚧 Active Development

**Current Version:** MVP

The project is currently focused on validating the core multi-model comparison and selection workflow before adding production AI providers and persistent storage.

---

# 👨‍💻 Author

**Kartik Kumar**

AI / GenAI Developer

---

## ⭐ If you find this project useful

Give the repository a ⭐ on GitHub and feel free to contribute.
