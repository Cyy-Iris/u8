"""Module containing utils for apache airflow.

It allows to auto create tasks handling dependencies with s3.

TODO (Guillaume): add capacity to auto resolve DAG from tasks definitions.

It contains the following:

    * :func:`airflow_task`: a decorator allowing to specify s3 folder paths for inputs
        and outputs. It uses airflow io (taskFlow) to resolve dependencies within s3 and
        then downloads files before the task and upload files at the end of the tasks.
"""
import functools
import inspect
import os
from typing import Any, Callable

import boto3
from airflow.decorators import task
from airflow.decorators.base import FParams, FReturn, Task
from airflow.operators.python import get_current_context

from automodeling.utils.file_storage_layer import FileStorageOperations


# TODO (Guillaume): improve typing of the callables
def airflow_task(
    s3folder_inputs: list[str], s3folder_outputs: list[str]
) -> Callable[
    [Callable], Callable[[Callable[FParams, FReturn]], Task[FParams, FReturn]]
]:
    if os.getenv("FILE_STORAGE_LAYER_ENV") == "local":
        file_storage_instance = FileStorageOperations()

    else:
        s3_client = boto3.client("s3")
        file_storage_instance = FileStorageOperations(s3_client)
    """Airflow task decorator allowing to specify inputs / outputs from s3.

    This decorator resolves s3 folder path into local file for the wrapped function. It
    uses s3 folder definitions from inputs / outputs specified when wrapping a function
    and airflow io passed into the task at execution time of the DAG.

    Important Notes:
        * :arg:`s3folder_inputs`: must match in length the wrapped function args length.
        * :arg:`s3folder_outputs`: must match in length the wrapped function outputs
            length.

    Args:
        s3folder_inputs: folder path in s3 where to find the files for a corresponding
            arg in the wrapped function.
        s3folder_outputs: folder path in s3 where to store the files resulting of the
            wrapped function execution.

    Returns:

        A decorator ready to wrap a function into an Airflow task.
    """

    def decorator(
        func: Callable[..., list[tuple[str, str]]],
    ) -> Callable[[Callable[FParams, FReturn]], Task[FParams, FReturn]]:
        # run sanity checks on func signature:
        sig = inspect.signature(func)

        # detect if ctx needed
        _ctx_required = False
        for param in sig.parameters.values():
            if param.name == "ctx":
                _ctx_required = True
                break

        if _ctx_required and len(sig.parameters) - 1 != len(s3folder_inputs):
            raise AttributeError(
                "The number of parameters didnt match the number of s3 inputs."
            )

        if not _ctx_required and len(sig.parameters) != len(s3folder_inputs):
            raise AttributeError(
                "The number of parameters didnt match the number of s3 inputs."
            )

        # TODO (Guillaume): we will have to adapt the task here to run as pod on the
        # k8s cluster.
        @task()
        @functools.wraps(func)
        def mytask(*airflow_inputss: dict[str, str]) -> dict[str, str]:
            """An airflow task auto created with the decorator.

            These tasks are meant to be chained using the Taskflow paradigm. In order to
            be chainable the args and return value are standard.

            Args:
                airflow_inputss: one or several dict coming from xcom args, containing
                    as keys the s3 folder path and values the corresponding file path to
                    take.

            Returns:
                a dict mapping s3 folder path to the file written for the next tasks to
                use.
            """
            # flatten all airflow inputs in case of multi input tasks:
            airflow_inputs: dict[str, str] = {}
            for d in airflow_inputss:
                for k, v in d.items():
                    airflow_inputs[k] = v

            # sanity check: airflow inputs must contain all s3folder_path for resolution
            s3_path_not_found = set(s3folder_inputs) - set(airflow_inputs.keys())
            if len(s3_path_not_found) > 0:
                raise AttributeError(
                    f"Unable to resolve the following path from airflow inputs: "
                    f"`{s3_path_not_found}`."
                )

            context = get_current_context()
            if "dag_run" not in context:
                raise KeyError("`dag_run` was not found in context provided by airflow")

            # build func arguments by converting s3 inputs dataset into local path.
            func_args: dict[str, Any] = {
                param.name: None
                for param in sig.parameters.values()
                if param.name != "ctx"
            }
            for key, dataset_path in zip(func_args.keys(), s3folder_inputs):
                s3_path = dataset_path + airflow_inputs[dataset_path]
                if os.getenv("FILE_STORAGE_LAYER_ENV") == "local":
                    s3_path = f"data/s3/{s3_path}"
                local_path = file_storage_instance.get_file(s3_path)
                func_args[key] = local_path

            # run the wrapped function.
            if _ctx_required:
                func_args["ctx"] = context

            func_outputs: list[tuple[str, str]] = func(**func_args)

            # build airflow outputs and upload to s3 for chaining tasks.
            airflow_outputs = {}
            for idx, (filename, content) in enumerate(func_outputs):
                run_id = context["dag_run"].run_id
                airflow_outputs[s3folder_outputs[idx]] = f"{run_id}/{filename}"
                s3_path = s3folder_outputs[idx] + airflow_outputs[s3folder_outputs[idx]]
                if os.getenv("FILE_STORAGE_LAYER_ENV") == "local":
                    s3_path = f"data/s3/{s3_path}"
                file_storage_instance.upload_file(content, s3_path)

            return airflow_outputs

        return mytask

    return decorator
