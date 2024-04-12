from ...dimensions.core import Dimensions as DimensionsTPL


class Mould2PsHalfDimensions(DimensionsTPL):
    names = ['diameter', 'inner_diameter', 'height']

    def __init__(self, tyre, dimensions: dict = None):
        super().__init__(dimensions)
        self._tyre = tyre
