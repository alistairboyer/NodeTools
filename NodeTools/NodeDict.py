from . import BLPropertiesUtils
from . import SocketUtils
from . import Options
import bpy
from mathutils import Vector
from typing import Dict, Iterable, Optional, Set, Union


def _log(*args, **kwargs):
    """
    Alias of ```print()```
    """
    print(*args, **kwargs)


def get_context(object):
    """
    Returns the context of a blender object using its ``id_data`` attribute.
    """
    if not hasattr(object, "id_data"):
        return None
    object_path = object.id_data.__repr__()
    return object_path[: object_path.find("[")]


class Base:
    def __new__(cls, data, *args, **kwargs):
        """
        Supply a `dict` to create a blender object,
        or a blender object to output a properties string.

        Args:
            data (`dict` or `bpy.data.bpy_struct`):
                a `dict` is passed to the class ``to_object()`` method or
                a `bpy.data.bpy_struct` object is passed to the class
                ``output()`` method.
            args : passed to the approprate method.
            kwargs : passed to the approprate method.

        Returns:
            passing in a `dict` will return the appropriate object; and
            passing in a `bpy.data.bpy_struct` will return `None` with output
            by the ``print()`` function.

        Raises:
            ValueError : if ``data`` is a `dict` or `bpy.data.bpy_struct`.

        """
        # Convert dicts to objects
        if type(data) == dict:
            return cls.to_object(data, *args, **kwargs)
        # Convert objects to dicts
        elif BLPropertiesUtils._bl_object_check(data):
            return cls.output(data, *args, **kwargs)
        raise ValueError(
            "Supply a dict to create an object, or a blender object to output a properties string."
        )


