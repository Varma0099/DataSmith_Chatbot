"""
Streamlit Frontend for Medical AI Chatbot
Post-Discharge Nephrology Care Assistant
"""
import streamlit as st
import os
import sys
import logging
from config import validate_config, MODEL_NAME
from logger import logger
from datetime import datetime

# Validate config on startup
try:
    validate_config()
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# Error handling wrapper
try:
    # Your main app code here
    pass
except Exception as e:
    logger.error(f"App error: {e}", exc_info=True)
    st.error(f"An error occurred. Please try again. Error: {str(e)}")

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import custom modules
from agents.crew import create_medical_crew
from rag.loader import setup_rag_system
from utils.logger import get_logger

# Page configuration
st.set_page_config(
    page_title="Post-Discharge Nephrology AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .disclaimer {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: right;
    }
    .assistant-message {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .stats-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Initialize the AI system (cached for performance)"""
    try:
        # Initialize logger
        logger = get_logger()
        logger.log_system_event("Streamlit app started")
        
        # Setup RAG system
        with st.spinner("Loading nephrology knowledge base..."):
            rag = setup_rag_system()
            retriever = rag.get_retriever(k=3)
        
        # Create medical crew
        with st.spinner("Initializing AI agents..."):
            crew = create_medical_crew(rag_retriever=retriever)
        
        logger.log_system_event("System initialization complete")
        return crew, logger, True
        
    except Exception as e:
        st.error(f"Error initializing system: {str(e)}")
        return None, None, False


def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">🏥 Post-Discharge Nephrology AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your 24/7 Virtual Care Companion</div>', unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Important Medical Disclaimer:</strong> This AI assistant is for educational and informational 
        purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. 
        Always seek the advice of your physician or other qualified health provider with any questions you may 
        have regarding a medical condition. In case of emergency, call 911 or your local emergency number immediately.
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system
    crew, logger, initialized = initialize_system()
    
    if not initialized:
        st.error("❌ System initialization failed. Please check your configuration and try again.")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This AI assistant helps patients after hospital discharge with:
        - 📋 Accessing discharge summaries
        - 💊 Medication information
        - 🍎 Dietary guidance
        - ⚠️ Warning signs to watch for
        - 📞 When to call your doctor
        """)
        
        st.divider()
        
        st.header("📊 Session Info")
        if 'message_count' not in st.session_state:
            st.session_state.message_count = 0
        st.metric("Messages Exchanged", st.session_state.message_count)
        
        st.divider()
        
        st.header("🔧 Quick Actions")
        if st.button("🔄 Clear Conversation"):
            st.session_state.messages = []
            st.session_state.message_count = 0
            logger.log_system_event("Conversation cleared by user")
            st.rerun()
        
        if st.button("📥 Download Chat History"):
            if 'messages' in st.session_state and st.session_state.messages:
                chat_history = "\n\n".join([
                    f"[{msg['role'].upper()}]: {msg['content']}" 
                    for msg in st.session_state.messages
                ])
                st.download_button(
                    label="Download",
                    data=chat_history,
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        st.divider()
        
        # Sample queries
        st.header("💡 Try asking:")
        sample_queries = [
            "My name is John Smith",
            "What should I eat?",
            "I have swelling in my legs",
            "When should I take my medications?",
            "What are warning signs I should watch for?"
        ]
        
        for query in sample_queries:
            if st.button(query, key=f"sample_{query}"):
                st.session_state.sample_query = query
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! 👋 I'm your post-discharge care assistant. I'm here to help you with questions about your discharge summary, medications, diet, and general care instructions.\n\nTo get started, could you please tell me your full name?"
            }
        ]
        logger.log_system_event("New conversation started")
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Handle sample query from sidebar
    if "sample_query" in st.session_state:
        prompt = st.session_state.sample_query
        del st.session_state.sample_query
    else:
        # Chat input
        prompt = st.chat_input("Type your message here...")
    
    # Process user input
    if prompt:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.message_count += 1
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Process message through crew
                    response = crew.process_message(prompt, st.session_state.messages)
                    
                    # Log conversation
                    logger.log_conversation(
                        user_message=prompt,
                        agent_response=response,
                        agent_type="auto-routed",
                        metadata={"message_count": st.session_state.message_count}
                    )
                    
                    # Display response
                    st.markdown(response)
                    
                    # Add to message history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.message_count += 1
                    
                except Exception as e:
                    error_msg = f"I apologize, but I encountered an error processing your request: {str(e)}\n\nPlease try again or rephrase your question."
                    st.error(error_msg)
                    logger.log_error(e, context="Processing user message", user_id="streamlit_user")
                    
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        # Rerun to update the display
        st.rerun()
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption("🤖 Powered by CrewAI & Google Gemini")
    with col2:
        st.caption("📚 Knowledge from Nephrology Guidelines")
    with col3:
        st.caption("🔐 Demo Version - Dummy Data Only")


if __name__ == "__main__":
    main()

