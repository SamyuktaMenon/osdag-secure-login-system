from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.account import Account
from appwrite.services.storage import Storage
from appwrite.services.databases import Databases

from app.config import settings


client = Client()


client.set_endpoint(settings.APPWRITE_ENDPOINT)
client.set_project(settings.APPWRITE_PROJECT_ID)
client.set_key(settings.APPWRITE_API_KEY)

account = Account(client)
users = Users(client)
storage = Storage(client)
databases = Databases(client)
