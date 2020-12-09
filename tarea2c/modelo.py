from OpenGL.GL import *
import OpenGL.GL.shaders
import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import scene_graph as sg

def createSnake():
    
    gpuSnake = es.toGPUShape(bs.createTextureCube("snake.png"), GL_REPEAT, GL_NEAREST)

    # Creating a snake
    snake1 = sg.SceneGraphNode("snake1")
    snake1.transform = tr.translate(0,0,0.5)
    snake1.childs += [gpuSnake]

    return snake1

#Creates a snake of length N 
def createSnakes(N,posiciones):

    # Creating the snake of length N
    final_snakes = sg.SceneGraphNode("final_snakes")
    final_snakes.transform = tr.identity()
    final_snakes.childs += [createSnake()]

    snakes = sg.SceneGraphNode("snakes")

    baseName = "snakes"
    for i in range(N):
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(posiciones[i][0], posiciones[i][1], 0.5)
        newNode.childs += [final_snakes]

        snakes.childs += [newNode]

    return snakes

def createWall():
    
    gpuWall = es.toGPUShape(bs.createTextureCube("wall.png"), GL_REPEAT, GL_NEAREST)

    #creating a wall
    wall1 = sg.SceneGraphNode("wall1")
    #wall1.transform = tr.identity()
    wall1.transform = tr.scale(1,1,2)
    wall1.childs += [gpuWall]
    
    return wall1

def createFullWall(posiciones):
        
    #creating a full wall
    final_walls = sg.SceneGraphNode("wall")
    final_walls.transform = tr.identity()
    final_walls.childs += [createWall()]

    walls = sg.SceneGraphNode("full_wall")

    baseName = "wall"
    for i in range(len(posiciones)):
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.translate(posiciones[i][0], posiciones[i][1], posiciones[i][2])
        newNode.childs += [final_walls]
        
        walls.childs += [newNode]

    return walls

def readFaceVertex(faceDescription):

    aux = faceDescription.split('/')

    assert len(aux[0]), "Vertex index has not been defined."

    faceVertex = [int(aux[0]), None, None]

    assert len(aux) == 3, "Only faces where its vertices require 3 indices are defined."

    if len(aux[1]) != 0:
        faceVertex[1] = int(aux[1])

    if len(aux[2]) != 0:
        faceVertex[2] = int(aux[2])

    return faceVertex



def readOBJ(filename, color):

    vertices = []
    normals = []
    textCoords= []
    faces = []

    with open(filename, 'r') as file:
        for line in file.readlines():
            aux = line.strip().split(' ')
            
            if aux[0] == 'v':
                vertices += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vn':
                normals += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vt':
                assert len(aux[1:]) == 2, "Texture coordinates with different than 2 dimensions are not supported"
                textCoords += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'f':
                N = len(aux)                
                faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                for i in range(3, N-1):
                    faces += [[readFaceVertex(faceVertex) for faceVertex in [aux[i], aux[i+1], aux[1]]]]

        vertexData = []
        indices = []
        index = 0

        # Per previous construction, each face is a triangle
        for face in faces:

            # Checking each of the triangle vertices
            for i in range(0,3):
                vertex = vertices[face[i][0]-1]
                normal = normals[face[i][2]-1]

                vertexData += [
                    vertex[0], vertex[1], vertex[2],
                    color[0], color[1], color[2],
                    normal[0], normal[1], normal[2]
                ]

            # Connecting the 3 vertices to create a triangle
            indices += [index, index + 1, index + 2]
            index += 3        

        return bs.Shape(vertexData, indices)
