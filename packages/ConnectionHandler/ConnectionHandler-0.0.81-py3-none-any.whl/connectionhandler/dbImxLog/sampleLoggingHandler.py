from .dbImxLog import LogHandler


def log_example():

    # Can be created without any arguments
    # Can pass log level, or the base logger name
    #
    #log_handler = LogHandler()
    file_handler = LogHandler(log_level="info", base_log_name="file_log")

    # You can also pass a format for the log message and a date format in the constructor
    #LogHandler(log_level="info", base_log_name="file_log", format=r'[%(asctime)s] %(message)s', datefmt=r'%m/%d/%Y %I:%M:%S %p')
    # the format and datefmt exmaples above are passing in what I have currently set as the default passing in your own formats will override my current settings.

    # You can create a log, or get another modules log

    # boto3 existing log
    file_handler.create_logger("boto3")
    # New custom log called MyNewLog
    file_handler.create_logger("MyNewLog")

    # if you want to create a log to file you just need to call the enable file logger and pass a file path
    # if you want to assign the file handler log to a specific logger you need to pass the logger name
    # you can also pass the log level to set it when it creates the handler

    # file_handler.enable_log_to_file()
    file_handler.enable_log_to_file(
        log_file="C:\\logs\\test.log", log_name="errorLog", log_level="error")

    # the same can be done for a streamhandler, which is used for logging items to a console
    file_handler.__create_stream_handler(log_name="ConLog", log_level="info")

    # Accepted log leves are Info, Debug, Warning, Error, and Critical
    # You can update the log level anytime, either during creation of the logger or after it has been created

    file_handler.set_log_level("critical")

    # to retrieve the logger use the get_logger method and pass the name of the logger you wish you use.
    # if no name is passed it will retrieve the "default" logger in the class
    # file_handler.get_logger()

    conLog = file_handler.get_logger("ConLog")

    # the logger that is returned is the standard logger from python and can be used like normal
    conLog.error("this is my error message")

    pass
