# test_llm.py
from src.utils.llm_manager import llm_manager

def test_llm_manager():
    """Test LLM manager functionality"""
    
    print("Testing LLM Manager...")
    print("-" * 40)
    
    # Test connection
    if llm_manager.test_connection():
        print("✅ LLM connection successful")
    else:
        print("❌ LLM connection failed")
        return
    
    # Test different model types
    for model_type in ["fast", "smart", "default"]:
        try:
            llm = llm_manager.get_llm(model_type)
            response = llm.invoke(f"Say 'Model {model_type} working!'")
            print(f"✅ {model_type.upper()} model: {response.content}")
        except Exception as e:
            print(f"⚠️ {model_type.upper()} model error: {e}")
    
    print("-" * 40)
    print("LLM Manager test complete!")

if __name__ == "__main__":
    test_llm_manager()