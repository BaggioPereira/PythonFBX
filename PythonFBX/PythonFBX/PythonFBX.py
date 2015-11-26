import FbxCommon
import fbx
import sys
import webbrowser
import glob, os

# global variables
filenames=[]
filenum = 0
vertices=[]
polygoncount = 0
vertexcount = 0
normalscount = 0
normal=[]


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
        print("File not found")
    node = scene.GetRootNode()
    for i in range(node.GetChildCount()):
        child = node.GetChild(i)
        attr_type = child.GetNodeAttribute().GetAttributeType()

        if attr_type==FbxCommon.FbxNodeAttribute.eMesh:
            mesh = child.GetNodeAttribute()
            triangulatedMesh = converter.Triangulate(mesh,False)
            vertices = mesh.GetControlPoints()
            vertlen = len(vertices)
            for i in range(vertlen):
                vert = vertices[i]
                


os.chdir(path)

f = open('index.html', 'w')
message = """<html>

<head><title> FBX Viewer </title></head>
<body><p>This is my FBX viewer!</p></body>

</html>"""

f.write(message)
f.close()

# webbrowser.open_new_tab('index.html')