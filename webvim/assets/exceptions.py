class CommandException(Exception):

    def __init__(self, error_code, error):
        self.error_code = int(error_code)
        self.error = str(error)

    def __str__(self):
        return "Error code: %s, %s" % (
            self.error_code,
            self.error,
        )
