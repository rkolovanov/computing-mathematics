import bpy
from math import pi

for o in bpy.data.objects:
    if o.type == 'MESH' or o.type == 'EMPTY':
        o.select = True
    else:
        o.select = False

# Delete all objects in the scene
bpy.ops.object.delete()

# Add the floor
bpy.ops.mesh.primitive_cube_add(radius=5, location=(0, 0, 0))
bpy.ops.transform.resize(value=(1, 1, 0.1))
bpy.ops.rigidbody.objects_add(type='PASSIVE')
boxObj = bpy.context.active_object
boxObj.rigid_body.collision_shape = "BOX"
boxObj.name = "Ground"

# Add the Coin
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=0.1, location=(0, 0, 3))
bpy.ops.rigidbody.objects_add(type='ACTIVE')
boxObj = bpy.context.active_object
boxObj.rigid_body.collision_shape = "CYLINDER"
bpy.context.object.rigid_body.friction = 0.25
bpy.context.object.rigid_body.restitution = 0.75
boxObj.name = "Coin"
# Set reference to the coin
coin = bpy.data.objects["Coin"]

# Set a reference to the scene
sce = bpy.context.scene
# Set first frame
sce.frame_set(1)
# Set Keyframes
coin.keyframe_insert(data_path="location")
coin.keyframe_insert(data_path="rotation_euler")
bpy.context.object.rigid_body.kinematic = True
bpy.context.object.keyframe_insert('rigid_body.kinematic')

# Advance two frames and add translational and rotational motion
sce.frame_set(3)
# Translate up a little
coin.location.z = 3.45
# Rotate coin predominantly around the x-axis
coin.rotation_euler.x = 1
coin.rotation_euler.y = 0.1
coin.rotation_euler.z = 0.1
# Set Keyframes
coin.keyframe_insert(data_path="location")
coin.keyframe_insert(data_path="rotation_euler")
bpy.context.object.rigid_body.kinematic = False
bpy.context.object.keyframe_insert('rigid_body.kinematic')

# Set frame to the end
sce.frame_set(250)

# Bake rigid body simulation
override = {'scene': bpy.context.scene,
            'point_cache': bpy.context.scene.rigidbody_world.point_cache}
# bake to current frame
bpy.ops.ptcache.bake(override, bake=False)

# Get transformations
tr = coin.matrix_world.translation
eu = coin.matrix_world.to_euler()
print("          X                  Y                  Z                  RX                  RY                  RZ")
print(tr.x, tr.y, tr.z, eu.x, eu.y, eu.z)

if eu.x > pi / 2.:
    print("Coin is heads")
else:
    print("Coin is tails")