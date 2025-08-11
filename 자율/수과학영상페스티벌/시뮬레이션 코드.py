import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from openpyxl import Workbook
import numpy as np

# -------- Perlin 관련 함수 --------

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def random_gradient():
    theta = random.uniform(0, 2 * math.pi)
    return [math.cos(theta), math.sin(theta)]

def dot_grid_gradient(ix, iy, x, y, gradients):
    dx = x - ix
    dy = y - iy
    gradient = gradients[iy][ix]
    return dx * gradient[0] + dy * gradient[1]

def perlin(x, y, gradients):
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1

    sx = fade(x - x0)
    sy = fade(y - y0)

    n00 = dot_grid_gradient(x0, y0, x, y, gradients)
    n10 = dot_grid_gradient(x1, y0, x, y, gradients)
    n01 = dot_grid_gradient(x0, y1, x, y, gradients)
    n11 = dot_grid_gradient(x1, y1, x, y, gradients)

    ix0 = (1 - sx) * n00 + sx * n10
    ix1 = (1 - sx) * n01 + sx * n11
    value = (1 - sy) * ix0 + sy * ix1

    return value

# -------- 지형 생성 --------

width, height = 100, 100
scale = 10.0
gradients = [[random_gradient() for _ in range(width + 1)] for _ in range(height + 1)]

values = [[0 for _ in range(width)] for _ in range(height)]

for y in range(height):
    for x in range(width):
        nx = x / scale
        ny = y / scale
        raw = perlin(nx, ny, gradients)
        normalized = (raw + 1) / 2
        height_value = 64 + normalized * 20
        stepped = round(height_value)
        values[y][x] = stepped

# -------- 2D 시각화 --------

plt.imshow(values, cmap='terrain')
plt.title("2D Perlin Terrain")
plt.colorbar(label='Block Height')
plt.show()

# -------- 3D 시각화 --------

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X = range(width)
Y = range(height)
X, Y = np.meshgrid(X, Y)
Z = np.array(values)  # 리스트 → 넘파이 배열로 변환

ax.plot_surface(X, Y, Z, cmap='terrain', edgecolor='none')

ax.set_title("3D Minecraft-style Terrain")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Height')
plt.show()

# -------- 엑셀 저장 --------

wb = Workbook()
ws = wb.active
ws.title = "PerlinTerrain"

for row in values:
    ws.append(row)

wb.save("minecraft_terrain.xlsx")

# -------- 마인크래프트 맵 텍스트 저장 --------

with open("minecraft_terrain_map.txt", "w") as f:
    for y in range(height):
        for x in range(width):
            f.write(f"{x},{y},{values[y][x]}\n")  # x,y,height
