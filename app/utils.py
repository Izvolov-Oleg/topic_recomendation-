import time
from contextlib import contextmanager
from loguru import logger


@contextmanager
def timer(name: str) -> None:
    t0 = time.time()
    yield
    total_time = time.time() - t0
    logger.info(f"{name} exec time: {total_time:.3f}s")
