from datetime import datetime

class Logger:
    def __init__(self, logUri):
        self.logUri = logUri
    
    def log(self, message):
        with open(self.logUri, "a") as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")}: {message}\r\n')
        