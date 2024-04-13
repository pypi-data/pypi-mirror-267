"""
Main application code.
"""
from mcaption.clip import clip
import torch
import numpy as np
from transformers import (
    GPT2Tokenizer,
)
import PIL.Image

try:
    from utils import (
        base_path,
        models,
        ClipCaptionModel,
        generate_beam,
        generate2,
    )
except ImportError:
    from .utils import (
        base_path,
        models,
        ClipCaptionModel,
        generate_beam,
        generate2,
    )


class Caption:
    """
    This will add auto-captioning to images.
    """
    model = None
    clip_model = None
    tokenizer = None
    weights = None

    def __init__(
            self, model: str = 'conceptual', device: str = 'cpu',
            prefix_length: int = 10, inherit: ['Caption', None] = None
    ):
        self.inherit = inherit
        self.torch_model = model
        self.torch_device = device
        self.clip_prefix_length = prefix_length
        self._set_inherit()

    def _set_inherit(self):
        """
        This will conditionally inherit the non-model-specific objects from another instance of mcaption.Caption
        or, alternatively, init them locally.

        This is to save resources in the event we are using multiple models / instances.
        """
        if self.inherit is not None:
            self.device = self.inherit.device
            self.clip_model, self.preprocess = self.inherit.clip_model, self.inherit.preprocess
            self.tokenizer = self.inherit.tokenizer
            self.prefix_length = self.inherit.prefix_length
        else:
            self.device = torch.device(self.torch_device)
            self.clip_model, self.preprocess = clip.load(
                "ViT-B/32", device=self.device, jit=False
            )
            self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            self.prefix_length = self.clip_prefix_length
        self.weights = torch.load(base_path / models[self.torch_model]['file'], map_location=self.device)
        self.model = ClipCaptionModel(self.prefix_length)
        self.model.load_state_dict(self.weights, strict=False)
        self.model = self.model.eval()  # I think we can just use eval...
        self.model = self.model.to(self.device)

    def predict(self, image: np.ndarray, beam: bool = False) -> str:
        """
        Create the image captions.
        """
        pil_image = PIL.Image.fromarray(image)
        image = self.preprocess(pil_image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            prefix = self.clip_model.encode_image(image).to(
                self.device, dtype=torch.float32
            )
            prefix_embed = self.model.clip_project(prefix).reshape(1, self.prefix_length, -1)
        if beam:
            result = generate_beam(self.model, self.tokenizer, embed=prefix_embed)[0]
        else:
            result = generate2(self.model, self.tokenizer, embed=prefix_embed)
        return result
