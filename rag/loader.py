"""
RAG (Retrieval-Augmented Generation) Loader
Processes nephrology reference materials and creates vector database
"""
import os
from typing import Optional, List
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


class NephrologyRAG:
    """RAG system for nephrology knowledge base"""
    
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize the RAG system.
        
        Args:
            persist_directory: Directory to store the vector database
        """
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.vectorstore = None
        
    def load_documents_from_pdf(self, pdf_path: str) -> List:
        """
        Load documents from a single PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of documents
        """
        print(f"Loading PDF from: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from PDF")
        return documents
    
    def load_documents_from_directory(self, directory_path: str) -> List:
        """
        Load all PDF documents from a directory.
        
        Args:
            directory_path: Path to directory containing PDFs
            
        Returns:
            List of documents
        """
        print(f"Loading PDFs from directory: {directory_path}")
        loader = DirectoryLoader(
            directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from directory")
        return documents
    
    def create_vector_database(self, documents: List, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Create vector database from documents.
        
        Args:
            documents: List of documents to process
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        print("Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        texts = text_splitter.split_documents(documents)
        print(f"Created {len(texts)} text chunks")
        
        print("Creating vector embeddings and storing in ChromaDB...")
        self.vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        print(f"Vector database created and persisted to {self.persist_directory}")
    
    def load_existing_database(self):
        """Load an existing vector database."""
        if os.path.exists(self.persist_directory):
            print(f"Loading existing vector database from {self.persist_directory}")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print("Vector database loaded successfully")
            return True
        else:
            print(f"No existing database found at {self.persist_directory}")
            return False
    
    def get_retriever(self, k: int = 3):
        """
        Get a retriever for the vector database.
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            Retriever object
        """
        if self.vectorstore is None:
            if not self.load_existing_database():
                raise ValueError("No vector database available. Please create one first.")
        
        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def query(self, query: str, k: int = 3) -> List[str]:
        """
        Query the vector database.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant document chunks
        """
        if self.vectorstore is None:
            if not self.load_existing_database():
                return ["No knowledge base available."]
        
        results = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]


def create_sample_nephrology_content():
    """
    Create sample nephrology content when no PDF is available.
    This is for demonstration purposes.
    """
    return """
# Nephrology Clinical Guide

## Chronic Kidney Disease (CKD)

### Definition
Chronic Kidney Disease is defined as abnormalities of kidney structure or function, present for more than 3 months, 
with implications for health. CKD is classified into 5 stages based on GFR (Glomerular Filtration Rate).

### Stages of CKD
- Stage 1: GFR ≥90 mL/min/1.73m² with kidney damage
- Stage 2: GFR 60-89 mL/min/1.73m² with kidney damage
- Stage 3a: GFR 45-59 mL/min/1.73m²
- Stage 3b: GFR 30-44 mL/min/1.73m²
- Stage 4: GFR 15-29 mL/min/1.73m²
- Stage 5: GFR <15 mL/min/1.73m² or on dialysis

### Management Principles
1. Blood Pressure Control: Target BP <130/80 mmHg
2. ACE inhibitors or ARBs for proteinuria
3. Dietary modifications: Protein restriction, sodium limitation
4. Management of complications: Anemia, bone disease, electrolyte disorders
5. Preparation for renal replacement therapy when appropriate

### Dietary Recommendations
- Sodium: <2g per day for most CKD patients
- Protein: 0.6-0.8 g/kg/day for Stage 3-5 CKD not on dialysis
- Potassium: Restrict to <2000mg/day in advanced CKD
- Phosphorus: <800-1000mg/day in Stage 3-5 CKD
- Fluid: Restriction based on urine output and dialysis status

### Warning Signs for Patients
Patients should seek immediate medical attention for:
- Severe swelling (edema) in legs, ankles, or around eyes
- Shortness of breath or difficulty breathing
- Chest pain or pressure
- Confusion or decreased alertness
- Severe nausea and vomiting
- Decreased or no urine output

## Dialysis

### Hemodialysis
Hemodialysis removes waste products and excess fluid from blood using an external filter (dialyzer).
- Frequency: Typically 3 times per week, 3-4 hours per session
- Access: Arteriovenous fistula (preferred), AV graft, or central venous catheter
- Diet: Strict potassium, phosphorus, and fluid restrictions

### Peritoneal Dialysis
Uses the peritoneal membrane as a natural filter.
- Types: Continuous Ambulatory PD (CAPD) or Automated PD (APD)
- Advantages: More flexible schedule, done at home
- Diet: Less restrictive, higher protein needs
- Complications: Peritonitis (watch for cloudy dialysate)

