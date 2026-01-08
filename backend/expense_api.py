"""
Expense Tracker API Endpoints
Integrates with n8n for email notifications
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime
import httpx
import os

from backend.database.connection import get_db_session
from backend.database.models import Expense, Budget
from backend.agents.planner_agent import PlannerAgent
from backend.rag.memory_store import MemoryStore

router = APIRouter(prefix="/api", tags=["expenses"])

# Initialize AI components
memory_store = MemoryStore(use_pinecone=False)
planner_agent = PlannerAgent(memory_store)

# n8n Webhook URL (from environment)
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://aurora123.app.n8n.cloud/webhook/expense-alert")


@router.post("/expenses")
async def create_expense(
    expense_data: Dict[str, Any],
    db: Session = Depends(get_db_session)
):
    """
    Create a new expense and check budget limits
    Triggers n8n webhook if budget exceeded
    """
    try:
        # Create expense record
        expense = Expense(
            amount=expense_data["amount"],
            category=expense_data["category"],
            description=expense_data["description"],
            date=datetime.fromisoformat(expense_data["date"]),
            user_email=expense_data.get("userEmail", "user@example.com")
        )
        
        # Get AI suggestion using AURORA planner
        ai_context = {
            "expense": {
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description
            },
            "task": "analyze_expense"
        }
        
        try:
            ai_decision = await planner_agent.execute(ai_context)
            expense.ai_suggestion = ai_decision.reasoning[:200]  # Store first 200 chars
        except Exception as e:
            print(f"AI suggestion failed: {e}")
            expense.ai_suggestion = "Smart categorization applied"
        
        db.add(expense)
        db.commit()
        db.refresh(expense)
        
        # Check budget for this category
        budget = db.query(Budget).filter(Budget.category == expense.category).first()
        budget_exceeded = False
        
        if budget:
            # Calculate total spent in this category
            total_spent = db.query(Expense).filter(
                Expense.category == expense.category
            ).with_entities(db.func.sum(Expense.amount)).scalar() or 0
            
            budget.spent = float(total_spent)
            budget.percentage = (budget.spent / budget.limit) * 100 if budget.limit > 0 else 0
            db.commit()
            
            # Check if budget exceeded
            if budget.percentage > 100:
                budget_exceeded = True
                
                # Trigger n8n webhook for email notification
                await send_budget_alert_email(
                    user_email=expense.user_email,
                    category=expense.category,
                    spent=budget.spent,
                    limit=budget.limit,
                    percentage=budget.percentage
                )
        
        return {
            "success": True,
            "expense": {
                "id": expense.id,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date": expense.date.isoformat(),
                "aiSuggestion": expense.ai_suggestion
            },
            "budgetExceeded": budget_exceeded
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/expenses")
async def get_expenses(
    limit: int = 50,
    db: Session = Depends(get_db_session)
):
    """Get all expenses"""
    try:
        expenses = db.query(Expense)\
            .order_by(Expense.date.desc())\
            .limit(limit)\
            .all()
        
        return {
            "expenses": [
                {
                    "id": exp.id,
                    "amount": exp.amount,
                    "category": exp.category,
                    "description": exp.description,
                    "date": exp.date.isoformat(),
                    "aiSuggestion": exp.ai_suggestion
                }
                for exp in expenses
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete an expense"""
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        
        category = expense.category
        db.delete(expense)
        db.commit()
        
        # Recalculate budget
        budget = db.query(Budget).filter(Budget.category == category).first()
        if budget:
            total_spent = db.query(Expense).filter(
                Expense.category == category
            ).with_entities(db.func.sum(Expense.amount)).scalar() or 0
            
            budget.spent = float(total_spent)
            budget.percentage = (budget.spent / budget.limit) * 100 if budget.limit > 0 else 0
            db.commit()
        
        return {"success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/budgets")
async def get_budgets(db: Session = Depends(get_db_session)):
    """Get all budget categories"""
    try:
        budgets = db.query(Budget).all()
        
        return {
            "budgets": [
                {
                    "category": b.category,
                    "limit": b.limit,
                    "spent": b.spent,
                    "percentage": b.percentage
                }
                for b in budgets
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/budgets")
async def create_budget(
    budget_data: Dict[str, Any],
    db: Session = Depends(get_db_session)
):
    """Create or update budget for a category"""
    try:
        budget = db.query(Budget).filter(
            Budget.category == budget_data["category"]
        ).first()
        
        if budget:
            budget.limit = budget_data["limit"]
        else:
            budget = Budget(
                category=budget_data["category"],
                limit=budget_data["limit"],
                spent=0,
                percentage=0
            )
            db.add(budget)
        
        db.commit()
        db.refresh(budget)
        
        return {"success": True, "budget": {
            "category": budget.category,
            "limit": budget.limit,
            "spent": budget.spent,
            "percentage": budget.percentage
        }}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def send_budget_alert_email(
    user_email: str,
    category: str,
    spent: float,
    limit: float,
    percentage: float
):
    """
    Send budget alert email via n8n webhook
    
    IMPORTANT: The user_email is dynamically passed from the expense
    This is the email the user used during Firebase login
    """
    try:
        payload = {
            "to": user_email,  # Dynamic user email from login
            "subject": f"⚠️ Budget Alert: {category} Limit Exceeded",
            "category": category,
            "spent": spent,
            "limit": limit,
            "percentage": percentage,
            "timestamp": datetime.utcnow().isoformat(),
            "message": f"You have exceeded your {category} budget! You've spent ${spent:.2f} out of ${limit:.2f} ({percentage:.1f}%)"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                N8N_WEBHOOK_URL,
                json=payload,
                timeout=10.0
            )
            
            if response.status_code == 200:
                print(f"✅ Budget alert email sent to {user_email}")
            else:
                print(f"❌ Failed to send email: {response.status_code}")
                
    except Exception as e:
        print(f"Error sending email via n8n: {e}")
        # Don't fail the expense creation if email fails
