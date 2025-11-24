# src/agents/technical_architect.py
"""
Technical Architect Agent - Assesses technical feasibility
"""

from crewai import Agent
from crewai_tools import tool
from typing import Dict
import json
from src.utils.llm_manager import llm_manager

class TechnicalArchitectAgent:
    """Agent specialized in technical assessment and architecture"""
    
    def __init__(self):
        self.llm = llm_manager.get_llm("fast")  # Use fast model for technical analysis
        self._create_tools()
        self.agent = self._create_agent()
        
    def _create_tools(self):
        """Create technical assessment tools"""
        
        @tool
        def assess_technical_complexity(idea: str) -> str:
            """
            Assess the technical complexity of a startup idea
            
            Args:
                idea: The startup idea to assess
            """
            # Analyze complexity based on keywords
            idea_lower = idea.lower()
            
            complexity_indicators = {
                'high': ['ai', 'machine learning', 'blockchain', 'ar', 'vr', 'quantum', 
                        'autonomous', 'robotics', 'deep learning', 'neural'],
                'medium': ['marketplace', 'platform', 'app', 'saas', 'api', 'integration',
                          'analytics', 'dashboard', 'automation', 'cloud'],
                'low': ['website', 'blog', 'landing page', 'newsletter', 'directory',
                       'simple', 'basic', 'static']
            }
            
            complexity = 'medium'  # default
            complexity_score = 5
            
            for level, keywords in complexity_indicators.items():
                if any(keyword in idea_lower for keyword in keywords):
                    complexity = level
                    complexity_score = {'high': 8, 'medium': 5, 'low': 3}[level]
                    break
            
            result = {
                'complexity': complexity,
                'score': complexity_score,
                'description': f"This project has {complexity} technical complexity"
            }
            
            return json.dumps(result)
        
        @tool
        def recommend_tech_stack(idea: str) -> str:
            """
            Recommend appropriate technology stack
            
            Args:
                idea: The startup idea
            """
            # Determine best tech stack based on idea type
            idea_lower = idea.lower()
            
            # Default modern stack
            stack = {
                'frontend': 'React/Next.js',
                'backend': 'Node.js/Python FastAPI',
                'database': 'PostgreSQL',
                'hosting': 'AWS/Vercel',
                'additional': []
            }
            
            # Customize based on requirements
            if 'mobile' in idea_lower or 'app' in idea_lower:
                stack['mobile'] = 'React Native or Flutter'
                stack['additional'].append('Push notifications')
            
            if 'ai' in idea_lower or 'machine learning' in idea_lower:
                stack['backend'] = 'Python FastAPI'
                stack['ml'] = 'TensorFlow/PyTorch'
                stack['additional'].append('GPU infrastructure')
            
            if 'real-time' in idea_lower or 'live' in idea_lower:
                stack['realtime'] = 'WebSockets/Socket.io'
                stack['additional'].append('Redis for caching')
            
            if 'marketplace' in idea_lower or 'payment' in idea_lower:
                stack['payments'] = 'Stripe/PayPal'
                stack['additional'].append('Payment processing')
            
            return json.dumps(stack)
        
        @tool
        def estimate_development_timeline(complexity: str) -> str:
            """
            Estimate development timeline based on complexity
            
            Args:
                complexity: Project complexity level (low/medium/high)
            """
            timelines = {
                'low': {
                    'mvp': '1-2 months',
                    'beta': '2-3 months',
                    'launch': '3-4 months',
                    'team_size': '1-2 developers'
                },
                'medium': {
                    'mvp': '3-4 months',
                    'beta': '4-6 months',
                    'launch': '6-8 months',
                    'team_size': '2-4 developers'
                },
                'high': {
                    'mvp': '6-8 months',
                    'beta': '8-10 months',
                    'launch': '10-12 months',
                    'team_size': '4-8 developers'
                }
            }
            
            timeline = timelines.get(complexity.lower(), timelines['medium'])
            
            return json.dumps(timeline)
        
        self.assess_complexity_tool = assess_technical_complexity
        self.recommend_stack_tool = recommend_tech_stack
        self.estimate_timeline_tool = estimate_development_timeline
        
        self.tools = [assess_technical_complexity, recommend_tech_stack, estimate_development_timeline]
    
    def _create_agent(self) -> Agent:
        """Create the technical architect agent"""
        
        return Agent(
            role="Chief Technology Officer",
            goal="""Assess technical feasibility, recommend technology stack,
                   estimate development timeline, and identify technical risks.""",
            backstory="""You are a former Google engineer and 3x startup CTO.
                        You excel at designing scalable architectures and selecting
                        the right technologies for rapid development.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )
    
    def analyze(self, startup_idea: str) -> Dict:
        """Main technical analysis"""
        
        # Assess complexity
        complexity_result = json.loads(self.assess_complexity_tool.run(startup_idea))
        
        # Recommend tech stack
        tech_stack = json.loads(self.recommend_stack_tool.run(startup_idea))
        
        # Estimate timeline
        timeline = json.loads(self.estimate_timeline_tool.run(complexity_result['complexity']))
        
        return {
            'complexity': complexity_result,
            'tech_stack': tech_stack,
            'timeline': timeline,
            'confidence': 0.85,
            'summary': f"Technical complexity: {complexity_result['complexity']}, MVP timeline: {timeline['mvp']}"
        }