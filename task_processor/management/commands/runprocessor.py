import logging
from argparse import ArgumentParser

from django.core.management import BaseCommand
from gunicorn.config import Config

from task_processor.threads import TaskRunner, TaskRunnerCoordinator
from task_processor.types import TaskProcessorConfig
from task_processor.utils import run_server

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._threads: list[TaskRunner] = []
        self._monitor_threads = True

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "--numthreads",
            type=int,
            help="Number of worker threads to run.",
            default=5,
        )
        parser.add_argument(
            "--sleepintervalms",
            type=int,
            help="Number of millis each worker waits before checking for new tasks",
            default=2000,
        )
        parser.add_argument(
            "--graceperiodms",
            type=int,
            help="Number of millis before running task is considered 'stuck'.",
            default=20000,
        )
        parser.add_argument(
            "--queuepopsize",
            type=int,
            help="Number of tasks each worker will pop from the queue on each cycle.",
            default=10,
        )
        parser.add_subparsers(dest="gunicorn").add_parser(
            "gunicorn arguments",
            add_help=False,
            aliases=["gunicorn"],
            parents=[Config().parser()],
        )

    def handle(self, *args, **options):
        config = TaskProcessorConfig(
            num_threads=options["numthreads"],
            sleep_interval_ms=options["sleepintervalms"],
            grace_period_ms=options["graceperiodms"],
            queue_pop_size=options["queuepopsize"],
        )

        logger.debug("Config: %s", config)

        coordinator = TaskRunnerCoordinator(config=config)
        coordinator.start()

        try:
            run_server(options=options)
        finally:
            coordinator.stop()
