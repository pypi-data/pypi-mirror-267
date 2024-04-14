from typing import List, Dict, Optional
from pipez.core import Node, Registry, Batch


def is_keys_available(
        data: Dict,
        keys: List[str]
):
    for key in keys:
        if not isinstance(data, dict):
            return False

        if key not in data:
            return False

        data = data[key]

    return True


@Registry.add
class Ungroup(Node):
    def __init__(
            self,
            keys: List[str],
            main_key: str,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._keys = keys
        self._main_key = main_key

    def processing(self, input: Optional[Batch]) -> Optional[Batch]:
        output = Batch(meta=input.meta)
        output.meta['idxs'] = []

        for idx, obj in enumerate(input):
            if not is_keys_available(obj, self._keys):
                continue

            for key in self._keys:
                obj = obj[key]

            for target_obj in obj:
                if isinstance(target_obj, dict):
                    output.append({self._main_key: target_obj[self._main_key]})
                else:
                    output.append({self._main_key: target_obj})

                output.meta['idxs'].append(idx)

        return output
