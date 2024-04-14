from typing import List, Optional

from pipez.core.batch import Batch
from pipez.core.enums import BatchStatus
from pipez.core.node import Node
from pipez.core.queue_wrapper import QueueWrapper


class Watchdog(Node):
    def __init__(
            self,
            pipeline: List[Node],
            **kwargs
    ):
        super().__init__(name='Watchdog', **kwargs)
        self._pipeline = pipeline
        self._build_pipeline()
        self.start()

    def _build_pipeline(self):
        queues = {}

        for node in self._pipeline:
            for queue in node.input + node.output:
                if queue in queues:
                    continue

                queues[queue] = QueueWrapper(name=queue, type=node.type, maxsize=32)

        for node in self._pipeline:
            for queue in node.input:
                node.input_queue.append(queues[queue])

            for queue in node.output:
                node.output_queue.append(queues[queue])

            node.start()

    def processing(self, input: Optional[Batch]) -> Optional[Batch]:
        if all(node.is_finish for node in self._pipeline):
            for node in self._pipeline:
                node.exit()

            return Batch(status=BatchStatus.END)

        elif any(node.is_terminate for node in self._pipeline):
            for node in self._pipeline:
                node.exit()
                node.drain()

            return Batch(status=BatchStatus.END)
