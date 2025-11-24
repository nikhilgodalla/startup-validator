# test_setup.py
"""Test if everything is installed correctly"""

def test_imports():
    """Test all required imports"""
    try:
        import crewai
        print("✅ CrewAI installed")
        
        import langchain
        print("✅ LangChain installed")
        
        import chromadb
        print("✅ ChromaDB installed")
        
        import streamlit
        print("✅ Streamlit installed")
        
        import plotly
        print("✅ Plotly installed")
        
        from duckduckgo_search import DDGS
        print("✅ DuckDuckGo search installed")
        
        print("\n✅ All packages installed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        return False

def test_api_keys():
    """Test API key configuration"""
    from config.settings import config
    
    if config.GROQ_API_KEY:
        print(f"✅ Groq API key configured: {config.GROQ_API_KEY[:10]}...")
    else:
        print("⚠️  Groq API key not set (required for FREE LLM)")
    
    if config.SERPER_API_KEY:
        print(f"✅ Serper API key configured: {config.SERPER_API_KEY[:10]}...")
    else:
        print("ℹ️  Serper API key not set (optional)")

# Update the test_groq_connection function in test_setup.py
def test_groq_connection():
    """Test Groq API connection"""
    from langchain_groq import ChatGroq
    from config.settings import config
    
    if not config.GROQ_API_KEY:
        print("⚠️  Skipping Groq test - no API key")
        return
    
    try:
        llm = ChatGroq(
            groq_api_key=config.GROQ_API_KEY,
            model_name="llama-3.1-8b-instant"  # Updated model name
        )
        response = llm.invoke("Say 'Hello, World!' if you're working")
        print(f"✅ Groq API working: {response.content}")
    except Exception as e:
        print(f"❌ Groq API error: {e}")
if __name__ == "__main__":
    print("=" * 50)
    print("🔧 TESTING STARTUP VALIDATOR SETUP")
    print("=" * 50)
    
    print("\n📦 Testing package imports...")
    test_imports()
    
    print("\n🔑 Testing API keys...")
    test_api_keys()
    
    print("\n🤖 Testing LLM connection...")
    test_groq_connection()
    
    print("\n" + "=" * 50)
    print("Setup test complete!")