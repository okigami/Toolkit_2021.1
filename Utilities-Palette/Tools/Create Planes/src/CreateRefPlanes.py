# coding: utf-8

import apex
from apex.construct import Point3D, Point2D

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()
apex.disableShowOutput()

def CreatePlanes(dic={}):
    NewPart = model_1.createPart(name="Reference planes")

    def doSketch_1():
        part_1 = model_1.getCurrentPart()
        if part_1 is None:
            part_1 = model_1.createPart()
        sketch_1 = part_1.createSketchOnGlobalPlane(
            name = 'Sketch 1',
            plane = apex.construct.GlobalPlane.YZ,
            alignSketchViewWithViewport = True
        )


        rectangle_1 = sketch_1.createRectangle2Point(
            name = "Rectangle 1",
            location = Point2D( -5.000000000000000, 5.000000000000000 ),
            diagonal = Point2D( 5.000000000000000, -5.000000000000000 )
        )

        return sketch_1.completeSketch( fillSketches = True )

    newbodies = doSketch_1()


    def doSketch_2():
        part_1 = model_1.getCurrentPart()
        if part_1 is None:
            part_1 = model_1.createPart()
        sketch_2 = part_1.createSketchOnGlobalPlane(
            name = 'Sketch 2',
            plane = apex.construct.GlobalPlane.ZX,
            alignSketchViewWithViewport = True
        )


        rectangle_2 = sketch_2.createRectangle2Point(
            name = "Rectangle 2",
            location = Point2D( -5.000000000000000, 5.000000000000000 ),
            diagonal = Point2D( 5.000000000000000, -5.000000000000000 )
        )

        return sketch_2.completeSketch( fillSketches = True )

    newbodies = doSketch_2()


    def doSketch_3():
        part_1 = model_1.getCurrentPart()
        if part_1 is None:
            part_1 = model_1.createPart()
        sketch_3 = part_1.createSketchOnGlobalPlane(
            name = 'Sketch 3',
            plane = apex.construct.GlobalPlane.XY,
            alignSketchViewWithViewport = True
        )


        rectangle_3 = sketch_3.createRectangle2Point(
            name = "Rectangle 3",
            location = Point2D( -5.000000000000000, 5.000000000000000 ),
            diagonal = Point2D( 5.000000000000000, -5.000000000000000 )
        )

        return sketch_3.completeSketch( fillSketches = True )

    newbodies = doSketch_3()

