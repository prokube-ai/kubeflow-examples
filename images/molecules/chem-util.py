import click
import logging
import random
import pandas as pd
from src.features import get_cfps
from src.utils import mol2html
from rdkit.Chem import PandasTools
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import roc_auc_score


logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command('preprocess')
@click.option('--input-data', '-i', help="Path to the input data (csv.zip).", required=True, type=str)
@click.option('--output-data', '-o', help="Path to the output.", required=True, type=str)
@click.option('--fp-bits', '-n', help="Number of the fingerprint bits.", required=False, type=int,
              default=1024)
@click.option('--id', '-d', help="Name of the ID col.", required=False, type=str, default='ID')
@click.option('--target', '-t', help="Name of the target col.", required=False, type=str, default='class')
@click.option('--sample', '-s', help="Path to where to store class samples.", required=False, type=str)
def preprocess(input_data, output_data, fp_bits, id, target, sample):
    logger.info(f"Reading in {input_data}.")
    df = pd.read_csv(input_data, index_col=0, compression='zip')
    logger.info("Calculating features.")
    PandasTools.AddMoleculeColumnToFrame(df, smilesCol='Smiles')  # adding mol objects
    fp_cols = [f'bit_{x}' for x in range(fp_bits)]
    df = df.join(
        pd.DataFrame(
            data=[get_cfps(row[1]['ROMol'], nBits=fp_bits) for row in df.iterrows()],
            columns=fp_cols
        )
    )
    logger.info(f"Storing to {output_data}.")
    df[[id, target] + fp_cols].to_csv(output_data, compression='zip')
    if sample:
        md_data = """# Sample molecules\n"""

        classes = df[target].unique()
        for c in classes:
            md_data += f"## Class {c}\n"
            m = df[df[target] == c].iloc[0]['ROMol']
            md_data += mol2html(m, legend=f'Class: {c}')
            md_data += "\n"
        with open(sample, 'w') as f:
            f.write(md_data)


@cli.command('split')
@click.option('--input-data', '-i', help="Path to the input data.", required=True, type=str)
@click.option('--output-train', '-o', help="Path to the train output.", required=True, type=str)
@click.option('--output-test', '-t', help="Path to the test output.", required=True, type=str)
@click.option('--test-fraction', '-f', help="Fraction of dataset to used for evaluation.",
              required=False, type=float, default=0.2)
@click.option('--seed', '-f', help="Random seed.",
              required=False, type=int, default=42)
def split(input_data, output_train, output_test, test_fraction, seed):
    logger.info(f"Reading in {input_data}.")
    df = pd.read_csv(input_data, index_col=0, compression='zip')
    logger.info("Splitting.")
    train, test = train_test_split(list(range(len(df))), random_state=seed)
    logger.info(f"Storing to {output_train}.")
    df.iloc[train].to_csv(output_train, compression='zip')
    logger.info(f"Storing to {output_test}.")
    df.iloc[test].to_csv(output_test, compression='zip')


@cli.command('train')
@click.option('--input-data', '-i', help="Path to the training data.", required=True, type=str)
@click.option('--output-model', '-o', help="Path to the output model.", required=True, type=str)
@click.option('--target', '-t', help="Name of the target col.", required=False, type=str, default='class')
@click.option('--n-trees', '-n', help="Number of trees.", required=False, type=int, default=16)
def train(input_data, output_model, target, n_trees):
    logger.info(f"Reading in {input_data}.")
    df = pd.read_csv(input_data, index_col=0, compression='zip')
    fp_cols = [x for x in df.columns if 'bit_' in x]
    logger.info(f'Detected {len(fp_cols)} fingerprint columns.')
    logger.info(f'Fitting a RandomForestClassifier model with {n_trees} trees.')
    clf = RandomForestClassifier(n_estimators=n_trees)
    clf.fit(df[fp_cols], df[target])
    logger.info(f'Saving model {output_model}')
    joblib.dump(clf, output_model)


@cli.command('evaluate')
@click.option('--input-data', '-i', help="Path to the test data.", required=True, type=str)
@click.option('--input-model', '-m', help="Path to the model.", required=True, type=str)
@click.option('--output-metrics', '-o', help="Filename where to store metrics.", required=False, type=str)
def evaluate(input_data, input_model, output_metrics):
    logger.info(f"Reading in {input_data}.")
    df = pd.read_csv(input_data, index_col=0, compression='zip')
    logger.info(f"Reading in the model {input_model}.")
    clf = joblib.load(input_model)
    fp_cols = [x for x in df.columns if 'bit_' in x]
    score = roc_auc_score(df['class'].values, clf.predict_proba(df[fp_cols])[:, 1])
    logger.info(f'Model roc auc score is: {score}.')
    if output_metrics:
        with open(output_metrics, 'w') as f:
            f.write(str(score))


if __name__ == '__main__':
    cli()
