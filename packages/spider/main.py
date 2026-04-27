import config
import spider


def main():
    db = config.init_db()
    spider.spider(db, "https://pypi.org/project/beautifulsoup4/")

    # config.init_redis()


if __name__ == "__main__":
    main()
