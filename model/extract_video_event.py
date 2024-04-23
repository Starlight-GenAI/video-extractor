import json

class ExtractVideoEvent(object):
    id: str 
    user_id: str
    is_use_subtitle: bool
    video_url: str
    
    def __init__(self, data_byte): 
        data_dict = json.loads(data_byte.decode('utf-8'))
        for key in data_dict: 
            setattr(self, key, data_dict[key])