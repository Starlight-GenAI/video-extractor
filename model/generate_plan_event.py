import json 

class GeneratePlanEvent:
    id: str
    user_id: str
    is_use_subtitle: bool
    object_name: str
    
    def __init__(self, id: str, user_id:str, is_use_subtitle: bool, object_name: str):
        self.id = id 
        self.user_id = user_id
        self.is_use_subtitle = is_use_subtitle
        self.object_name = object_name
    
    def to_byte(self):
        return json.dumps(self.__dict__).encode('utf-8')