import vtk

def main():

    # User specifies points and face connectivity
    # points for a hexahedron
    points3D = [
        (0.0, 0.0, 0.0),  # pid = 0
        (1.0, 0.0, 0.0),  # pid = 1
        (1.0, 1.0, 0.0),  # pid = 2
        (0.0, 1.0, 0.0),  # pid = 3
        (0.0, 0.0, 1.0),  # pid = 4
        (1.0, 0.0, 1.0),  # pid = 5
        (1.0, 1.0, 1.0),  # pid = 6
        (0.0, 1.0, 1.0),  # pid = 7
    ]

    # face connectivity for hexehedron
    hexFaceConn = [
        (6,             # number of faces in this cell.
         [0, 3, 2, 1],  # xy face normal to [0, 0, -1].
         [4, 5, 6, 7],  # xy face normal to [0, 0, 1].
         [0, 1, 5, 4],  # xz face normal to [0, -1, 0].
         [2, 3 ,7, 6],  # xz face normal to [0, 1, 0].
         [1, 2, 6, 5],  # yz face normal to [1, 0, 0].
         [0, 4, 7, 3],  # yz face normal to [-1, 0, 0].
        ),
    ]

    ugrid = MakePolyhedron(points3D, hexFaceConn)
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

def MakePolyhedron(points, face_conn):
    """
    Make general polyhedron give points and the face connectivity that define
    the cells of the polyhedron. Each the point indexes for each face
    specified in ``face_conn`` must be in counter clockwise order as viewed
    from the outside.

    Parameters
    ----------
    points: list of tuples
      List of points that define the 3D space.
    face_conn: list of tuples
      Each tuple contains face connectivity information a cell.
      The structure of each tuple is
      (num faces, [pids of face 1], ... ,[pids of face Nth face])
    """

    uGrid = vtk.vtkUnstructuredGrid()

    # populate vtkPoints
    pts = vtk.vtkPoints()
    for point in points:
        pts.InsertNextPoint(point[0], point[1], point[2])

    # add vtkPoints to uGrid.
    uGrid.SetPoints(pts)

    for cell in face_conn:
        facesIdList = vtk.vtkIdList()
        # insert number of faces that make up the cell
        facesIdList.InsertNextId(cell[0])
        for face in cell[1:]:
            # insert number of points of each face in the cell.
            facesIdList.InsertNextId(len(face))
            # insert pointIds of each face in the cell.
            [facesIdList.InsertNextId(i) for i in face]
        # insert face connectivity of a cell to ugrid.
        uGrid.InsertNextCell(vtk.VTK_POLYHEDRON, facesIdList)

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