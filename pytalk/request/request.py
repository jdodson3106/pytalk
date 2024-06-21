from pytalk.logger.logger import get_logger
from itertools import starmap
from pytalk.request.exceptions import NonAllowedMethodException
from typing import Tuple, Dict

class Request():
    """ Basic Request object. Currently only accepts text/html as body,
    and GET/POST as allowable request methods.
    """

    _ALLOWED_METHODS: set = {"GET", "POST"}

    def __init__(self, method: str, path: str, body="", headers={}):
        self.method = method
        self.params = {}
        self.base_url = ""
        self.path: str = path
        self.body: str = body
        self.headers: dict = headers


    @property
    def method(self):
        return self._method
    

    @method.setter
    def method(self, value):

        if value in self._ALLOWED_METHODS:
            self._method = value
            return

        raise NonAllowedMethodException(f"""
            {value} not legal method for server.
            Please choose from one of {", ".join(self._ALLOWED_METHODS)}"""
        )
    

    def _parse_path(self) -> None:
        path_parts = self.path.split("?")
        self.base_url = path_parts[0]
        
        if len(path_parts) > 1:

            params_string = path_parts[1]
            for param in params_string.split("&"):
                
                if len(param.split("=")) != 2:
                    continue

                key, value = param.split("=")
                if key in self.params:
                    continue

                self.params[key] = value

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value):
        self._path = value
        self._parse_path()



if __name__ == "__main__":

    logger = get_logger()
    request = Request(
        method="GET", 
        path="https://www.website.com/brawndo?foo=bar&plants=crave", 
    )

    logger.info(request.path)
    logger.info(request.base_url)
    logger.info(request.params)

