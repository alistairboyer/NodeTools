NodeTools
=========

  This package is designed to make creating and saving node trees within blender
  easy in python.

  You can use this package by including it (or a link to it) in your
  blender Scripts file path under the modules subdirectory.
  You can find the file path under the blender edit menu:
  Edit --> Preferences --> File Paths menu.



  The it can be imported within the blender scripting console using the
  following command::

    from NodeTools.NodeTools import NodeTree, Node, Socket, Link


  To get a text represenation of a node tree (or node or socket or link)
  pass your object to the relevant class::

    NodeTree(bpy.objects.node_groups['My Geometry Nodes'])

  This will create a text output that includes all the settings for the
  node tree, including its nodes sockets and links.
  The output can be copied/pasted/manipulated and most
  importantly, included in python script or copied into the python blender
  console to recreate the same object.

  For more detailed examples see the included examples in the "examples" folder:

    - AlignGeometryToVector

    - RedStripes


NodeDict
--------

.. automethod:: NodeTools.NodeDict.get_context

Base
^^^^

.. autoclass:: NodeTools.NodeDict.Base
  :members:
  :undoc-members:

NodeTree
^^^^^^^^

.. autoclass:: NodeTools.NodeDict.NodeTree
   :members:
   :undoc-members:
   :show-inheritance:

Socket
^^^^^^

.. autoclass:: NodeTools.NodeDict.Socket
   :members:
   :undoc-members:
   :show-inheritance:

Node
^^^^

.. autoclass:: NodeTools.NodeDict.Node
   :members:
   :undoc-members:
   :show-inheritance:

Link
^^^^

.. autoclass:: NodeTools.NodeDict.Link
   :members:
   :undoc-members:
   :show-inheritance:

BLPropertiesUtils
-----------------

.. automodule:: NodeTools.BLPropertiesUtils
   :members:
   :undoc-members:
   :show-inheritance:

Options
-------

.. automodule:: NodeTools.Options
   :members:
   :undoc-members:
   :show-inheritance:

SocketUtils
-----------

.. automodule:: NodeTools.SocketUtils
   :members:
   :undoc-members:
   :show-inheritance:
