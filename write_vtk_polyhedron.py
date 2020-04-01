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

    # face connectivity for polygon
    sqFaceConn = [
        [0, 3, 2, 1],  # xy face normal to [0, 0, -1].
        [2, 3 ,7, 6],  # xz face normal to [0, 1, 0].
    ]

    ugrid = MakePolyhedron(points3D, hexFaceConn)
    # Add scalars to ugrid cells
    volumeScalar = [25]
    AddScalars(ugrid, volumeScalar, 'volume')
    # output file
    WriteVtkXML(ugrid, 'volume', 'BINARY', 'ZLIB')

    pgrid = MakePolygon(points3D, sqFaceConn)
    # Add scalars to pgrid cells
    surfaceScalar = [15, 10]
    AddScalars(pgrid, surfaceScalar, "surface")
    # output file
    WriteVtkXML(pgrid, 'surface', 'ASCII')

def MakePolyhedron(points, faceConn):
    """
    Make general polyhedron given points and the face connectivity that define
    the cells of the polyhedron. The point indexes for each face
    specified in ``faceConn`` must be in counter clockwise order as viewed
    from the outside.

    Parameters
    ----------
    points: list of tuples
      List of points that define the 3D space.
    faceConn: list of tuples
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

    for cell in faceConn:
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

def MakePolygon(points, faceConn):
    """
    Make general polygon given points and the face connectivity that define
    the cells of the polygon. The point indexes for each face
    specified in ``faceConn`` must be in counter clockwise order as viewed
    from the outside.

    Parameters
    ----------
    points: list of tuples
      List of points that define the 3D space.
    faceConn: list of list
      Each list contains connectivity information for a face.
    """

    polyData = vtk.vtkPolyData()

    # populate vtkPoints
    pts = vtk.vtkPoints()
    for point in points:
        pts.InsertNextPoint(point[0], point[1], point[2])

    # add vtkPoints to polyData
    polyData.SetPoints(pts)

    polygons = vtk.vtkCellArray()
    for face in faceConn:
        polygon = vtk.vtkPolygon()
        # insert number of pointIds defining a face.
        polygon.GetPointIds().SetNumberOfIds(len(face))
        # insert pointIds that define a face.
        [polygon.GetPointIds().SetId(idx, pid) for
            idx, pid in enumerate(face)]
        # insert each polygon into polygons vtkCellArray.
        polygons.InsertNextCell(polygon)

    # insert polygons to polyData
    polyData.SetPolys(polygons)

    return polyData

def AddScalars(vtkDataModel, scalar, name):
    """
    Add scalar values to cells of a vtk data set.

    Parameters
    ----------
    vtkDataModel: :class::vtkCommonDataModelPython.
      A vtk unstructured grid or poly data.
    scalar: list
      List of scalar values, where indices of each item in the list
      corresponds to cell id.
    name: string
      Name of scalar field.
    """

    vtkScalar = vtk.vtkFloatArray()
    for idx, val in enumerate(scalar):
        vtkScalar.InsertTuple1(idx, val)
    vtkScalar.SetName(name)
    vtkDataModel.GetCellData().AddArray(vtkScalar)

def WriteVtkXML(vtkDataModel, name, fmt='ASCII', compression=None):
    """
    Write XML out XML file with specified format and compression.

    Parameters
    ----------
    vtkDataModel: :class::vtkCommonDataModelPython.
      A vtk unstructured grid or poly data.
    name: string
      Name of output file.
    fmt: string
      Format of file - `'ASCII'` or `'BINARY'`. Defaults to `'ASCII'`.
    compression: string
      Compression only applied when `fmt` is `'BINARY'`. Compression
      is defaulted to `None`. Available compression options are `'ZLIB'`, `'LZ4'`, and `'LZMA'`.
    """

    if isinstance(vtkDataModel, vtk.vtkUnstructuredGrid):
        writer = vtk.vtkXMLUnstructuredGridWriter()
        filename = name + '.vtu'
    else:
        writer = vtk.vtkXMLPolyDataWriter()
        filename = name + '.vtp'

    if fmt != 'ASCII':
        if compression is None:
            writer.SetCompressorTypeToNone()
        elif compression is 'ZLIB':
            writer.SetCompressorTypeToZLib()
        elif compression is 'LZ4':
            writer.SetCompressorTypeToLZ4()
        elif compression is 'LZMA':
            writer.SetCompressorTypeToLZMA()
        else:
            raise ValueError(f'Unrecognized compression type: {compression}')
    else:
        writer.SetDataModeToAscii()

    writer.SetInputData(vtkDataModel)
    writer.SetFileName(filename)
    writer.Write()

if __name__ == '__main__':
    main()