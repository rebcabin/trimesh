import numpy as np
import trimesh
import pprint

data_home_directory = '../../Ops-robotics-rsimcon/content/raw/mesh' \
                      '/64907_Fanuc_430_Robot/'

the_model = 'armature_rigging_groups-binary-7.4-z-forward-y-up.fbx'

meshes = trimesh.load_meshes(data_home_directory + the_model)

for i in range(len(meshes)):
    mesh = meshes[i]

    # if there are multiple bodies in the mesh we can split the mesh by
    # connected components of face adjacency. If this example mesh
    # is a single watertight body we get a list of one mesh
    # mesh.split()

    pp = pprint.PrettyPrinter(indent = 2)

    pp.pprint({'mesh_number':  i+1
           ,'asset_dir': data_home_directory
           ,'file_name': the_model
           ,"n_vertices": len(mesh.vertices)
           ,"area": mesh.area
           ,"is_winding_consistent": mesh.is_winding_consistent
           ,"is_convex": mesh.is_convex
           ,"n_facets": len(mesh.facets)
           ,"bounding_box_extents": mesh.bounding_box_oriented.extents
           ,"extents": mesh.extents
           ,"sum_area_faces": np.sum(mesh.area_faces)
           ,"sum_area_facets": np.sum(mesh.facets_area)
           ,"watertight_q": mesh.is_watertight
           ,"euler_number": mesh.euler_number
           ,"volume_by_convex_hull_ratio": np.divide(mesh.volume,
                                                     mesh.convex_hull.volume)
           ,"center_of_mass": mesh.center_mass
           ,'centroid': mesh.centroid
           ,"geometric_moment_of_inertia": mesh.moment_inertia
           ,"number_of_facets": len(mesh.facets)
           ,'number_of_edges': len(mesh.edges)
           ,'number_of_unique_edges': len(mesh.edges_unique)
           ,'number_of_face_edges': len(mesh.edges_face)
           ,'number_of_sorted_edges': len(mesh.edges_sorted)
           ,'number_of_face_adjacency_edges': len(mesh.face_adjacency_edges)
           ,'number_of_unique_face_edges': len(mesh.faces_unique_edges)
           ,'number_of_faces': len(mesh.faces)
           ,'number_of_triangles': len(mesh.triangles)
           ,'principal_inertia_components': mesh.principal_inertia_components
           ,'principal_inertia_vectors': mesh.principal_inertia_vectors
           ,'volume': mesh.volume
            })

    for facet in mesh.facets:
        mesh.visual.face_colors[facet] = trimesh.visual.random_color()

    # mesh.export(data_home_directory +
    #             'armature_rigging_groups_submesh_%0.3d.dae' % (i+1),
    #             'collada')

    mesh.export(data_home_directory +
                'armature_rigging_groups_submesh_%0.3d.off' % (i+1),
                'off')

    mesh.show()
