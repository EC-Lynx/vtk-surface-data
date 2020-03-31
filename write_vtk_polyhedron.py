import vtk

def main():
    ugrid = MakeHexahedron()
    pgrid = MakePolygon()

    # Add scalars to ugrid cells
    scalars = vtk.vtkFloatArray()
    scalars.InsertTuple1(0, 25)
    scalars.SetName("Volume")
    ugrid.GetCellData().SetScalars(scalars)

    # Add scalars to pgrid cells
    surfaceScalar = vtk.vtkFloatArray()
    surfaceScalar.InsertTuple1(0, 15)
    surfaceScalar.SetName("Surface")
    pgrid.GetCellData().SetScalars(surfaceScalar)

    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetInputData(ugrid)
    writer.SetFileName("unstructured_grid.vtk")
    writer.Write()

    writer = vtk.vtkPolyDataWriter()
    writer.SetInputData(pgrid)
    writer.SetFileName("polydata.vtk")
    writer.Write()

def MakeHexahedron():
    """
    Make a regular hexagon (cube) with all faces square and three squares
     around each vertex.

    Setup the coordinates of eight points
     (faces must be in counter clockwise order as viewed from the outside).
    """
    numberOfFaces = 6

    # Create the points
    points = vtk.vtkPoints()
    points.InsertNextPoint(0.0, 0.0, 0.0)  # pid = 0
    points.InsertNextPoint(1.0, 0.0, 0.0)  # pid = 1
    points.InsertNextPoint(1.0, 1.0, 0.0)  # pid = 2
    points.InsertNextPoint(0.0, 1.0, 0.0)  # pid = 3
    points.InsertNextPoint(0.0, 0.0, 1.0)  # pid = 4
    points.InsertNextPoint(1.0, 0.0, 1.0)  # pid = 5
    points.InsertNextPoint(1.0, 1.0, 1.0)  # pid = 6
    points.InsertNextPoint(0.0, 1.0, 1.0)  # pid = 7

    # Create faces
    # Dimensions are [numberOfFaces][numberOfFaceVertices]
    hexahedronFace = [
        [0, 3, 2, 1],  # xy face normal to [0, 0, -1].
        [4, 5, 6, 7],  # xy face normal to [0, 0, 1].
        [0, 1, 5, 4],  # xz face normal to [0, -1, 0].
        [2, 3 ,7, 6],  # xz face normal to [0, 1, 0].
        [1, 2, 6, 5],  # yz face normal to [1, 0, 0].
        [0, 4, 7, 3],  # yz face normal to [-1, 0, 0].
    ]

    hexahedronFacesIdList = vtk.vtkIdList()
    # Number faces that make up the cell.
    hexahedronFacesIdList.InsertNextId(numberOfFaces)
    for face in hexahedronFace:
        # Number of points in the face == numberOfFaceVertices
        hexahedronFacesIdList.InsertNextId(len(face))
        # Insert the pointIds for that face.
        [hexahedronFacesIdList.InsertNextId(i) for i in face]

    surfaceFacesIdList = vtk.vtkIdList()
    face=[0, 3, 2, 1]
    surfaceFacesIdList.InsertNextId(len(face))
    [surfaceFacesIdList.InsertNextId(i) for i in face]

    uGrid = vtk.vtkUnstructuredGrid()
    uGrid.InsertNextCell(vtk.VTK_POLYHEDRON, hexahedronFacesIdList)
    uGrid.InsertNextCell(vtk.VTK_POLYGON, 4, face)
    uGrid.SetPoints(points)

    return uGrid

def MakePolygon():
    """
    """

    # Create the points
    points = vtk.vtkPoints()
    points.InsertNextPoint(0.0, 0.0, 0.0)  # pid = 0
    points.InsertNextPoint(1.0, 0.0, 0.0)  # pid = 1
    points.InsertNextPoint(1.0, 1.0, 0.0)  # pid = 2
    points.InsertNextPoint(0.0, 1.0, 0.0)  # pid = 3
    points.InsertNextPoint(0.0, 0.0, 1.0)  # pid = 4
    points.InsertNextPoint(1.0, 0.0, 1.0)  # pid = 5
    points.InsertNextPoint(1.0, 1.0, 1.0)  # pid = 6
    points.InsertNextPoint(0.0, 1.0, 1.0)  # pid = 7

    # Create faces
    # Dimensions are [numberOfFaces][numberOfFaceVertices]
    polygonFaces = [
        [0, 3, 2, 1],  # xy face normal to [0, 0, -1].
    ]

    polygons = vtk.vtkCellArray()
    for face in polygonFaces:
        polygon = vtk.vtkPolygon()
        polygon.GetPointIds().SetNumberOfIds(len(face))
        for idx, pid in enumerate(face):
            polygon.GetPointIds().SetId(idx, pid)
        polygons.InsertNextCell(polygon)

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetPolys(polygons)

    return polyData

if __name__ == '__main__':
    main()