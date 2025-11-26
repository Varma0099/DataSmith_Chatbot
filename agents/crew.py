"""
Multi-Agent System using CrewAI
Coordinates Receptionist and Clinical Nephrology Agents
"""
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from dotenv import load_dotenv
import logging

# Import custom tools
from tools.patient_tool import get_patient_report, search_patient_by_id
from tools.web_search_tool import web_search

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='logs/agent_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MedicalAICrew:
    """Medical AI Multi-Agent System"""
    
    def __init__(self, rag_retriever=None):
        """
        Initialize the Medical AI Crew.
        
        Args:
            rag_retriever: Optional RAG retriever for clinical knowledge
        """
        self.rag_retriever = rag_retriever
        
        # Initialize LLM with Google Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your-google-api-key-here":
            logger.warning("Google Gemini API key not configured. Using fallback.")
            # For demo purposes, we'll still initialize but it won't work without a real key
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=api_key
        )
        
        # Create tools
        self.patient_tool = Tool(
            name="PatientReportRetrieval",
            func=get_patient_report,
            description="""
            Use this tool to retrieve a patient's discharge summary by their full name.
            Input should be the patient's full name (e.g., 'John Smith').
            Returns detailed discharge information including diagnosis, medications, and dietary restrictions.
            """
        )
        
        self.patient_id_tool = Tool(
            name="PatientIDLookup",
            func=search_patient_by_id,
            description="""
            Use this tool to retrieve a patient's information by their patient ID.
            Input should be the patient ID (e.g., 'P001').
            Returns patient information in JSON format.
            """
        )
        
        self.web_search_tool = Tool(
            name="MedicalWebSearch",
            func=web_search,
            description="""
            Use this tool to search for current medical information on the internet.
            Useful for questions about treatments, medications, or medical conditions that need up-to-date information.
            Input should be a clear search query about a medical topic.
            Returns relevant information from trusted medical sources.
            """
        )
        
        # Create agents
        self.receptionist_agent = self._create_receptionist_agent()
        self.clinical_agent = self._create_clinical_agent()
        
        logger.info("Medical AI Crew initialized successfully")
    
    def _create_receptionist_agent(self) -> Agent:
        """Create the Receptionist Agent"""
        return Agent(
            role="Patient Services Receptionist",
            goal="""
            Greet patients warmly, identify them by name, retrieve their discharge summaries,
            and route medical questions to the Clinical Agent. Provide excellent customer service
            and ensure patients feel cared for during their post-discharge period.
            """,
            backstory="""
            You are a compassionate and efficient hospital discharge coordinator with 10 years of experience.
            You excel at making patients feel comfortable and helping them navigate their post-discharge care.
            You have access to patient records and can quickly retrieve discharge summaries.
            When patients ask medical questions, you professionally hand off to the clinical team while
            ensuring continuity of care.
            """,
            tools=[self.patient_tool, self.patient_id_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )
    
    def _create_clinical_agent(self) -> Agent:
        """Create the Clinical Nephrology Agent"""
        return Agent(
            role="Nephrology Clinical Assistant",
            goal="""
            Answer patient medical questions accurately using the nephrology knowledge base,
            provide evidence-based guidance, and use web search for the latest information when needed.
            Always prioritize patient safety and provide appropriate medical disclaimers.
            """,
            backstory="""
            You are an AI clinical assistant specialized in nephrology with extensive training in kidney disease
            management, dialysis, transplantation, and post-discharge care. You have access to comprehensive
            nephrology reference materials and can search for the latest medical information.
            You provide clear, accurate medical information while always reminding patients to consult
            their healthcare providers for personalized medical advice. You are empathetic, thorough,
            and committed to patient education.
            """,
            tools=[self.web_search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def process_message(self, user_message: str, conversation_history: list = None) -> str:
        """
        Process a user message and route to appropriate agent.
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            
        Returns:
            Response from the agent system
        """
        try:
            logger.info(f"Processing message: {user_message[:100]}")
            
            # Determine which agent should handle this
            is_medical_question = self._is_medical_question(user_message)
            
            if is_medical_question:
                # Clinical question - needs clinical agent with RAG
                response = self._handle_clinical_question(user_message)
            else:
                # Receptionist handles greetings, patient lookup, general navigation
                response = self._handle_receptionist_task(user_message)
            
            logger.info("Message processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return f"I apologize, but I encountered an error: {str(e)}. Please try again or contact support."
    
    def _is_medical_question(self, message: str) -> bool:
        """Determine if message is a medical question"""
        medical_keywords = [
            'symptom', 'pain', 'medication', 'medicine', 'treatment', 'side effect',
            'swelling', 'kidney', 'dialysis', 'diet', 'food', 'eat', 'drink',
            'blood pressure', 'diabetes', 'creatinine', 'protein', 'urine',
            'should i', 'can i', 'is it normal', 'what if', 'how do i',
            'concern', 'worried', 'advice', 'recommendation'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in medical_keywords)
    
    def _handle_receptionist_task(self, message: str) -> str:
        """Handle receptionist tasks"""
        task = Task(
            description=f"""
            User message: {message}
            
            Your task:
            1. If this is a greeting, respond warmly and ask for the patient's name
            2. If the user provides their name, retrieve their discharge summary
            3. If the user asks a medical question, acknowledge and explain that you're
               connecting them with a clinical specialist
            4. Be friendly, professional, and helpful
            
            Provide a clear, concise response.
            """,
            agent=self.receptionist_agent,
            expected_output="A helpful response to the user's message"
        )
        
        crew = Crew(
            agents=[self.receptionist_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        return str(result)
    
    def _handle_clinical_question(self, message: str) -> str:
        """Handle clinical questions with RAG"""
        # Get relevant context from RAG if available
        context = ""
        if self.rag_retriever:
            try:
                docs = self.rag_retriever.get_relevant_documents(message)
                context = "\n\n".join([doc.page_content for doc in docs[:3]])
                logger.info(f"Retrieved {len(docs)} documents from RAG")
            except Exception as e:
                logger.warning(f"RAG retrieval failed: {e}")
                context = ""
        
        task = Task(
            description=f"""
            Patient question: {message}
            
            Relevant medical knowledge:
            {context if context else "Use web search tool for current medical information"}
            
            Your task:
            1. Answer the patient's question accurately using the provided medical knowledge
            2. If you need more current information, use the web search tool
            3. Provide clear, evidence-based guidance
            4. Include appropriate warnings signs if relevant
            5. Always end with a medical disclaimer reminding them to consult their healthcare provider
            
            Provide a comprehensive but clear response.
            """,
            agent=self.clinical_agent,
            expected_output="A thorough clinical answer with citations and appropriate disclaimers"
        )
        
        crew = Crew(
            agents=[self.clinical_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        
        # Add disclaimer if not present
        result_str = str(result)
        if "consult" not in result_str.lower() or "disclaimer" not in result_str.lower():
            result_str += "\n\n⚕️ **Medical Disclaimer**: This information is for educational purposes only. Always consult your healthcare provider for personalized medical advice."
        
        return result_str
    
    def process_conversation(self, messages: list) -> str:
        """
        Process a full conversation with context awareness.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Response from the agent system
        """
        if not messages:
            return "Hello! I'm your post-discharge care assistant. How can I help you today?"
        
        # Get the latest message
        latest_message = messages[-1]['content']
        
        # Build conversation context
        context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in messages[-5:]  # Last 5 messages for context
        ])
        
        return self.process_message(latest_message, messages)


def create_medical_crew(rag_retriever=None):
    """
    Factory function to create a Medical AI Crew.
    
    Args:
        rag_retriever: Optional RAG retriever for clinical knowledge
        
    Returns:
        MedicalAICrew instance
    """
    return MedicalAICrew(rag_retriever=rag_retriever)


if __name__ == "__main__":
    # Test the crew
    print("Initializing Medical AI Crew...")
    crew = create_medical_crew()
    
    print("\nTest 1: Greeting")
    response = crew.process_message("Hello, my name is John Smith")
    print(f"Response: {response}")
    
    print("\nTest 2: Medical Question")
    response = crew.process_message("What should I do if I have swelling in my legs?")
    print(f"Response: {response}")

