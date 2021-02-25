import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pointChargeEngine import *


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
        print(point_charge)
        for axis in range(0,4):
            coordinate_list[axis].append(charge_data[point_charge][axis])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs=coordinate_list[1], ys=coordinate_list[2], zs=coordinate_list[3], zdir='z', s=200, c=coordinate_list[0],cmap='seismic', depthshade=True, alpha=1)
    plt.show()
    # pick point