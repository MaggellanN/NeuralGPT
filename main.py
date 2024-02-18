from configurations import Config
from chat import Chat
from openai import OpenAI


def main():
    config_manager = Config()
    print("To start a chat, enter the command '/chat'. To change the configuration, enter the command '/config'. "
          "If you need to view the current configuration, enter the '/get' command. "
          "To exit the chat, enter the command '/exit'.")

    commands = {
        "/config": config_manager.edit,
        "/chat": chat_menu,
        "/exit": exit,
        "/get": config_manager.get
    }

    while True:
        command = input("Main menu >>> ").lower()

        if command in commands:
            commands[command]()
        else:
            print("Invalid command. Please try again.")


def chat_menu():
    # Function for handling the chat menu
    chat_manager = Chat()
    chats = chat_manager.list()

    commands = {
        "/new": chat_manager.create,
        "/menu": main,
        "/chats": lambda: chat_menu()
    }

    for i, chat in enumerate(chats["chats"].values(), 1):
        print(f"{i}. \"{chat['name']}\" tagged as {i}.")

    print("Enter the chat number or enter '/new' to create a new chat, "
          "if you need to return to the menu, enter '/menu'. To show the list of chats, enter '/chats': ")
    while True:
        command = input("Chat menu >>> ")
        if command in commands:
            commands[command]()
        elif command.isdigit():
            chat_id = chat_manager.get_id(command)
            handle_chat(chat_id)
        else:
            print("Invalid command. Please try again.")


def handle_chat(chat_id):
    # Function for handling a chat
    chat_manager = Chat()
    chat_command = {
        "/delete": lambda: (chat_manager.delete(chat_id), main()),
        "/menu": main,
        "/back": chat_menu,
        "/load": lambda: (dialogue(chat_manager.load(chat_id), chat_id), main())
    }

    chat_name = chat_manager.list()["chats"][chat_id]["name"]

    print("Type '/delete' to delete this chat, or '/menu' to return to the main menu or "
          "'/back' to return to the chat menu. Type '/load' to load this chat.")

    while True:
        command = input(f"{chat_name} menu >>> ")
        if command in chat_command:
            chat_command[command]()
        else:
            print("Invalid command. Please try again.")


def dialogue(chat, chat_id):
    chat_manager = Chat()
    config_manager = Config()

    client = OpenAI(api_key=config_manager.get()["api_key"])
    print(f"---{chat['name']}---")
    for message in chat["messages"]:
        if message["role"] == "user":
            print(f"You: {message['content']}")
            continue
        if message["role"] == "system":
            continue
        print(f"{message['role']}: {message['content']}")

    while True:
        message = input("You: ")
        if message == "/exit":
            print("Chat exited and saved.")
            chat_manager.save(chat, chat_id)
            chat_menu()
        else:
            chat["messages"].append({"role": "user", "content": message})
            response = client.chat.completions.create(
                model=config_manager.get()["model"],
                temperature=config_manager.get()["temperature"],
                messages=chat["messages"]
            )
            if response.choices:
                for choice in response.choices:
                    if choice.finish_reason == 'stop' and choice.message:
                        print(f"Assistant: {choice.message.content}")
                        chat["messages"].append({"role": "assistant", "content": choice.message.content})
            else:
                print("No response from the assistant.")


if __name__ == '__main__':
    config_manager = Config()
    print(f"Hello!\nCurrent Configuration: {config_manager.get()}")
    main()
