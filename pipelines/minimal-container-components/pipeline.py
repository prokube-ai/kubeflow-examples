from kfp import dsl
from kfp.dsl import Input, Output, Dataset, Markdown


COMPONENTS_IMAGE = 'alpine:3.18.2'


@dsl.container_component
def ingest_data(input_data: str, output: Output[Dataset]):
    return dsl.ContainerSpec(
        image=COMPONENTS_IMAGE,
        command=['sh', '-c', 'echo $0 >> $1'],  # using sh -c for more flexibility
        args=[input_data, output.path])


@dsl.container_component
def merge_data(dataset1: Input[Dataset], dataset2: Input[Dataset], output: Output[Dataset]):
    return dsl.ContainerSpec(
        image=COMPONENTS_IMAGE,
        command=['sh', '-c', 'cat $0 >> $2 && cat $1 >> $2'],
        args=[dataset1.path, dataset2.path, output.path])


@dsl.container_component
def copy_data(dataset: Input[Dataset], output: Output[Markdown]):
    # Certain output types are show as visualizations in task view
    return dsl.ContainerSpec(
        image=COMPONENTS_IMAGE,
        command=['cp'],  # passing arguments directly to a command
        args=[dataset.path, output.path])


@dsl.pipeline
def container_components_pipeline(input1: str, input2: str):
    # input1 and input2 arguments are exposed also in the UI
    result00 = ingest_data(input_data=input1)
    result01 = ingest_data(input_data=input2)
    merged = merge_data(dataset1=result00.output, dataset2=result01.output)
    copy_data(dataset=merged.output)
