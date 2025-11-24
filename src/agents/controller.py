# src/agents/controller.py
"""
Controller Agent - The main orchestrator of the validation system
This agent manages workflow, makes routing decisions, and handles errors
"""

from crewai import Agent
from typing import Dict, List, Optional
import json
from datetime import datetime
import logging
from src.utils.llm_manager import llm_manager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ControllerAgent:
    """
    Master orchestrator that coordinates all validation activities
    """
    
    def __init__(self):
        """Initialize the controller agent"""
        
        # Get LLM instance
        self.llm = llm_manager.get_llm("smart")  # Use smart model for complex decisions
        
        # Initialize the CrewAI agent
        self.agent = self._create_agent()
        
        # Workflow state management
        self.workflow_state = {
            "status": "idle",
            "current_task": None,
            "completed_tasks": [],
            "failed_tasks": [],
            "start_time": None,
            "validation_data": {}
        }
        
        # Decision rules for routing
        self.routing_rules = self._define_routing_rules()
        
        # Error handling strategies
        self.error_strategies = self._define_error_strategies()
        
    def _create_agent(self) -> Agent:
        """Create the controller agent with CrewAI"""
        
        return Agent(
            role="Chief Validation Orchestrator",
            goal="""Orchestrate the complete startup validation process efficiently. 
                   Coordinate all specialized agents, ensure data quality, handle errors gracefully,
                   and deliver comprehensive validation results within 60 seconds.""",
            backstory="""You are an experienced startup ecosystem expert who has evaluated 
                        thousands of startup ideas. You excel at coordinating complex analyses,
                        making strategic decisions, and ensuring all aspects of a startup idea
                        are thoroughly validated. You understand what makes startups succeed
                        or fail and can quickly identify critical validation points.""",
            verbose=True,
            allow_delegation=True,
            max_iter=3,  # Maximum retry attempts
            llm=self.llm,
            memory=True  # Enable memory for context retention
        )
    
    def _define_routing_rules(self) -> Dict:
        """Define rules for routing tasks to appropriate agents"""
        
        return {
            "market_validation": {
                "required": True,
                "order": 1,
                "agent": "market_analyst",
                "min_confidence": 0.7,
                "fallback": "basic_market_check",
                "success_criteria": {
                    "market_size_found": True,
                    "tam_calculated": True,
                    "growth_rate_identified": True
                }
            },
            "competitor_analysis": {
                "required": True,
                "order": 2,
                "agent": "competitor_researcher",
                "min_confidence": 0.6,
                "fallback": "simplified_competitor_search",
                "success_criteria": {
                    "competitors_found": ">=3",
                    "market_gaps_identified": True
                }
            },
            "technical_feasibility": {
                "required": True,
                "order": 3,
                "agent": "technical_architect",
                "min_confidence": 0.8,
                "fallback": "basic_tech_assessment",
                "success_criteria": {
                    "tech_stack_defined": True,
                    "timeline_estimated": True,
                    "risks_identified": True
                }
            },
            "financial_analysis": {
                "required": True,
                "order": 4,
                "agent": "financial_analyst",
                "min_confidence": 0.7,
                "fallback": "simple_cost_estimate",
                "success_criteria": {
                    "costs_calculated": True,
                    "revenue_projected": True,
                    "break_even_estimated": True
                }
            },
            "strategy_synthesis": {
                "required": True,
                "order": 5,
                "agent": "strategy_advisor",
                "min_confidence": 0.8,
                "fallback": "basic_recommendation",
                "success_criteria": {
                    "verdict_provided": True,
                    "score_calculated": True,
                    "next_steps_defined": True
                }
            }
        }
    
    def _define_error_strategies(self) -> Dict:
        """Define strategies for handling different types of errors"""
        
        return {
            "timeout": {
                "strategy": "use_partial_results",
                "max_wait": 60,  # seconds
                "action": self._handle_timeout
            },
            "api_failure": {
                "strategy": "retry_with_fallback",
                "max_retries": 3,
                "action": self._handle_api_failure
            },
            "data_quality": {
                "strategy": "validate_and_clean",
                "min_quality_score": 0.5,
                "action": self._handle_poor_data
            },
            "agent_failure": {
                "strategy": "use_fallback_agent",
                "action": self._handle_agent_failure
            }
        }
    
    def start_validation(self, startup_idea: str) -> Dict:
        """
        Main entry point to start the validation process
        
        Args:
            startup_idea: The startup idea to validate
            
        Returns:
            Complete validation results
        """
        logger.info(f"Starting validation for: {startup_idea}")
        
        # Initialize workflow state
        self.workflow_state["status"] = "running"
        self.workflow_state["start_time"] = datetime.now()
        self.workflow_state["validation_data"]["idea"] = startup_idea
        
        # Pre-validation checks
        if not self._pre_validation_check(startup_idea):
            return self._create_error_response("Invalid input")
        
        # Execute validation workflow
        try:
            # Route through each validation stage
            for task_name, rules in self.routing_rules.items():
                if rules["required"]:
                    result = self._execute_task(task_name, rules)
                    self.workflow_state["validation_data"][task_name] = result
                    
                    # Check success criteria
                    if not self._check_success_criteria(result, rules["success_criteria"]):
                        logger.warning(f"Task {task_name} didn't meet success criteria")
                        # Use fallback strategy
                        result = self._execute_fallback(task_name, rules["fallback"])
                        self.workflow_state["validation_data"][task_name] = result
            
            # Generate final report
            final_result = self._synthesize_results()
            
            # Update state
            self.workflow_state["status"] = "completed"
            
            return final_result
            
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            return self._handle_critical_error(e)
    
    def _pre_validation_check(self, startup_idea: str) -> bool:
        """Check if the input is valid for processing"""
        
        # Check minimum length
        if len(startup_idea) < 10:
            logger.warning("Startup idea too short")
            return False
        
        # Check for spam/nonsense
        spam_keywords = ["test", "asdf", "123", "xxx"]
        if any(keyword in startup_idea.lower() for keyword in spam_keywords):
            logger.warning("Potential spam detected")
            return False
        
        return True
    
    def _execute_task(self, task_name: str, rules: Dict) -> Dict:
        """Execute a specific validation task"""
        
        logger.info(f"Executing task: {task_name}")
        
        # This will be connected to actual agents in the next step
        # For now, return mock data
        return {
            "status": "completed",
            "confidence": 0.85,
            "data": f"Mock data for {task_name}"
        }
    
    def _execute_fallback(self, task_name: str, fallback_strategy: str) -> Dict:
        """Execute fallback strategy when main task fails"""
        
        logger.info(f"Executing fallback for {task_name}: {fallback_strategy}")
        
        return {
            "status": "completed_with_fallback",
            "confidence": 0.6,
            "data": f"Fallback data for {task_name}"
        }
    
    def _check_success_criteria(self, result: Dict, criteria: Dict) -> bool:
        """Check if task result meets success criteria"""
        
        # Simplified check - will be enhanced
        return result.get("status") == "completed" and result.get("confidence", 0) > 0.5
    
    def _synthesize_results(self) -> Dict:
        """Synthesize all validation results into final report"""
        
        validation_data = self.workflow_state["validation_data"]
        
        # Calculate overall score
        score = self._calculate_validation_score(validation_data)
        
        # Determine verdict
        verdict = self._determine_verdict(score)
        
        # Calculate execution time
        execution_time = (datetime.now() - self.workflow_state["start_time"]).seconds
        
        return {
            "idea": validation_data.get("idea"),
            "score": score,
            "verdict": verdict,
            "execution_time": execution_time,
            "market_analysis": validation_data.get("market_validation"),
            "competitors": validation_data.get("competitor_analysis"),
            "technical": validation_data.get("technical_feasibility"),
            "financial": validation_data.get("financial_analysis"),
            "strategy": validation_data.get("strategy_synthesis"),
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "confidence": self._calculate_confidence()
            }
        }
    
    def _calculate_validation_score(self, data: Dict) -> float:
        """Calculate overall validation score (0-10)"""
        
        # Weighted scoring based on different factors
        weights = {
            "market_validation": 0.3,
            "competitor_analysis": 0.2,
            "technical_feasibility": 0.2,
            "financial_analysis": 0.2,
            "strategy_synthesis": 0.1
        }
        
        total_score = 0
        for key, weight in weights.items():
            if key in data and data[key]:
                # Get confidence from each task
                confidence = data[key].get("confidence", 0.5)
                total_score += confidence * weight * 10
        
        return round(total_score, 1)
    
    def _determine_verdict(self, score: float) -> str:
        """Determine final verdict based on score"""
        
        if score >= 7.5:
            return "GO ✅"
        elif score >= 5.0:
            return "PIVOT ⚠️"
        else:
            return "NO-GO ❌"
    
    def _calculate_confidence(self) -> float:
        """Calculate overall confidence in the validation"""
        
        confidences = []
        for task_data in self.workflow_state["validation_data"].values():
            if isinstance(task_data, dict) and "confidence" in task_data:
                confidences.append(task_data["confidence"])
        
        return sum(confidences) / len(confidences) if confidences else 0.5
    
    # Error handling methods
    def _handle_timeout(self, task_name: str) -> Dict:
        """Handle timeout errors"""
        logger.warning(f"Timeout on task: {task_name}")
        return {"status": "timeout", "data": "Using cached/default data"}
    
    def _handle_api_failure(self, error: Exception) -> Dict:
        """Handle API failures"""
        logger.error(f"API failure: {str(error)}")
        return {"status": "api_error", "data": "Using offline data"}
    
    def _handle_poor_data(self, data: Dict) -> Dict:
        """Handle poor quality data"""
        logger.warning("Poor data quality detected")
        return {"status": "low_quality", "data": "Results may be incomplete"}
    
    def _handle_agent_failure(self, agent_name: str) -> Dict:
        """Handle agent failures"""
        logger.error(f"Agent failed: {agent_name}")
        return {"status": "agent_error", "data": "Using simplified analysis"}
    
    def _handle_critical_error(self, error: Exception) -> Dict:
        """Handle critical errors that stop the validation"""
        return {
            "error": True,
            "message": f"Validation failed: {str(error)}",
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_error_response(self, message: str) -> Dict:
        """Create standardized error response"""
        return {
            "error": True,
            "message": message,
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict:
        """Get current workflow status"""
        return {
            "status": self.workflow_state["status"],
            "current_task": self.workflow_state["current_task"],
            "completed_tasks": len(self.workflow_state["completed_tasks"]),
            "elapsed_time": (
                (datetime.now() - self.workflow_state["start_time"]).seconds
                if self.workflow_state["start_time"]
                else 0
            )
        }