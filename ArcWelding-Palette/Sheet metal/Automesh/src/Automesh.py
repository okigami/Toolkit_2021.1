# coding: utf-8

def ArcWeldAutomesh(dict={}):
    import apex
    from apex.construct import Point3D, Point2D
    from math import sqrt, pow, degrees, acos, pi
    import os
    from Midsurface import Midsurface as GetMidsurface
    from SuppressFeatures import SuppressFeatures
    from CreateBeads import BeadBySweep
    from SplitByTrajectories import SplitByTrajectories
    from MeshPartitions import CreateMeshPartitions
    from MeshNONPartitions import CreateMeshNONPartitions

    gotDict = dict


    try:
        apex.session.displayStatusMessage("Getting midsurface...")
        GetMidsurface()
        try:
            apex.session.displayStatusMessage("Suppressing features...")
            SuppressFeatures()
            try:
                apex.session.displayStatusMessage("Creating refinement regions...")
                BeadBySweep(gotDict)
                try:
                    apex.session.displayStatusMessage("Split regions...")
                    SplitByTrajectories()
                    try:
                        apex.session.displayStatusMessage("Fine meshing...")
                        CreateMeshPartitions(gotDict)
                        try:
                            apex.session.displayStatusMessage("Coarse meshing...")
                            CreateMeshNONPartitions(gotDict)
                        except:
                            apex.enableShowOutput()
                            print("Coarse meshing failed!")
                    except:
                        apex.enableShowOutput()
                        print("Fine meshing failed!")
                except:
                    apex.enableShowOutput()
                    print("Split failed!")
            except:
                apex.enableShowOutput()
                print("Create refinement regions failed!")
        except:
            apex.enableShowOutput()
            print("Suppress features failed!")
    except:
        apex.enableShowOutput()
        print("Midsurface failed!")


