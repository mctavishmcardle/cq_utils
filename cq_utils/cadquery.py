import cadquery
import typing


def get_positioned_component(
    assembly: cadquery.Assembly, name: str
) -> cadquery.Compound:
    """Get a named component out of an assembly

    This can be useful if e.g. the assembly is used to position components, and
    you need to use that position later on in the CAD script

    Args:
        assembly: The assembly from which the component should be retrieved
        name: The name of the component to look for

    Returns:
        A `Component` version of the
    """
    return list(assembly.objects[name].toCompound())[0]


def location_position(location: cadquery.Location) -> typing.Tuple[float]:
    """Get the vector position of a `Location`

    This is useful for printing locations to debug, or for converting them into
    `Vector`s

    Arsg:
        location: The location to extract the position from

    Returns:
        A tuple of vector components, in XYZ order
    """
    translation = location.wrapped.Transformation().TranslationPart()

    return (translation.X(), translation.Y(), translation.Z())


def plane_from_face(face: cadquery.Face) -> cadquery.Plane:
    """Get a plane parallel to a face, with the same center

    This translates from `cadquery`'s "topological" class (the face) into its
    "geometrical" class (the plane)

    Args:
        face: The face to construct a plane from

    Returns:
        A plane equivalent to the input face
    """
    return cadquery.Plane(face.Center(), normal=face.normalAt())


def workplane_with_copy(shape: cadquery.Shape) -> cadquery.Workplane:
    """Construct a workplane with an isolated copy of a given shape on the stack

    This can be useful because certain operations (e.g. selectors) are much more
    convenient to perform on a workplane containing an object, but some operations
    (see e.g. `get_positioned_component`) can produce shapes in isolation.

    Args:
        shape: The shape to isolate

    Returns:
        A workplane containing only a copy of the input shape
    """
    return cadquery.Workplane().add(shape.copy())
