examples
========

AlignGeometryToVector
---------------------

  This is an example of using the NodeTools package.

  This creates a Node Group called "AlignGeometryToVector".
  The node group rotates geometry by an amount that aligns the supplied
  vector to the Z axis (0,0,1). The target vector can be modified by
  changing the default values in the second inputs of dot and cross product nodes.

  The cross product of two vectors gives their perpendicular vector.
  The dot product between two vectors gives the cosine of the angle between them.
  Using these two relationships can give a rotation in axis/angle
  format that is applied to the Geometry using a Geometry Transform node.

  N.B. This calculation can also be performed using the Align Euler to Vector
  node with "Z" axis selected.

  import the example using the following::

    import NodeTools.examples.AlignGeometryToVector


  The source of the example is here::

    from NodeTools.NodeTools import NodeTree, Node, Socket, Link
    nt = NodeTree({'name': 'AlignGeometryToVector', 'TYPE': 'GeometryNodeTree', 'CONTEXT': 'bpy.data.node_groups', 'use_fake_user': False})
    Socket({'name': 'Geometry', 'identifier': 'Input_0', 'is_output': False, 'TYPE': 'NodeSocketGeometry', 'attribute_domain': 'POINT'})
    Socket({'name': 'Vector', 'identifier': 'Input_1', 'is_output': False, 'TYPE': 'NodeSocketVector', 'attribute_domain': 'POINT', 'default_value': (0.0, 0.0, 0.0)})
    Socket({'name': 'Translation', 'identifier': 'Input_2', 'is_output': False, 'TYPE': 'NodeSocketVector', 'attribute_domain': 'POINT', 'default_value': (0.0, 0.0, 0.0)})
    Socket({'name': 'Scale', 'identifier': 'Input_3', 'is_output': False, 'TYPE': 'NodeSocketVector', 'attribute_domain': 'POINT', 'default_value': (1.0, 1.0, 1.0)})
    Socket({'name': 'Geometry', 'identifier': 'Output_4', 'is_output': True, 'TYPE': 'NodeSocketGeometry', 'attribute_domain': 'POINT'})
    Node({'INDEX': 0, 'name': 'Group Input', 'TYPE': 'NodeGroupInput', 'location': (260, 20)})
    Node({'INDEX': 1, 'name': 'Vector Math', 'TYPE': 'ShaderNodeVectorMath', 'location': (500, 0), 'operation': 'NORMALIZE'})
    Node({'INDEX': 2, 'name': 'Vector Math.001', 'TYPE': 'ShaderNodeVectorMath', 'location': (750, 0), 'operation': 'CROSS_PRODUCT'})
    Socket({'name': 'Vector', 'identifier': 'Vector', 'is_output': False, 'TYPE': 'NodeSocketVector', 'default_value': (0.0, 0.0, 1.0)})
    Node({'INDEX': 3, 'name': 'Vector Math.002', 'TYPE': 'ShaderNodeVectorMath', 'location': (750, -200), 'operation': 'DOT_PRODUCT'})
    Socket({'name': 'Vector', 'identifier': 'Vector', 'is_output': False, 'TYPE': 'NodeSocketVector', 'default_value': (0.0, 0.0, 1.0)})
    Node({'INDEX': 4, 'name': 'Math', 'TYPE': 'ShaderNodeMath', 'location': (1000, 0), 'operation': 'ARCCOSINE', 'use_clamp': False})
    Node({'INDEX': 5, 'name': 'Rotate Euler', 'TYPE': 'FunctionNodeRotateEuler', 'location': (1250, 0), 'type': 'AXIS_ANGLE', 'space': 'OBJECT'})
    Socket({'name': 'Rotation', 'identifier': 'Rotation', 'is_output': False, 'TYPE': 'NodeSocketVectorEuler', 'hide_value': True, 'default_value': (0.0, 0.0, 0.0)})
    Node({'INDEX': 6, 'name': 'Transform', 'TYPE': 'GeometryNodeTransform', 'location': (1500, 0)})
    Node({'INDEX': 7, 'name': 'Group Output', 'TYPE': 'NodeGroupOutput', 'location': (1750, 0), 'is_active_output': True})
    Link({'FROM': {'INDEX': 0, 'name': 'Geometry', 'identifier': 'Input_0', 'TYPE': 'NodeSocketGeometry'}, 'TO': {'INDEX': 6, 'identifier': 'Geometry'}})
    Link({'FROM': {'INDEX': 0, 'name': 'Translation', 'identifier': 'Input_2', 'TYPE': 'NodeSocketVector'}, 'TO': {'INDEX': 6, 'identifier': 'Translation', 'TYPE': 'NodeSocketVectorTranslation'}})
    Link({'FROM': {'INDEX': 0, 'name': 'Scale', 'identifier': 'Input_3', 'TYPE': 'NodeSocketVector'}, 'TO': {'INDEX': 6, 'identifier': 'Scale', 'TYPE': 'NodeSocketVectorXYZ'}})
    Link({'FROM': {'INDEX': 0, 'name': 'Vector', 'identifier': 'Input_1', 'TYPE': 'NodeSocketVector'}, 'TO': {'INDEX': 1, 'identifier': 'Vector'}})
    Link({'FROM': {'INDEX': 1, 'name': 'Vector', 'TYPE': 'NodeSocketVector'}, 'TO': {'INDEX': 2, 'identifier': 'Vector_001'}})
    Link({'FROM': {'INDEX': 1, 'name': 'Vector', 'TYPE': 'NodeSocketVector'}, 'TO': {'INDEX': 3, 'identifier': 'Vector_001'}})
    Link({'FROM': {'INDEX': 3, 'name': 'Value', 'TYPE': 'NodeSocketFloat'}, 'TO': {'INDEX': 4}})
    Link({'FROM': {'INDEX': 2, 'name': 'Vector', 'TYPE': 'NodeSocketVector'}, 'TO': {'INDEX': 5, 'name': 'Axis', 'identifier': 'Axis', 'TYPE': 'NodeSocketVectorXYZ'}})
    Link({'FROM': {'INDEX': 4, 'name': 'Value', 'TYPE': 'NodeSocketFloat'}, 'TO': {'INDEX': 5, 'name': 'Angle', 'identifier': 'Angle', 'TYPE': 'NodeSocketFloatAngle'}})
    Link({'FROM': {'INDEX': 6, 'name': 'Geometry', 'TYPE': 'NodeSocketGeometry'}, 'TO': {'INDEX': 7, 'identifier': 'Output_4'}})
    Link({'FROM': {'INDEX': 5, 'name': 'Rotation', 'TYPE': 'NodeSocketVector'}, 'TO': {'INDEX': 6, 'TYPE': 'NodeSocketVectorEuler'}})

  Convert the node group back to text output::

    from NodeTools.NodeTools import NodeTree, Node, Socket, Link
    NodeTree(bpy.data.node_groups['AlignGeometryToVector'])


