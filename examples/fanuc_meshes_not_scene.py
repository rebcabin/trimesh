#  ___         _   _          ___
# | _ \_ _ ___| |_| |_ _  _  |   \ _  _ _ __  _ __  ___ _ _
# |  _/ '_/ -_)  _|  _| || | | |) | || | '  \| '_ \/ -_) '_|
# |_| |_| \___|\__|\__|\_, | |___/ \_,_|_|_|_| .__/\___|_|
#                      |__/                  |_|
"""
A perl Data.Dumper clone for Python
Author: simon@log4think.com
2011-07-08
"""

import sys
from types import *

def DEBUG(msg, level=None):
    pass


magin_space = '    '
break_base = False
break_string = False

break_before_list_item = True
break_before_list_begin = False
break_after_list_begin = False
break_before_list_end = True
break_after_list_end = False

break_before_tuple_item = True
break_before_tuple_begin = False
break_after_tuple_begin = False
break_before_tuple_end = True
break_after_tuple_end = False

break_before_dict_key = True
break_before_dict_value = False
break_before_dict_begin = False
break_after_dict_begin = False
break_before_dict_end = True
break_after_dict_end = False

DICT_TYPES = {DictionaryType: 1}


def atomic_type(t):
    return t in (
    NoneType, StringType, IntType, LongType, FloatType, ComplexType)


def simple_value(val):
    t = type(val)

    if atomic_type(val):
        return True

    if (not DICT_TYPES.has_key(t) and t not in (ListType, TupleType) and
            not is_instance(val)):
        return True

    elif t in (ListType, TupleType) and len(val) <= 10:
        for x in val:
            if not atomic_type(type(x)):
                return False
        return True

    elif DICT_TYPES.has_key(t) and len(val) <= 5:
        for (k, v) in val.items():
            if not (atomic_type(type(k)) and atomic_type(type(v))):
                return False
        return True

    else:
        return False


def is_instance(val):
    if type(val) is InstanceType:
        return True
    # instance of extension class, but not an actual extension class
    elif (hasattr(val, '__class__') and
              hasattr(val, '__dict__') and
              not hasattr(val, '__bases__')):
        return True
    else:
        return False


def is_class(val):
    return hasattr(val, '__bases__')


def indent(level=0, nextline=True):
    if nextline:
        return "\n" + magin_space * level
    else:
        return ""


class Dumper():
    def __init__(self, max_depth=999):
        self.max_depth = max_depth
        self.seen = {}

    def reset(self):
        self.seen = {}

    def dump_default(self, obj, level=0, nextline=True):
        DEBUG('; dump_default')
        if level + 1 > self.max_depth:
            return " <%s...>" % type(obj).__class__
        else:
            result = "%s::%s <<" % (type(obj).__name__, obj.__class__)
            if hasattr(obj, '__dict__'):
                result = "%s%s__dict__ :: %s" % (
                    result,
                    indent(level + 1),
                    self.dump_dict(obj.__dict__, level + 1)
                )

            if isinstance(obj, dict):
                result = "%s%sas_dict :: %s" % (
                    result,
                    indent(level + 1),
                    self.dump_dict(obj, level + 1)
                )
            elif isinstance(obj, list):
                result = "%s%sas_list :: %s" % (
                    result,
                    indent(level + 1),
                    self.dump_list(obj, level + 1)
                )

            result = result = "%s%s>>" % (result, indent(level))

        return result

    def dump_base(self, obj, level=0, nextline=True):
        DEBUG("; dump_%s", type(obj).__name__)
        return "%s%s" % (indent(level, break_base), obj)

    dump_NoneType = dump_base
    dump_int = dump_base
    dump_long = dump_base
    dump_float = dump_base

    def dump_str(self, obj, level=0, nextline=True):
        DEBUG('; dump_str')
        return "%s'%s'" % (indent(level, break_string), obj)

    def dump_tuple(self, obj, level=0, nextline=True):
        DEBUG('; dump_tuple')
        if level + 1 > self.max_depth:
            return "%s(...)%s" % (
                indent(level, break_before_tuple_begin),
                indent(level, break_after_tuple_end)
            )
        else:
            items = ["%s%s" % (
                indent(level + 1, break_before_tuple_item),
                self.dump(x, level + 1)
            ) for x in obj
                     ]
            return "%s(%s%s%s)%s" % (
                indent(level, nextline and break_before_tuple_begin),
                indent(level + 1, break_after_tuple_begin), ' '.join(items),
                indent(level, break_before_tuple_end),
                indent(level, break_after_tuple_end)
            )

    def dump_list(self, obj, level=0, nextline=True):
        DEBUG('; dump_list')
        if level + 1 > self.max_depth:
            return "%s[...]%s" % (
                indent(level, break_before_list_begin),
                indent(level, break_after_list_end)
            )
        else:
            items = ["%s%s" % (
                indent(level + 1, break_before_list_item),
                self.dump(x, level + 1)
            ) for x in obj
                     ]
            return "%s[%s%s%s]%s" % (
                indent(level, nextline and break_before_list_begin),
                indent(level + 1, break_after_list_begin), ' '.join(items),
                indent(level, break_before_list_end),
                indent(level, break_after_list_end)
            )

    def dump_dict(self, obj, level=0, nextline=True):
        DEBUG('; dump_dict')
        if level + 1 > self.max_depth:
            return "%s{...}%s" % (
                indent(level, break_before_dict_begin),
                indent(level, break_after_dict_end)
            )
        else:
            items = ["%s%s: %s%s" % (
                indent(level + 1, break_before_dict_key),
                self.dump(k, level + 1),
                indent(level + 2, break_before_dict_value),
                self.dump(v, level + 1)
            ) for k, v in obj.items()
                     ]
            return "%s{%s%s%s}%s" % (
                indent(level, nextline and break_before_dict_begin),
                indent(level + 1, break_after_dict_begin), ' '.join(items),
                indent(level, break_before_dict_end),
                indent(level, break_after_dict_end)
            )

    def dump(self, obj, level=0, nextline=True):
        DEBUG('; dump')
        if not simple_value(obj):
            if self.seen.has_key(id(obj)):
                return "%s::%s <<...>>" % (type(obj).__name__, obj.__class__)
            else:
                self.seen[id(obj)] = 1

        name = type(obj).__name__
        dump_func = getattr(self, "dump_%s" % name, self.dump_default)
        return dump_func(obj, level, nextline)


