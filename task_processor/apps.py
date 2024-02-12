from django.apps import AppConfig
from django.conf import settings
from health_check.plugins import plugin_dir

from task_processor.task_run_method import TaskRunMethod


class TaskProcessorAppConfig(AppConfig):
    name = "task_processor"

    def ready(self):
        # Import the tasks module to ensure that the code in the module is executed when
        # the app is loaded. This ensures that the tasks defined there are correctly
        # registered. This is a similar behaviour to how Django recommends defining signals.
        # https://docs.djangoproject.com/en/5.0/topics/signals/#connecting-receiver-functions
        from . import tasks  # noqa

        if (
            settings.ENABLE_TASK_PROCESSOR_HEALTH_CHECK
            and settings.TASK_RUN_METHOD == TaskRunMethod.TASK_PROCESSOR
        ):
            from .health import TaskProcessorHealthCheckBackend

            plugin_dir.register(TaskProcessorHealthCheckBackend)