class NodeTree(Base):
    """
    Interface to convert a ``bpy.data.NodeTree`` object to and from a `dict`.

    Examples:

        See the examples in the "examples" folder.
    """

    _autonode_map = dict()
    _autoparent_node = None
    _autoparent_socket = None
    _autoparent_link = None

    def __new__(cls, data, *args, **kwargs):
        cls._autonode_map = dict()
        return super().__new__(cls, data, *args, **kwargs)

    @classmethod
    def to_object(cls, d, overwrite=False, **kwargs):
        """
        Create a ``bpy.types.NodeTree`` from a `dict`.

        Required values in the `dict`:

        - "name" : the node tree name
        - "TYPE" : the node tree type
        - "CONTEXT" : the context of the node tree. If None is supplied
          then the node tree will be created in ``bpy.data.node_groups``.

        This will be set as the parent for Nodes, Sockets and Links created
        after by autoparenting.

        Args:
            d (dict) : a `dict` containing data to create a socket object.
            overwrite (bool)
              If `False` then if the node tree already exists, this will
              be returned. If `True` then a new tree will be created.
              [Default `False`]

        Return:
            ``bpy.types.NodeTree``

        """
        # types
        name: str
        treetype: str
        context: Union[str, bpy.types.bpy_struct]
        object: Union[bpy.types.NodeTree, bpy.types.bpy_struct]
        nodetree: bpy.types.NodeTree
        tree_parent: bpy.types.bpy_struct
        socket_info: Iterable[dict]
        socket_data: dict
        node_info: Iterable[dict]
        node_data: dict
        link_info: Iterable[dict]
        link_data: dict
        #
        name = d.pop("name")
        treetype = d.pop("TYPE")
        context = d.pop("CONTEXT", None)
        if context is not None:
            if type(context) == str:
                context = eval("bpy.data.{}".format(context.replace("bpy.data.", "")))
        if context is None or context == bpy.data.node_groups:
            object = bpy.data.node_groups.get(name, None)
            if object is None:
                object = bpy.data.node_groups.new(name, treetype)
            elif not overwrite:
                return object
            tree_parent = object
        else:
            tree_parent = context.get(name, None)
            if tree_parent is None:
                tree_parent = context.new(name)
            elif not overwrite:
                return tree_parent
            tree_parent.use_nodes = True
            object = tree_parent.node_tree
        object.nodes.clear()
        cls._autoparent(object)
        BLPropertiesUtils.update(object, d)
        for socket_data in kwargs.pop("socket_info", []):
            Socket(socket_data, parent=object)
        for node_data, node_socket_data in kwargs.pop("node_info", []):
            Node(node_data, parent=object, socket_data=node_socket_data)
        for link_data in kwargs.pop("socket_info", []):
            Link(socket_data, parent=object)
        return tree_parent

    @staticmethod
    def to_dict(nodetree, **kwargs):
        """
        Convert node tree properties to a `dict`.

        An object with a ``node_tree`` can be passed and that node tree will be converted.

        Properties are gathered using ``BLPropertiesUtils.to_dict()``.

        Custom/reserved values in the `dict`:

        - "name" : The name of the ``object`` from its "name" attribute.
        - "TYPE" : The type of the ``object`` from its "bl_idname" attribute.
        - "CONTEXT" : The ``object`` context, the node tree's parent context
          (`e.g.` bpy.data.Materials for a shader node tree)
          or ``bpy.data.node_groups``.

        Args:
            nodetree (``bpy.types.NodeLink``) : object to be converted to `dict`.
            node_map (dict) : passed to ``to_dict()`` method.
            socket_map (dict) : passed to ``to_dict()`` method.
            kwargs (dict) : included for compatibility but not used.

        Return:
            `dict` with property names as keys and values as values.

        """
        # types
        nodetree: Union[bpy.types.NodeTree, bpy.types.bpy_struct]
        d: dict
        defaults: dict
        skip_properties: set
        #
        d = dict()
        defaults = Options.NODE_TREE_DEFAULT_PROPERTIES
        skip_properties = set(Options.NODE_TREE_SKIP_PROPERTIES)
        # These properties are handled individually below
        skip_properties.add("name")
        d["name"] = nodetree.name
        if hasattr(nodetree, "node_tree"):
            nodetree = nodetree.node_tree
        # The supplied object does not use a node_tree
        if object is None:
            return
        d["TYPE"] = nodetree.bl_idname
        d["CONTEXT"] = get_context(nodetree)
        d.update(
            BLPropertiesUtils.to_dict(
                nodetree, defaults=defaults, skip_properties=skip_properties
            )
        )
        return d

    @staticmethod
    def output(node_tree, **print_kwargs):
        """
        Print the `dict` generated by ``NodeTree.to_dict()`` using ``print()``.
        Prints information from group sockets using the using the ``Socket.output()`` function.
        Prints the information for nodes using the ``Node.output()`` function.
        Prints the information for links using the ``Link.output()`` function.

        Links are skipped if they are hidden and
        ``Options.SKIP_HIDDEN_LINKS`` is `True`.

        Sockets of the node tree are evaluated in the order of
        `inputs` followed by `outputs` and a ``socket_index`` is incremented
        for every socket that is encountered. This ``socket_index`` is used with the
        ``Socket.nodetree_socket_to_dict()`` function.

        Nodes are sorted in the order given by the ``Node.key()`` functon.
        Then nodes are evaluated in this order and a ``node_index`` is incremented
        for every node that is encountered. This ``node_index`` is used with the
        ``Node.output()`` function.

        Args:
            node_tree : passed to ``NodeTree.to_dict()``.
            print_kwargs : passed to ``print()``.
        """
        # types
        nodetree: Union[bpy.types.NodeTree, bpy.types.bpy_struct]
        socket_index: int
        socket_map: dict
        node_index: int
        node_map: dict
        socket: Union[bpy.types.NodeSocket, bpy.type.NodeSocketInterface]
        node: bpy.types.Node
        link: bpy.types.NodeLink
        #
        socket_index = -1
        socket_map = dict()
        node_index = -1
        node_map = dict()
        # NodeTree
        print("NodeTree({})".format(NodeTree.to_dict(node_tree)), **print_kwargs)
        # Sockets
        if hasattr(node_tree, "node_tree"):
            node_tree = node_tree.node_tree
        for socket_context in [node_tree.inputs, node_tree.outputs]:
            for socket in socket_context:
                socket_index = socket_index + 1
                Socket.output(
                    socket,
                    socket_index=socket_index,
                    socket_map=socket_map,
                    **print_kwargs
                )
                # d = Socket.nodetree_socket_to_dict(
                #    socket, socket_index=socket_index, socket_map=socket_map
                # )
                # print("Socket({})".format(d), **print_kwargs)
        node_list = list(node_tree.nodes)
        node_list.sort(key=Node.key)
        for node in node_list:
            node_index = node_index + 1
            Node.output(node, node_index=node_index, node_map=node_map, **print_kwargs)
        for link in node_tree.links:
            if Options.SKIP_HIDDEN_LINKS and link.is_hidden:
                continue
            Link.output(link, node_map=node_map, socket_map=socket_map)

    @classmethod
    def _autoparent(cls, object):
        cls.autoparent_set(object, object, object, dict())

    @classmethod
    def autoparent_set(
        cls, node_parent=None, socket_parent=None, link_parent=None, node_map=dict()
    ):
        """
        Set the automatic values for parenting new objects.

        These can be stored and resinstated by the following sequence::

          autoparent_values = NodeTree.autoparent_get()
          NodeTree.autoparent_set(*autoparent_values)
        """
        cls._autoparent_node = node_parent
        cls._autoparent_socket = socket_parent
        cls._autoparent_link = link_parent
        cls._autonode_map = node_map

    @classmethod
    def autoparent_reset(cls):
        """
        Reset the automatic values for parenting new objects.
        """
        cls.autoparent_set()

    @classmethod
    def autoparent_get(cls):
        """
        Get the automatic values for parenting new objects.
        """
        return (
            cls._autoparent_node,
            cls._autoparent_socket,
            cls._autoparent_link,
            cls._autonode_map,
        )


