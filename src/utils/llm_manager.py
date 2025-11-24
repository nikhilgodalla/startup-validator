# src/utils/llm_manager.py
"""
LLM Manager - Handles all LLM interactions with fallback options
"""
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from config.settings import config
import time

class LLMManager:
    """Manages LLM connections with fallback options"""
    
    def __init__(self):
        self.primary_provider = config.DEFAULT_LLM
        self.llm_cache = {}
        
    def get_llm(self, model_type="default", temperature=0.7):
        """
        Get an LLM instance with automatic fallback
        
        Args:
            model_type: "fast", "smart", or "default"
            temperature: LLM temperature (0-1)
        """
        cache_key = f"{self.primary_provider}_{model_type}_{temperature}"
        
        # Return cached LLM if available
        if cache_key in self.llm_cache:
            return self.llm_cache[cache_key]
        
        # Try primary provider
        try:
            if self.primary_provider == "groq" and config.GROQ_API_KEY:
                model_name = config.MODELS["groq"][model_type]
                llm = ChatGroq(
                    groq_api_key=config.GROQ_API_KEY,
                    model_name=model_name,
                    temperature=temperature,
                    max_tokens=4096,
                    timeout=30,
                    max_retries=2,
                )
                self.llm_cache[cache_key] = llm
                return llm
                
            elif self.primary_provider == "openai" and config.OPENAI_API_KEY:
                model_name = config.MODELS["openai"][model_type]
                llm = ChatOpenAI(
                    api_key=config.OPENAI_API_KEY,
                    model=model_name,
                    temperature=temperature
                )
                self.llm_cache[cache_key] = llm
                return llm
                
        except Exception as e:
            print(f"⚠️ Primary LLM failed: {e}")
            
        # Fallback options
        return self._get_fallback_llm(temperature)
    
    def _get_fallback_llm(self, temperature):
        """Get fallback LLM if primary fails"""
        
        # Try alternative Groq model
        if config.GROQ_API_KEY:
            try:
                llm = ChatGroq(
                    groq_api_key=config.GROQ_API_KEY,
                    model_name="llama-3.1-8b-instant",  # Fallback model
                    temperature=temperature
                )
                print("ℹ️ Using fallback Groq model")
                return llm
            except:
                pass
        
        # If all fails, raise error
        raise Exception("No LLM available. Please check your API keys.")
    
    def test_connection(self):
        """Test LLM connection"""
        try:
            llm = self.get_llm("fast")
            response = llm.invoke("Respond with 'OK' if you're working")
            return "OK" in response.content
        except Exception as e:
            print(f"LLM test failed: {e}")
            return False

# Global instance
llm_manager = LLMManager()