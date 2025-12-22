# TelemetryBroker for Inter Process Communication for Robtics
# Client for Receiver Nodes
# Developed by Martin Novak at 2025/26
# pip install openpyxl
from libs.lib_telemtrybroker import TelemetryBroker

import openpyxl
import pygame
import sys
import time
import io
import base64
import math

class Map:
    def __init__(self, filename="map.xlsx"):
        self.__wb = openpyxl.load_workbook(filename, data_only=True)
        self.__sheet = self.__wb.active
                        
    def __is_wall(self, value):
        return value == "thick"
    
    def __convert_xls_to_index(self, value):
        x = ord(value[0]) - ord('A')
        y = int(value[1])-1
        return [x, y]

    def __convert_index_to_xls(self, coords):
        return chr(coords[0] + ord('A')) + str(coords[1] + 1)

    def __color_hex_to_dec(self, value):
        if value is None:
            return None
        return (int(value[2:4], 16), int(value[4:6], 16), int(value[6:8], 16))


    def __validate_color(self, color_obj):
        try:
            if color_obj.type == 'rgb':
                if color_obj.rgb == "00000000":
                    return "FFFFFFFF"
                return color_obj.rgb
            elif color_obj.type == 'indexed':
                try:
                    return COLOR_INDEX[color_obj.indexed]
                except (IndexError, TypeError):
                    pass
            elif color_obj.type == 'theme':
                return color_obj.theme
            elif color_obj.auto:
                return "FF000000"
        except:
            return "FFFFFFFF"

    def get_dimension(self):
        val=""
        for x in range(20):
            for y in range(20):
                val = self.get_tile_info([x,y])["value"]
                if val is None:
                    continue
                if val.lower() == "x":
                    return [x,y]

    def get_tile_info(self, coords):
        cell = self.__sheet[self.__convert_index_to_xls(coords)]

        value = cell.value
        color = self.__color_hex_to_dec(self.__validate_color(cell.fill.start_color.index))

        border_nord = self.__is_wall(cell.border.top.style)
        border_ost = self.__is_wall(cell.border.right.style)
        border_sud = self.__is_wall(cell.border.bottom.style)
        border_west = self.__is_wall(cell.border.left.style)

        border_nord_color = self.__color_hex_to_dec(self.__validate_color(cell.border.top.color))
        border_ost_color = self.__color_hex_to_dec(self.__validate_color(cell.border.right.color))
        border_sud_color = self.__color_hex_to_dec(self.__validate_color(cell.border.bottom.color))
        border_west_color = self.__color_hex_to_dec(self.__validate_color(cell.border.left.color))

        return {
            "coords": coords,
            "value": value,
            "color": color,
            "walls": {
                "ost": {"exists": border_ost, "color": border_ost_color},
                "west": {"exists": border_west, "color": border_west_color},
                "nord": {"exists": border_nord, "color": border_nord_color},
                "sud": {"exists": border_sud, "color": border_sud_color},
            }
        }
    


class Tile:
    def draw(self, info, maze_surface, TILE_SIZE=60):
        x = info["coords"][0]
        y = info["coords"][1]

        #print(info)

        tile_rect = pygame.Rect(TILE_SIZE*x+2, TILE_SIZE*y+2, TILE_SIZE-4, TILE_SIZE-4)
        pygame.draw.rect(maze_surface, info["color"], tile_rect)
       

        if info["walls"]["west"]["exists"]:
            wall_west_rect = pygame.Rect(TILE_SIZE*x-2, TILE_SIZE*y-2, 4, TILE_SIZE+4)
            pygame.draw.rect(maze_surface, info["walls"]["west"]["color"], wall_west_rect)
        if info["walls"]["ost"]["exists"]:
            wall_ost_rect = pygame.Rect(TILE_SIZE*x-2+TILE_SIZE, TILE_SIZE*y-2, 4, TILE_SIZE+4)
            pygame.draw.rect(maze_surface, info["walls"]["ost"]["color"], wall_ost_rect)
        if info["walls"]["nord"]["exists"]:
            wall_nord_rect = pygame.Rect(TILE_SIZE*x-2, TILE_SIZE*y-2, TILE_SIZE+4, 4)
            pygame.draw.rect(maze_surface, info["walls"]["nord"]["color"], wall_nord_rect)
        if info["walls"]["sud"]["exists"]:
            wall_sud_rect = pygame.Rect(TILE_SIZE*x-2, TILE_SIZE*y-2+TILE_SIZE, TILE_SIZE+4, 4)
            pygame.draw.rect(maze_surface, info["walls"]["sud"]["color"], wall_sud_rect)


        return maze_surface