class Socket(Base):
    """
    Interface to convert a ``bpy.data.NodeSocket`` or
    ``bpy.data.NodeSocketInterface`` object to and from a `dict`.

    Examples:

        This reads the value of the roughness socket within the default material's Principled BSDF node.

        >>> from NodeTools.NodeTools import Socket
        >>> example_nodetree = bpy.data.materials['Material'].node_tree
        >>> Socket(example_nodetree.nodes['Principled BSDF'].inputs['Roughness'])
        Socket({'name': 'Roughness', 'identifier': 'Roughness', 'is_output': False, 'TYPE': 'NodeSocketFloatFactor', 'default_value': 0.5})

        This sets the value of the roughness socket within the default material's Principled BSDF node to 0.2.

        >>> from NodeTools.NodeTools import Socket
        >>> example_nodetree = bpy.data.materials['Material'].node_tree
        >>> Socket({'name': 'Roughness', 'identifier': 'Roughness', 'is_output': False, 'TYPE': 'NodeSocketFloatFactor', 'default_value': 0.2}, parent=example_nodetree.nodes['Principled BSDF'])

    """

    @classmethod
    def to_object(cls, d, parent=None):
        """
        Create a ``bpy.types.NodeSocket`` or ``bpy.types.NodeSocketInterface``
        from a `dict`.

        Required values in the `dict`:

        - "name" : The name of the `socket`.
        - "identifier" : The identifier of the `socket`.
        - "is_output" : The direction of the `socket`.
        - "TYPE" :  The type of the `socket`.

        Args:
            d (dict) : a `dict` containing data to create a socket object.
            parent (``bpy.types.Node`` or ``bpy.Types.NodeTree`` or `None`)
              the node or node tree that is the parent of the socket object.
              If `None` is provided then the parent will be sought from
              the autoparenting feature in the ``NodeTree`` class.

        Return:
            ``bpy.types.NodeSocket`` when the parent is a node, otherwise
            ``bpy.types.NodeSocketInterface``.

        """
        # types
        d: dict
        parent: Union[bpy.types.NodeTree, bpy.types.Node]
        is_output: bool
        socket_context: bpy.types.bpy_prop_collection
        socket: Union[bpy.types.NodeSocket, bpy.types.NodeSocketInterface, None]
        key: str
        #
        if parent is None:
            parent = NodeTree._autoparent_socket
        if parent is None:
            raise ValueError("No parent for socket")
        is_output = d.pop("is_output")
        socket_context = parent.outputs if is_output else parent.inputs
        socket = SocketUtils.find(d, socket_context)
        # Sockets in node groups need creating because they are custom
        # but Node sockets are created when a node is created
        if socket is None and issubclass(type(parent), bpy.types.NodeTree):
            socket = socket_context.new(d.pop("TYPE"), d.pop("name"))
        for key in {"name", "TYPE", "identifier", "is_output"}:
            d.pop(key, None)
        BLPropertiesUtils.update(socket, d)
        return socket

    @staticmethod
    def to_dict(socket, **kwargs):
        """
        Convert ``bpy.types.NodeSocket`` properties to a `dict` using
        ``node_socket_to_dict()`` or ``bpy.types.NodeSocketInterface``
        attributes to a `dict` using ``nodetree_socket_to_dict()``.

        Attribtutes are gathered using ``BLPropertiesUtils.to_dict()``.

        Custom/reserved values in the `dict`:

        - "name" : The name of the ``object`` from its "name" attribute.
        - "identifier" : The identifier of the ``object`` from its "identifier" attribute.
        - "is_output" : The direction of the ``object`` from its "is_output" attribute.
        - "TYPE" :  The type of the ``object`` captured
          from its "bl_idname"  or "bl_socket_idname" attribute.

        Args:
            object (``bpy.types.NodeSocket`` or
              ``bpy.types.NodeSocketInterface``) : object to be converted to `dict`.
            kwargs (dict) : passed to relevant ``to_dict()``  function.

        Return:
            `dict` with attribute names as keys and values as values.

        Raises:
            ValueError: if the supplied object is not
              a ``bpy.types.NodeSocket`` or ``bpy.types.NodeSocketInterface``.

        """
        # types
        socket: Union[bpy.types.NodeSocket, bpy.types.NodeSocketInterface]
        #
        if issubclass(type(socket), bpy.types.NodeSocket):
            return Socket.node_socket_to_dict(socket, **kwargs)
        # Check for correct object types (already done NodeScoket above)
        if issubclass(type(socket), bpy.types.NodeSocketInterface):
            return Socket.nodetree_socket_to_dict(socket, **kwargs)
        raise ValueError(
            "An object of type bpy.types.NodeSocket or bpy.types.NodeSocketInterface must be supplied"
        )

    @staticmethod
    def nodetree_socket_to_dict(socket, socket_index=None, socket_map=None, **kwargs):
        """
        See ``Socket.to_dict()``.

        Convert ``bpy.types.NodeSocketInterface``
        attributes to a `dict`.

        Attributes are gathered using ``BLPropertiesUtils.to_dict()``.

        Any attributes with a value matching the one in
        ``Options.NODE_GROUP_SOCKET_DEFAULT_PROPERTIES`` will be skipped.

        Any attributes named in
        ``Options.NODE_GROUP_SOCKET_SKIP_PROPERTIES``` will be skipped.

        Socket names of group sockets have naming irregularities when altered
        in blender. For example, a group input with 4 inputs and one output
        that has a new input added will give a socket with name "Input_5".
        This name will persist even if other inputs are subsequently
        deleted. However, these names are not overriden when sockets are created.
        This function attemts to correct this by remapping sockets in the
        order that they are received.

        If the attribute value is a float or a float vector and the
        "max_value" or "min_value" are the defaults
        this is deleted from the `dict`.
        """
        # types
        socket: bpy.types.NodeSocketInterface
        socket_index: Optional[int]
        socket_map: Optional[dict]
        d: dict
        defaults: dict
        skip_properties: set
        socket_identifier: str
        # Check for correct object types
        if not issubclass(type(socket), bpy.types.NodeSocketInterface):
            raise ValueError(
                "An object of type bpy.types.NodeSocketInterface must be supplied"
            )
        #
        d = dict()
        defaults = Options.NODE_GROUP_SOCKET_DEFAULT_PROPERTIES
        skip_properties = set(Options.NODE_GROUP_SOCKET_SKIP_PROPERTIES)
        # These properties are handled individually below
        skip_properties.add("name")
        skip_properties.add("identifier")
        skip_properties.add("is_output")
        d["name"] = socket.name
        d["identifier"] = socket.identifier
        d["is_output"] = socket.is_output
        d["TYPE"] = socket.bl_socket_idname
        if socket_index is not None:
            socket_identifier = "{}_{}".format(
                "Output" if d["is_output"] else "Input", socket_index
            )
            if not d["identifier"] == socket_identifier:
                socket_map[d["identifier"]] = socket_identifier
                d["identifier"] = socket_identifier
        d.update(
            BLPropertiesUtils.to_dict(
                socket, defaults=defaults, skip_properties=skip_properties
            )
        )
        # Tidy up some default min/max values for floats / vectorfloats
        if d["TYPE"] in {"NodeSocketFloat", "NodeSocketVector"}:
            if d["max_value"] == 3.4028234663852886e38:
                del d["max_value"]
            if d["min_value"] == -3.4028234663852886e38:
                del d["min_value"]
        return d

    @staticmethod
    def node_socket_to_dict(socket, **kwargs):
        """
        See ``Socket.to_dict()``.

        Convert ``bpy.types.NodeSocket``
        attributes to a `dict`.

        Attributes are gathered using ``BLPropertiesUtils.to_dict()``.

        Any attributes with a value matching the one in
        ``Options.NODE_SOCKET_DEFAULT_PROPERTIES`` will be skipped.

        Any attributes named in
        ``Options.NODE_SOCKET_SKIP_PROPERTIES``` will be skipped.
        """
        # types
        socket: bpy.types.NodeSocket
        d: dict
        defaults: dict
        skip_properties: set
        # Check for correct object types
        if not issubclass(type(socket), bpy.types.NodeSocket):
            raise ValueError("An object of type bpy.types.NodeSocket must be supplied")
        #
        d = dict()
        defaults = Options.NODE_SOCKET_DEFAULT_PROPERTIES
        skip_properties = Options.NODE_SOCKET_SKIP_PROPERTIES
        # These properties are handled individually below
        skip_properties.add("name")
        skip_properties.add("identifier")
        skip_properties.add("is_output")
        d["name"] = socket.name
        d["identifier"] = socket.identifier
        d["is_output"] = socket.is_output
        d["TYPE"] = socket.bl_idname
        d.update(
            BLPropertiesUtils.to_dict(
                socket, defaults=defaults, skip_properties=skip_properties
            )
        )
        # Ouput values are generated
        if socket.is_output:
            d.pop("default_value", None)
        return d

    @classmethod
    def output(cls, socket, socket_index=None, socket_map=None, **print_kwargs):
        """
        Print the `dict` generated by ``Socket.to_dict()`` using ``print()``.

        Args:
            socket : passed to ``Socket.to_dict()``.
            socket_index : passed to ``Socket.to_dict()``.
            socket_map : passed to ``Socket.to_dict()``.
            print_kwargs : passed to ``print()``.
        """
        # types
        socket: Union[bpy.types.NodeSocket, bpy.types.NodeSocketInterface]
        socket_index: Optional[int]
        socket_map: Optional[dict]
        d: dict
        #
        d = Socket.to_dict(socket, socket_index=None, socket_map=None)
        print("{}({})".format(cls.__name__, d), **print_kwargs)


