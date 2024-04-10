import json

import pandas as pd
from .base import BaseFileHandler

class CsvHandler(BaseFileHandler):

    def load_from_fileobj(self, file, **kwargs):
        df = pd.read_csv(file,**kwargs)
        return df.to_dict('records')

    def dump_to_fileobj(self, obj, file, **kwargs): 
        df = pd.DataFrame(data = obj)
        df.to_csv(file,index=0,**kwargs)

    def dump_to_str(self, obj, **kwargs): 
        return json.dumps(obj, **kwargs)
