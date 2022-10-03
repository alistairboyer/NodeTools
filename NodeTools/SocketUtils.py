"""
Utilities for searching sockets.

Some nodes, especially those that handle mutltiple types, have lots of sockets
many of which are hidden and the naming convention for these is confusing.
However, sockets can be uniquely identified using
three pieces of information:

`name`
   available from socket_object.name
`identifier`
   available from socket_object.identifier
`type`
   available from socket_object.bl_idname for node sockets and
   available from socket_object.bl_socket_idname for node group sockets


"""


def socket_attribs(socket_info, get_bl_socket_id_name=True):
    """
    Convert an input to a tuple of strings: `name`, `identifier`, `socket_type`.

    ``socket_info`` can be a socket itself or values in a `dict`.

    ``socket_type`` is retreived from ``bl_idname`` for node sockets.
    If ``get_bl_socket_id_name`` is `True` then ``socket_type`` is
    retreived from ``bl_socket_idname`` where appropriate.

    Args:
        socket_info : Either a socket object, or a `dict`
          containing socket information.
        get_bl_socket_id_name (bool) : Retreive the socket name
          from Group Sockets if `True`.
          [Default `True`]

    Returns:
        Tuple of strings with socket information.

    Raises:
        ValueError : If supplied socket information could not be interpreted.
    """
    if type(socket_info) == dict:
        return (
            socket_info.get("name", None),
            socket_info.get("identifier", None),
            socket_info.get("TYPE", None),
        )
    if hasattr(socket_info, "name"):
        socket_type = None
        if hasattr(socket_info, "bl_idname"):
            socket_type = socket_info.bl_idname
        if get_bl_socket_id_name and socket_type is None:
            socket_type = socket_info.bl_socket_idname
        return (socket_info.name, socket_info.identifier, socket_type)
    raise ValueError("Could not interpret socket data.")


def compare_strict(a, b, get_bl_socket_id_name=False):
    """
    Compare two sockets either as objects or dicts of socket information.

    Information is passed through the ``socket_attribs()`` function.

    Socket types match by ``startswith`` comparison so that
    `e.g.` `NodeSocketVectorTranslation` matches with `NodeSocketVector`.

    Args:
        a : Socket or socket information for comparison.
        b : Socket or socket information for comparison.
        get_bl_socket_id_name (bool) : passed to ``socket_attribs()``.
          [Default `False`]

    Returns:
        `True` when socket name, identifier and type match else `False`.
        If any comparison value is set to `None` then `False`
        will be returned.

    Raises:
        ValueError : if either of the comparison data is all `None`.
    """
    a_name, a_identifier, a_type = socket_attribs(
        a, get_bl_socket_id_name=get_bl_socket_id_name
    )
    b_name, b_identifier, b_type = socket_attribs(
        b, get_bl_socket_id_name=get_bl_socket_id_name
    )
    if not a_name == b_name:
        return False
    if a_name is None:
        return False
    if not a_identifier == b_identifier:
        return False
    if a_identifier is None:
        return False
    # Need a None check first because we are uing str.startswith()
    if a_type is not None and b_type is not None:
        if a_type.startswith(b_type):
            return True
        if b_type.startswith(a_type):
            return True
    return False


def compare(a, b, strict=False, get_bl_socket_id_name=False):
    """
    Compare two sockets either as objects or dicts of socket information.

    Information is passed through the ``socket_attribs()`` function.

    If ``strict`` is `True`, returns the result of ``compare_strict()`` instead.

    Socket types match by ``startswith`` comparison so that `e.g.`
    `NodeSocketVectorTranslation` matches with `NodeSocketVector`.

    Args:
        a : Socket or socket information for comparison.
        b : Socket or socket information for comparison.
        strict (bool) : if `True` use ``compare_strict()``.
          [Default `False`]
        get_bl_socket_id_name (bool) : passed to ``socket_attribs()``.
          [Default `False`]

    Returns:
        `True` when socket name, identifier and type
        match when both are not `None`.

    Raises:
        ValueError : if either of the comparison data is all None.
    """
    if strict:
        return compare_strict(a, b, get_bl_socket_id_name=get_bl_socket_id_name)
    #
    a_name, a_identifier, a_type = socket_attribs(
        a, get_bl_socket_id_name=get_bl_socket_id_name
    )
    b_name, b_identifier, b_type = socket_attribs(
        b, get_bl_socket_id_name=get_bl_socket_id_name
    )
    if a_name is not None and b_name is not None:
        if not a_name == b_name:
            return False
    if a_identifier is not None and b_identifier is not None:
        if not a_identifier == b_identifier:
            return False
    if a_type is not None and b_type is not None:
        if b_type.startswith(a_type) or a_type.startswith(b_type):
            return True
        return False
    if a_name is None and a_identifier is None and a_type is None:
        raise ValueError("No data supplied for comparison", a)
    if b_name is None and b_identifier is None and b_type is None:
        raise ValueError("No data supplied for comparison", b)
    return True


def find(socket_info, iterable, **kwargs):
    """
    Finds a socket from an iterable of sockets.
    Will find the first matching socket or return `None`.
    Iterates through ``iterable`` and will return the first socket that
    matches according to the ``compare()`` criteria.


    Args:
        socket_info : Socket or socket information for search.
        iterable : Iterable containing sockets or socket data to search.
        kwargs : passed to ``compare()``.

    Returns:
        A socket object or information if a match is found else `None`.

    """
    for socket in iterable:
        if compare(socket_info, socket, **kwargs):
            return socket
    return None


def find_strict(socket_info, iterable, **kwargs):
    """
    Finds a socket from an iterable of sockets.
    Will find the first matching socket or return `None`.
    Iterates through ``iterable`` and will return the first socket that
    matches according to the ``compare_strict()`` criteria.


    Args:
        socket_info : Socket or socket information for search.
        iterable : Iterable containing sockets or socket data to search.
        kwargs : passed to ``compare_strict()``.

    Returns:
        A socket object or information if a match is found else `None`.

    """
    for socket in iterable:
        if compare_strict(socket_info, socket, **kwargs):
            return socket
    return None
