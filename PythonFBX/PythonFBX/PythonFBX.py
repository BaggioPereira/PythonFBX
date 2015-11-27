import FbxCommon
import fbx
import math
import sys
import webbrowser
import glob, os

# global variables
filenames = []
filenum = 0
vertices = []
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
            polygoncount = triangulateMesh.GetNode().GetMesh().GetPolygonCount()
            for i in range(polygoncount):
                vertexcount = triangulateMesh.GetNode().GetMesh().GetPolygonSize(i)
                for j in range(vertexcount):
                    vert = triangulateMesh.GetNode().GetMesh().GetPolygonVertex(i, j)
                    vertexData = triangulateMesh.GetNode().GetMesh().GetControlPointAt(vert)
                    vertx = vertexData[0]
                    verty = vertexData[1]
                    vertz = vertexData[2]
                    x0 = vertx
                    x0 = vertx
                    y0 = verty*math.cos(math.radians(45)) + vertz*math.sin(math.radians(45))
                    z0 = vertz*math.cos(math.radians(45)) - verty*math.sin(math.radians(45))
                    x1 = x0*math.cos(math.radians(45)) - z0*math.sin(math.radians(45))
                    y1 = y0
                    z1 = z0*math.cos(math.radians(45)) + x0*math.sin(math.radians(45))
                    x2 = x1*math.cos(math.radians(0)) + y1*math.sin(math.radians(0))
                    y2 = y1*math.cos(math.radians(0)) - x1*math.sin(math.radians(0))
                    vertices.append([x2,y2])

os.chdir(path)

f = open('index.html', 'w')
message = """<html>

<head><title> FBX Viewer </title></head>
<body><p>This is my FBX viewer!</p></body>

</html>"""

f.write(message)
f.close()

# webbrowser.open_new_tab('index.html')