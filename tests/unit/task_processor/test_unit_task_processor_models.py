from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from task_processor.decorators import register_task_handler
from task_processor.models import RecurringTask, Task
from task_processor.task_registry import initialise

now = timezone.now()
one_hour_ago = now - timedelta(hours=1)
one_hour_from_now = now + timedelta(hours=1)


def test_task_run():
    # Given
    @register_task_handler()
    def my_callable(arg_one: str, arg_two: str = None):
        """Example callable to use for tasks (needs to be global for registering to work)"""
        return arg_one, arg_two

    args = ["foo"]
    kwargs = {"arg_two": "bar"}

    initialise()

    task = Task.create(
        my_callable.task_identifier,
        scheduled_for=timezone.now(),
        args=args,
        kwargs=kwargs,
    )

    # When
    result = task.run()

    # Then
    assert result == my_callable(*args, **kwargs)


@pytest.mark.parametrize(
    "input, expected_output",
    (
        ({"value": Decimal("10")}, '{"value": 10}'),
        ({"value": Decimal("10.12345")}, '{"value": 10.12345}'),
    ),
)
def test_serialize_data_handles_decimal_objects(input, expected_output):
    assert Task.serialize_data(input) == expected_output


@pytest.mark.parametrize(
    "first_run_time, expected",
    ((one_hour_ago.time(), True), (one_hour_from_now.time(), False)),
)
def test_recurring_task_run_should_execute_first_run_at(first_run_time, expected):
    assert (
        RecurringTask(
            first_run_time=first_run_time, run_every=timedelta(days=1)
        ).should_execute
        == expected
    )
