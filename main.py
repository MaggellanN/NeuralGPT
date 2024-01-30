import openai
import json


def get_config():
    # Функция, которая возвращает конфигурацию из файла или создает новую, если файл отсутствует
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
            return config

    except FileNotFoundError:
        return create_config()


def create_config():
    # Функция для создания новой конфигурации и записи ее в файл
    api_key = input("Hello! To start using NeuralGPT, please enter your API key from OpenAI. If you don't have one, we "
                    "recommend you to register at openai.com, go to the developer section and get your key.\n")

    openai.api_key = api_key

    # Тестовый запрос, чтобы убедиться, что API ключ действителен
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Hello",
        max_tokens=50
    )

    try:
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
    except:

# Основная функция, вызывающая get_config
def main():
    config = get_config()
    print("Current Configuration:", config)


if __name__ == '__main__':
    main()
