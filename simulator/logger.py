import logging

# Configure logging for the entire simulator
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger("OrderExecutionSimulator")
