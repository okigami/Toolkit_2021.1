# coding: utf-8

import apex
apex.disableShowOutput()

def prepare_data_grid(grid={}):
    # Display nodes and elements counts
    model = apex.currentModel()
    meshItem = []
    grid['meshes'] = meshItem
    for Part in model.getParts(True):
        if Part.getVisibility():
            for Mesh in Part.getMeshes():
                print(Mesh)
                if Mesh.getVisibility():
                    meshInfo = {}
                    meshItem.append(meshInfo)
                    meshInfo['mesh_name'] = Mesh.getName()
                    meshInfo['parent_name'] = Mesh.getParent().getName()
                    meshInfo['elements_count'] = len(Mesh.getElements())
                    meshType = ""
                    if type(Mesh) == apex.mesh.SolidMesh:
                        meshType += "Tetra"
                    elif type(Mesh) == apex.mesh.SurfaceMesh:
                        meshType += "Surface"
                    elif type(Mesh) == apex.mesh.HexMesh:
                        meshType += "Hexa"
                    else:
                        meshType = "??"
                    meshInfo['mesh_type'] = meshType
    return grid

def calcSelected(grid={}):
    model = apex.currentModel()
    meshItem = []
    grid['meshes'] = meshItem
    for Elem in apex.selection.getCurrentSelection():
        if Elem.getVisibility():
            if type(Elem) == apex.Assembly:
                for Part in Elem.getParts(True):
                    for Mesh in Part.getMeshes():
                        if Mesh.getVisibility():
                            meshInfo = {}
                            meshItem.append(meshInfo)
                            meshInfo['mesh_name'] = Mesh.getName()
                            meshInfo['parent_name'] = Mesh.getParent().getName()
                            meshInfo['elements_count'] = len(Mesh.getElements())
                            meshType = ""
                            if Mesh.getEntityType() == 42:
                                meshType += "Tetra "
                            elif Mesh.getEntityType() == 43:
                                meshType += "Surface "
                            elif Mesh.getEntityType() == 45:
                                meshType += "Hexa "
                            else:
                                meshType = "??"
                            meshInfo['mesh_type'] = meshType

            elif type(Elem) == apex.Part:
                for Mesh in Elem.getMeshes():
                    if Mesh.getVisibility():
                        meshInfo = {}
                        meshItem.append(meshInfo)
                        meshInfo['mesh_name'] = Mesh.getName()
                        meshInfo['parent_name'] = Mesh.getParent().getName()
                        meshInfo['elements_count'] = len(Mesh.getElements())
                        meshType = ""
                        if Mesh.getEntityType() == 42:
                            meshType += "Tetra "
                        elif Mesh.getEntityType() == 43:
                            meshType += "Surface "
                        elif Mesh.getEntityType() == 45:
                            meshType += "Hexa "
                        else:
                            meshType = "??"
                        meshInfo['mesh_type'] = meshType

            elif type(Elem) == apex.mesh.SurfaceMesh:
                Mesh = Elem
                if Elem.getVisibility():
                    meshInfo = {}
                    meshItem.append(meshInfo)
                    meshInfo['mesh_name'] = Mesh.getName()
                    meshInfo['parent_name'] = Mesh.getParent().getName()
                    meshInfo['elements_count'] = len(Mesh.getElements())
                    meshType = ""
                    if Mesh.getEntityType() == 42:
                        meshType += "Tetra "
                    elif Mesh.getEntityType() == 43:
                        meshType += "Surface "
                    elif Mesh.getEntityType() == 45:
                        meshType += "Hexa "
                    else:
                        meshType = "??"
                    meshInfo['mesh_type'] = meshType

            elif type(Elem) == apex.mesh.SolidMesh:
                Mesh = Elem
                if Elem.getVisibility():
                    meshInfo = {}
                    meshItem.append(meshInfo)
                    meshInfo['mesh_name'] = Mesh.getName()
                    meshInfo['parent_name'] = Mesh.getParent().getName()
                    meshInfo['elements_count'] = len(Mesh.getElements())
                    meshType = ""
                    if Mesh.getEntityType() == 42:
                        meshType += "Tetra "
                    elif Mesh.getEntityType() == 43:
                        meshType += "Surface "
                    elif Mesh.getEntityType() == 45:
                        meshType += "Hexa "
                    else:
                        meshType = "??"
                    meshInfo['mesh_type'] = meshType

            elif type(Elem) == apex.mesh.HexMesh:
                Mesh = Elem
                if Elem.getVisibility():
                    meshInfo = {}
                    meshItem.append(meshInfo)
                    meshInfo['mesh_name'] = Mesh.getName()
                    meshInfo['parent_name'] = Mesh.getParent().getName()
                    meshInfo['elements_count'] = len(Mesh.getElements())
                    meshType = ""
                    if Mesh.getEntityType() == 42:
                        meshType += "Tetra "
                    elif Mesh.getEntityType() == 43:
                        meshType += "Surface "
                    elif Mesh.getEntityType() == 45:
                        meshType += "Hexa "
                    else:
                        meshType = "??"
                    meshInfo['mesh_type'] = meshType

    return grid