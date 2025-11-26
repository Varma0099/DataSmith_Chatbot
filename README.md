# 🏥 DataSmith AI - Post-Discharge Nephrology Care Assistant

A fully functional multi-agent AI chatbot system that assists patients after hospital discharge, specializing in nephrology (kidney disease) care. Built with CrewAI, LangChain, and Streamlit.

## 🎯 Project Overview

This Proof-of-Concept (POC) demonstrates a sophisticated AI system that:
- **Receptionist Agent**: Identifies patients and retrieves discharge summaries
- **Clinical Agent**: Answers medical questions using RAG + web search
- **RAG System**: Retrieves relevant information from nephrology knowledge base
- **Web Search Integration**: Falls back to Tavily API for current medical information
- **Comprehensive Logging**: Tracks all interactions with timestamps
- **Beautiful UI**: Streamlit-based web interface

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│                    (User Interface)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 Multi-Agent System (CrewAI)                  │
│  ┌──────────────────────┐    ┌───────────────────────────┐  │
│  │ Receptionist Agent   │    │  Clinical Agent           │  │
│  │ - Patient Lookup     │    │  - Medical Q&A            │  │
│  │ - Greetings          │    │  - RAG Retrieval          │  │
│  │ - Routing            │    │  - Web Search             │  │
│  └──────────────────────┘    └───────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌───▼────────┐ ┌─▼──────────┐
│ Patient DB   │ │  RAG       │ │ Web Search │
│ (JSON)       │ │ ChromaDB   │ │ (Tavily)   │
└──────────────┘ └────────────┘ └────────────┘
```

## ✨ Features

### Multi-Agent System
- **Receptionist Agent**: Handles greetings, patient identification, and retrieval of discharge summaries
- **Clinical Agent**: Provides evidence-based medical guidance using RAG and web search
- **Intelligent Routing**: Automatically routes queries to the appropriate agent

### RAG (Retrieval-Augmented Generation)
- Vector database using ChromaDB
- Semantic search over nephrology reference materials
- Fallback to comprehensive sample nephrology knowledge base

### Tools Integration
- **Patient Lookup Tool**: Retrieves discharge summaries from JSON database (27 patients)
- **Web Search Tool**: Tavily API integration for current medical information
- **Fallback Mode**: Mock search results when API not configured

### Comprehensive Logging
- Conversation logs with timestamps
- Agent activity tracking
- Error logging with context
- System event monitoring

### User Interface
- Clean, modern Streamlit interface
- Sample queries for easy testing
- Chat history download
- Session statistics
- Medical disclaimer prominently displayed

## 📋 Dataset

The system includes **27 detailed patient records** with realistic nephrology conditions:
- Chronic Kidney Disease (various stages)
- Acute Kidney Injury
- Dialysis patients (hemodialysis & peritoneal)
- Kidney transplant recipients
- Various kidney conditions (stones, PKD, nephrotic syndrome, etc.)

Each patient record includes:
- Demographics and diagnosis
- Medications with dosages
- Dietary restrictions
- Warning signs to monitor
- Follow-up information

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Google Gemini API key (FREE - for Gemini Pro)
- Tavily API key (optional, for web search)

### Installation

1. **Clone or download the project**
```bash
cd "Karthick's intern"
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API keys
# GOOGLE_API_KEY=your-actual-google-gemini-key (FREE)
# TAVILY_API_KEY=your-actual-tavily-key (optional)
```

**Get FREE Gemini API Key**: https://makersuite.google.com/app/apikey

5. **Run the application**
```bash
streamlit run app_streamlit.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Starting a Conversation
1. Open the app in your browser
2. The AI will greet you and ask for your name
3. Provide a patient name from the database (e.g., "John Smith")
4. The Receptionist Agent will retrieve your discharge summary

### Asking Medical Questions
- "What should I eat?"
- "I have swelling in my legs, what should I do?"
- "When should I take my medications?"
- "What are the warning signs I should watch for?"
- "Can you explain my diagnosis?"

### Testing Different Patients
Try these patient names:
- John Smith (CKD Stage 3)
- Maria Garcia (Acute Kidney Injury)
- Robert Johnson (ESRD on Hemodialysis)
- Linda Martinez (CKD Stage 4)
- Elizabeth Lee (Kidney Transplant)

## 🗂️ Project Structure

