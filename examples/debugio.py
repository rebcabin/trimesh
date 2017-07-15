import numpy as np
import trimesh

# load a file by name or from a buffer
# mesh = trimesh.load_mesh('../models/featuretype.STL')
# mesh = trimesh.load_mesh('../models/ADIS16480.STL')
# mesh = trimesh.load.mesh('../models/unit_sphere.STL')
# mesh = trimesh.load_mesh('../models/j39binary.fbx')
mesh = trimesh.load_mesh('../../Ops-robotics-rsimcon/content/raw/mesh'
                         '/64907_Fanuc_430_Robot/armature_rigging_groups'
                         '-binary-7.4-z-forward-y-up.fbx')
# mesh = trimesh.load_mesh('../../Ops-robotics-rsimcon/content/raw/mesh
# /64907_Fanuc_430_Robot/j3-9-binary.fbx')


# is the current mesh watertight?
print ({"watertight_q": mesh.is_watertight})

# what's the euler number for the mesh?
print ({"euler_number": mesh.euler_number})

# the convex hull is another Trimesh object that is available as a property
# lets compare the volume of our mesh with the volume of its convex hull
print ({"volume_by_convex_hull_ratio": np.divide(mesh.volume,
                                                 mesh.convex_hull.volume)})

# since the mesh is watertight, it means there is a
# volumetric center of mass which we can set as the origin for our mesh
mesh.vertices -= mesh.center_mass

# what's the moment of inertia for the mesh?
print ({"geometric_moment_of_inertia": mesh.moment_inertia})

# if there are multiple bodies in the mesh we can split the mesh by
# connected components of face adjacency
# since this example mesh is a single watertight body we get a list of one mesh
mesh.split()

print ({"number_of_facets": len(mesh.facets)})

# facets are groups of coplanar adjacent faces
# set each facet to a random color
# colors are 8 bit RGBA by default (n,4) np.uint8
for facet in mesh.facets:
    mesh.visual.face_colors[facet] = trimesh.visual.random_color()

# preview mesh in an opengl window if you installed pyglet with pip
mesh.show()

# transform method can be passed a (4,4) matrix and will cleanly apply the transform
mesh.apply_transform(trimesh.transformations.random_rotation_matrix())

# an axis aligned bounding box is available
mesh.bounding_box.primitive.extents

# a minimum volume oriented bounding box is available
mesh.bounding_box_oriented.primitive.extents

mesh.bounding_box_oriented.primitive.transform

# show the mesh overlayed with its oriented bounding box
# the bounding box is a trimesh.primitives.Box object, which subclasses
# Trimesh and lazily evaluates to fill in vertices and faces when requested
# (press w in viewer to see triangles)
(mesh + mesh.bounding_box_oriented).show()

# bounding spheres and bounding cylinders of meshes are also
# available, and will be the minimum volume version of each
# except in certain degenerate cases, where they will be no worse
# than a least squares fit version of the primitive.
print(mesh.bounding_box_oriented.volume,
      mesh.bounding_cylinder.volume,
      mesh.bounding_sphere.volume)