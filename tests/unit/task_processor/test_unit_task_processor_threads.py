import logging
import typing
from typing import Type

import pytest
from django.db import DatabaseError
from pytest_mock import MockerFixture

from task_processor.threads import TaskRunner

if typing.TYPE_CHECKING:
    # This import breaks private-package-test workflow in core
    from tests.unit.task_processor.conftest import GetTaskProcessorCaplog


@pytest.mark.parametrize(
    "exception_class, exception_message",
    [(DatabaseError, "Database error"), (Exception, "Generic error")],
)
def test_task_runner_is_resilient_to_errors(
    db: None,
    mocker: MockerFixture,
    get_task_processor_caplog: "GetTaskProcessorCaplog",
    exception_class: Type[Exception],
    exception_message: str,
) -> None:
    # Given
    caplog = get_task_processor_caplog(logging.DEBUG)

    task_runner = TaskRunner()
    mocker.patch(
        "task_processor.threads.run_tasks",
        side_effect=exception_class(exception_message),
    )

    # When
    task_runner.run_iteration()

    # Then
    assert len(caplog.records) == 1

    assert caplog.records[0].levelno == logging.ERROR
    assert (
        caplog.records[0].message
        == f"Received error retrieving tasks: {exception_message}."
    )
