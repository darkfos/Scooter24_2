import logging


def set_logger() -> None:
    logging.basicConfig(
        filemode="a",
        filename="scooter24-log.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
