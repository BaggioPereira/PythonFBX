import FbxCommon
import sys
import webbrowser

f = open('index.html', 'w')
message = """<html>

<head><title> FBX Viewer </title></head>
<body><p>This is my FBX viewer!</p></body>

</html>"""

f.write(message)
f.close()

webbrowser.open_new_tab('index.html')