def dump(obj, max_depth=999):
    d = Dumper(max_depth)
    return d.dump(obj)


#  __  __      _ _   _      _       __  __        _
# |  \/  |_  _| | |_(_)_ __| |___  |  \/  |___ __| |_  ___ ___
# | |\/| | || | |  _| | '_ \ / -_) | |\/| / -_|_-< ' \/ -_|_-<
# |_|  |_|\_,_|_|\__|_| .__/_\___| |_|  |_\___/__/_||_\___/__/
#                     |_|


import numpy as np
import trimesh
import pprint

# meshes = [trimesh.load_mesh('../../Ops-robotics-rsimcon/content/raw/mesh'
#                             '/64907_Fanuc_430_Robot'
#                             '/armature_rigging_just_mesh_19_after_mathematica'
#                             '.obj')]

# meshes = [trimesh.load_mesh('../../Ops-robotics-rsimcon/content/raw/mesh'
#                              '/64907_Fanuc_430_Robot'
#                              '/armature_rigging_just_mesh_19.stl')]

# meshes = [trimesh.load_mesh('../../Ops-robotics-rsimcon/content/raw/mesh'
#                             '/64907_Fanuc_430_Robot'
#                             '/armature_rigging_groups.obj')]

# meshes = [trimesh.load_mesh('../../Ops-robotics-rsimcon/content/raw/mesh'
#                             '/64907_Fanuc_430_Robot'
#                             '/one_two_three_cuboid_after_meshmixer.obj')]

# meshes = [trimesh.load_mesh('../../Ops-robotics-rsimcon/content/raw/mesh'
#                             '/64907_Fanuc_430_Robot'
# '/armature_rigging_just_mesh_19_after_repair_in_meshmixer_and_setting_units_to_meters.obj')]


data_home_directory = '../../Ops-robotics-rsimcon/content/raw/mesh' \
                      '/64907_Fanuc_430_Robot'

# not yet producing good output
def export_obj (mesh, filename):
    filepath = data_home_directory + '/' + filename
    fd = open (filepath, 'w')
    fd.write('# OBJ export from Trimesh [bbeckman, version of 15 Jul 2017')
    meshnym = str(mesh.identifier_md5)
    fd.write('o %s\n' % meshnym)
    for v in mesh.vertices:
        fd.write('v {:.7f} {:.7f} {:.7f}\n'.format(v[0], v[1], v[2]))
    # no texture coordinates
    for vn in mesh.vertex_normals:
        fd.write('vn {:.7f} {:.7f}\n'.format(vn[0], vn[1], vn[2]))
    for f in mesh.faces:
        fd.write('f {} {} {}\n'.format(f[0], f[1], f[2]))
    fd.flush()
    fd.close()
    pass