```
medical-ai-poc/
├── data/
│   └── patients.json              # 27 patient records
├── references/
│   └── (place nephrology PDFs here)
├── tools/
│   ├── patient_tool.py            # Patient lookup functionality
│   └── web_search_tool.py         # Tavily web search integration
├── agents/
│   └── crew.py                    # CrewAI multi-agent system
├── rag/
│   └── loader.py                  # RAG system with ChromaDB
├── utils/
│   └── logger.py                  # Comprehensive logging system
├── logs/
│   ├── system.log                 # System events
│   ├── conversations.log          # All conversations
│   ├── agent_activity.log         # Agent actions
│   └── errors.log                 # Error tracking
├── chroma_db/                     # Vector database (auto-created)
├── app_streamlit.py               # Main Streamlit application
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=...                 # Your Google Gemini API key (FREE!)

# Optional
TAVILY_API_KEY=tvly-...            # Tavily API key for web search
LOG_LEVEL=INFO                     # Logging level
ENVIRONMENT=development            # Environment setting
```

### API Keys

1. **Google Gemini API Key** (FREE)
   - Sign up at: https://makersuite.google.com/app/apikey
   - Click "Get API Key" button
   - Free tier: Generous limits for testing and development
   - No credit card required!

2. **Tavily API Key** (Optional)
   - Sign up at: https://tavily.com
   - Free tier: 1000 searches/month
   - If not configured, system uses mock search results

## 📊 Logging System

All system activities are logged in the `logs/` directory:

### Log Files
- **system.log**: System initialization, startup, and general events
- **conversations.log**: Complete conversation history with timestamps
- **agent_activity.log**: Agent actions, tool usage, RAG queries
- **errors.log**: All errors with stack traces and context

### Log Format
```json
{
  "timestamp": "2024-11-26T15:30:45.123456",
  "user_id": "user_001",
  "agent_type": "clinical",
  "user_message": "What should I eat?",
  "agent_response": "...",
  "metadata": {...}
}
```

## 🧪 Testing

### Manual Testing
1. Start the application
2. Test with different patient names
3. Ask various medical questions
4. Check logs in `logs/` directory

### Test the Tools Individually
```bash
# Test patient lookup
python tools/patient_tool.py

# Test web search
python tools/web_search_tool.py

# Test RAG system
python rag/loader.py

# Test logging
python utils/logger.py
```

## 🎨 Customization

### Adding New Patients
Edit `data/patients.json` and add new patient records following the existing format.

### Adding Nephrology References
1. Place PDF files in the `references/` directory
2. Delete the `chroma_db/` folder
3. Restart the application (it will rebuild the vector database)

### Modifying Agents
Edit `agents/crew.py` to customize:
- Agent roles and goals
- Tool assignments
- Routing logic
- Response formatting

## 🔒 Security & Privacy

⚠️ **Important Notes**:
- This is a demonstration system using **dummy data only**
- Never use real patient information
- Not HIPAA compliant
- Not for production medical use
- Always include medical disclaimers

## 📝 Assignment Checklist

- ✅ 27 dummy patients in JSON
- ✅ Nephrology knowledge base (sample content included)
- ✅ Receptionist Agent retrieves patient data
- ✅ Clinical Agent uses RAG with citations
- ✅ Web search fallback (Tavily integration)
- ✅ Comprehensive logging with timestamps
- ✅ Streamlit frontend with modern UI
- ✅ Medical disclaimer visible
- ✅ Complete documentation
- ✅ Ready for deployment

## 🚀 Deployment

### Local Deployment
```bash
streamlit run app_streamlit.py
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add environment variables in Streamlit settings
4. Deploy

### Docker (Optional)
```bash
# Create Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app_streamlit.py"]

# Build and run
docker build -t medical-ai .
docker run -p 8501:8501 medical-ai
```

## 🎥 Demo Video Script

For your 5-minute Loom video, cover:

1. **Introduction (30s)**
   - Project overview
   - Technology stack

2. **Architecture (45s)**
   - Show architecture diagram
   - Explain multi-agent approach

3. **Live Demo (3 min)**
   - Start application
   - Show patient lookup
   - Ask medical questions
   - Demonstrate RAG retrieval
   - Show web search fallback

4. **Code Walkthrough (45s)**
   - Quick tour of project structure
   - Show key files

5. **Logging (30s)**
   - Show log files
   - Explain logging system

## 📚 Technology Stack

- **Language**: Python 3.10+
- **LLM**: Google Gemini Pro (FREE!)
- **Framework**: CrewAI for multi-agent orchestration
- **Orchestration**: LangChain
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Web Search**: Tavily API
- **Frontend**: Streamlit
- **Logging**: Python logging module

## 🤝 Contributing

This is an assignment project, but suggestions are welcome!

## 📄 License

This is an educational project for the DataSmith AI GenAI Intern Assignment.

## 🙋 Support

For questions or issues:
1. Check the logs in `logs/` directory
2. Review the console output
3. Ensure API keys are correctly configured
4. Verify all dependencies are installed

## 🎓 Learning Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 📧 Contact

Created as part of DataSmith AI GenAI Intern Assignment

---

**⚕️ Medical Disclaimer**: This application is for educational and demonstration purposes only. It is not intended to provide medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with any questions about medical conditions.

