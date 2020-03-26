import vtk

def main():
    ugrid = MakePolyhedron()
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetInputData(ugrid)
    writer.SetFileName("unstructured_grid.vtk")
    writer.Write()

def MakePolyhedron():
    """
      Make a regular dodecahedron. It consists of twelve regular pentagonal
      faces with three faces meeting at each vertex.
    """
    # numberOfVertices = 20
    numberOfFaces = 12
    # numberOfFaceVertices = 5

    points = vtk.vtkPoints()
    points.InsertNextPoint(1.21412, 0, 1.58931)
    points.InsertNextPoint(0.375185, 1.1547, 1.58931)
    points.InsertNextPoint(-0.982247, 0.713644, 1.58931)
    points.InsertNextPoint(-0.982247, -0.713644, 1.58931)
    points.InsertNextPoint(0.375185, -1.1547, 1.58931)
    points.InsertNextPoint(1.96449, 0, 0.375185)
    points.InsertNextPoint(0.607062, 1.86835, 0.375185)
    points.InsertNextPoint(-1.58931, 1.1547, 0.375185)
    points.InsertNextPoint(-1.58931, -1.1547, 0.375185)
    points.InsertNextPoint(0.607062, -1.86835, 0.375185)
    points.InsertNextPoint(1.58931, 1.1547, -0.375185)
    points.InsertNextPoint(-0.607062, 1.86835, -0.375185)
    points.InsertNextPoint(-1.96449, 0, -0.375185)
    points.InsertNextPoint(-0.607062, -1.86835, -0.375185)
    points.InsertNextPoint(1.58931, -1.1547, -0.375185)
    points.InsertNextPoint(0.982247, 0.713644, -1.58931)
    points.InsertNextPoint(-0.375185, 1.1547, -1.58931)
    points.InsertNextPoint(-1.21412, 0, -1.58931)
    points.InsertNextPoint(-0.375185, -1.1547, -1.58931)
    points.InsertNextPoint(0.982247, -0.713644, -1.58931)

    # Dimensions are [numberOfFaces][numberOfFaceVertices]
    dodechedronFace = [
        [0, 1, 2, 3, 4],
        [0, 5, 10, 6, 1],
        [1, 6, 11, 7, 2],
        [2, 7, 12, 8, 3],
        [3, 8, 13, 9, 4],
        [4, 9, 14, 5, 0],
        [15, 10, 5, 14, 19],
        [16, 11, 6, 10, 15],
        [17, 12, 7, 11, 16],
        [18, 13, 8, 12, 17],
        [19, 14, 9, 13, 18],
        [19, 18, 17, 16, 15]
    ]

    dodechedronFacesIdList = vtk.vtkIdList()
    # Number faces that make up the cell.
    dodechedronFacesIdList.InsertNextId(numberOfFaces)
    for face in dodechedronFace:
        # Number of points in the face == numberOfFaceVertices
        dodechedronFacesIdList.InsertNextId(len(face))
        # Insert the pointIds for that face.
        [dodechedronFacesIdList.InsertNextId(i) for i in face]

    uGrid = vtk.vtkUnstructuredGrid()
    uGrid.InsertNextCell(vtk.VTK_POLYHEDRON, dodechedronFacesIdList)
    uGrid.SetPoints(points)

    return uGrid

if __name__ == '__main__':
    main()