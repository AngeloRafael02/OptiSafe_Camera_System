class UnequalArrayLengthException(Exception):
    def __init__(self, message="Arrays must have the same length"):
        self.message = message
        super().__init__(self.message)