import logging
import traceback
from typing import Optional, TypeVar, Mapping, Any

#Customer formatter
class ColorFormatter(logging.Formatter):
    # defined color list
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    # variables to set
    _debug_color: str
    _info_color: str
    _warning_color: str
    _error_color: str
    _critical_color: str
    
    # variable for saving format_str
    _format: str = r'[%(name)s]%(asctime)s - %(message)s'
    
    # list of formats for each level
    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: grey + _format + reset,
        logging.WARNING: f"{yellow}{_format}{reset}",
        logging.ERROR:  red + _format + reset,
        logging.CRITICAL: f"{bold_red}{_format}{reset}",
    }
    
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None, style: str = '%', validate: bool = True, *, defaults: Mapping[str, Any] | None = None) -> None:
        argument_list = {}
        
        if self.__validate_argument(fmt):
            self._format = fmt
            
        argument_list["fmt"] = self._format
        
        if self.__validate_argument(datefmt):
            argument_list["datefmt"] = datefmt
        
        argument_list["style"] = style
        argument_list["validate"] = validate
        
        if self.__validate_argument(defaults):
            argument_list["defaults"] = defaults
        
        super(ColorFormatter, self).__init__(**argument_list)
            
    def __validate_argument(self, argument: Any) -> bool:
        return argument is not None
    
    def format(self, record: logging.LogRecord) -> str:
        # sets the format to the corresponding record level format
        level_format = self.FORMATS.get(record.levelno)
        # returns the results from the partent format method
        level_formatter = logging.Formatter(level_format)
        results = level_formatter.format(record)
        # resets the format back to the original format
        self._fmt = self._format
        
        return results

