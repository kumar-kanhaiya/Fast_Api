from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb+srv://admin:pass@cluster0.mry58sh.mongodb.net/?appName=Cluster0"

client = AsyncIOMotorClient(uri)
db = client.authentication