## Common Kidney Conditions

### Acute Kidney Injury (AKI)
Sudden decrease in kidney function over hours to days.
- Causes: Dehydration, medications, obstruction, sepsis
- Management: Treat underlying cause, fluid management, avoid nephrotoxins
- Most cases are reversible with prompt treatment

### Diabetic Nephropathy
Kidney damage from long-standing diabetes.
- Prevention: Tight glucose control (HbA1c <7%)
- Treatment: ACE inhibitors/ARBs, BP control
- Monitoring: Annual urine albumin and eGFR testing

### Hypertensive Nephrosclerosis
Kidney damage from chronic high blood pressure.
- Treatment: Aggressive BP control, lifestyle modifications
- Target BP: <130/80 mmHg

### Polycystic Kidney Disease (PKD)
Genetic disorder causing multiple kidney cysts.
- Autosomal Dominant PKD most common
- Treatment: BP control, tolvaptan in select cases
- Complications: Pain, hematuria, infections

### Kidney Stones (Nephrolithiasis)
- Types: Calcium oxalate (most common), uric acid, struvite, cystine
- Prevention: High fluid intake (2.5-3L/day), dietary modifications
- Treatment: Pain control, medical expulsive therapy, lithotripsy, surgery

## Medications in CKD

### Medications That Protect Kidneys
- ACE Inhibitors: Lisinopril, enalapril, ramipril
- ARBs: Losartan, valsartan, irbesartan
- SGLT2 Inhibitors: May slow CKD progression in diabetics

### Medications Requiring Dose Adjustment
Many medications require dose adjustment based on kidney function:
- Antibiotics (many)
- Antidiabetic drugs (metformin, others)
- Anticoagulants (NOACs)
- Pain medications

### Medications to Avoid
- NSAIDs (ibuprofen, naproxen) - can worsen kidney function
- Some antibiotics (aminoglycosides) - nephrotoxic
- Contrast dye (when possible) - can cause contrast-induced nephropathy

## Post-Discharge Care

### Follow-Up Importance
Regular follow-up is crucial for:
- Monitoring kidney function (blood tests)
- Adjusting medications
- Managing complications
- Planning for dialysis or transplant if needed

### Self-Care at Home
1. Take medications as prescribed
2. Monitor blood pressure daily
3. Follow dietary restrictions
4. Track fluid intake/output if instructed
5. Report warning signs promptly
6. Attend all follow-up appointments

### When to Call Your Doctor
- New or worsening swelling
- Significant weight gain (>3 lbs in one day)
- Decreased urine output
- Severe fatigue or weakness
- Confusion or altered mental status
- Fever or signs of infection

## Emergency Situations

Seek immediate emergency care for:
- Chest pain or pressure
- Severe shortness of breath
- Altered consciousness
- Seizures
- Severe uncontrolled bleeding (especially dialysis patients)
- Signs of severe hyperkalemia (irregular heartbeat, severe weakness)

This guide is for educational purposes. Always follow your healthcare provider's specific instructions.
"""


def setup_rag_system(pdf_directory: str = "references", force_recreate: bool = False):
    """
    Setup the RAG system with nephrology knowledge.
    
    Args:
        pdf_directory: Directory containing PDF files
        force_recreate: Force recreation of vector database even if it exists
        
    Returns:
        NephrologyRAG instance
    """
    rag = NephrologyRAG()
    
    # Check if database already exists
    if os.path.exists(rag.persist_directory) and not force_recreate:
        print("Existing vector database found. Loading...")
        rag.load_existing_database()
        return rag
    
    # Check for PDF files
    if os.path.exists(pdf_directory) and os.listdir(pdf_directory):
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
        if pdf_files:
            print(f"Found {len(pdf_files)} PDF file(s) in {pdf_directory}")
            documents = rag.load_documents_from_directory(pdf_directory)
            rag.create_vector_database(documents)
            return rag
    
    # Fallback: Create sample content
    print("No PDF files found. Creating sample nephrology knowledge base...")
    from langchain.schema import Document
    
    sample_content = create_sample_nephrology_content()
    documents = [Document(page_content=sample_content, metadata={"source": "sample"})]
    
    rag.create_vector_database(documents, chunk_size=500, chunk_overlap=100)
    return rag


if __name__ == "__main__":
    # Test the RAG system
    print("Setting up RAG system...")
    rag = setup_rag_system()
    
    print("\nTesting query...")
    results = rag.query("What are the warning signs of kidney disease?", k=2)
    
    print("\n" + "="*60)
    print("Query Results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result[:200]}...")

