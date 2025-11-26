import os
from config import validate_config, GOOGLE_API_KEY

def check_health():
    """Check system health before startup"""
    checks = {
        "config": False,
        "api_key": False,
        "directories": False
    }
    
    try:
        validate_config()
        checks["config"] = True
    except Exception as e:
        print(f"Config check failed: {e}")
    
    checks["api_key"] = bool(GOOGLE_API_KEY)
    
    required_dirs = ["data", "logs", "utils", "agents"]
    checks["directories"] = all(os.path.exists(d) for d in required_dirs)
    
    return all(checks.values()), checks

if __name__ == "__main__":
    success, results = check_health()
    print(f"Health Check: {'✅ PASS' if success else '❌ FAIL'}")
    for check, status in results.items():
        print(f"  {check}: {'✅' if status else '❌'}")