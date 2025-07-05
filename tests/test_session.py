from app.core.dependencies import get_db

# Test session creation
db_gen = get_db()
db = next(db_gen)
print(f"Session created: {db}")
print(f"Session is bound: {db.bind is not None}")
db.close()
