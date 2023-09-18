import kserve
import click
from src.serving import MolTransformer, MolPredictor

DEFAULT_MODEL_NAME = "model"


@click.group()
def cli():
    pass


@cli.command('serve_transformer', context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option('--model_name', default=DEFAULT_MODEL_NAME,
              help='The name that the model is served under.', type=str)
@click.option('--predictor_host', help='The URL for the model predict function', required=True, type=str)
@click.option('--n_bits', help='Number of bits to use for the fingerprint', required=False, type=int,
              default=1024)
def serve_transformer(model_name, predictor_host, n_bits):
    transformer = MolTransformer(
        name=model_name,
        predictor_host=predictor_host,
        n_bits=n_bits
    )
    server = kserve.ModelServer()
    server.start(models=[transformer])


@cli.command('serve_predictor', context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option('--model_name', default=DEFAULT_MODEL_NAME,
              help='The name that the model is served under.', type=str)
def serve_predictor(model_name):
    predictor = MolPredictor(
        name=model_name,
    )
    server = kserve.ModelServer()
    server.start(models=[predictor])


if __name__ == "__main__":
    cli()
