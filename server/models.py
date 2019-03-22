from typing import Dict, NamedTuple
from uuid import uuid4


class Client(NamedTuple):
    id: str
    name: str
    phone_number: str
    email: str


class User:
    def __init__(self, login):
        self.login = login
        self.clients: Dict[str, Client] = {}
        self.phone_numbers = set()
        self.emails = set()

    def create_client(self, name: str, phone_number: str, email: str) -> Client:
        if phone_number in self.phone_numbers or email in self.emails:
            raise FileExistsError
        client = Client(
            id=uuid4().hex,
            name=name,
            phone_number=phone_number,
            email=email)
        self.clients[client.id] = client
        self.phone_numbers.add(phone_number)
        self.emails.add(email)
        return client

    def delete_client(self, client_id: str) -> None:
        self.phone_numbers.remove(self.clients[client_id].phone_number)
        self.emails.remove(self.clients[client_id].email)
        self.clients.pop(client_id)