class Node(Base):
    """
    Interface to convert a ``bpy.data.Node`` object to and from a `dict`.

    Examples:

        Generates a text representation of "Material Output" node within the default material.

        >>> from NodeTools.NodeTools import Node
        >>> example_nodetree = bpy.data.materials['Material'].node_tree
        >>> Node(example_nodetree.nodes['Material Output'])
        Node({'name': 'Material Output', 'TYPE': 'ShaderNodeOutputMaterial', 'location': (300, 300), 'is_active_output': True, 'target': 'ALL'})
        Socket({'name': 'Volume', 'identifier': 'Volume', 'is_output': False, 'TYPE': 'NodeSocketShader'})
        Socket({'name': 'Displacement', 'identifier': 'Displacement', 'is_output': False, 'TYPE': 'NodeSocketVector', 'hide_value': True, 'default_value': (0.0, 0.0, 0.0)})

        This example creates a new "Material Output" node within the default material
        but with a 'CYCLES' target.

        >>> from NodeTools.NodeTools import Node
        >>> example_nodetree = bpy.data.materials['Material'].node_tree
        >>> Node({'name': 'Material Output', 'TYPE': 'ShaderNodeOutputMaterial', 'location': (300, 100), 'is_active_output': False, 'target': 'CYCLES'}, parent=example_nodetree)

    """

    @classmethod
    def to_object(cls, d, parent=None, socket_data=list()):
        """
        Create a ``bpy.types.Node`` from a `dict`.

        Required values in the `dict`:

        - "TYPE" : the node type
        - "INDEX" : the node index. This will be transferred to the
          ``node_map`` for reference when creating other objects.

        This will be set as the parent for Sockets created
        after by autoparenting in ``NodeTree``.

        Args:
            d (dict) : a `dict` containing data to create a socket object.
            parent (``bpy.Types.NodeTree`` or `None`)
              the node tree that is the parent of the link.
              If `None` is provided then the ``parent``
              will be sought from
              the autoparenting feature in the ``NodeTree`` class.
            socket_data (`iterable` of `dict` or `None`)
              iterable data containing socket data
              that will be passed to ``Socket.to_object()``.

        Return:
            ``bpy.types.Node``

        Raises:
            ValueError : if a parent is not supplied and can not be inferred.

        """
        # types
        parent: Union[None, bpy.data.NodeTree]
        node: bpy.types.Node
        parent_index: Union[int, str, None]
        index: Union[int, str, None]
        socket_dict: dict
        socket_data: Iterable
        #
        if parent is None:
            parent = NodeTree._autoparent_node
        if parent is None:
            raise ValueError("No parent for node")
        node = parent.nodes.new(d.pop("TYPE"))
        cls._autoparent(node)
        parent_index = d.pop("parent", None)
        if parent_index is not None:
            node.parent = parent.nodes[NodeTree._autonode_map[parent_index]]
        index = d.pop("INDEX", None)
        BLPropertiesUtils.update(node, d)
        if index is not None:
            NodeTree._autonode_map[index] = node.name
        for socket_dict in socket_data:
            Socket(socket_dict, parent=node)
        return node

    @staticmethod
    def to_dict(node, node_index=None, node_map=None, **kwargs) -> dict:
        """
        Convert ``bpy.types.Node`` properties to a `dict`.

        Properties are gathered using ``BLPropertiesUtils.to_dict()``.

        Custom/reserved values in the `dict`:

        - "name" : The name of the ``object`` from its "name" attribute.
        - "TYPE" : The type of the ``object`` from its "bl_idname" attribute.
        - "location" : The location of the ``object`` from its "location"
          attribute rounded to the nearest integer.
        - "parent" :  The parent (`i.e.` frame) of the ``object`` caputred
          from the "parent" attribute corrected using the ``node_map``.

        Any attributes with a value matching the one in
        ``Options.NODE_DEFAULT_PROPERTIES`` will be skipped.

        Any attributes named in
        ``Options.NODE_SKIP_PROPERTIES``` will be skipped.

        Args:
            node (``bpy.types.NodeLink``) : object to be converted to `dict`.
            node_map (dict) : passed to ``to_dict()`` method.
            socket_map (dict) : passed to ``to_dict()`` method.
            kwargs (dict) : included for compatibility but not used.

        Return:
            `dict` with property names as keys and values as values.

        """
        # types
        node: bpy.types.Node
        node_index: Union[int, str, None]
        node_map: dict
        d: dict
        defaults: dict
        skip_properties: set
        parent: Union[str, int, None]
        # Check for correct object types
        if not issubclass(type(node), bpy.types.Node):
            raise ValueError("An object of type bpy.types.Node must be supplied")
        #
        d = dict()
        defaults = Options.NODE_DEFAULT_PROPERTIES
        skip_properties = set(Options.NODE_SKIP_PROPERTIES)
        # These properties are handled individually below
        skip_properties.add("name")
        skip_properties.add("parent")
        skip_properties.add("bl_idname")
        skip_properties.add("location")
        if node_index is not None:
            d["INDEX"] = int(node_index)
        # We already get this but want it to be first!
        d["name"] = node.name
        if node_map is not None:
            node_map[d["name"]] = d["INDEX"]
        d["TYPE"] = node.bl_idname
        if node.parent is not None:
            parent = node_map[node.parent.name]
        # Round the location to nice values
        d["location"] = tuple(round(x) for x in node.location)
        d.update(
            BLPropertiesUtils.to_dict(
                node, defaults=defaults, skip_properties=skip_properties
            )
        )
        # A parents is the  frame that the node is in
        if node.parent is not None:
            d["parent"] = parent
        return d

    @staticmethod
    def output(node, node_index=None, node_map=None, **print_kwargs):
        """
        Print the `dict` generated by ``Node.to_dict()`` using ``print()``.

        Prints the information for all node sockets using the
        ``Socket.output()`` function, except:

        - If ``Options.NODE_SOCKET_SKIP_DISABLED`` is `True`
          then sockets where the attribute ``enabled`` is `False`
          will be skipped.

        - If a socket type (``bl_idname``) is included in
          ``Options.NODE_SOCKET_SKIP_TYPES`` then this socket will be skipped.

        - If ``Options.NODE_SOCKET_SKIP_OUTPUTS`` is `True`
          and the socket is an output this it will be skipped.

        - If ``Options.NODE_SOCKET_SKIP_LINKED_OUTPUTS`` is `True`
          then input sockets where the attribute ``is_linked`` is `True`
          will be skipped.

        Args:
            object : passed to ``Node.to_dict()``.
            node_index : passed to ``Node.to_dict()``.
            node_map : passed to ``Node.to_dict()``.
            print_kwargs : passed to ``print()``.
        """
        # types
        node: bpy.types.Node
        node_index: Union[int, None]
        node_map: Union[dict, None]
        socket_context: bpy.types.bpy_prop_array
        socket: bpy.types.NodeSocket
        #
        d = Node.to_dict(node, node_index=node_index, node_map=node_map)
        print("Node({})".format(d), **print_kwargs)
        # Object Sockets
        for socket_context in [node.inputs, node.outputs]:
            for socket in socket_context:
                if Options.NODE_SOCKET_SKIP_DISABLED and not socket.enabled:
                    continue
                # Skip sockets in the NODE_SOCKET_SKIP_TYPES list
                if type(socket) in Options.NODE_SOCKET_SKIP_TYPES:
                    continue
                # Skip output properties - these are generated
                if Options.NODE_SOCKET_SKIP_OUTPUTS and socket.is_output:
                    continue
                # Skip input properties if the socket is_linked
                if (
                    Options.NODE_SOCKET_SKIP_LINKED_OUTPUTS
                    and not socket.is_output
                    and socket.is_linked
                ):
                    continue
                Socket.output(socket, **print_kwargs)

    @staticmethod
    def _autoparent(object):
        NodeTree._autoparent_socket = object

    @staticmethod
    def key(node) -> tuple:
        """
        Get a tuple of values: node type priority (``bl_idname``)
        as defined in ``Options.NODE_PRIORITIES``,
        followed by horizontal (``location.x``)
        and vertical (``location.y``)
        location that can be used to sort nodes.
        """
        # types
        node: bpy.types.Node
        location: Vector
        node_priority: int
        #
        location = node.location
        if hasattr(node, "bl_idname"):
            node_priority = Options.NODE_PRIORITIES.get(node.bl_idname, 1000)
        if node.parent is not None:
            location = location + node.parent.location
        return (node_priority, location.x, -location.y)


