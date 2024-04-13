import logging
import pathlib

import mlx.core as mx

from .mapping import map_key

logger = logging.getLogger("sillm")

def quantize_files(input_path: str,
                     output_path: str,
                     group_size: int = 32,
                     bits: int = 4
                     ):
    """
    Quantize weights files.
    Args:
        input_path: Path to load weights.
        output_path: Path to save quantized weights.
    """
    input_path = pathlib.Path(input_path)
    output_path = pathlib.Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    weights_files = sorted(list(input_path.glob("*.safetensors")))
    if len(weights_files) == 0:
        raise ValueError("No weights files found")
    
    def save_shard(shard, shard_path):
        mx.save_safetensors(shard_path, shard)
        logger.debug(f"Saved quantized shard to {shard_path}")
    
    shard = {}
    original_size = 0
    total_size = 0
    for weights_path in weights_files:
        logger.debug(f"Loading model weights file {weights_path}")

        weights = mx.load(str(weights_path))
        for key, weight in weights.items():
            original_size += weight.nbytes
            mlx_key = map_key(key)

            if key.endswith("weight") and len(weight.shape) > 1 and not mlx_key.startswith("tok_embeddings."):
                weight, scales, biases = mx.quantize(weight, group_size, bits)
                quant_size = weight.nbytes + scales.nbytes + biases.nbytes
                total_size += quant_size

                key_scales = key.replace(".weight", ".scales")
                key_biases = key.replace(".weight", ".biases")

                shard[key_scales] = scales
                shard[key_biases] = biases
            shard[key] = weight

        shard_path = str(output_path / weights_path.name)
        save_shard(shard, shard_path)
        shard = {}

    logger.debug(f"Quantization reduced weights size: {original_size//1024//1024:,} MB => {total_size//1024//1024:,} MB")