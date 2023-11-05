import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

pygame.init()
display = (1280, 720)
game_display = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glClearColor(0, 0, 0, 1)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, 1280, 720, 0, 0, 1)
glMatrixMode(GL_MODELVIEW)

# Colors
red = (1.0, 0.0, 0.0)
green = (0.0, 1.0, 0.0)


class GridDrawer:
    def __init__(self, grid_spacing, grid_size, grid_color, display_width, display_height):
        self.grid_spacing = grid_spacing
        self.grid_size = grid_size
        self.grid_color = grid_color
        self.display_width = display_width
        self.display_height = display_height

    def draw(self):
        glBegin(GL_LINES)
        glColor3f(*self.grid_color)
        spacing = self.grid_spacing
        size = self.grid_size
        width = self.display_width
        height = self.display_height

        # for i in range(-size, size + 1):
        #     glVertex3f(i * spacing, size * spacing, 0.0)
        #     glVertex3f(i * spacing, -size * spacing, 0.0)

        #     glVertex3f(size * spacing, i * spacing, 0.0)
        #     glVertex3f(-size * spacing, i * spacing, 0.0)
        # glEnd()

        for i in range(-size, size + 1):
            glVertex3f(i * spacing + width / 2, size * spacing + height / 2, 0.0)
            glVertex3f(i * spacing + width / 2, -size * spacing + height / 2, 0.0)

            glVertex3f(size * spacing + width / 2, i * spacing + height / 2, 0.0)
            glVertex3f(-size * spacing + width / 2, i * spacing + height / 2, 0.0)
        glEnd()


class Rectangle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.clicked = False

    def check_click(self, mouse_position):
        if (
            self.x <= mouse_position[0] <= self.x + self.width
            and self.y <= mouse_position[1] <= self.y + self.height
        ):
            self.clicked = not self.clicked

    def update_position(self, mouse_position):
        if self.clicked:
            self.x = mouse_position[0] - self.width / 2
            self.y = mouse_position[1] - self.height / 2

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(*self.color)

        #  Super wonky lmao TODO
        #  Also, add some kind of AA for the jagged edges (?) TODO
        if self.clicked:
            glVertex2f(self.x - self.y / 4, self.y)
            glVertex2f(self.x + self.width - self.y / 4, self.y)
            glVertex2f(self.x + self.width, self.y + self.height)
            glVertex2f(self.x, self.y + self.height)

        else:
            glVertex2f(self.x, self.y)
            glVertex2f(self.x + self.width, self.y)
            glVertex2f(self.x + self.width, self.y + self.height)
            glVertex2f(self.x, self.y + self.height)
        glEnd()


rectangle1 = Rectangle(50, 50, 100, 150, red)
rectangle2 = Rectangle(200, 200, 100, 150, green)

grid_drawer = GridDrawer(50, 10, (0.3, 0.3, 0.3), 1280, 720)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            rectangle1.check_click(mouse_position)
            rectangle2.check_click(mouse_position)

    mouse_position = pygame.mouse.get_pos()
    rectangle1.update_position(mouse_position)
    rectangle2.update_position(mouse_position)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    grid_drawer.draw()
    rectangle1.draw()
    rectangle2.draw()
    pygame.display.flip()
    pygame.time.wait(10)
