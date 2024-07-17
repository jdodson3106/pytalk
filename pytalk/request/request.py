from pytalk.logger.logger import get_logger
from pytalk.request.exceptions import NonAllowedMethodException
from http.client import HTTPMessage

class Request():
    """ Basic Request object. Currently only accepts text/html as body,
    and GET/POST as allowable request methods.
    """

    _ALLOWED_METHODS: set = {"GET", "POST"}

    def __init__(self, method: str, path: str, headers: HTTPMessage, body=""):
        self.method = method
        self.params = {}
        #self.base_url = ""
        self.headers = headers
        self.path: str = path
        self.body: list = body

    # print all instance variables, but ignore properties, like self._method
    def __repr__(self):
        items = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"): 
                continue
            if key == "headers": 
                items["headers"] = {key: value for key, value in self.headers.items()}
                continue
            items[key] = value
        
        return f"Request({items})"

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
        #self.base_url = path_parts[0]
        
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

    logger = get_logger(name="root")
    request = Request(
        method="GET", 
        path="/brawndo?foo=bar&plants=crave", 
    )
    logger.info(request)