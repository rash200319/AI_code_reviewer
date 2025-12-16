# --- AUTO-GENERATED CONSTANTS ---
MAGIC_NUM_4 = 5
MAGIC_NUM_9 = 100
# --------------------------------

# ai-code-reviewer/sample_project/example.py
import asyncio  ##lets you run multiple tasks concurrently
# A constant (should NOT be detected as a function)
MAX_RETRIES = 5

def calculate_discount(price: float, percentage: float) -> float:
    """Calculates the final price after applying a discount."""
    if percentage > 1.0:
        percentage /= 100
    return price * (1.0 - percentage)

class UserService:
    def __init__(self, db_conn):
        self.db = db_conn

    def get_user_data(self, user_id: int):
        # This is a method, but the AST treats it as a FunctionDef node
        return self.db.fetch_user(user_id)

async def main_async_loop():
    """An asynchronous function."""
    print("Running background task...")
    await asyncio.sleep(1)

def calculate_area(radius):
    # The number 3.14 is a "Magic Number" (should be math.pi or a constant)
    return 3.14 * radius * radius

def get_status_code():
    # The number 200 is a "Magic Number" (should be HTTP_OK)
    return 200