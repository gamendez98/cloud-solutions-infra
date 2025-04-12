import json
from http.client import responses

from locust import HttpUser, task, between
import random
import string

with open("variables.json") as f:
    VARIABLES = json.load(f)


def get_random_account():
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return {
        "username": username,
        "password": password,
        "email": f"{username}@gmail.com"
    }


def create_account(http_user: HttpUser, account: dict):
    print("Creating account", account)
    return http_user.client.post("/accounts", json=account)


def login(http_user: HttpUser, account: dict):
    response = http_user.client.post("/accounts/login",
                                     data={"username": account["username"], "password": account["password"]})

    if response.status_code == 200:
        token = response.json().get("token")
        http_user.client.headers.update({
            "Authorization": f"Bearer {token}"
        })
    else:
        print("Login failed:", response.text)


# Scenario 1: Indexado de documentos
# limit --- rate 2
class DocumentIndexingUser(HttpUser):
    wait_time = between(0.7, 1.3)
    host = "http://34.69.143.161"

    def on_start(self):
        random_account = get_random_account()
        response = create_account(self, random_account)
        if response.status_code == 201:
            login(self, random_account)
        else:
            print("Account creation failed:", response.text)

    @task(7)
    def index_documents(self):
        self.client.post("/documents", files={"file": open("test.pdf", "rb")})

    @task(3)
    def get_documents(self):
        self.client.get("/accounts/documents")


# Scenario 2: Generación de respuestas con LLM
class GenerateAnswersUser(HttpUser):
    wait_time = between(0.1, 0.1)
    host = "http://34.69.143.161"
    sequential = 0
    prompt = "Por favor necesito que me des informacion aleatoria de uno de los documentos que haz recibido, ademas dime si existen documentos repetidos."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = None

    @classmethod
    def get_sequential_index(cls):
        cls.sequential += 1
        return cls.sequential

    def on_start(self):
        random_account = VARIABLES['accounts'][0]
        login(self, random_account)
        self.create_chat()

    def create_chat(self):
        response = self.client.post("/chats", json={"name": "Test chat"})
        if response.status_code == 201:
            self.chat_id = response.json().get("id")
            return self.chat_id
        else:
            print("Chat creation failed:", response.text)
            return None

    @task
    def post_message(self):
        self.client.post(f"/chats/{self.chat_id}/messages", json={
            "text": self.prompt,
            "sender": "user"
        })


# Scenario 3: Information retrieval
class InformationRetrivalUser(HttpUser):
    wait_time = between(1, 3)  # Simulates user wait time between tasks
    host = "http://34.69.143.161"

    def on_start(self):
        random_user = VARIABLES['accounts'][0]
        print(random_user)
        login(self, random_user)

    @task(1)
    def get_documents(self):
        self.client.get("/accounts/documents")

    @task(1)
    def get_chats(self):
        self.client.get("/accounts/chats")


# Scenario 4: Full Load Test
class FullLoadTestUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://34.69.143.161"
    prompt = "Por favor necesito que me des informacion aleatoria de uno de los documentos que haz recibido, ademas dime si existen documentos repetidos."
    sequential = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = None

    @classmethod
    def get_sequential_index(cls):
        cls.sequential += 1
        cls.sequential %= len(VARIABLES['accounts'])
        return cls.sequential - 1

    def on_start(self):
        random_account = VARIABLES['accounts'][0]
        login(self, random_account)
        self.create_chat()

    def create_chat(self):
        response = self.client.post("/chats", json={"name": "Test chat"})
        if response.status_code == 201:
            self.chat_id = response.json().get("id")
            return self.chat_id
        else:
            print("Chat creation failed:", response.text)
            return None

    @task(40)
    def get_documents(self):
        self.client.get("/accounts/documents")

    @task(40)
    def get_chats(self):
        self.client.get("/accounts/chats")

    @task(10)
    def post_message(self):
        self.client.post(f"/chats/{self.chat_id}/messages", json={
            "text": self.prompt,
            "sender": "user"
        })


    @task(10)
    def index_documents(self):
        self.client.post("/documents", files={"file": open("test.pdf", "rb")})



