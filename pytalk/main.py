from server.server import PytalkServer


def main():
    server = PytalkServer(port=8080)
    server.start()


if __name__ == "__main__":
    main()
