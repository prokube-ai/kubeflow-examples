from pytorch_lightning.plugins.environments import KubeflowEnvironment
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning import Trainer
import click
from typing import List
from custom_callbacks import MinioSynchingCallback, StdOutLoggerCallback
from mnist_lightning_modules import SimpleCNN, MNISTDataModule
from loguru import logger
import os


@click.command()
@click.option("--batch_size", default=64, help="Batch size for training.")
@click.option("--learning_rate", default=0.001, help="Learning rate for optimizer.")
@click.option("--epochs", default=10, help="Number of epochs to train.")
@click.option(
    "--num_nodes",
    default=1,
    help="Number of nodes (master+worker) to train the model on",
)
@click.option(
    "--num_data_loader_workers",
    default=0,
    help="Number of processes for the data loader per pod",
)
@click.option(
    "--run_as_pytorchjob",
    default=True,
    type=bool,
    help="Whether to run as a PyTorchJob on Kubeflow.",
)
@click.option("--dropout_rate", default=0.2, help="Dropout rate for the network.")
@click.option(
    "--logs_bucket",
    default="kubeflow-examples",
    help="Name of the Minio bucket where logs will be stored.",
)
@click.option(
    "--logs_folder",
    default="mnist-logs",
    help="Name of the folder within the Minio bucket where logs will be stored.",
)
@click.option(
    "--sync_with_minio",
    default=True,
    type=bool,
    help="Whether to sync logs and checkpoints with Minio or not.",
)
@click.option(
    "--use_std_out_logger",
    default=True,
    type=bool,
    help="Whether print train and val loss to standard out or not.",
)
def main(
    batch_size: int = 64,
    learning_rate: float = 0.001,
    epochs: int = 10,
    run_as_pytorchjob: bool = True,
    logs_bucket: str = "kubeflow-examples",
    logs_folder: str = "mnist-logs",
    dropout_rate: float = 0.2,
    sync_with_minio: bool = True,
    num_nodes: int = 1,
    num_data_loader_workers: int = 4,
    use_std_out_logger: bool = False,
) -> None:
    # Log relevant environment variables
    logger.debug(f'NODE_RANK: {os.environ.get("NODE_RANK", "Not set")}')
    logger.debug(f'LOCAL_RANK: {os.environ.get("LOCAL_RANK", "Not set")}')
    logger.debug(f'WORLD_SIZE: {os.environ.get("WORLD_SIZE", "Not set")}')

    # Initialize model and data module
    logger.debug(f"Input for run_as_pytorchjob {run_as_pytorchjob}")
    model = SimpleCNN(lr=learning_rate, dropout_rate=dropout_rate)
    data_module = MNISTDataModule(
        batch_size=batch_size, num_workers=num_data_loader_workers
    )

    # Initialize tensorboard logger
    tb_logger = TensorBoardLogger(
        save_dir=f"{logs_bucket}/{logs_folder}", name="PytorchLightningMNIST"
    )

    # Initialize callbacks
    callbacks: List = [ModelCheckpoint(save_top_k=1, verbose=True)]
    if sync_with_minio:
        callbacks.append(
            MinioSynchingCallback(
                minio_bucket=logs_bucket,
                minio_logs_folder=logs_folder,
            )
        )
    if use_std_out_logger:
        callbacks.append(StdOutLoggerCallback())

    # Initialize trainer
    trainer = Trainer(
        logger=tb_logger,
        plugins=[KubeflowEnvironment()] if run_as_pytorchjob else [],
        max_epochs=epochs,
        callbacks=callbacks,
        default_root_dir=f"{logs_bucket}/{logs_folder}",
        strategy="ddp",
        num_nodes=num_nodes,
        devices=1,
    )

    # Log relevant trainer attributes
    logger.debug(f"Trainer accelerator: {trainer.accelerator}")
    logger.debug(f"Trainer strategy: {trainer.strategy}")
    logger.debug(f"Trainer global_rank: {trainer.global_rank}")
    logger.debug(f"Trainer local_rank: {trainer.local_rank}")

    # Training
    trainer.fit(model, data_module)


if __name__ == "__main__":
    main()
