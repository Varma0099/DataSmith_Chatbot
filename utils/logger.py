"""
Comprehensive Logging System
Tracks all interactions, agent activities, and system events
"""
import logging
import os
from datetime import datetime
from typing import Optional
import json


class MedicalAILogger:
    """Centralized logging for the Medical AI system"""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize the logging system.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Create formatters
        self.detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        self.simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Setup different loggers
        self.system_logger = self._setup_logger("system", "system.log")
        self.conversation_logger = self._setup_logger("conversation", "conversations.log")
        self.agent_logger = self._setup_logger("agents", "agent_activity.log")
        self.error_logger = self._setup_logger("errors", "errors.log", level=logging.ERROR)
        
    def _setup_logger(self, name: str, filename: str, level=logging.INFO) -> logging.Logger:
        """Setup a logger with file handler"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Remove 
        logger.handlers = []
        
        # File handler
        file_handler = logging.FileHandler(
            os.path.join(self.log_dir, filename),
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(self.detailed_formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        if level >= logging.ERROR:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(self.simple_formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def log_conversation(
        self, 
        user_message: str, 
        agent_response: str, 
        agent_type: str,
        user_id: Optional[str] = None,
        metadata: Optional[dict] = None
    ):
        """
        Log a conversation interaction.
        
        Args:
            user_message: The user's message
            agent_response: The agent's response
            agent_type: Type of agent (receptionist/clinical)
            user_id: Optional user identifier
            metadata: Additional metadata to log
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id or "anonymous",
            "agent_type": agent_type,
            "user_message": user_message,
            "agent_response": agent_response,
            "metadata": metadata or {}
        }
        
        self.conversation_logger.info(json.dumps(log_entry, ensure_ascii=False))
        self.system_logger.info(
            f"Conversation logged - Agent: {agent_type}, User: {user_id or 'anonymous'}"
        )
    
    def log_patient_lookup(self, patient_name: str, success: bool, user_id: Optional[str] = None):
        """Log patient record lookup attempts"""
        status = "SUCCESS" if success else "FAILED"
        self.agent_logger.info(
            f"Patient lookup - Name: {patient_name}, Status: {status}, User: {user_id or 'anonymous'}"
        )
    
    def log_web_search(self, query: str, user_id: Optional[str] = None):
        """Log web search queries"""
        self.agent_logger.info(
            f"Web search performed - Query: '{query}', User: {user_id or 'anonymous'}"
        )
    
    def log_rag_query(self, query: str, num_results: int, user_id: Optional[str] = None):
        """Log RAG system queries"""
        self.agent_logger.info(
            f"RAG query - Query: '{query}', Results: {num_results}, User: {user_id or 'anonymous'}"
        )
    
    def log_error(self, error: Exception, context: str = "", user_id: Optional[str] = None):
        """
        Log an error with context.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
            user_id: Optional user identifier
        """
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id or "anonymous",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context
        }
        
        self.error_logger.error(json.dumps(error_entry, ensure_ascii=False), exc_info=True)
    
    def log_system_event(self, event: str, details: Optional[dict] = None):
        """Log system events"""
        event_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details or {}
        }
        self.system_logger.info(json.dumps(event_entry, ensure_ascii=False))
    
    def log_agent_activity(
        self, 
        agent_name: str, 
        action: str, 
        details: Optional[dict] = None,
        user_id: Optional[str] = None
    ):
        """
        Log agent activity.
        
        Args:
            agent_name: Name of the agent
            action: Action performed
            details: Additional details
            user_id: Optional user identifier
        """
        activity_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
            "user_id": user_id or "anonymous",
            "details": details or {}
        }
        self.agent_logger.info(json.dumps(activity_entry, ensure_ascii=False))


# Global logger instance
_global_logger = None


def get_logger() -> MedicalAILogger:
    """Get or create the global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = MedicalAILogger()
        _global_logger.log_system_event("Logger initialized")
    return _global_logger


if __name__ == "__main__":
    # Test the logger
    logger = get_logger()
    
    logger.log_system_event("System startup", {"version": "1.0.0"})
    logger.log_conversation(
        user_message="Hello, I'm John Smith",
        agent_response="Welcome Mr. Smith! I've retrieved your discharge summary.",
        agent_type="receptionist",
        user_id="test_user_001"
    )
    logger.log_patient_lookup("John Smith", success=True, user_id="test_user_001")
    logger.log_web_search("chronic kidney disease diet", user_id="test_user_001")
    
    print("Test logs created successfully. Check the logs/ directory.")

