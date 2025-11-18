from log_class import LogLevel, LogClass

def main():
    logger = LogClass()
    logger.add_log(LogLevel.INFO, "Program Manager", "Process 0x12345 has been started", "System")
    logger.add_log(LogLevel.DEBUG, "User Program", "Hello World!", "User", additional_info="debugging")
    logger.add_log(LogLevel.WARN, "Device Manager", "GPU temperature warning", "System", additional_info="temperature = 90")
    logger.add_log(LogLevel.ERROR, "Program Manager", "Process 0x12345 terminated with error 00000001", "System")
    logger.add_log(LogLevel.FATAL, "Device Manager", "GPU device disconnected unexpectedly", "System")
    
if __name__ == "__main__":
    main()