import FbxCommon
import fbx
import math
import sys
import webbrowser
import glob, os
from xml.etree import ElementTree as et

# global variables
filenames = []
filenum = 0
polygoncount = 0
vertexcount = 0
normalscount = 0
normalscount=[]

sdk_manager, scene = FbxCommon.InitializeSdkObjects()
converter = fbx.FbxGeometryConverter(sdk_manager)

path = os.getcwd()
newpath=path+"\Fbx Files"
print(newpath)

os.chdir(newpath)
for file in glob.glob("*.fbx"):
    filenames.append(file)

filenum = len(filenames)
doc = et.Element('svg', width='480', height='480', version='1.1', xmlns='http://www.w3.org/2000/svg')
for file in range(filenum):
    if not FbxCommon.LoadScene(sdk_manager, scene, filenames[file]):
        print("Not found")

    contents = ''
    node = scene.GetRootNode()
    for i in range(node.GetChildCount()):
        child = node.GetChild(i)
        attr_type = child.GetNodeAttribute().GetAttributeType()

        if attr_type == FbxCommon.FbxNodeAttribute.eMesh:
            mesh = child.GetNodeAttribute()
            contents += "edges = ["
            edgecount = mesh.GetNode().GetMesh().GetMeshEdgeCount()
            polygoncount = mesh.GetNode().GetMesh().GetPolygonCount()
            for edge in range(edgecount):
                start, end = mesh.GetNode().GetMesh().GetMeshEdgeVertices(edge)
                contents += "[" + str(start) + "," + str(end)+"],"
            contents = contents[:-1]+"]\n"
            contents += "faces =["
            for polygon in range(polygoncount):
                contents+="["
                for size in range(mesh.GetNode().GetMesh().GetPolygonSize(polygon)):
                    contents += str(mesh.GetNode().GetMesh().GetPolygonVertex(polygon,size))+","
                contents = contents[:-1]+"],"
            contents = contents[:-1]+"]\n"
            contents+="depth = ["
            for depth in range(mesh.GetNode().GetMesh().GetPolygonCount()):
                contents += "0,"
            contents = contents[:-1]+"]\n"

            xCoords = "x coords = ["
            yCoords = "y coords = ["
            zCoords = "z coords = ["
            smallestControlPointX = 0
            smallestControlPointY = 0
            smallestControlPointZ = 0
            for controlpoint in range(mesh.GetNode().GetMesh().GetControlPointsCount()):
                if(smallestControlPointX>mesh.GetNode().GetMesh().GetControlPoints()[controlpoint][0]):
                    smallestControlPointX=mesh.GetNode().GetMesh().GetControlPoints()[controlpoint][0]
                    if(smallestControlPointY>mesh.GetNode().GetMesh().GetControlPoints()[controlpoint][1]):
                        smallestControlPointY=mesh.GetNode().GetMesh().GetControlPoints()[controlpoint][1]
                        if(smallestControlPointZ>mesh.GetNode().GetMesh().GetControlPoints()[controlpoint][2]):
                            smallestControlPointZ=mesh.GetNode().GetMesh().GetControlPoints()[controlpoint][2]

            for controlpoint in range(child.GetMesh().GetControlPointsCount()):
                xCoords += str(child.GetMesh().GetControlPoints()[controlpoint][0] - smallestControlPointX) + ","
                yCoords += str(child.GetMesh().GetControlPoints()[controlpoint][1] - smallestControlPointY) + ","
                zCoords += str(child.GetMesh().GetControlPoints()[controlpoint][2] - smallestControlPointZ) + ","

            xCoords = xCoords[:-1] + "];\n"
            yCoords = yCoords[:-1] + "];\n"
            zCoords = zCoords[:-1] + "];\n"

    
os.chdir(path)
f = open('sample.svg', 'w')
f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
f.write('<script type="text/ecmascript"> \n<![CDATA[\n')
f.write(contents)
f.write(xCoords)
f.write(yCoords)
f.write(zCoords)
f.close()



f = open('index.html', 'w')
message = """<html>

<head><title> FBX Viewer </title></head>
<body><p>This is my FBX viewer!</p><object data="sample.svg" type="image/svg+xml"></object></body>

</html>"""

f.write(message)
f.close()

#webbrowser.open_new_tab('index.html')