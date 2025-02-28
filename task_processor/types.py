from dataclasses import dataclass


@dataclass
class TaskProcessorConfig:
    num_threads: int
    sleep_interval_ms: int
    grace_period_ms: int
    queue_pop_size: int
