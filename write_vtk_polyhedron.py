import vtk

def main():
    ugrid = MakeHexahedron()
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetInputData(ugrid)
    writer.SetFileName("unstructured_grid.vtk")
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

    uGrid = vtk.vtkUnstructuredGrid()
    uGrid.InsertNextCell(vtk.VTK_POLYHEDRON, hexahedronFacesIdList)
    uGrid.SetPoints(points)

    return uGrid

if __name__ == '__main__':
    main()