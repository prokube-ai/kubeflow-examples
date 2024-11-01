import click
import torch
from typing import Union
from loguru import logger
from kserve import (
    ModelServer,
)
from llama2_chat.predictor import Llama2ChatPredictor


@click.command()
@click.option("--name", type=str, default="llama2-chat", help="Model name.")
@click.option("--loglevel", type=str, default="INFO", help="Log level for loguru.")
@click.option(
    "--hf-model-string",
    type=str,
    default="meta-llama/Llama-2-13b-chat-hf",
    help="Index of the model in the hugging face model registry.",
)
@click.option(
    "--device",
    default="cpu",
    help="Device (0, 1, ..., 'cpu', 'cuda').",
)
def main(name: str, loglevel: str, hf_model_string: str, device: Union[str, int]):
    """
    Main function to initiate and start the KServe Model Server.

    Parameters:
        name: The name of the model.
        loglevel: The logging level for loguru.
        hf_model_string: Identifier for the Hugging Face model.
        device: Computational device to utilize (0, 1, 2, ..., 'cpu', 'gpu').
    """
    logger.info(f"Cuda is available? -> {torch.cuda.is_available()}")
    device = int(device) if device not in ('cpu', 'gpu', 'mps') else device
    kserve_model = Llama2ChatPredictor(
        name=name,
        hf_model_string=hf_model_string,
        loguru_loglevel=loglevel,
        device=device,
    )
    ModelServer().start([kserve_model])


if __name__ == "__main__":
    main()
