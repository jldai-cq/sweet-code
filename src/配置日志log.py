import logging
import sys

# 配置日志
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger.info(f"Rank saved results to temp_file")
# 05/20/2025 00:22:21 - INFO - __main__ - Rank saved results to temp_file