## Pytorch Implementation of ViT
Original Paper link: <a href="https://arxiv.org/abs/2010.11929">An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale(Alexey Dosovitskiy et al.)</a>

## Install

```bash
$ pip install vit-pytorch-implementation
```

#Usage:

```python
import torch
from vit_pytorch import lilViT

v = lilViT(
                 img_size=224, 
                 in_channels=3,
                 patch_size=16, 
                 num_transformer_layers=12,
                 embedding_dim=768,
                 mlp_size=3072,
                 num_heads=12, 
                 attn_dropout=0,
                 mlp_dropout=0.1,
                 embedding_dropout=0.1,
                 num_classes=1000
)

img = torch.randn(1, 3, 224, 224)

preds = v(img) # (1, 1000)
preds.shape
```


## Parameters

- `img_size`: int.  
Image resolution. Default=224(224x224)
- `in_channels`: int.  
Image channels. Default `3`
- `patch_size`: int.  
Size of patches. `image_size` must be divisible by `patch_size`.  
The number of patches is: ` n = (image_size // patch_size) ** 2` and `n` **must be greater than 16**. Default `16`
- `num_transformer_layers`: int.  
Depth(number of transformer blocks). Default `12`
- `embedding_dim`: int.  
Embedding dimension. Default `768`
- `mlp_size`: int.  
MLP size. Default `3072`
- `num_heads`: int.  
Number of heads in Multi-head Attention layer. Default `12`
- `attn_dropout`: float.  
Dropout for attention projection. Default `0`
- `mlp_dropout`: float  
Dropout for dense/MLP layers. Default `0.1` 
- `embedding_dropout`: float.   
Dropout for patch and position embeddings.Default `0.1`
- `num_classes`: int.  
Number of classes to classify. Default `1000`
