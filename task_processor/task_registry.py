import enum
import logging
import typing
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class TaskType(enum.Enum):
    STANDARD = "STANDARD"
    RECURRING = "RECURRING"


@dataclass
class RegisteredTask:
    task_identifier: str
    task_function: typing.Callable
    task_type: TaskType = TaskType.STANDARD
    task_kwargs: typing.Dict[str, typing.Any] = None


registered_tasks: typing.Dict[str, RegisteredTask] = {}


def initialise() -> None:
    global registered_tasks

    from task_processor.models import RecurringTask

    for task_identifier, registered_task in registered_tasks.items():
        logger.debug("Initialising task '%s'", task_identifier)

        if registered_task.task_type == TaskType.RECURRING:
            logger.debug("Persisting recurring task '%s'", task_identifier)
            RecurringTask.objects.update_or_create(
                task_identifier=task_identifier,
                defaults=registered_task.task_kwargs,
            )


def get_task(task_identifier: str) -> RegisteredTask:
    global registered_tasks

    return registered_tasks[task_identifier]


def register_task(task_identifier: str, callable_: typing.Callable) -> None:
    global registered_tasks

    logger.debug("Registering task '%s'", task_identifier)

    registered_task = RegisteredTask(
        task_identifier=task_identifier,
        task_function=callable_,
    )
    registered_tasks[task_identifier] = registered_task

    logger.debug(
        "Registered tasks now has the following tasks registered: %s",
        list(registered_tasks.keys()),
    )


def register_recurring_task(
    task_identifier: str, callable_: typing.Callable, **task_kwargs
) -> None:
    global registered_tasks

    logger.debug("Registering recurring task '%s'", task_identifier)

    registered_task = RegisteredTask(
        task_identifier=task_identifier,
        task_function=callable_,
        task_type=TaskType.RECURRING,
        task_kwargs=task_kwargs,
    )
    registered_tasks[task_identifier] = registered_task

    logger.debug(
        "Registered tasks now has the following tasks registered: %s",
        list(registered_tasks.keys()),
    )
