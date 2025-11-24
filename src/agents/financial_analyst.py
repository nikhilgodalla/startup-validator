# src/agents/financial_analyst.py
"""
Financial Analyst Agent - Creates financial projections
"""

from crewai import Agent
from crewai_tools import tool
from typing import Dict
import json
from src.utils.llm_manager import llm_manager

class FinancialAnalystAgent:
    """Agent specialized in financial analysis and projections"""
    
    def __init__(self):
        self.llm = llm_manager.get_llm("fast")
        self._create_tools()
        self.agent = self._create_agent()
        
    def _create_tools(self):
        """Create financial analysis tools"""
        
        @tool
        def calculate_startup_costs(idea_type: str) -> str:
            """
            Calculate initial startup costs
            
            Args:
                idea_type: Type of startup (saas, marketplace, app, etc)
            """
            idea_lower = idea_type.lower()
            
            # Base costs by type
            if 'marketplace' in idea_lower or 'platform' in idea_lower:
                costs = {
                    'development': 50000,
                    'marketing': 20000,
                    'operations': 15000,
                    'legal': 10000,
                    'other': 5000
                }
            elif 'app' in idea_lower or 'mobile' in idea_lower:
                costs = {
                    'development': 30000,
                    'marketing': 15000,
                    'operations': 10000,
                    'legal': 5000,
                    'other': 5000
                }
            elif 'saas' in idea_lower or 'software' in idea_lower:
                costs = {
                    'development': 40000,
                    'marketing': 25000,
                    'operations': 10000,
                    'legal': 5000,
                    'other': 5000
                }
            else:
                costs = {
                    'development': 25000,
                    'marketing': 10000,
                    'operations': 8000,
                    'legal': 3000,
                    'other': 4000
                }
            
            total = sum(costs.values())
            costs['total'] = total
            costs['formatted_total'] = f"${total:,}"
            
            return json.dumps(costs)
        
        @tool
        def project_revenue(market_size: str, capture_rate: float = 0.001) -> str:
            """
            Project revenue based on market size
            
            Args:
                market_size: Target market size
                capture_rate: Expected market capture rate
            """
            # Extract number from market size string
            import re
            
            # Try to extract billions/millions
            if 'B' in market_size or 'billion' in market_size.lower():
                multiplier = 1_000_000_000
            elif 'M' in market_size or 'million' in market_size.lower():
                multiplier = 1_000_000
            else:
                multiplier = 1_000_000  # default to millions
            
            # Extract the number
            numbers = re.findall(r'[\d.]+', market_size)
            base_number = float(numbers[0]) if numbers else 100
            
            market_value = base_number * multiplier
            
            # Calculate revenue projections
            projections = {
                'year_1': int(market_value * capture_rate * 0.1),  # 10% of target in year 1
                'year_2': int(market_value * capture_rate * 0.3),  # 30% in year 2
                'year_3': int(market_value * capture_rate * 1.0),  # 100% in year 3
                'year_5': int(market_value * capture_rate * 2.5),  # 250% in year 5
            }
            
            # Format for display
            formatted = {
                f'{key}_formatted': f"${val:,}" for key, val in projections.items()
            }
            projections.update(formatted)
            
            return json.dumps(projections)
        
        @tool
        def calculate_break_even(costs: str, monthly_revenue: str) -> str:
            """
            Calculate break-even point
            
            Args:
                costs: Initial costs (JSON string)
                monthly_revenue: Projected monthly revenue
            """
            try:
                # Parse costs
                if isinstance(costs, str):
                    costs_data = json.loads(costs) if '{' in costs else {'total': 100000}
                else:
                    costs_data = {'total': 100000}
                
                total_costs = costs_data.get('total', 100000)
                
                # Estimate monthly burn rate (30% of initial costs per month)
                monthly_burn = total_costs * 0.3 / 12
                
                # Estimate monthly revenue growth (starting at 10% of target)
                starting_revenue = 5000
                revenue_growth = 1.15  # 15% monthly growth
                
                # Calculate break-even
                months = 0
                cumulative_loss = 0
                current_revenue = starting_revenue
                
                while cumulative_loss < total_costs and months < 36:
                    months += 1
                    profit = current_revenue - monthly_burn
                    cumulative_loss = max(0, cumulative_loss - profit)
                    current_revenue *= revenue_growth
                
                result = {
                    'months_to_break_even': months,
                    'break_even_timeline': f"{months} months",
                    'initial_investment': f"${total_costs:,}",
                    'monthly_burn': f"${monthly_burn:,.0f}"
                }
                
                return json.dumps(result)
                
            except Exception as e:
                return json.dumps({
                    'months_to_break_even': 18,
                    'break_even_timeline': "18 months",
                    'note': 'Estimated based on industry average'
                })
        
        self.calculate_costs_tool = calculate_startup_costs
        self.project_revenue_tool = project_revenue
        self.calculate_break_even_tool = calculate_break_even
        
        self.tools = [calculate_startup_costs, project_revenue, calculate_break_even]
    
    def _create_agent(self) -> Agent:
        """Create the financial analyst agent"""
        
        return Agent(
            role="Chief Financial Officer",
            goal="""Create financial projections, calculate startup costs,
                   project revenue, and determine funding requirements.""",
            backstory="""You are a former Goldman Sachs analyst and startup CFO.
                        You excel at creating realistic financial models and
                        understanding what investors look for.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )
    
    def analyze(self, startup_idea: str, market_data: Dict = None) -> Dict:
        """Main financial analysis"""
        
        # Calculate costs
        costs = json.loads(self.calculate_costs_tool.run(startup_idea))
        
        # Project revenue (use market data if available)
        market_size = "$100B" if not market_data else market_data.get('TAM', {}).get('formatted', '$100B')
        revenue = json.loads(self.project_revenue_tool.run(market_size))
        
        # Calculate break-even
        break_even = json.loads(self.calculate_break_even_tool.run(json.dumps(costs), "10000"))
        
        return {
            'startup_costs': costs,
            'revenue_projections': revenue,
            'break_even_analysis': break_even,
            'confidence': 0.75,
            'summary': f"Initial investment: {costs['formatted_total']}, Break-even: {break_even['break_even_timeline']}"
        }