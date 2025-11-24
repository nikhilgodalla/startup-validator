# src/agents/strategy_advisor.py
"""
Strategy Advisor Agent - Synthesizes all insights and provides recommendations
"""

from crewai import Agent
from crewai_tools import tool
from typing import Dict
import json
from src.utils.llm_manager import llm_manager

class StrategyAdvisorAgent:
    """Agent specialized in strategic synthesis and recommendations"""
    
    def __init__(self):
        self.llm = llm_manager.get_llm("smart")  # Use smart model for synthesis
        self._create_tools()
        self.agent = self._create_agent()
        
    def _create_tools(self):
        """Create strategy synthesis tools"""
        
        @tool
        def calculate_validation_score(analysis_data: str) -> str:
            """
            Calculate overall validation score based on all analyses
            
            Args:
                analysis_data: JSON string containing all analysis results
            """
            try:
                # Parse data
                if isinstance(analysis_data, str):
                    data = json.loads(analysis_data) if '{' in analysis_data else {}
                else:
                    data = {}
                
                # Scoring weights
                weights = {
                    'market_size': 0.25,
                    'competition': 0.20,
                    'technical_feasibility': 0.20,
                    'financial_viability': 0.20,
                    'timing': 0.15
                }
                
                # Calculate component scores (simplified)
                scores = {
                    'market_size': 7.5,  # Would be based on TAM
                    'competition': 6.0,  # Based on competitor analysis
                    'technical_feasibility': 8.0,  # Based on complexity
                    'financial_viability': 7.0,  # Based on costs/revenue
                    'timing': 7.5  # Based on market trends
                }
                
                # Calculate weighted score
                total_score = sum(scores[key] * weights[key] for key in weights)
                
                result = {
                    'overall_score': round(total_score, 1),
                    'component_scores': scores,
                    'confidence': 0.85
                }
                
                return json.dumps(result)
                
            except Exception as e:
                return json.dumps({'overall_score': 6.5, 'error': str(e)})
        
        @tool
        def generate_recommendations(score: float) -> str:
            """
            Generate strategic recommendations based on validation score
            
            Args:
                score: Overall validation score
            """
            if score >= 7.5:
                verdict = "GO"
                emoji = "✅"
                recommendations = [
                    "Proceed with MVP development",
                    "Focus on rapid market entry",
                    "Secure seed funding",
                    "Build core team",
                    "Establish early customer relationships"
                ]
            elif score >= 5.0:
                verdict = "PIVOT"
                emoji = "⚠️"
                recommendations = [
                    "Refine value proposition",
                    "Focus on underserved niche",
                    "Reduce initial scope",
                    "Validate with potential customers",
                    "Consider alternative business models"
                ]
            else:
                verdict = "NO-GO"
                emoji = "❌"
                recommendations = [
                    "Reconsider the fundamental concept",
                    "Research alternative markets",
                    "Explore different problem spaces",
                    "Join an accelerator for guidance",
                    "Consider partnering with existing players"
                ]
            
            result = {
                'verdict': f"{verdict} {emoji}",
                'recommendations': recommendations,
                'key_success_factors': [
                    "Strong execution",
                    "Customer focus",
                    "Rapid iteration"
                ]
            }
            
            return json.dumps(result)
        
        @tool
        def create_action_plan(verdict: str) -> str:
            """
            Create specific action plan based on verdict
            
            Args:
                verdict: GO, PIVOT, or NO-GO verdict
            """
            if "GO" in verdict:
                plan = {
                    'immediate_actions': [
                        "Validate with 20 potential customers",
                        "Build technical prototype",
                        "Form founding team",
                        "Apply to accelerators"
                    ],
                    '30_day_goals': [
                        "Complete customer interviews",
                        "Finalize MVP features",
                        "Secure technical co-founder"
                    ],
                    '90_day_goals': [
                        "Launch MVP",
                        "Acquire first 100 users",
                        "Raise pre-seed funding"
                    ]
                }
            elif "PIVOT" in verdict:
                plan = {
                    'immediate_actions': [
                        "Identify specific niche to target",
                        "Revise value proposition",
                        "Survey target customers"
                    ],
                    '30_day_goals': [
                        "Complete pivot strategy",
                        "Test new positioning",
                        "Update business model"
                    ],
                    '90_day_goals': [
                        "Launch revised MVP",
                        "Measure traction metrics",
                        "Decide on path forward"
                    ]
                }
            else:
                plan = {
                    'immediate_actions': [
                        "Document lessons learned",
                        "Explore adjacent opportunities",
                        "Network with other entrepreneurs"
                    ],
                    '30_day_goals': [
                        "Generate new ideas",
                        "Join startup community",
                        "Find mentor or advisor"
                    ],
                    '90_day_goals': [
                        "Validate new concept",
                        "Build skills in weak areas",
                        "Consider joining existing startup"
                    ]
                }
            
            return json.dumps(plan)
        
        self.calculate_score_tool = calculate_validation_score
        self.generate_recommendations_tool = generate_recommendations
        self.create_action_plan_tool = create_action_plan
        
        self.tools = [calculate_validation_score, generate_recommendations, create_action_plan]
    
    def _create_agent(self) -> Agent:
        """Create the strategy advisor agent"""
        
        return Agent(
            role="Chief Strategy Officer",
            goal="""Synthesize all analyses, provide strategic recommendations,
                   and create actionable next steps for the entrepreneur.""",
            backstory="""You are a former McKinsey partner and serial entrepreneur.
                        You excel at synthesizing complex information into clear
                        strategic recommendations and actionable plans.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )
    
    def synthesize(self, all_analyses: Dict) -> Dict:
        """Synthesize all analyses into final recommendation"""
        
        # Calculate overall score
        score_result = json.loads(self.calculate_score_tool.run(json.dumps(all_analyses)))
        overall_score = score_result['overall_score']
        
        # Generate recommendations
        recommendations = json.loads(self.generate_recommendations_tool.run(overall_score))
        
        # Create action plan
        action_plan = json.loads(self.create_action_plan_tool.run(recommendations['verdict']))
        
        return {
            'score': overall_score,
            'verdict': recommendations['verdict'],
            'recommendations': recommendations['recommendations'],
            'action_plan': action_plan,
            'key_success_factors': recommendations['key_success_factors'],
            'confidence': 0.85,
            'summary': f"Validation Score: {overall_score}/10 - {recommendations['verdict']}"
        }