RedStripes
----------

  This is an example of using the NodeTools package.

  This creates a Material called "RedStripes" and its node tree.
  The color of a diffuse BSDF is supplied by a mix node that is set to
  red (0.8, 0.0, 0.0, 0.0) as the first input and white (0.8, 0.8, 0.8, 1.0)
  as the second input. The value of the mix shader is supplied by a map range node
  that is stepped in one step to give either 0.0 or 1.0 as an output.
  This node is driven by a Wave Texture that has an input
  from the generated texture coordinate.

  import the example using the following::

    import NodeTools.examples.RedStripes

  The source of the example is here::

    from NodeTools.NodeTools import NodeTree, Node, Socket, Link
    m = NodeTree({'name': 'RedStripes', 'TYPE': 'ShaderNodeTree', 'CONTEXT': 'bpy.data.materials', 'use_fake_user': False, 'use_extra_user': True})
    Node({'INDEX': 0, 'name': 'Texture Coordinate', 'TYPE': 'ShaderNodeTexCoord', 'location': (-600, 300), 'object': None, 'from_instancer': True})
    Node({'INDEX': 1, 'name': 'Wave Texture.001', 'TYPE': 'ShaderNodeTexWave', 'location': (-380, 300), 'width': 150.0, 'show_texture': True, 'wave_type': 'BANDS', 'bands_direction': 'Z', 'rings_direction': 'X', 'wave_profile': 'TRI'})
    Socket({'name': 'Scale', 'identifier': 'Scale', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 1.0})
    Socket({'name': 'Distortion', 'identifier': 'Distortion', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 1.0})
    Socket({'name': 'Detail', 'identifier': 'Detail', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 0.0})
    Socket({'name': 'Detail Scale', 'identifier': 'Detail Scale', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 4.0})
    Socket({'name': 'Detail Roughness', 'identifier': 'Detail Roughness', 'is_output': False, 'TYPE': 'NodeSocketFloatFactor', 'default_value': 1.0})
    Socket({'name': 'Phase Offset', 'identifier': 'Phase Offset', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 0.0})
    Node({'INDEX': 2, 'name': 'Map Range', 'TYPE': 'ShaderNodeMapRange', 'location': (-140, 300), 'clamp': False, 'interpolation_type': 'STEPPED', 'data_type': 'FLOAT'})
    Socket({'name': 'From Min', 'identifier': 'From Min', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 0.0})
    Socket({'name': 'From Max', 'identifier': 'From Max', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 1.0})
    Socket({'name': 'To Min', 'identifier': 'To Min', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 0.0})
    Socket({'name': 'To Max', 'identifier': 'To Max', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 1.0})
    Socket({'name': 'Steps', 'identifier': 'Steps', 'is_output': False, 'TYPE': 'NodeSocketFloat', 'default_value': 1.0})
    Node({'INDEX': 3, 'name': 'Mix', 'TYPE': 'ShaderNodeMixRGB', 'location': (80, 300), 'blend_type': 'MIX', 'use_alpha': False, 'use_clamp': False})
    Socket({'name': 'Color1', 'identifier': 'Color1', 'is_output': False, 'TYPE': 'NodeSocketColor', 'default_value': (0.8, 0.0, 0.0, 1.0)})
    Socket({'name': 'Color2', 'identifier': 'Color2', 'is_output': False, 'TYPE': 'NodeSocketColor', 'default_value': (0.8, 0.8, 0.8, 1.0)})
    Node({'INDEX': 4, 'name': 'Diffuse BSDF', 'TYPE': 'ShaderNodeBsdfDiffuse', 'location': (300, 300), 'width': 150.0})
    Socket({'name': 'Roughness', 'identifier': 'Roughness', 'is_output': False, 'TYPE': 'NodeSocketFloatFactor', 'default_value': 0.0})
    Socket({'name': 'Normal', 'identifier': 'Normal', 'is_output': False, 'TYPE': 'NodeSocketVector', 'hide_value': True, 'default_value': (0.0, 0.0, 0.0)})
    Node({'INDEX': 5, 'name': 'Material Output', 'TYPE': 'ShaderNodeOutputMaterial', 'location': (520, 300), 'is_active_output': True, 'target': 'ALL'})
    Socket({'name': 'Volume', 'identifier': 'Volume', 'is_output': False, 'TYPE': 'NodeSocketShader'})
    Socket({'name': 'Displacement', 'identifier': 'Displacement', 'is_output': False, 'TYPE': 'NodeSocketVector', 'hide_value': True, 'default_value': (0.0, 0.0, 0.0)})
    Link({'FROM': {'INDEX': 2, 'name': 'Result', 'TYPE': 'NodeSocketFloat'}, 'TO': {'INDEX': 3, 'name': 'Fac', 'identifier': 'Fac', 'TYPE': 'NodeSocketFloatFactor'}})
    Link({'FROM': {'INDEX': 1, 'name': 'Fac', 'TYPE': 'NodeSocketFloat'}, 'TO': {'INDEX': 2, 'name': 'Value', 'identifier': 'Value'}})
    Link({'FROM': {'INDEX': 0, 'name': 'Generated', 'TYPE': 'NodeSocketVector'}, 'TO': {'INDEX': 1, 'name': 'Vector', 'identifier': 'Vector'}})
    Link({'FROM': {'INDEX': 4, 'name': 'BSDF', 'TYPE': 'NodeSocketShader'}, 'TO': {'INDEX': 5, 'name': 'Surface', 'identifier': 'Surface'}})
    Link({'FROM': {'INDEX': 3, 'name': 'Color', 'TYPE': 'NodeSocketColor'}, 'TO': {'INDEX': 4}})

  Convert the node group back to text output::

    from NodeTools.NodeTools import NodeTree, Node, Socket, Link
    NodeTree(bpy.data.materials['RedStripes'])

  or::

    from NodeTools.NodeTools import NodeTree, Node, Socket, Link
    NodeTree(bpy.data.materials['RedStripes'].node_tree)
