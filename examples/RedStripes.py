"""
This is an example of using the NodeTools package.

This creates a Material called "RedStripes" and its node tree.
The color of a diffuse BSDF is supplied by a mix node that is set to
red (0.8, 0.0, 0.0, 0.0) as the first input and white (0.8, 0.8, 0.8, 1.0)
as the second input. The value of the mix shader is supplied by a map range node
that is stepped in one step to give either 0.0 or 1.0 as an output.
This node is driven by a Wave Texture that has an input
from the generated texture coordinate.
"""

from ..NodeTools import NodeTree, Socket, Node, Link

# fmt: off
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
# fmt: on

print(
    "Material {} created with node tree with {} nodes.".format(
        m.name, len(m.node_tree.nodes)
    )
)
