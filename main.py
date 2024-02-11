from configurations import Config


def main():
    config_manager = Config()
    print(f"Hello!\nCurrent Configuration: {config_manager.get()}")
    print("To start a chat enter /chat, to change the configuration enter /config, and to exit enter /exit.")

    while True:
        command = input(">>> ").lower()
        print(command)

        if command in ["/config", "/cnfg", "/cnf"]:
            config_manager.edit()

        elif command in ["/exit", "/quit", "/e", "/q", "/z^"]:
            break

        elif command == "/chat":
            pass

        else:
            print("Invalid command. Please try again.")


if __name__ == '__main__':
    main()
