from datetime import time, timedelta

import dj_database_url
from environs import Env

from task_processor.task_run_method import TaskRunMethod

env = Env()

INSTALLED_APPS = ("task_processor",)

TASK_DELETE_RUN_EVERY = timedelta(days=1)
TASK_DELETE_RUN_TIME = time(5, 0, 0)
ENABLE_TASK_PROCESSOR_HEALTH_CHECK = True
TASK_RUN_METHOD = TaskRunMethod.TASK_PROCESSOR
ENABLE_CLEAN_UP_OLD_TASKS = True
TASK_DELETE_RETENTION_DAYS = 15
TASK_DELETE_INCLUDE_FAILED_TASKS = False
RECURRING_TASK_RUN_RETENTION_DAYS = 15
TASK_DELETE_BATCH_SIZE = 2000

DATABASES = {"default": dj_database_url.parse(env("DATABASE_URL"))}

USE_TZ = True
