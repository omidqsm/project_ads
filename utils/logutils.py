import structlog

# if we switched from structlog to another logger we can simply modify this file to return
# appropriate logger


def get_logger(name: str):
    return structlog.get_logger(name)
