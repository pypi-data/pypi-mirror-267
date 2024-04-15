import sys
from typing import Any, Tuple, Union, cast

if sys.version_info >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence

from ._files import FoamFile

try:
    import numpy as np
    from numpy.typing import NDArray
except ModuleNotFoundError:
    pass


class FoamFieldFile(FoamFile):
    """An OpenFOAM dictionary file representing a field as a mutable mapping."""

    class BoundariesDictionary(FoamFile.Dictionary):
        def __getitem__(self, keyword: str) -> "FoamFieldFile.BoundaryDictionary":
            value = super().__getitem__(keyword)
            if not isinstance(value, FoamFieldFile.BoundaryDictionary):
                assert not isinstance(value, FoamFile.Dictionary)
                raise TypeError(f"boundary {keyword} is not a dictionary")
            return value

    class BoundaryDictionary(FoamFile.Dictionary):
        """An OpenFOAM dictionary representing a boundary condition as a mutable mapping."""

        def __setitem__(
            self,
            key: str,
            value: FoamFile._SetValue,
        ) -> None:
            if key == "value":
                self._setitem(key, value, assume_field=True)
            else:
                self._setitem(key, value)

        @property
        def type(self) -> str:
            """Alias of `self["type"]`."""
            ret = self["type"]
            if not isinstance(ret, str):
                raise TypeError("type is not a string")
            return ret

        @type.setter
        def type(self, value: str) -> None:
            self["type"] = value

        @property
        def value(
            self,
        ) -> Union[
            int,
            float,
            Sequence[Union[int, float, Sequence[Union[int, float]]]],
            "NDArray[np.generic]",
        ]:
            """Alias of `self["value"]`."""
            ret = self["value"]
            if not isinstance(ret, (int, float, Sequence)):
                raise TypeError("value is not a field")
            return cast(Union[int, float, Sequence[Union[int, float]]], ret)

        @value.setter
        def value(
            self,
            value: Union[
                int,
                float,
                Sequence[Union[int, float, Sequence[Union[int, float]]]],
                "NDArray[np.generic]",
            ],
        ) -> None:
            self["value"] = value

        @value.deleter
        def value(self) -> None:
            del self["value"]

    def __getitem__(
        self, keywords: Union[str, Tuple[str, ...]]
    ) -> Union[FoamFile.Value, FoamFile.Dictionary]:
        if not isinstance(keywords, tuple):
            keywords = (keywords,)

        ret = super().__getitem__(keywords)
        if keywords[0] == "boundaryField" and isinstance(ret, FoamFile.Dictionary):
            if len(keywords) == 1:
                ret = FoamFieldFile.BoundariesDictionary(self, keywords)
            elif len(keywords) == 2:
                ret = FoamFieldFile.BoundaryDictionary(self, keywords)
        return ret

    def __setitem__(self, keywords: Union[str, Tuple[str, ...]], value: Any) -> None:
        if not isinstance(keywords, tuple):
            keywords = (keywords,)

        if keywords == ("internalField",):
            self._setitem(keywords, value, assume_field=True)
        elif keywords == ("dimensions",):
            self._setitem(keywords, value, assume_dimensions=True)
        else:
            self._setitem(keywords, value)

    @property
    def dimensions(self) -> FoamFile.DimensionSet:
        """Alias of `self["dimensions"]`."""
        ret = self["dimensions"]
        if not isinstance(ret, FoamFile.DimensionSet):
            raise TypeError("dimensions is not a DimensionSet")
        return ret

    @dimensions.setter
    def dimensions(
        self, value: Union[FoamFile.DimensionSet, Sequence[Union[int, float]]]
    ) -> None:
        self["dimensions"] = value

    @property
    def internal_field(
        self,
    ) -> Union[
        int,
        float,
        Sequence[Union[int, float, Sequence[Union[int, float]]]],
        "NDArray[np.generic]",
    ]:
        """Alias of `self["internalField"]`."""
        ret = self["internalField"]
        if not isinstance(ret, (int, float, Sequence)):
            raise TypeError("internalField is not a field")
        return cast(Union[int, float, Sequence[Union[int, float]]], ret)

    @internal_field.setter
    def internal_field(
        self,
        value: Union[
            int,
            float,
            Sequence[Union[int, float, Sequence[Union[int, float]]]],
            "NDArray[np.generic]",
        ],
    ) -> None:
        self["internalField"] = value

    @property
    def boundary_field(self) -> "FoamFieldFile.BoundariesDictionary":
        """Alias of `self["boundaryField"]`."""
        ret = self["boundaryField"]
        if not isinstance(ret, FoamFieldFile.BoundariesDictionary):
            assert not isinstance(ret, FoamFile.Dictionary)
            raise TypeError("boundaryField is not a dictionary")
        return ret
