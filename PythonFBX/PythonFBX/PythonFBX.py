import FbxCommon
import sys
import webbrowser
import glob, os

sdk_manager, scene = FbxCommon.InitializeSdkObjects()

path = os.getcwd()
newpath=path+"\Fbx Files"
print(newpath)

os.chdir(newpath)
for file in glob.glob("*.fbx"):
    print(file)

os.chdir(path)

f = open('index.html', 'w')
message = """<html>

<head><title> FBX Viewer </title></head>
<body><p>This is my FBX viewer!</p></body>

</html>"""

f.write(message)
f.close()

# webbrowser.open_new_tab('index.html')