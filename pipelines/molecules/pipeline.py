from kfp import dsl
from kfp.dsl import Input, Output, Dataset, Markdown, Model, Metrics
from kfp import compiler
import os

# You will likely want to set COMPONENTS_IMAGE env var accordingly
COMPONENTS_IMAGE = os.environ.get('COMPONENTS_IMAGE', None)

if not COMPONENTS_IMAGE:
    raise EnvironmentError("COMPONENTS_IMAGE env variable is not defined")


@dsl.container_component
def preprocess(input_data: Input[Dataset], output: Output[Dataset], viz: Output[Markdown], n_bits: int):
    return dsl.ContainerSpec(
        image=COMPONENTS_IMAGE,
        command=["/opt/conda/bin/python", "chem-util.py"],
        args=["preprocess", "-i", input_data.path, "-o", output.path, "-s", viz.path, '--fp-bits', n_bits])


@dsl.container_component
def split(input_data: Input[Dataset], output_train: Output[Dataset], output_test: Output[Dataset]):
    return dsl.ContainerSpec(
        image=COMPONENTS_IMAGE,
        command=["/opt/conda/bin/python", "chem-util.py"],
        args=["split", "-i", input_data.path, "-o", output_train.path, "-t", output_test.path])


@dsl.container_component
def train(input_data: Input[Dataset], output: Output[Model], n_trees: int):
    return dsl.ContainerSpec(
        image=COMPONENTS_IMAGE,
        command=["/opt/conda/bin/python", "chem-util.py"],
        args=["train", "-i", input_data.path, "-o", output.path, "--n-trees", n_trees])


@dsl.container_component
def evaluate(input_data: Input[Dataset], model: Input[Model], metric: dsl.OutputPath(float)):
    return dsl.ContainerSpec(
        image=COMPONENTS_IMAGE,
        command=["/opt/conda/bin/python", "chem-util.py"],
        args=["evaluate", "-i", input_data.path, "-m", model.path, "-o", metric])


@dsl.component
def report_metric(metric: float, metric_output: Output[Metrics]):
    # Using regular component to report a metric
    metric_output.log_metric("ROC AUC", metric)


@dsl.pipeline
def chem_classification_pipeline(n_bits: int, n_trees: int):
    importer = dsl.importer(
        artifact_uri='minio://kubeflow-examples/data/molecules/ames.csv.zip',
        artifact_class=dsl.Dataset,
        reimport=True,
    )
    preprocessed = preprocess(input_data=importer.output, n_bits=n_bits)
    split_data = split(input_data=preprocessed.outputs['output'])
    train_model = train(input_data=split_data.outputs['output_train'], n_trees=n_trees)
    metric = evaluate(input_data=split_data.outputs['output_test'], model=train_model.output)
    report_metric(metric=metric.outputs['metric'])


if __name__ == "__main__":
    compiler.Compiler().compile(chem_classification_pipeline, 'pipeline.yaml')
