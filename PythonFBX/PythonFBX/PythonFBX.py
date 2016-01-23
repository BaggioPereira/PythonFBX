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

    node = scene.GetRootNode()
    for i in range(node.GetChildCount()):
        child = node.GetChild(i)
        attr_type = child.GetNodeAttribute().GetAttributeType()

        if attr_type==FbxCommon.FbxNodeAttribute.eMesh:
            
            mesh = child.GetNodeAttribute()
            if not mesh.GetNode().GetMesh().IsTriangleMesh():
                triangulateMesh=converter.Triangulate(mesh,False)
                print("Triangulated")
            """textfilex = open('pointsx.txt', 'w')
            textfiley = open('pointsy.txt', 'w')"""
            polygoncount = triangulateMesh.GetNode().GetMesh().GetPolygonCount()
            for i in range(polygoncount):
                vertexcount = triangulateMesh.GetNode().GetMesh().GetPolygonSize(i)
                vertices = []
                for j in range(vertexcount):
                    vert = triangulateMesh.GetNode().GetMesh().GetPolygonVertex(i, j)
                    vertexData = triangulateMesh.GetNode().GetMesh().GetControlPointAt(vert)
                    vertx = vertexData[0]
                    verty = vertexData[1]
                    vertz = vertexData[2]
                    x0 = vertx
                    y0 = verty*math.cos(math.radians(0)) + vertz*math.sin(math.radians(0))
                    z0 = vertz*math.cos(math.radians(0)) - verty*math.sin(math.radians(0))
                    x1 = x0*math.cos(math.radians(45)) - z0*math.sin(math.radians(45))
                    y1 = y0
                    z1 = z0*math.cos(math.radians(45)) + x0*math.sin(math.radians(45))
                    x2 = x1*math.cos(math.radians(0)) + y1*math.sin(math.radians(0))
                    y2 = y1*math.cos(math.radians(0)) - x1*math.sin(math.radians(0))
                    y2 = y2 * -1
                    vertices.append([x2,y2])
                point1 = vertices[0][0] * 8
                point2 = vertices[0][1] * 8
                point3 = vertices[1][0] * 8
                point4 = vertices[1][1] * 8
                point5 = vertices[2][0] * 8
                point6 = vertices[2][1] * 8
                point1 += 250
                point2 += 250
                point3 += 250
                point4 += 250
                point5 += 250
                point6 += 250
                string = str(point1) + (',') + str(point2) + (' ') + str(point3) + (',') + str(point4) + (' ') + str(point5) + (',') + str(point6)
                et.SubElement(doc, 'polyline', points = string, stroke='lightblue', fill='blue')
                

            """verticesLength = len(vertices)
            for i in range(verticesLength):
                point = vertices[i]
                xpoint=point[0]
                textfilex.write(str(xpoint))
                textfilex.write("\n")
            for i in range(verticesLength):
                point = vertices[i]
                ypoint=point[1]
                textfiley.write(str(ypoint))
                textfiley.write("\n")
            textfilex.close()
            textfiley.close()"""
os.chdir(path)
f = open('sample.svg', 'w')
f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
f.write(et.tostring(doc))
f.close()



f = open('index.html', 'w')
message = """<html>

<head><title> FBX Viewer </title></head>
<body><p>This is my FBX viewer!</p><object data="sample.svg" type="image/svg+xml"></object></body>

</html>"""

f.write(message)
f.close()

webbrowser.open_new_tab('index.html')
