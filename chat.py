import json
import uuid


class Chat:
    def list(self):
        # Function for listing all the chats
        try:
            with open("chat.json", 'r') as f:
                chats = json.load(f)
            return chats
        except FileNotFoundError:
            print("No chats found. Creating a new one...")
            return self.create()

    def create(self):
        # Function for creating a new chat
        name = input("Enter a name for your chat: ")

        chat = {
            "name": name,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        }

        return self.save(chat)

    def save(self, chat, chat_id=None):
        # Функция для сохранения чата
        try:
            with open("chat.json", 'r+') as f:
                chats = json.load(f)
        except FileNotFoundError:
            chats = {"chats": {}}

        if chat_id:
            chats["chats"][chat_id] = chat  # update existing chat
        else:
            new_id = self.generate_new_id()
            chats["chats"][new_id] = chat  # create new chat

        with open("chat.json", 'w') as f:
            json.dump(chats, f)

        return chats

    def generate_new_id(self):
        # Function for generating a new ID
        return str(uuid.uuid4())

    def delete(self, chat_id):
        # Function for deleting a chat
        chats = self.list()
        if chat_id in chats["chats"]:
            print(f"Deleting chat '{chats['chats'][chat_id]['name']}'")
            while True:
                confirmation = input("Are you sure you want to delete this chat? (y/n): ").lower()
                if confirmation == "y":
                    del chats["chats"][chat_id]
                    with open("chat.json", 'w') as f:
                        json.dump(chats, f)
                    print("Chat deleted.")
                    break
                elif confirmation == "n":
                    print("Chat not deleted.")
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        else:
            print("Chat not found.")

    def get_id(self, command):
        # Function for getting the ID of a chat
        chats = self.list()
        chats_count = len(chats["chats"])
        if 1 <= int(command) <= chats_count:
            chat_id: str = list(chats["chats"].keys())[int(command) - 1]
            return chat_id
        else:
            print("Invalid chat number.")
            return None  # Return None if chat number is invalid

    def load(self, chat_id):
        # Function for loading a chat
        chats = self.list()
        if chat_id in chats["chats"]:
            return chats["chats"][chat_id]
        else:
            print("Chat not found.")
            return None
