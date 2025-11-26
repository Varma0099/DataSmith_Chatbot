"""
Setup script for Medical AI POC
Creates necessary directories and initializes the system
"""
import os
import sys


def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        "data",
        "references",
        "tools",
        "agents",
        "rag",
        "logs",
        "utils",
        "frontend"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created/verified directory: {directory}/")


def check_env_file():
    """Check if .env file exists, if not, create from example"""
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            print("\n⚠️  No .env file found!")
            print("📝 Please create a .env file with your API keys:")
            print("   1. Copy env.example to .env")
            print("   2. Add your OpenAI API key")
            print("   3. (Optional) Add your Tavily API key")
            print("\nExample:")
            print("   copy env.example .env     (Windows)")
            print("   cp env.example .env       (Linux/Mac)")
        return False
    else:
        print("✓ .env file found")
        return True


def check_dependencies():
    """Check if key dependencies are installed"""
    required_packages = [
        "streamlit",
        "langchain",
        "crewai",
        "chromadb",
        "sentence_transformers",
        "openai"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package} installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} not installed")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True


def main():
    """Main setup function"""
    print("=" * 60)
    print("🏥 Medical AI POC - Setup Script")
    print("=" * 60)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Checking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n3. Checking environment configuration...")
    env_ok = check_env_file()
    
    print("\n" + "=" * 60)
    if deps_ok and env_ok:
        print("✅ Setup complete! You can now run:")
        print("   streamlit run app_streamlit.py")
    else:
        print("⚠️  Setup incomplete. Please address the issues above.")
    print("=" * 60)


if __name__ == "__main__":
    main()

