class Logger():
    @staticmethod
    def logrecord(exception) -> None:
        with open("log_error.txt", 'a') as file:
            file.write(exception)
        return None       
