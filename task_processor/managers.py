import typing

from django.db.models import Manager, QuerySet

if typing.TYPE_CHECKING:
    from task_processor.models import RecurringTask, Task


class TaskManager(Manager):
    def get_tasks_to_process(self, num_tasks: int) -> QuerySet["Task"]:
        return self.raw("SELECT * FROM get_tasks_to_process(%s)", [num_tasks])


class RecurringTaskManager(Manager):
    def get_tasks_to_process(self, num_tasks: int) -> QuerySet["RecurringTask"]:
        return self.raw("SELECT * FROM get_recurringtasks_to_process(%s)", [num_tasks])
