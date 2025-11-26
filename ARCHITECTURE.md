# 🏗️ System Architecture Documentation

## Overview

The Medical AI POC is a multi-agent system designed to assist patients with post-discharge care. The system uses a modular architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                         │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Streamlit Web Application                       │   │
│  │  • Chat Interface                                            │   │
│  │  • Session Management                                        │   │
│  │  • Sample Queries                                            │   │
│  │  • Chat History Download                                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                               │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              CrewAI Multi-Agent System                       │   │
│  │                                                               │   │
│  │  ┌────────────────────┐        ┌─────────────────────────┐  │   │
│  │  │ Receptionist Agent │        │  Clinical Agent         │  │   │
│  │  │                    │        │                         │  │   │
│  │  │ • Greets patients  │        │ • Medical Q&A          │  │   │
│  │  │ • Identifies users │        │ • RAG retrieval        │  │   │
│  │  │ • Retrieves records│        │ • Web search           │  │   │
│  │  │ • Routes questions │        │ • Evidence-based info  │  │   │
│  │  │                    │◄──────►│                         │  │   │
│  │  │ Tools:             │        │ Tools:                  │  │   │
│  │  │ - Patient lookup   │        │ - Web search           │  │   │
│  │  │ - Patient ID lookup│        │ - (RAG via context)    │  │   │
│  │  └────────────────────┘        └─────────────────────────┘  │   │
│  │                                                               │   │
│  │  Decision Logic: Routes based on query type                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   TOOLS      │    │     RAG     │    │  WEB SEARCH  │
│   LAYER      │    │    LAYER    │    │    LAYER     │
├──────────────┤    ├─────────────┤    ├──────────────┤
│ Patient DB   │    │  ChromaDB   │    │ Tavily API   │
│              │    │             │    │              │
│ • Load JSON  │    │ • Embeddings│    │ • Real-time  │
│ • Search by  │    │ • Semantic  │    │   search     │
│   name       │    │   search    │    │ • Medical    │
│ • Search by  │    │ • Retrieval │    │   sources    │
│   ID         │    │             │    │ • Fallback   │
│              │    │ Embedding:  │    │   mocks      │
│ Format:      │    │ all-MiniLM  │    │              │
│ JSON         │    │   -L6-v2    │    │              │
└──────────────┘    └─────────────┘    └──────────────┘
        │                   │                   │
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────┐
│              DATA/KNOWLEDGE LAYER                     │
├──────────────────────────────────────────────────────┤
│  • 27 Patient Records (JSON)                         │
│  • Nephrology Knowledge Base (Text/PDF)              │
│  • Web Search Results (Dynamic)                      │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│              LOGGING & MONITORING LAYER               │
├──────────────────────────────────────────────────────┤
│  • system.log          - System events               │
│  • conversations.log   - All conversations           │
│  • agent_activity.log  - Agent actions               │
│  • errors.log          - Error tracking              │
└──────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

**Technology**: Streamlit
**Responsibilities**:
- Render chat interface
- Manage session state
- Display messages and responses
- Handle user input
- Provide utility features (download history, clear chat)

**Key Features**:
- Responsive design
- Real-time chat updates
- Session persistence
- Sample query shortcuts
- Medical disclaimers

### 2. Orchestration Layer (CrewAI)

**Technology**: CrewAI + LangChain
**Responsibilities**:
- Route queries to appropriate agents
- Manage agent interactions
- Coordinate tool usage
- Handle context and conversation flow

#### Receptionist Agent
```python
Role: Patient Services Receptionist
Goal: Identify patients, retrieve records, route queries
Tools: 
  - Patient lookup by name
  - Patient lookup by ID
Delegation: Yes (to Clinical Agent)
```

#### Clinical Agent
```python
Role: Nephrology Clinical Assistant
Goal: Answer medical questions with evidence
Tools:
  - Web search (Tavily)
  - RAG context (via retriever)
Delegation: No
```

**Routing Logic**:
```
Query received → Is it medical? 
                 ├─ Yes → Clinical Agent + RAG + Web Search
                 └─ No  → Receptionist Agent + Patient Tools
```

### 3. Tools Layer

#### Patient Lookup Tool
- **Input**: Patient name (string)
- **Process**: 
  1. Load patients.json
  2. Search case-insensitive
  3. Handle duplicates
  4. Format output
- **Output**: Formatted discharge summary or error message

#### Web Search Tool
- **Input**: Medical query (string)
- **Process**:
  1. Check for Tavily API key
  2. If available: Real-time search
  3. If not: Mock results
  4. Filter medical sources
- **Output**: Formatted search results with citations

### 4. RAG Layer

**Technology**: ChromaDB + sentence-transformers
**Embeddings Model**: all-MiniLM-L6-v2 (384 dimensions)

**Pipeline**:
```
PDF Documents
    ↓
Text Extraction (PyPDF)
    ↓
Chunking (RecursiveCharacterTextSplitter)
  • chunk_size: 1000
  • chunk_overlap: 200
    ↓
Embedding Generation (HuggingFace)
    ↓
Vector Storage (ChromaDB)
    ↓
Semantic Search (k=3)
    ↓
Context for LLM
```

**Features**:
- Persistent vector store
- Semantic similarity search
- Configurable retrieval count
- Sample knowledge base fallback

