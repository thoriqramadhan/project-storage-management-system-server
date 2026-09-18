from typing import Literal
from typing import Any
import json
Status = Literal['sucess', 'failed']
def general_response(status:Status , message:str , data: dict[str, Any]):
    return json.dumps({
        "status": status ,
        "message": message,
        "data": data
    }, default=str).encode('utf-8')