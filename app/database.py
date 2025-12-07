import motor.motor_asyncio

# Connection String
MONGO_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.boardcerts_db

# Dependency Injection function
async def get_database():
    return db