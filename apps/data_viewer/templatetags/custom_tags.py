import json
import pandas as pd

from django import template


register = template.Library()


@register.filter
def get(dictionary, key):
    return dictionary.get(key)


@register.filter
def jsonify(obj):
    return json.dumps(obj, default=json_serial)

def json_serial(obj):
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    raise TypeError("Type not serializable")
