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
        self.body: str = body 

    # print all instance variables, but ignore properties, like self._method
    # HOWEVER, although this is ignoring _method, it's not catching method :/
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
    def body(self):
        return self._body
    
    @body.setter
    def body(self, value: str):

        content_type = self.headers.get("Content-Type")
        if content_type == None:
            self._body = ""
            return
        if content_type == "text/html":
            self._body = value
        elif content_type.split(";")[0] == "multipart/form-data": 
            body_lines = value.split("\r\n")
            form_data = {}
            for i, body_line in enumerate(body_lines): 
                if not body_line:
                    continue
                if "name=" in body_line:
                    key = body_line.split("name=")[-1][1:-1] #strip quotes
                    value = body_lines[i+2]
                    form_data[key] = value
            self._body = form_data


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