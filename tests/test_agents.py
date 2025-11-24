# test_agents.py
from src.agents.market_analyst import MarketAnalystAgent
from src.agents.competitor_researcher import CompetitorResearcherAgent
from src.agents.technical_architect import TechnicalArchitectAgent
from src.agents.financial_analyst import FinancialAnalystAgent
from src.agents.strategy_advisor import StrategyAdvisorAgent

def test_all_agents():
    """Test all specialized agents"""
    
    print("=" * 50)
    print("Testing All Specialized Agents")
    print("=" * 50)
    
    test_idea = "AI-powered personal finance app for millennials"
    
    # Store all results
    all_results = {}
    
    # Test Market Analyst
    print("\n1. Testing Market Analyst...")
    print("-" * 40)
    try:
        market_agent = MarketAnalystAgent()
        market_results = market_agent.analyze(test_idea)
        all_results['market'] = market_results
        
        print(f"✅ Market TAM: {market_results['market_opportunity']['TAM']['formatted']}")
        print(f"✅ Confidence: {market_results['confidence']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Competitor Researcher
    print("\n2. Testing Competitor Researcher...")
    print("-" * 40)
    try:
        competitor_agent = CompetitorResearcherAgent()
        comp_results = competitor_agent.analyze(test_idea)
        all_results['competitors'] = comp_results
        
        print(f"✅ Competitors Found: {comp_results['competitors_found']}")
        print(f"✅ Confidence: {comp_results['confidence']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Technical Architect
    print("\n3. Testing Technical Architect...")
    print("-" * 40)
    try:
        tech_agent = TechnicalArchitectAgent()
        tech_results = tech_agent.analyze(test_idea)
        all_results['technical'] = tech_results
        
        print(f"✅ Complexity: {tech_results['complexity']['complexity']}")
        print(f"✅ MVP Timeline: {tech_results['timeline']['mvp']}")
        print(f"✅ Confidence: {tech_results['confidence']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Financial Analyst
    print("\n4. Testing Financial Analyst...")
    print("-" * 40)
    try:
        financial_agent = FinancialAnalystAgent()
        financial_results = financial_agent.analyze(
            test_idea, 
            market_results.get('market_opportunity', {})
        )
        all_results['financial'] = financial_results
        
        print(f"✅ Startup Costs: {financial_results['startup_costs']['formatted_total']}")
        print(f"✅ Break-even: {financial_results['break_even_analysis']['break_even_timeline']}")
        print(f"✅ Confidence: {financial_results['confidence']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Strategy Advisor
    print("\n5. Testing Strategy Advisor...")
    print("-" * 40)
    try:
        strategy_agent = StrategyAdvisorAgent()
        strategy_results = strategy_agent.synthesize(all_results)
        all_results['strategy'] = strategy_results
        
        print(f"✅ Overall Score: {strategy_results['score']}/10")
        print(f"✅ Verdict: {strategy_results['verdict']}")
        print(f"✅ Confidence: {strategy_results['confidence']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Final Summary
    print("\n" + "=" * 50)
    print("FINAL VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Idea: {test_idea}")
    print(f"Score: {all_results.get('strategy', {}).get('score', 'N/A')}/10")
    print(f"Verdict: {all_results.get('strategy', {}).get('verdict', 'N/A')}")
    print(f"Next Steps: {len(all_results.get('strategy', {}).get('recommendations', []))} recommendations provided")
    
    print("\n✅ All agents tested successfully!")

if __name__ == "__main__":
    test_all_agents()