### 5. Data Layer

#### Patient Database
- **Format**: JSON
- **Size**: 27 records
- **Fields**: 
  - Demographics (name, age, gender)
  - Medical (diagnoses, medications)
  - Care instructions (diet, warnings)
  - Follow-up information

#### Knowledge Base
- **Primary**: Nephrology PDFs (user-provided)
- **Fallback**: Comprehensive sample content
- **Topics**:
  - CKD stages and management
  - Dialysis care
  - Common kidney conditions
  - Medications
  - Post-discharge guidelines

### 6. Logging Layer

**Technology**: Python logging module

**Log Types**:
1. **System Logs**: Startup, initialization, configuration
2. **Conversation Logs**: Complete message history (JSON format)
3. **Agent Activity**: Tool calls, decisions, retrievals
4. **Error Logs**: Exceptions with stack traces

**Log Format**:
```
{
  "timestamp": "ISO-8601",
  "level": "INFO|WARNING|ERROR",
  "component": "agent|tool|rag",
  "message": "...",
  "metadata": {...}
}
```

## Data Flow

### Patient Lookup Flow
```
User: "My name is John Smith"
    ↓
Streamlit UI captures input
    ↓
MedicalAICrew.process_message()
    ↓
Routing: Not medical → Receptionist Agent
    ↓
Agent uses Patient Lookup Tool
    ↓
Tool loads patients.json
    ↓
Search and match patient
    ↓
Format discharge summary
    ↓
Return to agent
    ↓
Agent formats response
    ↓
Logger records interaction
    ↓
Display in Streamlit
```

### Medical Question Flow
```
User: "What should I eat with kidney disease?"
    ↓
Streamlit UI captures input
    ↓
MedicalAICrew.process_message()
    ↓
Routing: Medical → Clinical Agent
    ↓
RAG retriever gets relevant docs (k=3)
    ↓
Agent analyzes question + context
    ↓
If needed: Web search tool call
    ↓
Agent synthesizes answer
    ↓
Add medical disclaimer
    ↓
Logger records all steps
    ↓
Display in Streamlit
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit | Web UI |
| Orchestration | CrewAI | Multi-agent system |
| LLM | Google Gemini Pro | Language understanding (FREE!) |
| Framework | LangChain | Tool integration |
| Vector DB | ChromaDB | Semantic search |
| Embeddings | HuggingFace Transformers | Text encoding |
| Web Search | Tavily API | Real-time info |
| Data Storage | JSON | Patient records |
| Logging | Python logging | Monitoring |

## Design Patterns

### 1. Factory Pattern
```python
def create_medical_crew(rag_retriever=None):
    return MedicalAICrew(rag_retriever=rag_retriever)
```

### 2. Singleton Pattern
```python
@st.cache_resource
def initialize_system():
    # Cached system initialization
```

### 3. Strategy Pattern
```python
def _is_medical_question(message):
    # Route based on content strategy
```

### 4. Observer Pattern
```python
# Logging observes all system activities
logger.log_conversation(...)
logger.log_agent_activity(...)
```

## Scalability Considerations

### Current Limitations
- In-memory vector store
- JSON file database
- Single-threaded Streamlit
- No user authentication

### Future Enhancements
1. **Database**: PostgreSQL for patient records
2. **Vector Store**: Pinecone or Weaviate for cloud scale
3. **Authentication**: User login and session management
4. **API**: FastAPI backend for better separation
5. **Caching**: Redis for response caching
6. **Monitoring**: Prometheus + Grafana
7. **Deployment**: Docker + Kubernetes

## Security Considerations

### Current Implementation
- ⚠️ Demo system with dummy data only
- ⚠️ No encryption
- ⚠️ No authentication
- ⚠️ API keys in .env (local only)

### Production Requirements
- ✅ HIPAA compliance measures
- ✅ End-to-end encryption
- ✅ Role-based access control
- ✅ Audit logging
- ✅ Secure API key management (AWS Secrets Manager, etc.)
- ✅ Data anonymization

## Performance Metrics

### Typical Response Times
- Patient lookup: < 100ms
- RAG retrieval: 200-500ms
- LLM response: 2-5 seconds
- Web search: 1-3 seconds
- Total user experience: 3-8 seconds

### Optimization Opportunities
1. Cache frequent queries
2. Preload embeddings
3. Batch RAG retrievals
4. Streaming LLM responses

## Error Handling

### Strategy
1. **Try-Catch**: All tool calls wrapped in try-catch
2. **Fallbacks**: Mock data when APIs unavailable
3. **User Messages**: Friendly error messages
4. **Logging**: Detailed error logs with context
5. **Recovery**: System continues operating on partial failure

### Example Flow
```
API Call Failed
    ↓
Log detailed error
    ↓
Use fallback/mock data
    ↓
Inform user gracefully
    ↓
Continue operation
```

## Testing Strategy

### Manual Testing
- Patient lookup with valid/invalid names
- Medical questions of varying complexity
- Edge cases (empty input, long text)

### Integration Testing
- Agent → Tool integration
- RAG → LLM integration
- Logging across all components

### User Acceptance Testing
- Real-world scenarios
- Different patient personas
- Various medical questions

---

**Document Version**: 1.0
**Last Updated**: November 2024
**Maintained By**: DataSmith AI Team

