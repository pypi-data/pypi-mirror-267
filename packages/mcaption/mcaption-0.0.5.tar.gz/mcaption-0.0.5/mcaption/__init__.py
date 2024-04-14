"""
You guessed it...
"""
from quickdl import dl
try:
    from utils import (
        models,
        base_path,
    )
    from main import (
        Caption
    )
except ImportError:
    from .utils import (
        models,
        base_path,
    )
    from .main import (
        Caption
    )


for model_key in models.keys():
    model_record = models[model_key]
    dl(base_path, model_record['url'])
