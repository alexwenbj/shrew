from copy import deepcopy

_shrew_actions__ = []
RAINBOW = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

class animation():
    def __init__(self, duration=1):
        self.duration = duration

    def __enter__(self):
        _shrew_actions__.append((None, 'animation', [self.duration]))

    def __exit__(self, *args):
        _shrew_actions__.append((None, 'animation-end', [self.duration]))


class AbstractShape:
    _shape_count__ = 0
    _shape_type__ = None
    _default_arguments__ = {
        'x': 0,
        'y': 0,
        'color': 'black',
        'width': 100,
        'height': 100,
        'transparency': 0,
        'rotation': 0,
    }
    # which properties should be passed to svg.js constructor
    _svg_constructor_arguments = []

    def __init__(self, copy_from=None, **kwargs):
        self.__dict__['_properties__'] = {}  # avoid calling __setattr__

        unknow_kwargs = set(kwargs.keys()).difference(set(self._default_arguments__.keys()))
        if unknow_kwargs:
            raise TypeError("'{}' got an unexpected keyword argument '{}'"
                            .format(self.__class__.__name__, unknow_kwargs.pop()))

        # Populate properties
        for property, default in self._default_arguments__.items():
            if copy_from is not None:
                default = deepcopy(copy_from._properties__[property])
            self._properties__[property] = deepcopy(kwargs.get(property, default))

        self._log__init()

    def _log__init(self):
        """
        Logs shape creation and all its properties.
        """
        # Get a unique id for the shape
        AbstractShape._shape_count__ += 1
        self.__id = 'shape{}'.format(AbstractShape._shape_count__)

        # Gather constructor arguments and log creation
        log_args = [self._shape_type__]
        for name in self._svg_constructor_arguments:
            log_args.append(self._properties__[name])
        self._log_action__('created', log_args)

        # Log the rest of the properties
        for name, value in self._properties__.items():
            if name not in self._svg_constructor_arguments:
                self._log_action__(name, value, initial=True)

    def copy(self, **kwargs):
        return self.__class__(copy_from=self, **kwargs)

    def _log_action__(self, command, value, initial=False):
        # Corrections
        if command == 'color':
            command = 'fill'
        if command == 'transparency':
            command = 'opacity'
            value = 1 - value / 100
        if command == 'rotation':
            command = 'rotate'
        if command == 'points':
            command = 'plot'

        _shrew_actions__.append((self.__id, command, value, initial))

    def flip_horizontal(self):
        self._log_action__("flip", "y")

    def flip_vertical(self):
        self._log_action__("flip", "x")

    def __getattr__(self, name):
        try:
            return self._properties__[name]
        except KeyError:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))

    def __setattr__(self, name, value):
        if name in self._properties__:
            value = deepcopy(value)
            self._properties__[name] = value
            self._log_action__(name, value)
        else:
            self.__dict__[name] = value


class AbstractShapePoints(AbstractShape):
    _default_arguments__ = deepcopy(AbstractShape._default_arguments__)
    _default_arguments__.update({
        'points': [0, 0, 100, 100],
        'width': None,
        'height': None,
        'x': None,
        'y': None,
    })


class Rectangle(AbstractShape):
    _shape_type__ = 'rect'
    _svg_constructor_arguments = ['width', 'height']


Square = Rectangle


class Ellipse(AbstractShape):
    _shape_type__ = 'ellipse'
    _svg_constructor_arguments = ['width', 'height']


Circle = Ellipse


class Line(AbstractShapePoints):
    _shape_type__ = 'line'
    _svg_constructor_arguments = ['points']

    def _log_action__(self, action, value, initial=False):
        if action == 'color':
            action = 'stroke'
        AbstractShape._log_action__(self, action, value, initial)


class Polygon(AbstractShapePoints):
    _shape_type__ = 'polygon'
    _svg_constructor_arguments = ['points']


class Path(AbstractShapePoints):
    _shape_type__ = 'path'
    _svg_constructor_arguments = ['path']
    _default_arguments__ = deepcopy(AbstractShape._default_arguments__)
    _default_arguments__.update({
        'path': "M504 256c0 136.997-111.043 248-248 248S8 392.997 8 256C8 119.083 119.043 8 256 8s248 111.083 248 248zM262.655 90c-54.497 0-89.255 22.957-116.549 63.758-3.536 5.286-2.353 12.415 2.715 16.258l34.699 26.31c5.205 3.947 12.621 3.008 16.665-2.122 17.864-22.658 30.113-35.797 57.303-35.797 20.429 0 45.698 13.148 45.698 32.958 0 14.976-12.363 22.667-32.534 33.976C247.128 238.528 216 254.941 216 296v4c0 6.627 5.373 12 12 12h56c6.627 0 12-5.373 12-12v-1.333c0-28.462 83.186-29.647 83.186-106.667 0-58.002-60.165-102-116.531-102zM256 338c-25.365 0-46 20.635-46 46 0 25.364 20.635 46 46 46s46-20.636 46-46c0-25.365-20.635-46-46-46z",
    })


class Text(AbstractShape):
    _shape_type__ = 'text'
    _svg_constructor_arguments = ['text']

    _default_arguments__ = deepcopy(AbstractShape._default_arguments__)
    _default_arguments__.update({
        'text': "Example text",
    })
