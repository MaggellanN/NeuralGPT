from openai import OpenAI
import openai
import json
import os


def create_config():
    # Функция для создания новой конфигурации и записи ее в файл
    api_key = input("Hello! To start using NeuralGPT, please enter your API key from OpenAI. If you don't have one, we "
                    "recommend you to register at openai.com, go to the developer section and get your key.\n")

    try:
        # Проверяем валидность API ключа
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hi."},
            ]
        )

        # Создаем новую конфигурацию
        config = {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1500,
            "api_key": api_key
        }

        # Записываем конфигурацию в файл
        with open("config.json", 'w') as f:
            json.dump(config, f)

        return config

    except openai.AuthenticationError as e:

        print(f"OpenAI Authentication Error: {e}")

        print("Looks like the provided API key is invalid. Please check and try again.")

    except Exception as e:

        print(f"Error: {e}")


def get_config():
    # Функция, которая возвращает конфигурацию из файла или создает новую, если файл отсутствует
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
            return config

    except FileNotFoundError:
        return create_config()


def main():
    config = get_config()
    print(f"Hello!\nCurrent Configuration: {config}")
    print("To start a chat enter /chat, to change the configuration enter /config, and to exit enter /exit.")

    while True:
        command = input("> ")


if __name__ == '__main__':
    main()
