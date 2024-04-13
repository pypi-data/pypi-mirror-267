import sys
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, NamedTuple, Optional, Union

if sys.version_info >= (3, 9):
    from collections.abc import Mapping, Sequence
else:
    from typing import Mapping, Sequence

try:
    import numpy as np
    from numpy.typing import NDArray
except ModuleNotFoundError:
    pass


class FoamDictionaryBase:
    class DimensionSet(NamedTuple):
        mass: Union[int, float] = 0
        length: Union[int, float] = 0
        time: Union[int, float] = 0
        temperature: Union[int, float] = 0
        moles: Union[int, float] = 0
        current: Union[int, float] = 0
        luminous_intensity: Union[int, float] = 0

        def __repr__(self) -> str:
            return f"{type(self).__qualname__}({', '.join(f'{n}={v}' for n, v in zip(self._fields, self) if v != 0)})"

    @dataclass
    class Dimensioned:
        value: Union[int, float, Sequence[Union[int, float]]] = 0
        dimensions: Union[
            "FoamDictionaryBase.DimensionSet", Sequence[Union[int, float]]
        ] = ()
        name: Optional[str] = None

        def __post_init__(self) -> None:
            if not isinstance(self.dimensions, FoamDictionaryBase.DimensionSet):
                self.dimensions = FoamDictionaryBase.DimensionSet(*self.dimensions)

    Value = Union[
        str,
        int,
        float,
        bool,
        Dimensioned,
        DimensionSet,
        Sequence["Value"],
        Mapping[str, "Value"],
    ]
    """
    A value that can be stored in an OpenFOAM dictionary.
    """

    _Dict = Dict[str, Union["Value", "_Dict"]]

    @abstractmethod
    def as_dict(self) -> _Dict:
        """Return a nested dict representation of the dictionary."""
        raise NotImplementedError

    _SetValue = Union[Value, "NDArray[np.generic]"]
