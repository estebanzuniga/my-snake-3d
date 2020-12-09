
#Tarea 1
#Esteban Zuniga Salamanca
#20366619-5

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import lighting_shaders as ls
import scene_graph as sg
import modelo as mo
import random

class Controller:
    def __init__(self):
        self.fillPolygon = True

posiciones_wall = []
for i in range(20):
    posiciones_wall.append([10,i-10,0.5])
    posiciones_wall.append([-10,i-9,0.5])
    posiciones_wall.append([i-9,10,0.5])
    posiciones_wall.append([i-10,-10,0.5])

controller = Controller()
x_ap = random.randint(-9,9)
y_ap = random.randint(-9,9)
x = 0
y = 0
n = 3
x_cam = 0
y_cam = -n
posiciones_snake = [[0,0,0]]
largo = 1
i = 1
cola = []
state = "UP"
up = 6
viewPos = np.array([x_cam,y_cam,up])
cam_state = "HEAD"

def update():
    global snake
    global x
    global y
    global x_cam
    global y_cam
    global viewPos
    global i
    global cola
    if state == "UP":
        y += 1
        cola = posiciones_snake.pop(len(posiciones_snake)-1)
        i += 1
        posiciones_snake.insert(0,[x,y,0])
        snake.transform = tr.translate(x, y, 0)
        y_cam += 1
        viewPos = np.array([x_cam,y_cam,up])
    elif state == "DOWN":
        y -= 1
        cola = posiciones_snake.pop(len(posiciones_snake)-1)
        i += 1
        posiciones_snake.insert(0,[x,y,0])
        snake.transform = tr.translate(x, y, 0)
        y_cam -= 1
        viewPos = np.array([x_cam,y_cam,up])
    elif state == "RIGHT":
        x += 1
        cola = posiciones_snake.pop(len(posiciones_snake)-1)
        i += 1
        posiciones_snake.insert(0,[x,y,0])
        snake.transform = tr.translate(x, y, 0)
        x_cam += 1
        viewPos = np.array([x_cam,y_cam,up])
    elif state == "LEFT":
        x -= 1
        cola = posiciones_snake.pop(len(posiciones_snake)-1)
        i += 1
        posiciones_snake.insert(0,[x,y,0])
        snake.transform = tr.translate(x, y, 0)
        x_cam -= 1
        viewPos = np.array([x_cam,y_cam,up])
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    global controller
    global state
    global x_cam
    global y_cam
    global viewPos
    global cam_state
    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
        print("Toggle GL_FILL/GL_LINE")
    elif key == glfw.KEY_ESCAPE:
        sys.exit()
    elif (key == glfw.KEY_RIGHT or key == glfw.KEY_D) and cam_state == "HEAD":
        if state == "RIGHT":
            state = "DOWN"
            x_cam += n
            y_cam += n
            viewPos = np.array([x_cam,y_cam,up])
        elif state == "DOWN":
            state = "LEFT"
            x_cam += n
            y_cam -= n
            viewPos = np.array([x_cam,y_cam,up])
        elif state == "LEFT":
            state = "UP"
            x_cam -= n
            y_cam -= n
            viewPos = np.array([x_cam,y_cam,up])
        elif state == "UP":
            state = "RIGHT"
            x_cam -= n
            y_cam += n
            viewPos = np.array([x_cam,y_cam,up])
    elif (key == glfw.KEY_LEFT or key == glfw.KEY_A) and cam_state == "HEAD":
        if state == "LEFT":
            state = "DOWN"
            x_cam -= n
            y_cam += n
            viewPos = np.array([x_cam,y_cam,up])
        elif state == "DOWN":
            state = "RIGHT"
            x_cam -= n
            y_cam -= n
            viewPos = np.array([x_cam,y_cam,up])
        elif state == "RIGHT":
            state = "UP"
            x_cam += n
            y_cam -= n
            viewPos = np.array([x_cam,y_cam,up])
        elif state == "UP":
            state = "LEFT"
            x_cam += n
            y_cam += n
            viewPos = np.array([x_cam,y_cam,up])
    elif (key == glfw.KEY_RIGHT or key == glfw.KEY_D) and (cam_state == "UP" or cam_state == "DIAGONAL"):
        if state != "LEFT":
            state = "RIGHT"
    elif (key == glfw.KEY_LEFT or key == glfw.KEY_A) and (cam_state == "UP" or cam_state == "DIAGONAL"):
        if state != "RIGHT":
            state = "LEFT"
    elif (key == glfw.KEY_UP or key == glfw.KEY_W) and (cam_state == "UP" or cam_state == "DIAGONAL"):
        if state != "DOWN":
            state = "UP"
    elif (key == glfw.KEY_DOWN or key == glfw.KEY_S) and (cam_state == "UP" or cam_state == "DIAGONAL"):
        if state != "UP":
            state = "DOWN"
    elif key == glfw.KEY_R:
        cam_state = "HEAD"
        if state == "UP":
            x_cam = x
            y_cam = y-n
        elif state == "DOWN":
            x_cam = x
            y_cam = y+n
        elif state == "RIGHT":
            x_cam = x-n
            y_cam = y
        elif state == "LEFT":
            x_cam = x+n
            y_cam = y
    elif key == glfw.KEY_E:
        cam_state = "UP"
    elif key == glfw.KEY_T:
        cam_state = "DIAGONAL"
    else:
        print('Unknown key')

