# Create test script test_db.py in project root:
from sqlalchemy import text
from app.core.database import engine
print("Testing database connection...")
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Success!" if result.fetchone()[0] == 1 else "Failed")