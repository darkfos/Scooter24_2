import logging


def set_logger() -> None:
    logging.basicConfig(
        filemode="a",
        filename="scooter24-log.log",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S"
    )