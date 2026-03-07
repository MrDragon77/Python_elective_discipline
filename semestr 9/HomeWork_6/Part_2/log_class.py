from audioop import add
from datetime import datetime
from enum import Enum

class LogLevel(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"

class LogClass:
    def __init__(self, path_to_log_file='log.log'):
        self.path_to_log_file = path_to_log_file
        self.event_counter = 0
        
    def get_timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    def make_event(self):
        self.event_counter += 1
        return self.event_counter
    
    def write_to_file(self, log_message):
        try:
            with open(self.path_to_log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
                f.flush()
        except:
            raise RuntimeError("Error while writing log to file")
    
    def add_log(self, level: LogLevel, source, message, user, additional_info=None):
        timestamp = self.get_timestamp()
        event_id = self.make_event()
        
        log_text = f"id: {event_id} | {timestamp} | level: {level.value} // {source} --- {message} | user: {user}"

        if additional_info:
            log_text += f" // Additional: {additional_info}"
        
        self.write_to_file(log_text)


