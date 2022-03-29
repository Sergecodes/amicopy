

class WSClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

