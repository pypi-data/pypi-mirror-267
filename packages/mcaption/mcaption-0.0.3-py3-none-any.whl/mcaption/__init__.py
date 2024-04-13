"""
You guessed it...
"""
try:
    from utils import (
        download_if_not_exist,
        models,
        base_path,
    )
    from main import (
        Caption
    )
except ImportError:
    from .utils import (
        download_if_not_exist,
        models,
        base_path,
    )
    from .main import (
        Caption
    )


for model_key in models.keys():
    model_record = models[model_key]
    download_if_not_exist(base_path, model_record['url'])
