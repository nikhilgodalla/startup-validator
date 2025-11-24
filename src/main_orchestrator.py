# src/main_orchestrator.py
"""
Main Orchestrator - Updated to use real research agents
"""

from src.agents.controller import ControllerAgent

# Import BOTH versions - fixed for real research, original for others
try:
    # Try to import fixed versions first
    from src.agents.market_analyst_fixed import MarketAnalystAgent
    from src.agents.competitor_researcher_fixed import CompetitorResearcherAgent
    print("✅ Using REAL research agents (market & competitor)")
except ImportError:
    # Fallback to original if fixed versions don't exist
    from src.agents.market_analyst import MarketAnalystAgent
    from src.agents.competitor_researcher import CompetitorResearcherAgent
    print("⚠️ Using original agents (may have mock data)")

# Keep original agents for now (you can update these later)
from src.agents.technical_architect import TechnicalArchitectAgent
from src.agents.financial_analyst import FinancialAnalystAgent
from src.agents.strategy_advisor import StrategyAdvisorAgent

import time
from datetime import datetime
from typing import Dict
import os

class StartupValidatorOrchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        """Initialize all agents"""
        print("=" * 50)
        print("🚀 Initializing AI Startup Validator System...")
        print("=" * 50)
        
        # Check for API keys
        if os.getenv('SERPER_API_KEY'):
            print("✅ Serper API key found - will use real web search")
        else:
            print("⚠️ No Serper API key - will use fallback data")
        
        if os.getenv('GROQ_API_KEY'):
            print("✅ Groq API key found - using Groq LLMs")
        else:
            print("⚠️ No Groq API key - check your .env file")
        
        print("-" * 50)
        
        # Initialize agents
        print("Loading agents...")
        self.controller = ControllerAgent()
        print("  ✓ Controller Agent")
        
        self.market_analyst = MarketAnalystAgent()
        print("  ✓ Market Analyst (Real Research)")
        
        self.competitor_researcher = CompetitorResearcherAgent()
        print("  ✓ Competitor Researcher (Real Search)")
        
        self.technical_architect = TechnicalArchitectAgent()
        print("  ✓ Technical Architect")
        
        self.financial_analyst = FinancialAnalystAgent()
        print("  ✓ Financial Analyst")
        
        self.strategy_advisor = StrategyAdvisorAgent()
        print("  ✓ Strategy Advisor")
        
        print("-" * 50)
        print("✅ All agents initialized successfully!")
        print("=" * 50 + "\n")
    
    def validate_idea(self, startup_idea: str, progress_callback=None) -> Dict:
        """
        Main validation method that orchestrates all agents
        
        Args:
            startup_idea: The startup idea to validate
            progress_callback: Optional callback for progress updates
            
        Returns:
            Complete validation results with real research data
        """
        start_time = time.time()
        results = {
            'idea': startup_idea,
            'timestamp': datetime.now().isoformat(),
            'status': 'processing',
            'using_real_data': bool(os.getenv('SERPER_API_KEY'))
        }
        
        try:
            # Step 1: Market Analysis (REAL DATA)
            if progress_callback:
                progress_callback("🔍 Researching real market data...", 20)
            
            print(f"\n📊 Phase 1: Market Analysis")
            print(f"   Searching for real market data on: {startup_idea[:50]}...")
            market_results = self.market_analyst.analyze(startup_idea)
            results['market_analysis'] = market_results
            
            # Log if we got real data
            if market_results.get('market_research', {}).get('search_successful'):
                print(f"   ✅ Found real market data!")
                print(f"   - TAM: {market_results.get('market_opportunity', {}).get('TAM', {}).get('formatted', 'Unknown')}")
                print(f"   - Source: {market_results.get('data_source', 'Unknown')}")
            else:
                print(f"   ⚠️ Using fallback market data")
            
            # Step 2: Competitor Research (REAL SEARCH)
            if progress_callback:
                progress_callback("🎯 Finding real competitors...", 40)
            
            print(f"\n🎯 Phase 2: Competitor Research")
            print(f"   Searching for actual competitors...")
            competitor_results = self.competitor_researcher.analyze(startup_idea)
            results['competitor_analysis'] = competitor_results
            
            # Log competitors found
            comp_count = competitor_results.get('competitors_found', 0)
            if comp_count > 0:
                print(f"   ✅ Found {comp_count} real competitors!")
                for comp in competitor_results.get('competitor_list', [])[:3]:
                    print(f"      - {comp.get('name', 'Unknown')}")
            else:
                print(f"   ⚠️ No competitors found via search")
            
            # Step 3: Technical Assessment
            if progress_callback:
                progress_callback("⚙️ Assessing technical feasibility...", 60)
            
            print(f"\n⚙️ Phase 3: Technical Assessment")
            technical_results = self.technical_architect.analyze(startup_idea)
            results['technical_analysis'] = technical_results
            print(f"   - Complexity: {technical_results.get('complexity', {}).get('complexity', 'Unknown')}")
            print(f"   - MVP Timeline: {technical_results.get('timeline', {}).get('mvp', 'Unknown')}")
            
            # Step 4: Financial Projections (using real market data)
            if progress_callback:
                progress_callback("💰 Creating financial projections...", 80)
            
            print(f"\n💰 Phase 4: Financial Analysis")
            print(f"   Using market data: TAM = {market_results.get('market_opportunity', {}).get('TAM', {}).get('formatted', 'Unknown')}")
            financial_results = self.financial_analyst.analyze(
                startup_idea,
                market_results.get('market_opportunity', {})
            )
            results['financial_analysis'] = financial_results
            print(f"   - Initial Investment: {financial_results.get('startup_costs', {}).get('formatted_total', 'Unknown')}")
            print(f"   - Break-even: {financial_results.get('break_even_analysis', {}).get('break_even_timeline', 'Unknown')}")
            
            # Step 5: Strategic Synthesis
            if progress_callback:
                progress_callback("📊 Synthesizing recommendations...", 90)
            
            print(f"\n📊 Phase 5: Strategic Synthesis")
            all_analyses = {
                'market': market_results,
                'competitors': competitor_results,
                'technical': technical_results,
                'financial': financial_results
            }
            
            strategy_results = self.strategy_advisor.synthesize(all_analyses)
            results['strategy'] = strategy_results
            print(f"   - Score: {strategy_results.get('score', 0)}/10")
            print(f"   - Verdict: {strategy_results.get('verdict', 'Unknown')}")
            
            # Calculate execution time
            execution_time = time.time() - start_time
            results['execution_time'] = round(execution_time, 2)
            results['status'] = 'completed'
            
            # Add confidence score based on data quality
            results['confidence_score'] = self._calculate_overall_confidence(results)
            
            # Add overall summary
            results['summary'] = self._create_summary(results)
            
            if progress_callback:
                progress_callback("✅ Validation complete!", 100)
            
            print(f"\n" + "=" * 50)
            print(f"✅ VALIDATION COMPLETE in {execution_time:.1f} seconds")
            print(f"   Data Quality: {'REAL' if results['using_real_data'] else 'SIMULATED'}")
            print(f"   Confidence: {results['confidence_score']}%")
            print(f"=" * 50 + "\n")
            
            return results
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            results['status'] = 'error'
            results['error'] = str(e)
            return results
    
    def _calculate_overall_confidence(self, results: Dict) -> int:
        """Calculate overall confidence based on data quality"""
        
        confidence_scores = []
        
        # Check market data quality
        if results.get('market_analysis', {}).get('market_research', {}).get('search_successful'):
            confidence_scores.append(90)
        else:
            confidence_scores.append(60)
        
        # Check competitor data quality
        if results.get('competitor_analysis', {}).get('competitors_found', 0) >= 3:
            confidence_scores.append(85)
        elif results.get('competitor_analysis', {}).get('competitors_found', 0) > 0:
            confidence_scores.append(70)
        else:
            confidence_scores.append(50)
        
        # Add other agent confidences
        for key in ['technical_analysis', 'financial_analysis', 'strategy']:
            if key in results and 'confidence' in results[key]:
                confidence_scores.append(results[key]['confidence'] * 100)
        
        return int(sum(confidence_scores) / len(confidence_scores)) if confidence_scores else 50
    
    def _create_summary(self, results: Dict) -> Dict:
        """Create executive summary from all results"""
        
        # Check if we used real data
        real_market_data = results.get('market_analysis', {}).get('data_source', '').startswith('Real')
        real_competitor_data = results.get('competitor_analysis', {}).get('data_source', '').startswith('Real')
        
        return {
            'score': results.get('strategy', {}).get('score', 0),
            'verdict': results.get('strategy', {}).get('verdict', 'Unknown'),
            'market_size': results.get('market_analysis', {}).get('market_opportunity', {}).get('TAM', {}).get('formatted', 'Unknown'),
            'competitors_found': results.get('competitor_analysis', {}).get('competitors_found', 0),
            'technical_complexity': results.get('technical_analysis', {}).get('complexity', {}).get('complexity', 'Unknown'),
            'initial_investment': results.get('financial_analysis', {}).get('startup_costs', {}).get('formatted_total', 'Unknown'),
            'break_even': results.get('financial_analysis', {}).get('break_even_analysis', {}).get('break_even_timeline', 'Unknown'),
            'top_recommendations': results.get('strategy', {}).get('recommendations', [])[:3],
            'data_quality': {
                'market': 'Real Research' if real_market_data else 'Estimated',
                'competitors': 'Real Search' if real_competitor_data else 'Estimated'
            }
        }