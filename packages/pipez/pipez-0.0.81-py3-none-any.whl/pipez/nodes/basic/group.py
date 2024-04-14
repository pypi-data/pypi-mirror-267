from typing import Optional
from pipez.core import Node, Registry, Batch


@Registry.add
class Group(Node):
    def __init__(
            self,
            class_name: str,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._class_name = class_name

    def processing(self, input: Optional[Batch]) -> Optional[Batch]:
        idxs = iter(input.meta.pop('idxs'))
        output = Batch(data=[{} for _ in range(input.meta['batch_size'])], meta=input.meta)

        for obj in input:
            idx = next(idxs)
            output[idx].setdefault(self._class_name, []).append(obj['output'])

        return output
