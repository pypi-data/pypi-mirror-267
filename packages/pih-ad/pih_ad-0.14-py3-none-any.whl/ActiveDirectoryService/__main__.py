import ipih


def start() -> None:
    from ActiveDirectoryService.service import start

    start(True)


if __name__ == "__main__":
    start()
