# This is a python script, written for blender for batch conversion of dexterous hand collada (.dae) mesh files to .stl
# format, for use in the Mujoco simulator.

import bpy
import os

sr_description_path = '/home/user/projects/shadow_robot/base_deps/src/sr_common/sr_description'

file_names = ['forearm', 'forearm_muscle', 'forearm_muscle_disk', 'forearm_lite', 'wrist', 'palm', 'knuckle', 'lfmetacarpal', 'F1', 'F2', 'F3', 'TH1_z', 'TH2_z', 'TH3_z']

for file_name in file_names:
    source_file_name = '{0}/hand/model/{1}.dae'.format(sr_description_path, file_name)
    dest_file_name = '{0}/mujoco_models/meshes/arm_and_hand_meshes/{1}.stl'.format(sr_description_path, file_name)
    print('Converting {0} to {1}...'.format(source_file_name, dest_file_name))

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    bpy.ops.wm.collada_import(filepath=source_file_name) # change this line

    bpy.ops.object.select_all(action='SELECT')
    
    bpy.ops.transform.rotate(value=4.71238898038, axis=(1.0, 0, 0))

    bpy.ops.export_mesh.stl(filepath=dest_file_name)