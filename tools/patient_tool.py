"""
Patient Report Retrieval Tool
Retrieves discharge summaries for patients by name
"""
import json
import os
from typing import Optional


def get_patient_report(patient_name: str) -> str:
    """
    Retrieve patient's discharge report by name.
    
    Args:
        patient_name: The full name of the patient (case-insensitive)
        
    Returns:
        JSON string with patient information or error message
    """
    try:
        # project root
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        patient_file = os.path.join(current_dir, "data", "patients.json")
        
        with open(patient_file, 'r') as f:
            patients = json.load(f)
        
        # Search for patient
        patient_name_lower = patient_name.lower().strip()
        matches = [p for p in patients if p["patient_name"].lower() == patient_name_lower]
        
        if len(matches) == 0:
            return f"❌ No patient found with name '{patient_name}'. Please check the spelling and try again."
        elif len(matches) > 1:
            return f"⚠️ Multiple patients found with name '{patient_name}'. Please provide more specific information (e.g., patient ID)."
        
        # Format the patient
        patient = matches[0]
        report = f"""
✅ **Patient Discharge Summary Found**

**Patient Information:**
- Patient ID: {patient['patient_id']}
- Name: {patient['patient_name']}
- Age: {patient['age']} years old
- Gender: {patient['gender']}
- Discharge Date: {patient['discharge_date']}

**Medical Information:**
- Primary Diagnosis: {patient['primary_diagnosis']}
- Secondary Diagnosis: {patient['secondary_diagnosis']}

**Medications:**
{chr(10).join([f"  • {med}" for med in patient['medications']])}

**Dietary Restrictions:**
{patient['dietary_restrictions']}

**Warning Signs to Watch For:**
{patient['warning_signs']}

**Follow-up:**
- Date: {patient['follow_up_date']}
- Doctor: {patient['doctor']}

---
📋 This discharge summary is retrieved from hospital records.
"""
        return report
        
    except FileNotFoundError:
        return "❌ Error: Patient database file not found. Please contact system administrator."
    except json.JSONDecodeError:
        return "❌ Error: Patient database is corrupted. Please contact system administrator."
    except Exception as e:
        return f"❌ Error retrieving patient information: {str(e)}"


def search_patient_by_id(patient_id: str) -> str:
    """
    Retrieve patient's discharge report by patient ID.
    
    Args:
        patient_id: The patient ID (e.g., P001)
        
    Returns:
        JSON string with patient information or error message
    """
    try:
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        patient_file = os.path.join(current_dir, "data", "patients.json")
        
        with open(patient_file, 'r') as f:
            patients = json.load(f)
        
        matches = [p for p in patients if p["patient_id"].upper() == patient_id.upper()]
        
        if len(matches) == 0:
            return f"❌ No patient found with ID '{patient_id}'."
        
        patient = matches[0]
        return json.dumps(patient, indent=2)
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


if __name__ == "__main__":
    # Test the tool
    print("Testing patient lookup tool...")
    print("\n" + "="*60)
    result = get_patient_report("John Smith")
    print(result)