class Robot:
    def __init__(self, x, y, tilesize, surface):
        robot1_base64 = "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"
        #raw_image = pygame.image.load(imagepath).convert_alpha()
        raw_image = pygame.image.load(io.BytesIO(base64.b64decode(robot1_base64)))
        #image = raw_image
        image = pygame.transform.scale(raw_image, (tilesize/2, tilesize/2))
        self.x = x
        self.y = y
        self.original_image = image.copy()  # Das Originalbild (zeigt z.B. nach oben)
        self.image = image.copy()           # Das aktuelle Bild (wird gedreht)
        self.direction = 0               # Aktuelle Blickrichtung
        self.tilesize = tilesize
        self.layer_robot=pygame.Surface(surface.get_size())
        self.layer_robot.set_colorkey((255, 255, 255))
        self.surface = surface
        self.rect_robot = self.image.get_rect()
        self.rect_robot.center = (self.x + self.tilesize / 2, self.y + self.tilesize / 2)

    def get_sensor_rotation(self):
        return self.direction

    def move(self, linear_x, angular_z):
        if linear_x != 0 and angular_z == 0:
            # linear
            a=1*math.sin(math.radians(self.direction))
            b=1*math.cos(math.radians(self.direction))
            x=self.rect_robot.center[0]+a
            y=self.rect_robot.center[1]-b

            self.x = x
            self.y = y

            self.layer_robot.fill((255,255,255))
            self.rect_robot = self.image.get_rect()
            self.rect_robot.center = (self.x, self.y)
            self.layer_robot.blit(self.image,self.rect_robot)

        elif linear_x == 0 and angular_z != 0:
            # angular
            if angular_z > 0:
                self.direction += 1
            else:
                self.direction -= 1
            self.image = pygame.transform.rotate(self.original_image, self.direction)

            self.layer_robot.fill((255,255,255))
            self.rect_robot = self.image.get_rect()
            px = self.x + self.tilesize / 2
            py = self.y + self.tilesize / 2
            self.rect_robot.center = (px, py)
            self.layer_robot.blit(self.image,self.rect_robot)
        else:
            self.layer_robot.fill((255,255,255))
            self.rect_robot = self.image.get_rect()
            self.rect_robot.center = (self.x + self.tilesize / 2, self.y + self.tilesize / 2)
            self.layer_robot.blit(self.image,self.rect_robot)
        return self.layer_robot

                
class Gametable():
    def __init__(self, WIDTH, HEIGHT):
        self.maze_surface = pygame.Surface((WIDTH, HEIGHT))
    
    def draw(self, maze_surface=None):
        WHITE = (255, 255, 255)

        self.maze_surface.set_colorkey(WHITE)
        self.maze_surface.fill(WHITE)

        tile = Tile()

        for x in range(wx):
            for y in range(wy):
                tile.draw(mymap.get_tile_info([x, y]), self.maze_surface, TILE_SIZE)

        return self.maze_surface


mb = TelemetryBroker()

vel_dict = {"vel_linear_x":0, "vel_angular_z":0}
sensor_dict = {"sensor_rotation":0}

# READ DATA FROM EXCEL MAP
mymap = Map()

# GENERATE MAZE
TILE_SIZE = 90
wx, wy = mymap.get_dimension()
WIDTH = wx * TILE_SIZE
HEIGHT = wy * TILE_SIZE
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
#screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Node for simulation maze")

# LOAD GAMETABLE
mygametable = Gametable(WIDTH, HEIGHT)
maze_surface = mygametable.draw()

# LOAD ROBOT
myrobot = Robot(0, 0, TILE_SIZE, maze_surface)

# RUNNING ENGINE
linear_x=0
angular_z=100
running = True
while running:

    # STOP ENGINE WITH ESCAPE KEY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # GET VELOCITY DATA
    vel_dict = mb.getmulti(vel_dict.keys())

    # DRAW GAMETABLE NAD ROBOT
    screen.fill(WHITE)
    screen.blit(maze_surface, (0, 0))
    robot_surface = myrobot.move(vel_dict["vel_linear_x"], vel_dict["vel_angular_z"])
    sensor_dict["sensor_rotation"] = myrobot.get_sensor_rotation()
    mb.setmulti(sensor_dict)
    screen.blit(robot_surface, (0, 0))
    pygame.display.flip()

    time.sleep(0.1)
pygame.quit()
sys.exit()