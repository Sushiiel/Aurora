"""
Critic Agent - Evaluates proposed actions and approves/rejects them
Acts as a safety layer to prevent harmful decisions
"""
from typing import Dict, Any
import logging
from backend.agents.base_agent import BaseAgent, AgentType, AgentDecision, AgentDecisionType
from backend.config import settings

logger = logging.getLogger(__name__)


class CriticAgent(BaseAgent):
    """
    The Critic Agent evaluates decisions from the Planner Agent.
    It acts as a safety mechanism to prevent harmful or low-confidence actions.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.CRITIC, config)
        self.approval_threshold = config.get("approval_threshold", settings.critic_threshold) if config else settings.critic_threshold
    
    async def analyze(self, context: Dict[str, Any]) -> AgentDecision:
        """
        Analyze a proposed decision from the Planner
        
        Context should include:
        - proposed_decision: The decision to evaluate
        - current_state: Current system state
        - risk_factors: Potential risks
        """
        proposed_decision = context.get("proposed_decision")
        
        if not proposed_decision:
            return AgentDecision(
                decision_type=AgentDecisionType.NO_ACTION,
                reasoning="No decision provided for evaluation",
                confidence=0.0,
                context=context
            )
        
        # Evaluate the decision
        evaluation = await self._evaluate_decision(proposed_decision, context)
        
        return evaluation
    
    async def _evaluate_decision(
        self, 
        proposed_decision: AgentDecision, 
        context: Dict[str, Any]
    ) -> AgentDecision:
        """Evaluate a proposed decision"""
        
        decision_type = proposed_decision.decision_type
        confidence = proposed_decision.confidence
        
        # Check confidence threshold
        if confidence < self.approval_threshold:
            return AgentDecision(
                decision_type=AgentDecisionType.NO_ACTION,
                reasoning=(
                    f"Rejected: Confidence ({confidence:.2%}) below threshold "
                    f"({self.approval_threshold:.2%}). "
                    f"Original proposal: {decision_type.value}"
                ),
                confidence=0.95,
                context={
                    "rejected_decision": proposed_decision.to_dict(),
                    "reason": "low_confidence"
                }
            )
        
        # Evaluate risk based on decision type
        risk_assessment = self._assess_risk(decision_type, context)
        
        if risk_assessment["risk_level"] == "high":
            return AgentDecision(
                decision_type=AgentDecisionType.NO_ACTION,
                reasoning=(
                    f"Rejected: High risk detected for {decision_type.value}. "
                    f"Risk factors: {', '.join(risk_assessment['factors'])}"
                ),
                confidence=0.90,
                context={
                    "rejected_decision": proposed_decision.to_dict(),
                    "risk_assessment": risk_assessment
                }
            )
        
        # Check system constraints
        if not self._check_system_constraints(decision_type, context):
            return AgentDecision(
                decision_type=AgentDecisionType.NO_ACTION,
                reasoning=(
                    f"Rejected: System constraints violated for {decision_type.value}. "
                    f"Current system load or resources insufficient."
                ),
                confidence=0.85,
                context={
                    "rejected_decision": proposed_decision.to_dict(),
                    "reason": "system_constraints"
                }
            )
        
        # Approve the decision
        return AgentDecision(
            decision_type=decision_type,
            reasoning=(
                f"Approved: {decision_type.value} with confidence {confidence:.2%}. "
                f"Risk level: {risk_assessment['risk_level']}. "
                f"Original reasoning: {proposed_decision.reasoning[:100]}"
            ),
            confidence=confidence,
            context={
                "approved_decision": proposed_decision.to_dict(),
                "risk_assessment": risk_assessment
            },
            recommended_actions=proposed_decision.recommended_actions
        )
    
    def _assess_risk(
        self, 
        decision_type: AgentDecisionType, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess risk level of a decision"""
        
        risk_factors = []
        risk_level = "low"
        
        current_state = context.get("current_state", {})
        system_load = current_state.get("system_load", {})
        
        # High-risk decisions
        if decision_type == AgentDecisionType.RETRAIN:
            if system_load.get("cpu_usage", 0) > 0.8:
                risk_factors.append("high_cpu_usage")
                risk_level = "high"
            
            if current_state.get("active_requests", 0) > 1000:
                risk_factors.append("high_traffic")
                risk_level = "medium" if risk_level == "low" else risk_level
        
        elif decision_type == AgentDecisionType.REPLACE:
            risk_factors.append("model_replacement")
            risk_level = "high"
        
        elif decision_type == AgentDecisionType.SCALE:
            if system_load.get("memory_usage", 0) > 0.9:
                risk_factors.append("memory_pressure")
                risk_level = "medium"
        
        return {
            "risk_level": risk_level,
            "factors": risk_factors,
            "decision_type": decision_type.value
        }
    
    def _check_system_constraints(
        self, 
        decision_type: AgentDecisionType, 
        context: Dict[str, Any]
    ) -> bool:
        """Check if system can handle the proposed action"""
        
        current_state = context.get("current_state", {})
        system_load = current_state.get("system_load", {})
        
        # Resource-intensive operations
        if decision_type in [AgentDecisionType.RETRAIN, AgentDecisionType.FINE_TUNE]:
            # Check if we have enough resources
            if system_load.get("cpu_usage", 0) > 0.9:
                return False
            if system_load.get("memory_usage", 0) > 0.9:
                return False
            if system_load.get("gpu_usage", 0) > 0.9:
                return False
        
        return True
