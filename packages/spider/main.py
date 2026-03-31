import config


def main():
    config.init_db()
    config.init_redis()


if __name__ == "__main__":
    main()