class Link(Base):
    """
    Interface to convert a ``bpy.data.NodeLink`` to and from a `dict`.

    Examples:

        Generates a text representation of the first link in the default material node tree.

        >>> from NodeTools.NodeTools import Link
        >>> example_nodetree = bpy.data.materials['Material']
        >>> Link(example_nodetree.node_tree.links[0])
        Link({'FROM': {'INDEX': 'Principled BSDF', 'name': 'BSDF', 'TYPE': 'NodeSocketShader'}, 'TO': {'INDEX': 'Material Output', 'name': 'Surface', 'identifier': 'Surface'}})

        Creates a link between the "Group Input" and the "Group Output" nodes.
        The ``links.clear()`` deletes all links with in a node group.
        Please note that there is fails under default startup
        because there are no Geometry Nodes. A default geometry node tree
        called "Geometry Nodes"
        should be created for this examle.

        >>> from NodeTools.NodeTools import Link
        >>> example_nodetree = bpy.data.node_groups["Geometry Nodes"]
        >>> example_nodetree.links.clear()
        >>> Link({"FROM":{"INDEX":"Group Input", "TYPE":"NodeSocketGeometry", "name":"Geometry", "identifier":"Input_0"}, "TO":{"INDEX":"Group Output", "identifier":"Output_1"}}, parent=example_nodetree)
    """

    @classmethod
    def to_object(cls, d, parent=None, node_map=dict()):
        """
        Create a ``bpy.types.NodeLink`` from a `dict`.

        Required values in the `dict`:

            For each end of the link "FROM" and "TO", information
            is supplied as a `dict`:

            - "INDEX" : the node index
            - "name : socket name
            - "identifier" : socket identifier
            - "type" : socket type

            This information is unpacked by ``Link.dict_unpack()``.

        Args:
            d (dict) : a `dict` containing data to create a socket object.
            parent (``bpy.Types.NodeTree`` or `None`)
              the node tree that is the parent of the link.
              If `None` is provided then the ``parent`` and the
              ``node_map``
              will be sought from
              the autoparenting feature in the ``NodeTree`` class.
            node_map (`dict`) : `dict` map of nodes for index mapping.

        Return:
            ``bpy.types.NodeLink``

        Raises:
            ValueError : if a parent is not supplied and can not be inferred.

        """
        # types
        parent: Union[None, bpy.data.NodeTree]
        node_map: dict
        from_data: dict
        from_object_index: int
        from_node: bpy.types.Node
        from_socket: bpy.types.NodeSocket
        to_data: dict
        to_object_index: int
        to_node: bpy.types.Node
        to_socket: bpy.types.NodeSocket
        #
        if parent is None:
            parent = NodeTree._autoparent_link
            node_map = NodeTree._autonode_map
        if parent is None:
            raise ValueError("No parent for socket")
        Link.dict_unpack(d)
        #
        from_data = d.pop("FROM")
        from_object_index = from_data.pop("INDEX")
        from_node = parent.nodes[node_map.get(from_object_index, from_object_index)]
        from_socket = SocketUtils.find(from_data, from_node.outputs)
        if from_socket is None:
            _log("From socket is not found", from_data)
            return
        #
        to_data = d.pop("TO")
        to_object_index = to_data.pop("INDEX")
        to_node = parent.nodes[node_map.get(to_object_index, to_object_index)]
        to_socket = SocketUtils.find(to_data, to_node.inputs)
        if to_socket is None:
            _log("To socket is not found", to_data)
            return
        # Create link
        link = parent.links.new(from_socket, to_socket)
        # update link properties
        BLPropertiesUtils.update(link, d)
        return link

    @staticmethod
    def to_dict(link, node_map=None, socket_map=None, **kwargs) -> dict:
        """
        Convert ``bpy.types.NodeLink`` attribtutes to a `dict`.

        Attributes are gathered using ``BLPropertiesUtils.to_dict()``.

        Custom/reserved values in the `dict`:

            For each end of the link "FROM" and "TO", information
            is captured as a `dict`:

            - "INDEX" : the node index
            - "name : socket name
            - "identifier" : socket identifier
            - "type" : socket type (``bl_idname``)

            This information is packed by ``Link.dict_pack()``.

        Any attributes with a value matching the one in
        ``Options.NODE_LINK_DEFAULT_PROPERTIES`` will be skipped.

        Any attributes named in
        ``Options.NODE_LINK_SKIP_PROPERTIES``` will be skipped.

        Args:
            link (``bpy.types.NodeLink``) : object to be converted to `dict`.
            node_map (dict) : ##
            socket_map (dict) : ##

        Return:
            `dict` with attribute names as keys and values as values.

        """
        # types
        link: bpy.types.NodeLink
        node_map: Optional[dict]
        socket_map: Optional[dict]
        d: Dict[str, str]
        defaults: dict
        skip_properties: Set[str]
        # Check for correct object types
        if not issubclass(type(link), bpy.types.NodeLink):
            raise ValueError("An object of type bpy.types.NodeLink must be supplied")
        #
        d = dict()
        defaults = Options.NODE_LINK_DEFAULT_PROPERTIES
        skip_properties = Options.NODE_LINK_SKIP_PROPERTIES
        d["FROM"] = {
            "INDEX": link.from_node.name,
            "name": link.from_socket.name,
            "identifier": link.from_socket.identifier,
            "TYPE": link.from_socket.bl_idname,
        }
        d["TO"] = {
            "INDEX": link.to_node.name,
            "name": link.to_socket.name,
            "identifier": link.to_socket.identifier,
            "TYPE": link.to_socket.bl_idname,
        }
        if socket_map is not None:
            if link.from_node.bl_idname == "NodeGroupInput":
                d["FROM"]["identifier"] = socket_map.get(
                    d["FROM"]["identifier"], d["FROM"]["identifier"]
                )
            if link.to_node.bl_idname == "NodeGroupOutput":
                d["TO"]["identifier"] = socket_map.get(
                    d["TO"]["identifier"], d["TO"]["identifier"]
                )
        if node_map is not None:
            d["FROM"]["INDEX"] = node_map[d["FROM"]["INDEX"]]
            d["TO"]["INDEX"] = node_map[d["TO"]["INDEX"]]
        Link.dict_pack(d)
        d.update(
            BLPropertiesUtils.to_dict(
                link, defaults=defaults, skip_properties=skip_properties
            )
        )
        return d

    @staticmethod
    def output(link, node_map=None, socket_map=None, **print_kwargs):
        """
        Print the `dict` generated by ``Link.to_dict()`` using ``print()``.

        Args:
            link (``bpy.types.NodeLink``) : object to be converted to
              output, passed to ``Link.to_dict()`` method.
            node_map (dict) : passed to ``Link.to_dict()`` method.
            socket_map (dict) : passed to ``Link.to_dict()`` method.
            print_kwargs (dict) : `kwargs` passed to ``print()`` method.
        """
        # types
        link: bpy.types.NodeLink
        node_map: Optional[dict]
        socket_map: Optional[dict]
        #
        d = Link.to_dict(link, node_map=node_map, socket_map=socket_map)
        print("Link({})".format(d), **print_kwargs)

    # There is a lot of duplication in link information so we can pack / unpack it
    # To make ouput more readable
    @staticmethod
    def dict_pack(d):
        """
        Pack data in a link information `dict` to remove duplication.

        Information in the `TO` socket that matches information in the `FROM`
        socket is deleted.
        If the `FROM` socket identifier matches the
        `FROM` socket name this is also deleted.

        Operates on the `dict` directly does not return any value.

        The reverse of this function is ``dict_unpack()``.

        Args:
            d (dict) : the `dict` to pack.
        """
        # types
        d: dict
        # Delete data from the TO socket if it matches the FROM socket.
        for key in d["FROM"]:
            if d["FROM"][key] == d["TO"][key]:
                del d["TO"][key]
        # Delete data duplicated between name and identifier properties
        if d["FROM"]["identifier"] == d["FROM"]["name"]:
            del d["FROM"]["identifier"]

    @staticmethod
    def dict_unpack(d):
        """
        Perform the reverse operation of ``dict_pack()``.

        Operates on the `dict` directly does not return any value.

        Args:
            d (dict) : the `dict` to unpack.

        """
        # types
        d: dict
        # Restore duplicate data between name and identifier properties
        try:
            d["FROM"]["identifier"]
        except KeyError:
            d["FROM"]["identifier"] = d["FROM"]["name"]
        # Restore duplicate data between FROM and TO sockets
        for key in d["FROM"]:
            try:
                d["TO"][key]
            except KeyError:
                d["TO"][key] = d["FROM"][key]
