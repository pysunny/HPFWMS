import json
import datetime
from datetime import timedelta, timezone

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)