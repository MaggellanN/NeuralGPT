import json
from openai import OpenAI
import openai


class Config:

    def create(self):
        # Function for creating a new configuration and writing it to a file
        api_key = input("Hello! To start using NeuralGPT, please enter your API key from OpenAI. If you don't have one,"
                        " we recommend you to register at openai.com, go to the developer section and get your key.\n"
                        "Enter your API key: ")
        print("Waiting for API key verification...")

        while not self.api_key_verification(api_key):
            print("Invalid API key. Please try again.")
            api_key = input("Enter your API ke  y: ")

        print("API key verified.")

        config = {
            "api_key": api_key,
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 2500
        }

        with open("config.json", 'w') as f:
            json.dump(config, f)

        return config

    def get(self):
        # A function that returns a configuration from a file or creates a new one if no file exists
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
                return config

        except FileNotFoundError:
            return self.create()

    def edit(self):
        # Function for updating the configuration
        config = Config.get(self)

        models = ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-1106", "gpt-4", "gpt-4-32k-0613", "gpt-4-32k",
                  "gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-4-1106-preview"]

        new_api_key = input("Enter new API key (press Enter to keep the existing one): ").strip()

        if new_api_key:
            print("Waiting for API key verification...")
            while not self.api_key_verification(new_api_key):
                print("Invalid API key. Please try again.")
                new_api_key = input("Enter your API key: ").strip()
                print("Waiting for API key verification...")
            print("API key verified.")
            config["api_key"] = new_api_key

        new_model = input(f"Models: {models}\nEnter new model (press Enter to keep the existing one): ").strip()

        if new_model:
            while new_model not in models:
                print("Incorrect model. Try again")
                new_model = input(f"Models: {models}\nEnter new model: ").strip()
            config["model"] = new_model

        new_temperature = input("Enter new temperature 0-2 (press Enter to keep the existing one): ").strip()

        if new_temperature:
            while True:
                try:
                    new_temperature = float(new_temperature)
                    if 0 <= new_temperature <= 2:
                        break
                    else:
                        print("Invalid input. Please enter a number between 0 and 2.")
                        new_temperature = input("Enter new temperature 0-2: ")
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 2.")
                    new_temperature = input("Enter new temperature 0-2: ")

            config["temperature"] = new_temperature

        new_max_tokens = input("Enter the maximum number of tokens that ChatGPT can use per request"
                               " (press Enter to keep the existing one): ").strip()

        if new_max_tokens:
            while True:
                try:
                    new_max_tokens = int(new_max_tokens)
                    if new_max_tokens > 0:
                        break
                    else:
                        print("Invalid input. Please enter a positive integer.")
                        new_max_tokens = input("Enter new max tokens: ")
                except ValueError:
                    print("Invalid input. Please enter a positive integer.")
                    new_max_tokens = input("Enter new max tokens: ")

            config["max_tokens"] = new_max_tokens

        with open("config.json", 'w') as f:
            json.dump(config, f)

        print("Configuration updated successfully.")

        return config

    def api_key_verification(self, api_key):
        # Function to check the validity of the API key
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.7,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hi."},
                ]
            )
            return True
        except openai.AuthenticationError:
            return False
