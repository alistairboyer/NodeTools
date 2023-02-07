"""
A selection of methods to transfer proprties to and from a blender object.

"""

import bpy
from mathutils import Vector, Color, Quaternion, Matrix, Euler
from typing import Any, Dict, Sequence, Tuple, Union


def _log(*args, **kwargs):
    """
    Alias of ``print()``.
    """
    print(*args, **kwargs)


def to_builtin(
    value, float_round=6
) -> Union[float, int, str, bool, Tuple[float], Tuple[float, Tuple[float]]]:
    """
    Convert a value to a python builtin.

    Values are converted following the following operations depending
    on their type:

    - `None`: returns `None`.

    - `int`, `str`, `bool`: returns the original value.

    - `float`: if float_round is `None` then the float is returned directly
      otherwise the float is processed using ``round(value, float_round)``.

    - `Vector`, `Color`, `Quaternion`, `bpy.types.bpy_prop_array`:
      returns a tuple of float values that are processed according
      to float as above or ``Vector.to_tuple(float_round)``.

    - `Matrix`: returns a tuple of tuple of float values `via` conversion to a
      Vector that is processed according to float as above.

    - `Euler`: returns a tuple of float values in XYZ order. The float values
      are processed according to float as above. Consideration should be
      given to reppresenting these as fractional values of pi where appropriate.

    - `Other`: other values, such as objects, are converted to a
      representation using the repr() method.

    Args:
        value (Any) : The value for conversion.
        float_round (int) : The rounding of float values [default=6].

    Returns:
        The value converted to python builtins.

    Raises:
        ValueError : if ``float_round`` is applied and is less than 0.

    """
    # Types
    value: Any
    float_round: int
    # Return builtin values directly
    if value is None:
        return None
    t = type(value)
    if t in {int, str, bool}:
        return value
    # Round floats if float_round is not None
    if t == float:
        if float_round is not None:
            if float_round < 0:
                # float() accepts negative values but
                # Vector.to_tuple() does not so
                # don't allow negative values for consistency
                raise ValueError("float_round must be >= 0")
            return round(value, int(float_round))
        return value
    # Convert Vector, Color, Quaternion, Matrix and prop_array to
    # tuples of their constituent values
    #
    # Notes:
    #   A slice of a Matrix returns a Vector
    #   This is exploited by recursion here
    #
    #   Vector has a built in conversion to_tuple() that
    #   performs float rounding
    if t == Vector:
        if float_round is not None:
            return value.to_tuple(int(float_round))
        return value.to_tuple()
    if t in {Color, Quaternion, Matrix, bpy.types.bpy_prop_array}:
        return tuple(to_builtin(x) for x in value)
    # Decompose Euler to constituent values
    if t == Euler:
        # When tuples are assigned to Euler properties an XYZ order is assumed
        # So just return the values as a tuple if the order is XYZ
        if value.order == "XYZ":
            return tuple(to_builtin(x) for x in value)
        # If the Euler wasn't XYZ then we need to swap to XYZ
        return tuple(to_builtin(x) for x in value.to_matrix().to_euler("XYZ"))
    # Get here when the type of the value can not be understood
    # Most of the this is when the value is an object
    # The object is not guaranteed to exist at time of assignment so
    # an error is logged and the object is converted to its str representation
    # with the memory address removed
    _log("# Could not convert to base type:", value)
    return repr(value)


def to_dict(
    object,
    only_editable_properties=True,
    convert_to_builtins=True,
    defaults=dict(),
    skip_properties=set(),
) -> Dict:
    """
    Convert the properties of a blender object to a `dict`.

    Args:
        object (``bpy.types.bpy_struct``) : The object for conversion.
        only_editable_properties (bool) : If True, then properties that are
          marked as ``is_readonly`` or ``is_registered`` are skipped.
          [default `True`]
        defaults (dict) : If the object's property is set to the
          value in this `dict` where the key is the property name
          then it is skipped.
          [default `dict()`]
        skip_properties (sequence) : If a property is named in this sequence
          then it is skipped.
          [default `set()`]

    Returns:
        A `dict` representation of the supplied blender object.

    Raises:
        ValueError : If the supplied object is not a blender object.

    """
    # types
    object: bpy.types.bpy_struct
    only_editable_properties: bool
    convert_to_builtins: bool
    defaults: dict
    skip_properties: Sequence
    #
    if not _bl_object_check(object):
        raise ValueError("Not a blender object with rna properties")
    properties = dict()
    for p in object.bl_rna.properties:
        if p.identifier in skip_properties:
            continue
        if only_editable_properties:
            if p.is_readonly:
                continue
            if p.is_registered:  # these properties start with bl_
                continue
        val = eval("object.{}".format(p.identifier))
        if convert_to_builtins:
            val = to_builtin(val)
        try:
            if defaults[p.identifier] == val:
                continue
        except KeyError:
            pass
        properties[p.identifier] = val
    return properties


def update(object, properties=dict()):
    """
    Update an object attributes with the values from a `dict`.

    Args:
        object (object) : The `object` to be updated.
        properties (dict) : The `dict` of properties to be applied
          to the ``object``.
          [Default `dict()`]

    Raises:
        ValueError : The value could not be set.

    """
    # Types
    object: object
    properties: dict
    #
    for property_identifier, value in properties.items():
        try:
            exec("object.{} = value".format(property_identifier))
        except ValueError:
            _log(
                "Could not update object property:",
                object.__repr__(),
                property_identifier,
                value,
            )


def _bl_object_check(object) -> bool:
    """
    Check an object is a blender object.

    Simple check to see if object is a subclass of ``bpy.types.bpy_struct``.

    Args:
        object (Any) : The object to be checked.

    Returns:
        `bool` that is `True` if the object is a blender object.

    """
    #
    object: Any
    #
    return issubclass(type(object), bpy.types.bpy_struct)
