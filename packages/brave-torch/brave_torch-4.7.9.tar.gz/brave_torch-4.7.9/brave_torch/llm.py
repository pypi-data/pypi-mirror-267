import torch
from torch import nn
from zeta.structs import Decoder, Transformer, AutoregressiveWrapper
from brave_torch.main import BraveMultiModalFusion

class LLM(nn.Module):
    """
    Andromeda is a transformer-based model architecture. It initializes with
    a Transformer and AutoregressiveWrapper with default or user-specified parameters.

    Args:
    - num_tokens: Number of tokens in the vocabulary
    - max_seq_len: Maximum sequence length
    - dim: Dimension of the model
    - depth: Depth of the model
    - dim_head: Dimension of the model head
    - heads: Number of heads
    - use_abs_pos_emb: Whether to use absolute position embedding
    - alibi_pos_bias: Alibi position bias
    - alibi_num_heads: Number of alibi heads
    - rotary_xpos: Rotary position
    - attn_flash: Attention flash
    - deepnorm: Deep normalization
    - shift_tokens: Number of tokens to shift
    - attn_one_kv_head: Attention one key/value head
    - qk_norm: Query-key normalization
    - attn_qk_norm: Attention query-key normalization
    - attn_qk_norm_dim_scale: Attention query-key normalization dimension scale

    """

    def __init__(
        self,
        num_tokens=50432,
        max_seq_len=8192,
        dim=2560,
        depth=32,
        dim_head=128,
        heads=24,
        use_abs_pos_emb=False,
        alibi_pos_bias=True,
        alibi_num_heads=12,
        rotary_xpos=True,
        attn_flash=True,
        attn_kv_heads=2,
        qk_norm=True,
        kv_heads: int = 4,
        attn_qk_norm=True,
        attn_qk_norm_dim_scale=True,
        image_size: int = 256,
        patch_size: int = 32,
        encoder_dim: int = 512,
        encoder_depth: int = 6,
        encoder_heads: int = 8,
        num_of_vits: int = 4,
        *args,
        **kwargs,
    ):
        """
        Initialize the model with specified or default parameters.
        Args:
        - num_tokens: Number of tokens in the vocabulary
        - max_seq_len: Maximum sequence length
        - dim: Dimension of the model
        - depth: Depth of the model
        - dim_head: Dimension of the model head
        - heads: Number of heads
        - use_abs_pos_emb: Whether to use absolute position embedding
        - alibi_pos_bias: Alibi position bias
        - alibi_num_heads: Number of alibi heads
        - rotary_xpos: Rotary position
        - attn_flash: Attention flash
        - deepnorm: Deep normalization
        - shift_tokens: Number of tokens to shift
        - attn_one_kv_head: Attention one key/value head
        - qk_norm: Query-key normalization
        - attn_qk_norm: Attention query-key normalization
        - attn_qk_norm_dim_scale: Attention query-key normalization dimension scale
        - embedding_provider: Embedding provider module
        """
        super(LLM, self).__init__()

        try:
            self.andromeda = Transformer(
                num_tokens=num_tokens,
                max_seq_len=max_seq_len,
                use_abs_pos_emb=use_abs_pos_emb,
                attn_layers=Decoder(
                    dim=dim,
                    depth=depth,
                    dim_head=dim_head,
                    heads=heads,
                    alibi_pos_bias=alibi_pos_bias,
                    alibi_num_heads=alibi_num_heads,
                    rotary_xpos=rotary_xpos,
                    attn_flash=attn_flash,
                    attn_kv_heads=attn_kv_heads,
                    qk_norm=qk_norm,
                    kv_heads=kv_heads,
                    attn_qk_norm=attn_qk_norm,
                    attn_qk_norm_dim_scale=attn_qk_norm_dim_scale,
                    *args,
                    **kwargs,
                ),
            )

            # Decoder
            self.decoder = AutoregressiveWrapper(self.andromeda)
            
            # Encoder and Fusion
            self.fuse = BraveMultiModalFusion(
                dim=dim,
                mult=4,
                depth=1,
                image_size=image_size,
                patch_size=patch_size,
                encoder_dim=encoder_dim,
                encoder_depth=encoder_depth,
                encoder_heads=encoder_heads,
                num_of_vits=num_of_vits,
            )
            
            
            # Projection between fusion and decoder

        except Exception as e:
            print("Failed to initialize Andromeda: ", e)
            raise

    def forward(self, x: torch.Tensor, img: torch.Tensor, **kwargs):
        """
        Forward pass through the model. It expects the input x.
        Args:
        - x: Input tokens
        - kwargs: Other arguments
        Returns:
        - output from the decoder
        """
        try:
            fused = self.fuse(x, img)
            b, s, d = fused.shape
            
            # Norm
            fused = nn.LayerNorm(d)(fused)
            fused = nn.Linear(d, self.dim)(fused)
            
            model_input = self.decoder.forward(x)[0]
            return self.decoder(
                model_input, padded_x=model_input[0], **kwargs
            )
        except Exception as e:
            print(f"Failed to run forward pass: {e}")
            raise
        
        
x = torch.randn(1, 1000, 512)

img = torch.randn(1, 3, 256, 256)

model = LLM(
    dim=512,
    depth=1,
    heads=8,
    image_size=256,
    patch_size=32,
    encoder_dim=512,
    encoder_depth=6,
    encoder_heads=8,
    num_of_vits=4,
)

out = model(x, img)
print(out)
