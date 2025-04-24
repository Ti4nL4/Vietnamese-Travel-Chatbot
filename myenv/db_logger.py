import logging
import os
import time
import functools
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/db_operations_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('db_logger')

def log_db_operation(operation_name):
    """
    Decorator to log database operations
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.info(f"Starting {operation_name}")
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                logger.info(f"Completed {operation_name} in {elapsed_time:.2f} seconds")
                return result
            except Exception as e:
                elapsed_time = time.time() - start_time
                logger.error(f"Error in {operation_name} after {elapsed_time:.2f} seconds: {str(e)}")
                raise
        return wrapper
    return decorator

def log_query(query, params=None):
    """
    Log a SQL query and its parameters
    """
    if params:
        logger.debug(f"Query: {query}")
        logger.debug(f"Parameters: {params}")
    else:
        logger.debug(f"Query: {query}")

def log_query_result(result):
    """
    Log the result of a query
    """
    if isinstance(result, list):
        logger.debug(f"Query returned {len(result)} rows")
    else:
        logger.debug(f"Query result: {result}") 