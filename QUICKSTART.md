# ⚡ Quick Start Guide

Get the Medical AI POC running in 5 minutes!

## Prerequisites

- Python 3.10+ installed
- Google Gemini API key ([Get one FREE](https://makersuite.google.com/app/apikey))

## 5-Step Setup

### 1️⃣ Install Dependencies (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2️⃣ Configure API Key (1 minute)

```bash
# Windows:
copy env.example .env
# Mac/Linux:
cp env.example .env
```

Edit `.env` and add your Google Gemini API key:
```
GOOGLE_API_KEY=your-key-here
```

**Get FREE Gemini API Key**: https://makersuite.google.com/app/apikey

### 3️⃣ Run Setup Check (30 seconds)

```bash
python setup.py
```

Should show all ✓ checks passed.

### 4️⃣ Start Application (30 seconds)

```bash
# Windows:
run.bat
# Mac/Linux:
chmod +x run.sh
./run.sh

# Or directly:
streamlit run app_streamlit.py
```

### 5️⃣ Test It! (1 minute)

1. Browser opens automatically at http://localhost:8501
2. Type: "My name is John Smith"
3. See the discharge summary appear
4. Ask: "What should I eat?"
5. Get medical advice!

## 🎯 Test Patients

Try these names:
- **John Smith** - CKD Stage 3
- **Maria Garcia** - Acute Kidney Injury
- **Robert Johnson** - On Hemodialysis
- **Elizabeth Lee** - Kidney Transplant

## 💡 Sample Questions

- "What medications should I take?"
- "What foods should I avoid?"
- "I have swelling in my legs, what should I do?"
- "When should I call my doctor?"
- "Can you explain my diagnosis?"

## 🔧 Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Error: Google Gemini API error
Check your API key in `.env` file (get free key at https://makersuite.google.com/app/apikey)

### Port already in use
```bash
streamlit run app_streamlit.py --server.port 8502
```

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for detailed setup

## 🎥 Demo Video

For the assignment, record a 5-minute demo showing:
1. Patient lookup
2. Medical question answering
3. RAG retrieval demonstration
4. Log file review

---

**Ready?** Let's go! 🚀

```bash
streamlit run app_streamlit.py
```

