"""
Initialize Expense Tracker Database
Creates tables and sample data for testing
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.connection import engine, SessionLocal
from backend.database.models import Base, Expense, Budget

# Sample categories
CATEGORIES = [
    'Food & Dining',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Bills & Utilities',
    'Healthcare',
    'Other'
]

# Sample expense descriptions
EXPENSE_DESCRIPTIONS = {
    'Food & Dining': ['Lunch at cafe', 'Grocery shopping', 'Dinner with friends', 'Coffee', 'Fast food'],
    'Transportation': ['Uber ride', 'Gas station', 'Parking fee', 'Bus ticket', 'Car maintenance'],
    'Shopping': ['Clothing', 'Electronics', 'Books', 'Home decor', 'Gifts'],
    'Entertainment': ['Movie tickets', 'Concert', 'Streaming subscription', 'Video games', 'Sports event'],
    'Bills & Utilities': ['Electricity bill', 'Internet', 'Phone bill', 'Water bill', 'Rent'],
    'Healthcare': ['Doctor visit', 'Pharmacy', 'Gym membership', 'Vitamins', 'Health insurance'],
    'Other': ['Miscellaneous', 'Emergency expense', 'Donation', 'Pet supplies', 'Other']
}

# Default budget limits
DEFAULT_BUDGETS = {
    'Food & Dining': 500.0,
    'Transportation': 300.0,
    'Shopping': 400.0,
    'Entertainment': 200.0,
    'Bills & Utilities': 800.0,
    'Healthcare': 250.0,
    'Other': 150.0
}


def init_expense_tables():
    """Create all tables"""
    print("Creating expense tracker tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")


def create_sample_budgets():
    """Create sample budget limits"""
    db = SessionLocal()
    try:
        print("\nCreating sample budgets...")
        
        for category, limit in DEFAULT_BUDGETS.items():
            # Check if budget already exists
            existing = db.query(Budget).filter(Budget.category == category).first()
            if not existing:
                budget = Budget(
                    category=category,
                    limit=limit,
                    spent=0.0,
                    percentage=0.0
                )
                db.add(budget)
                print(f"  ✅ Created budget for {category}: ${limit}")
            else:
                print(f"  ⏭️  Budget for {category} already exists")
        
        db.commit()
        print("✅ Budgets created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating budgets: {e}")
        db.rollback()
    finally:
        db.close()


def create_sample_expenses(count=20):
    """Create sample expenses for testing"""
    db = SessionLocal()
    try:
        print(f"\nCreating {count} sample expenses...")
        
        for i in range(count):
            category = random.choice(CATEGORIES)
            description = random.choice(EXPENSE_DESCRIPTIONS[category])
            
            # Random amount based on category
            if category == 'Bills & Utilities':
                amount = round(random.uniform(50, 200), 2)
            elif category == 'Food & Dining':
                amount = round(random.uniform(10, 80), 2)
            elif category == 'Transportation':
                amount = round(random.uniform(5, 50), 2)
            elif category == 'Shopping':
                amount = round(random.uniform(20, 150), 2)
            else:
                amount = round(random.uniform(10, 100), 2)
            
            # Random date within last 30 days
            days_ago = random.randint(0, 30)
            expense_date = datetime.utcnow() - timedelta(days=days_ago)
            
            expense = Expense(
                amount=amount,
                category=category,
                description=description,
                date=expense_date,
                user_email='demo@aurora.app',
                ai_suggestion=f'AI: Consider budgeting for {category.lower()}'
            )
            
            db.add(expense)
            print(f"  ✅ Added: ${amount} - {description} ({category})")
        
        db.commit()
        
        # Update budget spent amounts
        print("\nUpdating budget calculations...")
        from sqlalchemy import func
        
        for category in CATEGORIES:
            budget = db.query(Budget).filter(Budget.category == category).first()
            if budget:
                total_spent = db.query(Expense).filter(
                    Expense.category == category
                ).with_entities(func.sum(Expense.amount)).scalar() or 0
                
                budget.spent = float(total_spent)
                budget.percentage = (budget.spent / budget.limit) * 100 if budget.limit > 0 else 0
                print(f"  ✅ {category}: ${budget.spent:.2f} / ${budget.limit} ({budget.percentage:.1f}%)")

        
        db.commit()
        print("✅ Sample expenses created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating expenses: {e}")
        db.rollback()
    finally:
        db.close()


def show_summary():
    """Show database summary"""
    db = SessionLocal()
    try:
        print("\n" + "="*60)
        print("📊 EXPENSE TRACKER DATABASE SUMMARY")
        print("="*60)
        
        total_expenses = db.query(Expense).count()
        total_budgets = db.query(Budget).count()
        
        print(f"\n📝 Total Expenses: {total_expenses}")
        print(f"💰 Total Budget Categories: {total_budgets}")
        
        print("\n📊 Budget Overview:")
        print("-" * 60)
        budgets = db.query(Budget).all()
        for budget in budgets:
            status = "🔴 EXCEEDED" if budget.percentage > 100 else "🟢 OK"
            print(f"{budget.category:20} ${budget.spent:8.2f} / ${budget.limit:8.2f} ({budget.percentage:5.1f}%) {status}")
        
        print("\n" + "="*60)
        print("✅ Database initialized successfully!")
        print("="*60)
        
        print("\n🚀 Next Steps:")
        print("1. Start the application: ./start.sh")
        print("2. Open browser: http://localhost:5173/expenses")
        print("3. Set up n8n: See docs/N8N_EMAIL_SETUP.md")
        print("4. Test budget alerts by adding expenses!")
        
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Initializing Expense Tracker Database...")
    print("="*60)
    
    # Create tables
    init_expense_tables()
    
    # Create budgets
    create_sample_budgets()
    
    # Create sample expenses
    create_sample_expenses(count=25)
    
    # Show summary
    show_summary()
