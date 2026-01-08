"""
Base Agent Class
All agents inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Agent type enumeration"""
    PLANNER = "planner"
    CRITIC = "critic"
    EXECUTOR = "executor"


class AgentDecisionType(Enum):
    """Types of decisions agents can make"""
    RETRAIN = "retrain"
    FINE_TUNE = "fine_tune"
    ROUTE = "route"
    CACHE = "cache"
    REPLACE = "replace"
    SCALE = "scale"
    ALERT = "alert"
    NO_ACTION = "no_action"
    OPTIMIZE_MODEL = "optimize_model"


class AgentDecision:
    """Structured agent decision output"""
    
    def __init__(
        self,
        decision_type: AgentDecisionType,
        reasoning: str,
        confidence: float,
        context: Dict[str, Any],
        recommended_actions: Optional[Dict[str, Any]] = None
    ):
        self.decision_type = decision_type
        self.reasoning = reasoning
        self.confidence = confidence
        self.context = context
        self.recommended_actions = recommended_actions or {}
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert decision to dictionary"""
        return {
            "decision_type": self.decision_type.value,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "context": self.context,
            "recommended_actions": self.recommended_actions,
            "timestamp": self.timestamp.isoformat()
        }


class BaseAgent(ABC):
    """Base class for all AURORA agents"""
    
    def __init__(self, agent_type: AgentType, config: Optional[Dict[str, Any]] = None):
        self.agent_type = agent_type
        self.config = config or {}
        self.logger = logging.getLogger(f"aurora.agent.{agent_type.value}")
    
    @abstractmethod
    async def analyze(self, context: Dict[str, Any]) -> AgentDecision:
        """
        Analyze the given context and make a decision
        
        Args:
            context: Dictionary containing relevant system state and metrics
            
        Returns:
            AgentDecision object with reasoning and recommendations
        """
        pass
    
    def log_decision(self, decision: AgentDecision):
        """Log agent decision"""
        self.logger.info(
            f"{self.agent_type.value.upper()} Decision: {decision.decision_type.value} "
            f"(confidence: {decision.confidence:.2f}) - {decision.reasoning[:100]}"
        )
    
    async def execute(self, context: Dict[str, Any]) -> AgentDecision:
        """
        Execute the agent's analysis pipeline
        
        Args:
            context: System context for analysis
            
        Returns:
            AgentDecision with recommendations
        """
        try:
            decision = await self.analyze(context)
            self.log_decision(decision)
            return decision
        except Exception as e:
            self.logger.error(f"Agent execution failed: {e}")
            return AgentDecision(
                decision_type=AgentDecisionType.NO_ACTION,
                reasoning=f"Agent failed with error: {str(e)}",
                confidence=0.0,
                context=context
            )