if __name__ == "__main__":
    # Initialize glfw
    if not glfw.init():
        sys.exit()
    width = 900
    height = 900
    window = glfw.create_window(width, height, "Snake3D", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)
    
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    stpipeline = es.SimpleTextureTransformShaderProgram()
    tpipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    opipeline = ls.SimpleGouraudShaderProgram()
    glUseProgram(pipeline.shaderProgram)
    
    glClearColor(0.85, 0.85, 0.85, 1.0)
    glEnable(GL_DEPTH_TEST)

    #Creating shapes on GPU memory    
    gpuGrass = es.toGPUShape(bs.createTextureQuad("grass.png",10,10), GL_REPEAT, GL_NEAREST)
    grassTransform = tr.uniformScale(21)
    
    gpuWall = mo.createFullWall(posiciones_wall)
    wallTransform = tr.identity()

    gpuSky = es.toGPUShape(bs.createTextureCube('skybox.png'), GL_REPEAT, GL_LINEAR)
    skyTransform = tr.uniformScale(30)

    gpuSky2 = es.toGPUShape(bs.createTextureCube('skybox.png'), GL_REPEAT, GL_LINEAR)
    sky2Transform = tr.uniformScale(36)

    gpuSnake = mo.createSnakes(largo,posiciones_snake)
    snakeTransform = tr.identity()
    
    gpuCarrot = es.toGPUShape(shape = mo.readOBJ('carrot.obj', (234/256,190/256,63/256)))
    carrotTransform = tr.matmul([tr.translate(x_ap,y_ap,0),tr.rotationX(np.pi/2)])

    gpuGameOver = es.toGPUShape(bs.createTextureQuad("game_over.png",1,1), GL_REPEAT, GL_NEAREST)
    gameOverTransform = tr.scale(1, 0.5, 1)
    
    perder = False
    laps = 0

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Setting up the view transform
        if perder == False and cam_state == "HEAD" and state == "UP":
            view = tr.lookAt(viewPos,np.array([x,y+2,1]),np.array([0,0,1]))
        elif perder == False and cam_state == "HEAD" and state == "RIGHT":
            view = tr.lookAt(viewPos,np.array([x+2,y,1]),np.array([0,0,1]))
        elif perder == False and cam_state == "HEAD" and state == "LEFT":
            view = tr.lookAt(viewPos,np.array([x-2,y,1]),np.array([0,0,1]))
        elif perder == False and cam_state == "HEAD" and state == "DOWN":
            view = tr.lookAt(viewPos,np.array([x,y-2,1]),np.array([0,0,1]))
        elif perder == False and cam_state == "UP":
            view = tr.lookAt(np.array([0,-0.1,18]),np.array([0,0,1]),np.array([0,0,1]))
        elif perder == False and cam_state == "DIAGONAL":
            view = tr.lookAt(np.array([0,-15,17]),np.array([0,0,1]),np.array([0,0,1]))
        elif perder == True:
            view = tr.lookAt(np.array([10,10,5]),np.array([0,0,1]),np.array([0,0,1]))
            
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)   #Clearing the screen in both, color and depth

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glUseProgram(tpipeline.shaderProgram)
        #grass
        glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "model"), 1, GL_TRUE, grassTransform)
        glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        tpipeline.drawShape(gpuGrass)
        
        #wall
        glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "model"), 1, GL_TRUE, wallTransform)
        glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(gpuWall, tpipeline, "model")

        #sky
        if cam_state == "UP" or cam_state == "DIAGONAL":
            glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "model"), 1, GL_TRUE, sky2Transform)
            glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            tpipeline.drawShape(gpuSky2)
        else:
            glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "model"), 1, GL_TRUE, skyTransform)
            glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(tpipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            tpipeline.drawShape(gpuSky)

        if i > len(posiciones_snake):
            i = 1

        if x_ap-0.001 <= x <= x_ap+0.001 and y_ap-0.001 <= y <= y_ap+0.001:
            x_ap = random.randint(-9,9)
            y_ap = random.randint(-9,9)
            while [x_ap,y_ap,0.5] in posiciones_snake:
                x_ap = random.randint(-9,9)
                y_ap = random.randint(-9,9)
            carrotTransform = tr.matmul([tr.translate(x_ap,y_ap,0),tr.rotationX(np.pi/2)])
            largo += 1
            posiciones_snake.append(cola)
            gpuSnake = mo.createSnakes(largo,posiciones_snake)
            i = 1
            
        if perder == False:    
            snake = sg.findNode(gpuSnake, "snakes"+str(len(posiciones_snake)-i))
            sg.drawSceneGraphNode(gpuSnake, tpipeline, "model")
            
            glUseProgram(opipeline.shaderProgram)
            glUniform3f(glGetUniformLocation(opipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(opipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(opipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

            glUniform3f(glGetUniformLocation(opipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
            glUniform3f(glGetUniformLocation(opipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
            glUniform3f(glGetUniformLocation(opipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

            glUniform3f(glGetUniformLocation(opipeline.shaderProgram, "lightPosition"), -3, 0, 3)
            glUniform3f(glGetUniformLocation(opipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
            glUniform1ui(glGetUniformLocation(opipeline.shaderProgram, "shininess"), 100)
            glUniform1f(glGetUniformLocation(opipeline.shaderProgram, "constantAttenuation"), 0.001)
            glUniform1f(glGetUniformLocation(opipeline.shaderProgram, "linearAttenuation"), 0.1)
            glUniform1f(glGetUniformLocation(opipeline.shaderProgram, "quadraticAttenuation"), 0.01)

            glUniformMatrix4fv(glGetUniformLocation(opipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(opipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(opipeline.shaderProgram, "model"), 1, GL_TRUE, carrotTransform)

            opipeline.drawShape(gpuCarrot)

        glUseProgram(tpipeline.shaderProgram)
            
        laps += 1
        if laps%30 == 0:
            update()
            laps = 0

        t = glfw.get_time() 
        theta = 0.2 * np.cos(0.5 * t)       

        if x <= -10 or x >= 10 or y <= -10 or y >= 10 or posiciones_snake[0] in posiciones_snake[1:len(posiciones_snake)] or perder == True:
            glUseProgram(stpipeline.shaderProgram)
            perder = True
            gameOver = sg.SceneGraphNode("gameOver")
            gameOver.transform = tr.rotationZ(theta)
            gameOver.childs += [gpuGameOver]
            game_over = sg.findNode(gameOver, "gameOver")
            sg.drawSceneGraphNode(gameOver, stpipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
