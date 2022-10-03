"""
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
"""

from ..NodeTools import NodeTree, Socket, Node, Link

# fmt: off
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
# fmt: on

print("Node group {} created with {} nodes.".format(nt.name, len(nt.nodes)))
