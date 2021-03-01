import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pointChargeEngine import *
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib import cm

import numpy as np

def plot_points(field_space):
    charge_data ={}
    for point_charge in field_space.charge_dict.keys():
        charge_data[point_charge] = field_space.charge_dict[point_charge].properties()

    charge_list =[]
    x_list =[]
    y_list =[]
    z_list =[]
    coordinate_list = [charge_list,x_list,y_list,z_list]
    for point_charge in charge_data:
        for axis in range(0,4):
            coordinate_list[axis].append(charge_data[point_charge][axis])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs=coordinate_list[1], ys=coordinate_list[2], zs=coordinate_list[3], zdir='z', s=200, c=coordinate_list[0],cmap='seismic', depthshade=True, alpha=1)
    plt.show()
    # pick point
#broken
def plot_electric_field(field_space):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    charge_data ={}
    for point_charge in field_space.charge_dict.keys():
        charge_data[point_charge] = field_space.charge_dict[point_charge].properties()
    x_field = np.array([])
    y_field = np.array([])
    z_field = np.array([])
    u_field = np.array([])
    v_field = np.array([])
    w_field = np.array([])
    electric_field_tensor = field_space.compute_electrical_field_array(magOnly=True)
    x= len(electric_field_tensor[0][0])
    for slab in range(x):  # get lowest slab
        for row in range(x):  # get current row in slab
            for point in range(x):
                x_field= np.append(x_field,electric_field_tensor[slab][row][point][1][0])
                y_field= np.append(y_field,electric_field_tensor[slab][row][point][1][1])
                z_field= np.append(z_field,electric_field_tensor[slab][row][point][1][2])
                u_field= np.append(u_field,electric_field_tensor[slab][row][point][0][0])



    '''dot_field = []
    for vectors in u_field:
        dot_field.append(np.dot(u_field[vectors], u_field[vectors]))
        print(dot_field)'''




    charge_list =[]
    x_list =[]
    y_list =[]
    z_list =[]
    coordinate_list = [charge_list,x_list,y_list,z_list]
    for point_charge in charge_data:
        for axis in range(0,4):
            coordinate_list[axis].append(charge_data[point_charge][axis])

    charges = ax.scatter(xs=coordinate_list[1], ys=coordinate_list[2], zs=coordinate_list[3], zdir='z', s=200, c=coordinate_list[0],cmap='seismic', depthshade=True, alpha=1)

    field = ax.scatter(xs=x_field, ys=y_field, zs=z_field, zdir='z', s=1 ,c=u_field, cmap='seismic', depthshade=True, alpha=0.25)
    plt.legend(*charges.legend_elements())
    plt.colorbar(field)

    plt.show()
    # pick point


#broken
def test_field(field_space):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make the grid
    x, y, z = np.meshgrid(np.arange(-0.8, 1, 0.2),
                          np.arange(-0.8, 1, 0.2),
                          np.arange(-0.8, 1, 0.8))

    # Make the direction data for the arrows
    u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
    v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
    w = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) *
         np.sin(np.pi * z))

    ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)

    plt.show()
