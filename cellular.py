import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import numpy as np
import random
import sys
from OpenGL.arrays import vbo
from PIL import Image
from PIL import ImageOps
from datetime import datetime

# Global vars
controller = None
res = 650
n = 1
r_nth = 0
g_nth = 0
b_nth = 0
r = 1
g = 1
b = 1
mode = "u"
isolines = 0
metric = ""
metric_list = ["manhattan",
               "canberra",
               "chebyshev",
               "euclidean",
               "third_power",
               "forth_power",
               "half_power",
               "negative_power",
               "knights",
               "iron_cross",
               "octagon",
               "mod_euclidean",
               "mod_octagon",
               "mod_manhattan"]

class Controller():
    def __init__(self, w, h, vertex_shader, fragment_shader):
        self.width = w
        self.height = h
        self.shader = None
        self._init(vertex_shader, fragment_shader)
        nodes = []
        for i in range(n):
            nodes.append((random.uniform(0,1), random.uniform(0,1)))
        self.nodes = np.asarray(nodes, dtype=np.float32)
        
    def _init(self, vertex_shader, fragment_shader):
        global shader

        # shader setup
        shader = gl.shaders.compileProgram(
            shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
            shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER),
        )
        gl.glLinkProgram(shader)

    def draw(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode (gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        
        global shader

        self.vbo = vbo.VBO(
            np.array([
                [1, 1, 0, 1],
                [1, -1, 0, 1],
                [-1, -1, 0, 1],
                [1, 1, 0, 1],
                [-1, 1, 0, 1],
                [-1, -1, 0, 1],
            ], dtype=np.float32)
        )

        
        
        shaders.glUseProgram(shader)
        try:
            self.vbo.bind()
            try:
                isolines_offset = gl.glGetUniformLocation(shader, b'isolines')
                gl.glUniform1i(isolines_offset, isolines)
                r_offset = gl.glGetUniformLocation(shader, b'r')
                gl.glUniform1i(r_offset, r)
                g_offset = gl.glGetUniformLocation(shader, b'g')
                gl.glUniform1i(g_offset, g)
                b_offset = gl.glGetUniformLocation(shader, b'b')
                gl.glUniform1i(b_offset, b)
                r_nth_offset = gl.glGetUniformLocation(shader, b'r_nth')
                gl.glUniform1i(r_nth_offset, r_nth)
                g_nth_offset = gl.glGetUniformLocation(shader, b'g_nth')
                gl.glUniform1i(g_nth_offset, g_nth)
                b_nth_offset = gl.glGetUniformLocation(shader, b'b_nth')
                gl.glUniform1i(b_nth_offset, b_nth)
                res_offset = gl.glGetUniformLocation(shader, b'res')
                gl.glUniform1f(res_offset, res)
                nodes_offset = gl.glGetUniformLocation(shader, b'node')
                gl.glUniform2fv(nodes_offset, n, self.nodes)
                gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
                gl.glVertexPointerf(self.vbo)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
            finally:
                self.vbo.unbind()
                gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        finally:
            shaders.glUseProgram(0)
            
        gl.glFlush()

def parse_arg():
    if len(sys.argv) == 2 and sys.argv[1] in ["list", "-h", "help"]:
        print("Possible distance metrics:")
        for m in metric_list:
            print(m)
        exit()
    elif len(sys.argv) > 3 or len(sys.argv) <= 2:
        print("Error: Invalid number of arguments.")
        print("Syntax: python {} <# of nodes > [list | help | -h | <distance metric>]".format(sys.argv[0]))
        exit()
    else:
        try:
            global n
            n = int(sys.argv[1])
        except ValueError:
            print("Error: First arg must be an integer.")
            exit()
        arg = sys.argv[2]
        if arg not in metric_list:
            print("Error: Invalid distance metric specified.")
            exit()
        else:
            return arg
        
def idle_cb():
    global controller
    glut.glutPostRedisplay()


def display_cb():
    global controller
    controller.draw()

def keyboard_cb(key, x, y):
    global nth
    global r
    global g
    global b
    global r_nth
    global g_nth
    global b_nth
    global isolines
    global mode
    global metric
    #^C or q to quit
    if key == b'\x03' or key == b'q':
        exit()
    #Change which point to use in current channel mode
    if key == b'1':
        if mode == "u":
            r_nth = 0
            g_nth = 0
            b_nth = 0
        if mode == "r":
            r_nth = 0
        if mode == "g":
            g_nth = 0
        if mode == "b":
            b_nth = 0
    if key == b'2':
        if mode == "u":
            r_nth = 1
            g_nth = 1
            b_nth = 1
        if mode == "r":
            r_nth = 1
        if mode == "g":
            g_nth = 1
        if mode == "b":
            b_nth = 1
    if key == b'3':
        if mode == "u":
            r_nth = 2
            g_nth = 2
            b_nth = 2
        if mode == "r":
            r_nth = 2
        if mode == "g":
            g_nth = 2
        if mode == "b":
            b_nth = 2
    #Change brightness of current channel mode
    if key == b'>':
        if mode == "u":
            r += 1
            g += 1
            b += 1
        if mode == "r":
            r += 1
        if mode == "g":
            g += 1
        if mode == "b":
            b += 1
    if key == b'<':
        if mode == "u":
            r = r - 1 if r - 1 >= 0 else 0
            g = g - 1 if g - 1 >= 0 else 0
            b = b - 1 if b - 1 >= 0 else 0
        if mode == "r":
            r = r - 1 if r - 1 >= 0 else 0
        if mode == "g":
            g = g - 1 if g - 1 >= 0 else 0
        if mode == "b":
            b = b - 1 if b - 1 >= 0 else 0
    #Change color channel mode
    if key == b'r':
        mode = "r"
    if key == b'g':
        mode = "g"
    if key == b'b':
        mode = "b"
    if key == b'u':
        mode = "u"
    #Reset colours
    if key == b'w':
        mode = "u"
        r = 1
        g = 1
        b = 1
        r_nth = 0
        g_nth = 0
        b_nth = 0
    #Toggle isolines
    if key == b'i':
      if isolines == 0:
          isolines = 1
      else:
          isolines = 0
    #Save to png
    if key == b's':
        now = datetime. now()
        time = now.strftime("%H-%M-%S")
        print("Saving image as {}--{}.png".format(metric, time))
        gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
        data = gl.glReadPixels(0, 0, res, res, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (res, res), data)
        image.save("{}--{}.png".format(metric, time), "PNG")

if __name__ == "__main__":
    # Shaders
    metric = parse_arg()
    vertex_shader = open("vertex.c", "r").read()
    fragment_shader = open("fragment.c", "r").read().replace("?", str(n))
    fragment_shader = fragment_shader.replace("METRIC_FUNC", metric)
    # Initialize GLUT library
    glut.glutInit()

    glut.glutInitWindowSize(res, res)
    glut.glutInitWindowPosition(0, 0)
    glut.glutInitDisplayMode(glut.GLUT_SINGLE | glut.GLUT_RGB)
    glut.glutCreateWindow("Cellular Noise")
    
    glut.glutIdleFunc(idle_cb)
    glut.glutDisplayFunc(display_cb)
    glut.glutKeyboardFunc(keyboard_cb)

    controller = Controller(res, res, vertex_shader, fragment_shader)

    glut.glutMainLoop()
