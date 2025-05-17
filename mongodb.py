from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME   = "dental_mongo"

client = AsyncIOMotorClient(MONGO_URL)
mongo_db = client[DB_NAME]
