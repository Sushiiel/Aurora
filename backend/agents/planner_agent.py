"""
Planner Agent - Decides what actions are needed based on system state
Uses RAG to retrieve relevant past experiences and best practices
"""
from typing import Dict, Any, List
import logging
from backend.agents.base_agent import BaseAgent, AgentType, AgentDecision, AgentDecisionType
from backend.rag.memory_store import MemoryStore

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """
    The Planner Agent analyzes system state and decides what actions to take.
    It uses RAG to retrieve similar past situations and their outcomes.
    """
    
    def __init__(self, memory_store: MemoryStore, config: Dict[str, Any] = None):
        super().__init__(AgentType.PLANNER, config)
        self.memory_store = memory_store
        self.decision_threshold = config.get("decision_threshold", 0.7) if config else 0.7
    
    async def analyze(self, context: Dict[str, Any]) -> AgentDecision:
        """
        Analyze system state and plan actions
        
        Context should include:
        - model_metrics: Current model performance
        - data_drift: Drift detection results
        - system_load: Resource utilization
        - recent_errors: Error logs
        """
        try:
            # Extract key metrics
            model_metrics = context.get("model_metrics", {})
            data_drift = context.get("data_drift", {})
            system_load = context.get("system_load", {})
            
            # Query RAG memory for similar situations
            similar_cases = await self._retrieve_similar_cases(context)
            
            # Analyze and decide
            decision = await self._make_decision(
                model_metrics, 
                data_drift, 
                system_load, 
                similar_cases
            )
            
            return decision
            
        except Exception as e:
            logger.error(f"Planner analysis failed: {e}")
            return AgentDecision(
                decision_type=AgentDecisionType.NO_ACTION,
                reasoning=f"Analysis failed: {str(e)}",
                confidence=0.0,
                context=context
            )
    
    async def _retrieve_similar_cases(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve similar past cases from RAG memory"""
        try:
            # Create query from context
            query = self._create_query_from_context(context)
            
            # Search memory store
            results = await self.memory_store.search(query, top_k=5)
            
            return results
        except Exception as e:
            logger.warning(f"Failed to retrieve similar cases: {e}")
            return []
    
    def _create_query_from_context(self, context: Dict[str, Any]) -> str:
        """Create a search query from system context"""
        metrics = context.get("model_metrics", {})
        drift = context.get("data_drift", {})
        
        query_parts = []
        
        if metrics.get("accuracy", 1.0) < 0.8:
            query_parts.append("low model accuracy")
        
        if drift.get("detected", False):
            query_parts.append("data drift detected")
        
        if metrics.get("latency_ms", 0) > 1000:
            query_parts.append("high latency")
        
        return " ".join(query_parts) if query_parts else "system optimization"
    
    async def _make_decision(
        self,
        model_metrics: Dict[str, Any],
        data_drift: Dict[str, Any],
        system_load: Dict[str, Any],
        similar_cases: List[Dict[str, Any]]
    ) -> AgentDecision:
        """Make a decision based on analysis"""
        
        # Decision logic based on metrics
        accuracy = model_metrics.get("accuracy", 1.0)
        drift_detected = data_drift.get("detected", False)
        drift_score = data_drift.get("score", 0.0)
        latency = model_metrics.get("latency_ms", 0)
        
        # 1. Critical Performance Drop (e.g., Lighting Change)
        if accuracy < 0.60:
            return AgentDecision(
                decision_type=AgentDecisionType.OPTIMIZE_MODEL,  # Use generic type, pass specific action
                reasoning=(
                     f"CRITICAL: Accuracy dropped to {accuracy:.2%}. "
                     f"Drift Score: {drift_score:.2f}. "
                     f"Environment change detected (likely lighting/noise)."
                ),
                confidence=0.98,
                context=model_metrics,
                recommended_actions={
                    "action": "switch_model",
                    "target_model": "resnet_night_vision",
                    "priority": "critical"
                }
            )

        # 2. Check for moderate drift
        if drift_detected and drift_score > 0.4:  # Lowered from 0.5
            return AgentDecision(
                decision_type=AgentDecisionType.FINE_TUNE,
                reasoning=(
                    f"Moderate data drift detected (score: {drift_score:.2f}). "
                    f"Fine-tuning recommended to maintain performance."
                ),
                confidence=0.85,
                context={
                    "data_drift": data_drift,
                    "model_metrics": model_metrics
                },
                recommended_actions={
                    "action": "fine_tune",
                    "priority": "medium",
                    "estimated_time": "30-60 minutes"
                }
            )
        
        # Check for latency issues
        if latency > 1000:
            return AgentDecision(
                decision_type=AgentDecisionType.CACHE,
                reasoning=(
                    f"High latency detected ({latency}ms). "
                    f"Implementing caching strategy for frequent queries."
                ),
                confidence=0.85,
                context={
                    "latency": latency,
                    "system_load": system_load
                },
                recommended_actions={
                    "action": "enable_cache",
                    "priority": "medium",
                    "cache_ttl": 3600
                }
            )
        
        # All systems nominal
        return AgentDecision(
            decision_type=AgentDecisionType.NO_ACTION,
            reasoning=(
                f"System operating within normal parameters. "
                f"Accuracy: {accuracy:.2%}, Latency: {latency}ms"
            ),
            confidence=0.90,
            context={
                "model_metrics": model_metrics,
                "status": "healthy"
            }
        )