# LogHandler class:
class LogHandler:
    """
    Summary:
    LogHandler class is used to track all of your python logs in one place. 
    It allows you to create and track the handlers for Console logging and file logging as well.
    You can also use this handler to update existing modules logs, such as adjusting log level of Boto3
    """

    # Private variables
    _loggers: dict[str, logging.Logger]
    _default_log_name: str = "AppLog"
    _default_log_level_name: str = "info"
    _default_date_format: str = r'%m/%d/%Y %I:%M:%S %p'
    _default_msg_format: str = r'[%(name)s]%(asctime)s - %(message)s'

    Log_Level = TypeVar('Log_Level')

    def __init__(self):
        """
        Constructor:
        Creates an instance of the log handler class
        Returns:
            Self: LogHandler Instance
        """
        self._loggers = {}

    def create_logger(self, log_name: Optional[str] = None,  log_level: Optional[str] = None, format: Optional[str] = None, datefmt: Optional[str] = None,  useDefaultFormat: bool = False) -> logging.Logger:
        """
        create_logger: Creates new Logger instance and returns the Logger

        Args:
            log_name (Optional[str]): Name of the default log, leave empty to use [AppLog]. Defaults to None.
            log_level (Optional[str]): Log level value. Defaults to None.
            format (Optional[str]): Configuration message format if empty defaults to [[AscTime] - message]. Defaults to None.
            datefmt (Optional[str]): Configuration date format if empty defaults to ['%m/%d/%Y %I:%M:%S %p]. Defaults to None.
        """

        # Sets initial configuration values
        _datefmt = datefmt if self.__check_value(
            datefmt) else self._default_date_format

        _format = format if self.__check_value(
            format) else self._default_msg_format

        # Creates Logger and sets initial value to info
        _log_name = log_name if self.__check_value(
            log_name) else self._default_log_name

        _level_string = log_level if self.__check_value(
            log_level) else self._default_log_level_name

        _level = self.__get_log_level(_level_string)

        logger = logging.getLogger(_log_name)
        logger.propagate = False
        logger.setLevel(_level)

        self._loggers[logger.name] = logger

        _formatter = ColorFormatter(_format, _datefmt) if not useDefaultFormat else logging.Formatter(_format, _datefmt)

        self.__create_stream_handler(
            log_name=logger.name, log_level=_level_string, formatter=_formatter)

        return logger

    def set_log_level(self, log_name: str, log_level: str) -> None:
        """
        set_log_level: Takes a string and sets the log level to mathinc level if valid

        Args:
            log_name (str): Name of log that should aply the new level changes
            log_level (str): Log level name that should be applied
        """

        if log_name not in self._loggers.keys:
            self.__handle_error(f"Error finding logger with name %{log_name}")
        else:
            found_logger = self._loggers[log_name]
            _level = self.__get_log_level(log_level)

            found_logger.setLevel(_level)

    def __get_log_level(self, log_level_string: str) -> Log_Level:
        _level = None
        match(log_level_string.upper()):
            case "INFO":
                _level = logging.INFO
            case "DEBUG":
                _level = logging.DEBUG
            case "WARNING":
                _level = logging.WARNING
            case 'ERROR':
                _level = logging.ERROR
            case 'CRITICAL':
                _level = logging.CRITICAL
            case _:
                _level = logging.INFO
                self.__handle_error(
                    f"Error log_level [{log_level_string}] is not a vaild log level. Set to default log level [INFO]")
        return _level

    def enable_log_to_file(self, log_file: str, log_name: Optional[str] = None, log_level: Optional[str] = None):
        """
        Enable Log To File: 
        Creates a new log file handler and attaches that handler to the logger with the passed name.
        If no logger was passsed it will attach the handler to the default logger.

        Args:
            log_file (str): Path of the file for the log entries
            log_name (Optional[str]): Name of the logger that will have the file handler attached. Defaults to None.
            log_level (Optional[str]): Name of the log level for file handler. Defaults to None.
        """
        _log_name = log_name if self.__check_value(
            log_name) else self._default_log_name
        _level_string = log_level if self.__check_value(
            log_level) else self._default_log_level_name

        _logger = self._loggers[_log_name]

        _level = self.__get_log_level(_level_string)

        file_handler = logging.FileHandler(filename=log_file)
        file_handler.setLevel(_level)

        _logger.addHandler(file_handler)

    def __create_stream_handler(self, log_name: Optional[str], log_level: Optional[str] = None, formatter: Optional[ColorFormatter] = None) -> None:
        """
        Create stream handler for a given Logger:
        Creates a new log console handler and attaches that handler to the logger with the passed name.
        If no logger was passsed it will attach the handler to the default logger.  

        Args:
            log_name (Optional[str]): Name of the logger that will have the console handler attached. Defaults to None.
            log_level (Optional[str]): log_level (Optional[str]): Name of the log level for file handler. Defaults to None.
            formatter (Optional[Formatter]): Formatter to set the format of the stream handler. Defaults to None.
        """
    
        # Creats the streamHandler
        console_handler = logging.StreamHandler()
        
        # Checks to make sure the log_level is valid, grabs the default log level if it is not
        _level_string = log_level if self.__check_value(log_level) else self._default_log_level_name
        _level = self.__get_log_level(_level_string)
        console_handler.setLevel(_level)
        
        # Validates the log name and sets it to default if in-valid
        _log_name = log_name if self.__check_value(log_name) else self._default_log_name
        _logger = self._loggers[_log_name] if _log_name in self._loggers else logging.getLogger(_logger)
        
        # Validats if the formatter exists, otherwise it creates a formatter based on default options
        if formatter is None:
            formatter = ColorFormatter(self._default_msg_format, self._default_date_format)
            
        console_handler.setFormatter(formatter)  
        
        _logger.addHandler(console_handler)

    def get_logger(self, log_name: Optional[str] = None) -> logging.Logger:
        """_summary_

        Args:
            log_name (Optional[str]): Name of the logger that will be retrieved.

        Returns:
            Logger | None: 
            Returns the logger if found, otherwise it will return None.
        """
        _log_name = log_name if self.__check_value(
            log_name) else self._default_log_name
        _logger = None

        if log_name in self._loggers:
            _logger = self._loggers[_log_name]

        return _logger

    def __handle_error(self, error: Exception, custom_msg: Optional[str] = None) -> None:
        traceback.print_exc()
        logging.error(error)

    def __check_value(self, value: str) -> bool:
        '''Checks variables to make sure value is not [None]'''
        return value is not None
