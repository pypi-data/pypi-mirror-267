from ...dimensions.core import Dimensions as DimensionsTPL


class RingDimensions(DimensionsTPL):
    names = ['diameter', 'inner_diameter', 'height']

    def __init__(self, dimensions: dict = None):
        super().__init__(dimensions)

    @property
    def diameter(self):
        return self['diameter']

    @diameter.setter
    def diameter(self, dim: float | int = None):
        self['diameter'] = dim

    @property
    def inner_diameter(self):
        return self['inner_diameter']

    @inner_diameter.setter
    def inner_diameter(self, dim: float | int = None):
        self['inner_diameter'] = dim

    @property
    def height(self):
        return self['height']

    @height.setter
    def height(self, dim: float | int = None):
        self['height'] = dim
