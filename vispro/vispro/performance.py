import logging
import time

perf_logger = logging.getLogger("performance")

start = time.time()
# some heavy operation
end = time.time()

perf_logger.info(f"Execution time: {end - start:.2f} seconds")
