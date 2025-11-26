"""
Web Search Tool for Medical Information
Uses Tavily API for real-time medical information retrieval
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def web_search(query: str, max_results: int = 3) -> str:
    """
    Search the web for up-to-date medical information.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 3)
        
    Returns:
        Formatted string with search results including titles, content, and URLs
    """
    try:
        # Try to use Tavily API
        tavily_key = os.getenv("TAVILY_API_KEY")
        
        if tavily_key and tavily_key != "your-tavily-api-key-here":
            try:
                from tavily import TavilyClient
                
                client = TavilyClient(api_key=tavily_key)
                results = client.search(
                    query=query,
                    max_results=max_results,
                    search_depth="advanced",
                    include_domains=["mayoclinic.org", "kidney.org", "niddk.nih.gov", "ncbi.nlm.nih.gov"]
                )
                
                if not results.get("results"):
                    return "⚠️ No search results found. Please rephrase your query."
                
                formatted_results = "🔍 **Web Search Results:**\n\n"
                for i, result in enumerate(results["results"], 1):
                    formatted_results += f"**{i}. {result['title']}**\n"
                    formatted_results += f"   {result['content']}\n"
                    formatted_results += f"   🔗 Source: {result['url']}\n\n"
                
                return formatted_results
                
            except ImportError:
                pass  # Fall through to mock results
            except Exception as e:
                return f"⚠️ Web search temporarily unavailable: {str(e)}\nPlease rely on the knowledge base for now."
        
        # Fallback: Return helpful message if Tavily is not configured
        return _get_mock_search_results(query)
        
    except Exception as e:
        return f"❌ Error performing web search: {str(e)}"


def _get_mock_search_results(query: str) -> str:
    """
    Provide mock search results when Tavily API is not available.
    This is useful for development and testing.
    """
    query_lower = query.lower()
    
    # Provide relevant mock results based on common nephrology queries
    if any(word in query_lower for word in ["kidney", "renal", "nephro"]):
        return """🔍 **Web Search Results:**

**1. National Kidney Foundation - Kidney Disease Overview**
   Chronic kidney disease (CKD) affects millions worldwide. Key management includes blood pressure control, dietary modifications, and regular monitoring. Patients should watch for symptoms like swelling, fatigue, and changes in urination.
   🔗 Source: https://www.kidney.org/atoz/content/about-chronic-kidney-disease

**2. Mayo Clinic - Kidney Disease Symptoms and Causes**
   Signs and symptoms of kidney disease develop over time as kidney damage progresses slowly. Warning signs include nausea, fatigue, sleep problems, decreased mental sharpness, muscle cramps, and swelling of feet and ankles.
   🔗 Source: https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/

**3. NIDDK - Managing Chronic Kidney Disease**
   Managing CKD involves working with your healthcare team, taking medicines as prescribed, meeting with a dietitian, being physically active, and managing other health conditions like diabetes and high blood pressure.
   🔗 Source: https://www.niddk.nih.gov/health-information/kidney-disease/

⚠️ Note: Tavily API not configured. These are sample results. Configure TAVILY_API_KEY in .env for live search.
"""
    
    elif any(word in query_lower for word in ["dialysis", "hemodialysis"]):
        return """🔍 **Web Search Results:**

**1. National Kidney Foundation - What is Dialysis?**
   Dialysis is a treatment that filters and purifies the blood using a machine. This helps keep your fluids and electrolytes in balance when the kidneys can't do their job. Hemodialysis is typically done 3 times per week.
   🔗 Source: https://www.kidney.org/atoz/content/dialysisinfo

**2. American Kidney Fund - Hemodialysis Diet**
   People on hemodialysis need to limit fluids, potassium, phosphorus, and sodium. Working with a renal dietitian is essential to create a meal plan that meets your needs.
   🔗 Source: https://www.kidneyfund.org/prevention/hemodialysis-diet

⚠️ Note: Tavily API not configured. These are sample results. Configure TAVILY_API_KEY in .env for live search.
"""
    
    elif any(word in query_lower for word in ["medication", "medicine", "drug"]):
        return """🔍 **Web Search Results:**

**1. National Institute of Diabetes and Digestive and Kidney Diseases**
   Medications for CKD include ACE inhibitors or ARBs to control blood pressure and protect kidneys, phosphate binders, vitamin D supplements, and erythropoietin-stimulating agents for anemia.
   🔗 Source: https://www.niddk.nih.gov/health-information/kidney-disease/chronic-kidney-disease-ckd

**2. National Kidney Foundation - Medications to Avoid**
   People with kidney disease should avoid certain over-the-counter medications, especially NSAIDs like ibuprofen. Always consult your doctor before taking new medications.
   🔗 Source: https://www.kidney.org/atoz/content/medications-avoid

⚠️ Note: Tavily API not configured. These are sample results. Configure TAVILY_API_KEY in .env for live search.
"""
    
    else:
        return """🔍 **Web Search Results:**

**1. General Medical Information**
   For specific medical questions, please consult with your healthcare provider. Always follow your discharge instructions and contact your doctor if you experience concerning symptoms.
   🔗 Source: Medical Guidelines

⚠️ Note: Tavily API not configured. These are sample results. Configure TAVILY_API_KEY in .env for live search.
"""


if __name__ == "__main__":
    # Test the tool
    print("Testing web search tool...")
    print("\n" + "="*60)
    result = web_search("chronic kidney disease management")
    print(result)

