import FbxCommon
import fbx
import math
import sys
import webbrowser
import glob, os
from xml.etree import ElementTree as et
import Image

# global variables
filenames = []
filenum = 0
edges = []
depth = []
vertices = []
xPoints = []
yPoints = []
zPoints = []
centerX = 0
centerY = 0 
centerZ = 0
minX = 0 
minY = 0 
maxX = 0
maxY = 0
textureArray = fbx.FbxTextureArray()

#Gets the path where the FBX files are
path = os.getcwd()
newpath=path+"\Fbx Files"
print(newpath)

#Looks for all FBX files in the path
os.chdir(newpath)
for file in glob.glob("*.fbx"):
    filenames.append(file)

print "number of files ", len(filenames)

filenum = len(filenames)
#Creates an svg element
doc = et.Element('svg', width='480', height='480', version='1.1', xmlns='http://www.w3.org/2000/svg', viewBox = '0,0,0,0', preserveAspectRatio = 'xMidYMid meet', onload='init(evt)')
script = et.SubElement(doc,'script', type='text/ecmascript')
data = '![CDATA[\n'
doc.text=("\n")

def clamp(x): 
    return max(0, min(x, 255))

#Load a file from the list of FBX files
for file in range(len(filenames)):
    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    if not FbxCommon.LoadScene(sdk_manager, scene, filenames[file]): 
        print str(filenames[file])
        print("Not found")      #print if unable to find/load

    rotation =  180
    rotation = rotation * 3.1415926 / 180

    #Get the root node of the file
    node = scene.GetRootNode()
    for i in range(node.GetChildCount()):
        child = node.GetChild(i)
        attr_type = child.GetNodeAttribute().GetAttributeType()
        edges = []
        vertices = []
        if attr_type==FbxCommon.FbxNodeAttribute.eMesh:          
            mesh = child.GetNodeAttribute()
            mesh.GetNode().GetMesh().RemoveBadPolygons()
            #Get the edge count
            edgecount = mesh.GetNode().GetMesh().GetMeshEdgeCount()
            #Get the polygon count
            polygoncount = mesh.GetNode().GetMesh().GetPolygonCount()
            #Make a list of all edges in a string
            contents = "edges = ["
            for edge in range(edgecount):
                start, end = mesh.GetNode().GetMesh().GetMeshEdgeVertices(edge)
                contents += "[" + str(start) + "," + str(end) + "],"
            contents = contents[:-1] +"]\n"
            #Make a list of all faces in a string
            contents += "faces = ["
            for polygon in range(polygoncount):
                contents += "["
                for size in range(mesh.GetNode().GetMesh().GetPolygonSize(polygon)):
                    contents +=str(mesh.GetNode().GetMesh().GetPolygonVertex(polygon,size))+","
                contents = contents[:-1] +"],"
            contents = contents[:-1] + "]\n"
            #Make a list of all depths
            contents += "depth =["
            depth = []
            for polygon in range(mesh.GetNode().GetMesh().GetPolygonCount()):
                contents += "0,"
            contents = contents[:-1] + "]\n"

            #Get all x, y and z 3D coordinates
            xPoints = "x_coords = ["
            yPoints = "y_coords = ["
            zPoints = "z_coords = ["
            smallestControlPointX = 0
            smallestControlPointY = 0
            smallestControlPointZ = 0

            #Set smallest control points
            for point in range(mesh.GetNode().GetMesh().GetControlPointsCount()):
                if(smallestControlPointX > mesh.GetNode().GetMesh().GetControlPoints()[point][0]):
                    smallestControlPointX = mesh.GetNode().GetMesh().GetControlPoints()[point][0]
                    if(smallestControlPointY > mesh.GetNode().GetMesh().GetControlPoints()[point][1]):
                        smallestControlPointY = mesh.GetNode().GetMesh().GetControlPoints()[point][1]
                        if(smallestControlPointZ > mesh.GetNode().GetMesh().GetControlPoints()[point][2]):
                            smallestControlPointZ = mesh.GetNode().GetMesh().GetControlPoints()[point][2]

            #Add to list for x, y and z coords
            for point in range(mesh.GetNode().GetMesh().GetControlPointsCount()):
                xPoints += str(mesh.GetNode().GetMesh().GetControlPoints()[point][0] - smallestControlPointX) + ","
                yPoints += str(mesh.GetNode().GetMesh().GetControlPoints()[point][1] - smallestControlPointY) + ","
                zPoints += str(mesh.GetNode().GetMesh().GetControlPoints()[point][2] - smallestControlPointZ) + ","
                      
            xPoints = xPoints[:-1] +"];\n"
            yPoints = yPoints[:-1] +"];\n"
            zPoints = zPoints[:-1] +"];\n"
            contents += xPoints + yPoints + zPoints
            data += contents
            
            #Functions
            data += "\n\ncentre_x = "+str(-smallestControlPointX)+";\ncentre_y = "+str(-smallestControlPointY)+";\ncentre_z = "+str(-smallestControlPointZ)+";\n\n\n\n\tvar minX = -999;\n\tvar minY = -999;\n\tvar maxX = -999;\n\tvar maxY = -999;\n\n"
            data += "function init(evt)\n{\n\tif ( window.svgDocument == null )\n\t{\n\t\tsvgDocument = evt.target.ownerDocument;\n\t}\n\trotateAboutY("+str((135*3.14/180))+");\n\trotateAboutX("+str(-(135*3.14/180))+");\n\tcalculateDepth()\n\tdrawBox();\n\tsetViewBox();\nif(minX < 0 || minY < 0)\n{\n\tfixCoords();\n\tdrawBox();\n\tsetViewBox();\n}}"

            data += "\n\n\nfunction setViewBox()\n{\n\tminX = -999;\n\tminY = -999;\n\tmaxX = -999;\n\tmaxY = -999;\n\t\n\tfor(var i = 0; i < x_coords.length; i++)\n\t{\n\t\tif(minX == -999 || x_coords[i] < minX)\n\t\t\tminX = x_coords[i];\n\t\tif(minY == -999 || y_coords[i] < minY)\n\t\t\tminY = y_coords[i];\n\t\tif(maxX == -999 || x_coords[i] > maxX)\n\t\t\tmaxX = x_coords[i];\n\t\tif(maxY == -999 || y_coords[i] > maxY)\n\t\t\tmaxY = y_coords[i];\n\t}\n\tshape = document.getElementsByTagName('svg')[0];\n\tshape.setAttribute('viewBox', minX+'" + str(file*50) + " '+ minY+' '+ maxX+'" + str(file*50) + " '+maxY);\n}"
            data += "\n\n\nfunction fixCoords()\n{\n\tif(minX < 0)\n\t{\n\t\tcentre_x += -minX;\n\t\tfor(var i = 0; i < x_coords.length;i++)\n\t\t{\n\t\t\tx_coords[i] += -minX;\n\t\t}\n\t}\n\tif(minY < 0)\n\t{\n\t\tcentre_y += -minY;\n\t\tfor(var i = 0; i < y_coords.length;i++)\n\t\t{\n\t\t\ty_coords[i] += -minY;\n\t\t}\n\t}\n}"            
            data += "\n\n\nfunction calculateDepth()\n{\n\tvar facesDepth = Array(faces.length);\n\tfor(var i = 0; i < faces.length; i++)\n\t{\n\t\tvar currentDepth = 0;\n\t\tfor(var u = 0; u < faces[i].length; u ++)\n\t\t{\n\t\t\tcurrentDepth += z_coords[faces[i][u]];\n\t\t}\n\t\tcurrentDepth /= faces[i].length;\n\t\tfacesDepth[i] = currentDepth;\n\t}\n\tfor(var i = 0; i < depth.length; i++)\n\t{\n\t\tvar smallest = -1;\n\t\tfor(var u = 0; u < facesDepth.length; u++)\n\t\t{\n\t\t\tif(facesDepth[u] != -99999 && (smallest == -1 || facesDepth[smallest] > facesDepth[u]))\n\t\t\t\tsmallest = u;\n\t\t}\n\t\tdepth[i] = smallest;\n\t\tfacesDepth[smallest] = -99999;\n\t}\n}"
            data += "\n\n\nfunction drawBox()\n{\n\tfor(var i=0; i<depth.length; i++)\n\t{\n\t\tface = svgDocument.getElementById('face-'+i);\n\t\tvar d = 'm'+x_coords[faces[depth[i]][0]]+' '+y_coords[faces[depth[i]][0]];\n\t\tfor(var u = 1; u < faces[depth[i]].length; u++)\n\t\t{\n\t\t\td+= ' ' + 'L'+x_coords[faces[depth[i]][u]]+' '+y_coords[faces[depth[i]][u]];\n\t\t}\n\t\td+= ' Z';\n\t\tface.setAttributeNS(null, 'd', d);\n\t}\n}"
            

            data += "\n\n\nfunction rotateAboutX(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\ty = y_coords[i] - centre_y;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(y*y + z*z);\n\t\ttheta  = Math.atan2(y, z) + radians;\n\t\ty_coords[i] = centre_y + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n}"
            data += "\n\n\nfunction rotateAboutY(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\tx = x_coords[i] - centre_x;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(x*x + z*z);\n\t\ttheta  = Math.atan2(x, z) + radians;\n\t\tx_coords[i] = centre_x + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n}"
            data += "\n\n\nfunction rotateAboutZ(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\tx = x_coords[i] - centre_x;\n\t\ty = y_coords[i] - centre_y;\n\t\td = Math.sqrt(x*x + y*y);\n\t\ttheta  = Math.atan2(x, y) + radians;\n\t\tx_coords[i] = centre_x + d * Math.sin(theta);\n\t\ty_coords[i] = centre_y + d * Math.cos(theta);\n\t}\n}"

            data += "\n]]"
            cdata = et.SubElement(script, data)

            #Get the colour for each polygon
            for polygon in range (mesh.GetNode().GetMesh().GetPolygonCount()):
                poly = FbxCommon.FbxPropertyDouble3(mesh.GetNode().GetMesh().FindProperty("Color")).Get()
                r = clamp(poly[0] * 255 - poly[0] * 0.4 * ((polygon+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                g = clamp(poly[1] * 255 - poly[1] * 0.4 * ((polygon+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                b = clamp(poly[2] * 255 - poly[2] * 0.4 * ((polygon+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                svgPath = et.SubElement(doc, 'path', stroke = str('#%02x%02x%02x' % (r,g,b)), fill = str('#%02x%02x%02x' % (r,g,b)), id = "face-"+str(polygon), d = '')
                svgPath.text = "\n"

            #Create an svg file and store all the data
            os.chdir(path)
            f = open(str(filenames[file]) + '.svg', 'w')
            f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
            f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
            f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
            f.write(et.tostring(doc))
            f.close()

            #Cleanup the svg file
            r = open(str(filenames[file]) + '.svg', 'r')
            filedata = r.read()
            r.close()

            newdata = filedata.replace("] />", "]>")

            f = open(str(filenames[file]) + '.svg', 'w')
            f.write(newdata)
            f.close()



#Update the index.html
f = open('index.html', 'w')
message = """<html>

<head><title> FBX Viewer </title></head>
<body><p>This is my FBX viewer!</p>"""
for file in range(filenum):
    message += """<object data="""
    message += str(filenames[file])
    message +=""".svg type="image/svg+xml"></object>"""
message +="""</body>

</html>"""

f.write(message)
f.close()