"""

Options for the ``NodeTools.NodeDict`` module.

``SKIP_HIDDEN_LINKS`` : see ``NodeTree.output()``.

``NODE_SOCKET_SKIP_DISABLED`` : see ``Node.output()``.

``NODE_SOCKET_SKIP_TYPES`` : see ``Node.output()``.

``NODE_SOCKET_SKIP_OUTPUTS`` : see ``Node.output()``.

``NODE_SOCKET_SKIP_LINKED_OUTPUTS`` : see ``Node.output()``.

``NODE_PRIORITIES`` : see ``Node.key()``.

``NODE_TREE_DEFAULT_PROPERTIES`` : see ``NodeTree.to_dict()``.

``NODE_TREE_SKIP_PROPERTIES`` : see ``NodeTree.to_dict()``.

``NODE_LINK_DEFAULT_PROPERTIES`` : see ``Link.to_dict()``.

``NODE_LINK_SKIP_PROPERTIES`` : see ``Link.to_dict()``.

``NODE_DEFAULT_PROPERTIES`` : see ``Node.to_dict()``.

``NODE_SKIP_PROPERTIES`` : see ``Node.to_dict()``.

``NODE_SOCKET_DEFAULT_PROPERTIES`` : see ``Socket.to_dict()``.

``NODE_SOCKET_SKIP_PROPERTIES`` : see ``Socket.to_dict()``.

``NODE_GROUP_SOCKET_DEFAULT_PROPERTIES`` : see ``Socket.to_dict()``.

``NODE_GROUP_SOCKET_SKIP_PROPERTIES`` : see ``Socket.to_dict()``.

"""

import bpy


SKIP_HIDDEN_LINKS = True
# These types of socket are skipped
NODE_SOCKET_SKIP_OUTPUTS = True
NODE_SOCKET_SKIP_LINKED_OUTPUTS = True
NODE_SOCKET_SKIP_DISABLED = True


# Default priority is 0
# Higher has higher priority
NODE_PRIORITIES = {"NodeFrame": 1, "GroupInput": 10, "GroupOutput": -1}

# These are skipped when loaded from a blender object
# if the value is set to the value in this dict
NODE_TREE_DEFAULT_PROPERTIES = {
    "use_fake_user": True,
    "use_extra_user": False,
    "tag": False,
    "grease_pencil": None,
    "active_input": -1,
    "active_output": -1,
}

# These are skipped when loaded from a blender object
NODE_TREE_SKIP_PROPERTIES = set()

# These are skipped when loaded from a blender object
# if the value is set to the value in this dict
NODE_LINK_DEFAULT_PROPERTIES = {"is_valid": True, "is_muted": False}

# These are skipped when loaded from a blender object
NODE_LINK_SKIP_PROPERTIES = set()

# These are skipped when loaded from a blender object
# if the value is set to the value in this dict
NODE_DEFAULT_PROPERTIES = {
    "height": 100.0,
    "width": 140.0,
    "width_hidden": 42.0,
    "label": "",
    "use_custom_color": False,
    "select": False,
    "show_options": True,
    "show_preview": False,
    "hide": False,
    "mute": False,
    "show_texture": False,
    "color": (0.608, 0.608, 0.608),
    "is_active_output": False,
}

# These are skipped when loaded from a blender object
NODE_SKIP_PROPERTIES = {"select"}

# These are skipped when loaded from a blender object
# if the value is set to the value in this dict
NODE_SOCKET_DEFAULT_PROPERTIES = {
    "description": "",
    "hide": False,
    "enabled": True,
    "link_limit": 1,
    "show_expanded": False,
    "hide_value": False,
    "active_input": -1,
    "active_output": -1,
    "default_attribute_name": "",
}
# These are skipped when loaded from a blender object
# if the value is set to the value in this dict

NODE_SOCKET_SKIP_PROPERTIES = {"display_shape", "link_limit", "type"}

# These types of socket are skipped
NODE_SOCKET_SKIP_TYPES = {bpy.types.NodeSocketVirtual}

# These are skipped when loaded from a blender object
# if the value is set to the value in this dict
NODE_GROUP_SOCKET_DEFAULT_PROPERTIES = NODE_SOCKET_DEFAULT_PROPERTIES

# These are skipped when loaded from a blender object
NODE_GROUP_SOCKET_SKIP_PROPERTIES = NODE_SOCKET_SKIP_PROPERTIES
