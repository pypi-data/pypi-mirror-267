class VlocDetectError(Exception):

    def __init__(self,  message: str):
        self.message = message


class VlocOcrError(Exception):

    def __init__(self,  message: str):
        self.message = message