meshes = trimesh.load_meshes('../../Ops-robotics-rsimcon/content/raw/mesh'
                             '/64907_Fanuc_430_Robot/armature_rigging_groups'
                             '-binary-7.4-z-forward-y-up.fbx')

def short (collection, near = 3):
    """Friendly subsetting for notebooks. Casts its argument to a list."""
    assert (near > 0)
    lyst = list(collection)
    far = len(lyst) - near
    if (near < far):
        return lyst[:near] + ["..."] + lyst[far:]
    else:
        return lyst


for i in range(len(meshes)):
    mesh = meshes[i]

    # ??????????????????????????????????????????????????????????????????????
    # since the mesh is watertight ???????????????? , it means there is a
    # volumetric center of mass which we can set as the origin for our mesh
    mesh.vertices -= mesh.center_mass

    # if there are multiple bodies in the mesh we can split the mesh by
    # connected components of face adjacency. If this example mesh
    # is a single watertight body we get a list of one mesh
    mesh.split()

    pp = pprint.PrettyPrinter(indent = 2)
    # pp.pprint(mesh._cache.cache)
    # pp.pprint(
    #     {"n_vertices":            len(mesh.vertices)
    #     #,"vertices_short":        short(mesh.vertices)
    #     ,"n_triangles":           len(mesh.triangles)
    #     #,"triangles_short":       short(mesh.triangles)
    #     ,"area":                  mesh.area
    #     ,"n_area_faces":          len(mesh.area_faces)
    #     #,"area_faces_short":      short(mesh.area_faces)
    #     ,'is_watertight':         mesh.is_watertight
    #     ,'is_convex':             mesh.is_convex
    #     ,'is_winding_consistent': mesh.is_winding_consistent
    #     ,'n_facets':              len(mesh.facets)
    #     ,'facets_short':          short(mesh.facets)
    #     }
    # )

    def cyl_mi (r, h): # https://en.wikipedia.org/wiki/List_of_moments_of_inertia
        r2 = r * r
        x_and_y = (3.0 * r2  +  h * h)/12.0
        return [x_and_y, x_and_y, 0.5 * r2]

    def box_mi (w, h, d):
        '''https://en.wikipedia.org/wiki/List_of_moments_of_inertia'''
        w2 = w * w
        h2 = h * h
        d2 = d * d
        return [(h2 + d2) / 12.0, (w2 + d2) / 12.0, (h2 + w2) / 12.0]


    pp.pprint({'mesh_number':  i+1
           ,"n_vertices": len(mesh.vertices)
           ,"bounding_box_oriented_inertia_tensor": box_mi(
            mesh.bounding_box_oriented.extents[0], # w?
            mesh.bounding_box_oriented.extents[2], # h?
            mesh.bounding_box_oriented.extents[1]) # d?
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

    mesh.export(data_home_directory + '/' +
                'armature_rigging_groups_submesh_%0.3d.dae' % (i+1),
                'collada')

    mesh.export(data_home_directory + '/' +
                'armature_rigging_groups_submesh_%0.3d.off' % (i+1),
                'off')

    # export_obj(
    #     mesh,
    #     'armature_rigging_groups_submesh_%0.3d.obj' % (i + 1))

    # mesh.show()
    # (mesh + mesh.bounding_cylinder).show()

    # mesh.apply_transform(trimesh.transformations.random_rotation_matrix())

    # # an axis-aligned bounding box is available
    # mesh.bounding_box.primitive.extents
    #
    # # a minimum volume oriented bounding box is available
    # mesh.bounding_box_oriented.primitive.extents
    # mesh.bounding_box_oriented.primitive.transform

    # show the mesh overlayed with its oriented bounding box
    # the bounding box is a trimesh.primitives.Box object, which subclasses
    # Trimesh and lazily evaluates to fill in vertices and faces when requested
    # (press w in viewer to see triangles)
    # (mesh + mesh.bounding_box_oriented).show()

    # bounding spheres and bounding cylinders of meshes are also
    # available, and will be the minimum volume version of each
    # except in certain degenerate cases, where they will be no worse
    # than a least squares fit version of the primitive.
    # print(mesh.bounding_box_oriented.volume,
    #     mesh.bounding_cylinder.volume,
    #     mesh.bounding_sphere.volume)