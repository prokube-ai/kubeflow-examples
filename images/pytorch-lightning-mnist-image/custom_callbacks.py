import s3fs
from pytorch_lightning.callbacks import Callback
import os
import pytorch_lightning as pl
from loguru import logger
from typing import Dict, Any
from pytorch_lightning import Trainer

class StdOutLoggerCallback(Callback):
    """
    Callback for logging training and validation loss to standard output.

    This callback is designed for use with Katib hyperparameter tuning.
    It prints the training and validation loss metrics in a way that Katib
    can parse from the logs to understand the objective metric.
    """

    def on_save_checkpoint(
        self,
        trainer: "pl.Trainer",
        _: "pl.LightningModule",  # Unused variable pl_module
        __: Dict[str, Any],  # Unused variable checkpoint
    ) -> None:
        epoch = trainer.current_epoch
        metrics = trainer.callback_metrics
        if 'train_loss' in metrics and 'val_loss' in metrics:
            print(f"\nepoch {epoch}:")
            print(f"train_loss={metrics['train_loss'].item():.1e}")
            print(f"val_loss={metrics['val_loss'].item():.1f}")




class MinioSynchingCallback(Callback):
    """
    A PyTorch Lightning Callback to synchronize training logs and model checkpoints
    between a local folder and a Minio S3 Bucket.
    """

    def __init__(self, minio_bucket: str, minio_logs_folder: str) -> None:
        super().__init__()
        self.fs = self.create_s3_client()
        self.logs_folder = f"{minio_bucket}/{minio_logs_folder}"

        # Ensure the Minio bucket and folder exist
        self.create_bucket_if_not_exists(minio_bucket)
        self.create_folder_if_not_exists()

        # Download any existing logs from Minio
        self.download_existing_logs()

    @staticmethod
    def create_s3_client() -> s3fs.S3FileSystem:
        """Initializes the S3 Client."""
        return s3fs.S3FileSystem(
            anon=False,
            use_ssl=False,
            client_kwargs={
                "endpoint_url": f'http://{os.environ["S3_ENDPOINT"]}',
                "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
                "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
            },
        )

    def download_existing_logs(self) -> None:
        """Downloads existing logs from Minio bucket if they are not already present locally."""
        if not os.path.exists(self.logs_folder):
            logger.debug(
                f"Downloading minio logs to this local directory: {self.logs_folder}"
            )
            self.fs.download(self.logs_folder, self.logs_folder, recursive=True)

    def create_folder_if_not_exists(self) -> None:
        """Creates the Minio folder if it does not already exist."""
        if not self.fs.exists(self.logs_folder):
            logger.debug(f"Attempting to create folder in Minio at: {self.logs_folder}")
            self.fs.touch(f"{self.logs_folder}/empty_file")

    def create_bucket_if_not_exists(self, bucket_name: str) -> None:
        """Creates the Minio bucket if it does not already exist."""
        if bucket_name not in self.fs.ls("/"):
            logger.debug(f"Creating bucket {bucket_name}")
            self.fs.mkdir(f"/{bucket_name}")

    def on_save_checkpoint(
        self,
        trainer: "pl.Trainer",
        _: "pl.LightningModule",  # Unused variable pl_module
        __: Dict[str, Any],  # Unused variable checkpoint
    ) -> None:
        """Called when a new checkpoint is saved. Here, we synchronize the checkpoints with Minio."""
        # only do this in the master in case we run a distributed training
        if trainer.global_rank == 0:
            checkpoint_files = self.fs.ls(f"{trainer.logger.log_dir}/checkpoints")
            if checkpoint_files:
                self.fs.rm(checkpoint_files)
                logger.debug(f"Removed checkpoint files: {checkpoint_files}")

            logger.debug("Uploading logs from local to Minio at the end of the epoch.")
            self.fs.upload(
                f"{self.logs_folder}/*",
                self.logs_folder,
                recursive=True,
            )
