"""
This module provides a custom Logger class for logging messages with 
additional information.

The Logger class provides static methods for logging messages at different 
levels (INFO, DEBUG, WARNING, ERROR, CRITICAL). Each log message includes 
the current time, file name, function name, and line number.
"""

# pylint: disable=C0103

import inspect
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Close the log handlers
for handler in logging.root.handlers[:]:
    handler.close()
    logging.root.removeHandler(handler)

# Rename the existing latest.log file to a timestamped filename
if os.path.exists("logs/latest.log"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    try:
        os.rename("logs/latest.log", f"logs/{timestamp}.log")
    except PermissionError:
        print(
            "Warning: Could not rename the log file because it is being used by another process."
        )


class Logger:
    """
    A custom Logger class for logging messages with additional information.

    This Logger provides static methods for logging messages at different levels
    (INFO, DEBUG, WARNING, ERROR, CRITICAL). Each log message includes the current
    time, file name, function name, and line number.
    """

    @staticmethod
    def setup():
        """
        Sets up the logger to print to both the terminal and a file.
        """
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s, %(message)s",
            handlers=[logging.FileHandler("logs/latest.log"), logging.StreamHandler()],
        )

    @staticmethod
    def INFO(message: str):
        """
        Logs an informational message.

        Parameters:
        message (str): The message to log.
        """
        Logger.log(message, logging.INFO)

    @staticmethod
    def DEBUG(message: str):
        """
        Logs a debug message.

        Parameters:
        message (str): The message to log.
        """
        Logger.log(message, logging.DEBUG)

    @staticmethod
    def WARNING(message: str):
        """
        Logs a warning message.

        Parameters:
        message (str): The message to log.
        """
        Logger.log(message, logging.WARNING)

    @staticmethod
    def ERROR(message: str):
        """
        Logs an error message.

        Parameters:
        message (str): The message to log.
        """
        Logger.log(message, logging.ERROR)

    @staticmethod
    def CRITICAL(message: str):
        """
        Logs a critical message.

        Parameters:
        message (str): The message to log.
        """
        Logger.log(message, logging.CRITICAL)

    @staticmethod
    def log(message: str, level: int):
        """
        Logs a message with the current time, file name, function name, and line number.

        Parameters:
        message (str): The message to log.
        level (int): The logging level of the message (e.g., logging.INFO, logging.DEBUG).
        """
        # Get the previous frame in the stack, otherwise it would be this function
        frame = (
            inspect.currentframe().f_back.f_back
        )  # One more step back to get the caller of INFO, DEBUG, etc.
        if frame is not None:
            func = frame.f_code

            # Prepare the log message
            log_message = (
                f"Level: {logging.getLevelName(level)}, "
                f"File: {os.path.normpath(func.co_filename)}, "
                f"Function: {func.co_name}, Line: {frame.f_lineno}, "
                f"Message: {message}"
            )

            # Log the message at the appropriate level
            logging.log(level, log_message)
        else:
            logging.error("Error: Could not get the current frame.")


# Setup the logger
Logger.setup()