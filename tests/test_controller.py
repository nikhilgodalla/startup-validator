# test_controller.py
from src.agents.controller import ControllerAgent

def test_controller():
    """Test the controller agent"""
    
    print("=" * 50)
    print("Testing Controller Agent")
    print("=" * 50)
    
    # Initialize controller
    controller = ControllerAgent()
    print("✅ Controller initialized")
    
    # Test with a sample idea
    test_idea = "An AI-powered personal finance app for millennials that helps them save money"
    
    print(f"\nTesting with idea: {test_idea}")
    print("-" * 50)
    
    # Start validation
    result = controller.start_validation(test_idea)
    
    # Display results
    print("\nValidation Results:")
    print(f"Score: {result.get('score', 'N/A')}/10")
    print(f"Verdict: {result.get('verdict', 'N/A')}")
    print(f"Execution Time: {result.get('execution_time', 'N/A')} seconds")
    
    print("\n✅ Controller test complete!")

if __name__ == "__main__":
    test_controller()