import math
import numpy as np

# Define Constants

# Electrostatic Constant
ELECTROSTATIC_CONSTANT = 8.89e9
# Permittivity Constant
PERMITTIVITY_CONSTANT = 8.85e-12
# Fundamental Charge
FUNDAMENTAL_CHARGE = 1.6e-19


class PointCharge():
    def __init__(self, charge, position, mass=0):
        self.charge = charge
        self.position = position  # 3x1 position vector
        self.mass = mass

    def distance_from_origin(self):
        distance = math.sqrt(self.position[0] ** 2 + self.position[1] ** 2 + self.position[2] ** 2)
        return distance

    def properties(self):
        return [self.charge, self.position[0], self.position[1], self.position[2], self.mass]
    def info(self):
        print('Charge:',self.charge,'C')
        print('Mass:',self.mass,'kg')
        print('x-position:',self.position[0],'m')
        print('y-position:',self.position[1],'m')
        print('z-position:',self.position[2],'m')
        print('Distance from origin:', self.distance_from_origin(),'m')



class Space(object):
    def __init__(self, granularity=0.001):
        self.charge_dict = {}

    def add_charge(self, charge_properties, name='CHARGE'):
        if name not in self.charge_dict.keys():
            # Add statement to ensure no two particles have the same position
            self.charge_dict[name] = charge_properties
        else:
            print('Charge with', name, 'already exists. Please give the charge a unique name!')

    def remove_charge(self, name):
        if name in self.charge_dict.keys():
            del self.charge_dict[name]
        else:
            print(name, 'does not exist in the current space')

    def clear_charges(self, ):
        print('Removing:', end=' ')
        for key in self.charge_dict.keys():
            print(key, ', ', end='')
        print('\n .....')
        self.charge_dict = {}
        print('Cleared all charges')

    def compute_electric_field_strength(self, charge_name, point,components=False):
        global PERMITTIVITY_CONSTANT
        if charge_name in self.charge_dict.keys():
            charge_properties = self.charge_dict[charge_name]  # get charge properties from dictionary
            r = math.sqrt((charge_properties[1] - point[0]) ** 2 + (charge_properties[2] - point[1]) ** 2 + (charge_properties[3] - point[2]) ** 2)  # calculate position vector difference in R3
            E = (1 / (4 * math.pi * PERMITTIVITY_CONSTANT)) * self.charge_dict[charge_name][0] / r ** 2
            if not components:
                return [E] + point
            elif components:
                theta_x = math.acos((charge_properties[1] - charge_properties[1]) / r)  # angle position vector makes with the x-axis
                theta_y = math.acos((charge_properties[2] - charge_properties[2]) / r)  # angle position vector makes with the y-axis
                theta_z = math.acos((charge_properties[3] - charge_properties[3]) / r)  # angle position vector makes with the z-axis
                return [E*math.cos(theta_x),E*math.cos(theta_y),E*math.cos(theta_z)] + point
        else:
            print(charge_name, 'does not exist in the current space')

    def compute_electric_force(self,charge_1_name, charge_2_name,components=False):  # method could be imporoved by using numpy and returning components
        global ELECTROSTATIC_CONSTANT
        if charge_1_name in self.charge_dict.keys() and charge_2_name in self.charge_dict.keys():

            charge_1_object = self.charge_dict[charge_1_name] # get charge 1 properties from dictionary
            charge_2_object = self.charge_dict[charge_2_name]  # get charge 2 properties from dictionary

            charge_1_properties = charge_1_object.properties()  # get charge 1 properties from dictionary
            charge_2_properties = charge_2_object.properties()  # get charge 2 properties from dictionary


            r = math.sqrt((charge_1_properties[1] - charge_2_properties[1])**2 + (charge_1_properties[2] - charge_2_properties[2])**2 + (charge_1_properties[3] - charge_2_properties[3])**2)  # calculate position vector difference in R3

            charge_1 = charge_1_properties[0]
            charge_2 = charge_2_properties[0]

            position_1 = [charge_1_properties[1], charge_1_properties[2],charge_1_properties[3]]  # charge 1 position in xyz
            position_2 = [charge_2_properties[1], charge_2_properties[2],charge_2_properties[3]]  # charge 2 position in xyz
            force = (ELECTROSTATIC_CONSTANT * abs(charge_1) * abs(charge_2)) / (r ** 2)  # calculate the electrostatic force between the two user defined charges

            if not components:
                return force  # return the force value

            elif components:
                theta_x = math.acos((charge_1_properties[1] - charge_2_properties[1]) / r)  # angle position vector makes with the x-axis
                theta_y = math.acos((charge_1_properties[2] - charge_2_properties[2]) / r)  # angle position vector makes with the y-axis
                theta_z = math.acos((charge_1_properties[3] - charge_2_properties[3]) / r)  # angle position vector makes with the z-axis

                x_force = force * math.cos(theta_x)
                y_force = force * math.cos(theta_y)
                z_force = force * math.cos(theta_z)
                return [x_force, y_force, z_force]

        else:
            print('Either one or both of the specified charges does not exist in the current space')


    def summate_forces(self, target_charge, components=False):
        target_charge =target_charge
        if target_charge in self.charge_dict.keys():
            sum_dict = self.charge_dict
            target_charge_properties = self.charge_dict[target_charge].properties()

            #charge_array = np.zeros((len(sum_dict)-1, 4))
            i = 0
            summed_components = [0, 0, 0]
            for point_charge in sum_dict.keys():
                if point_charge == target_charge:
                    pass
                else:
                    point_charge_on_target_force = self.compute_electric_force(target_charge, point_charge, components=True)
                    point_charge_properties = sum_dict[point_charge].properties()

                    #charge_array[i] = [target_charge_properties[0], point_charge_properties] + point_charge_on_target_force  # store components of interacting forces along side charges of both charges for the current iteration

                    target_charge_sign = 1 if target_charge_properties[0] > 0 else -1
                    point_charge_sign = 1 if point_charge_properties[0] > 0 else -1
                    repel = True if target_charge_sign == point_charge_sign else False

                    for axis in list(range(1,4)):
                        if target_charge_properties[axis] > point_charge_properties[axis] and repel: # same sign and target charge has a greater value on the axis than other point
                            summed_components[axis-1] += point_charge_on_target_force[axis-1]

                        elif target_charge_properties[axis] < point_charge_properties[axis] and repel: # same sign and target charge has a lesser value on the axis than other point
                            summed_components[axis - 1] -= point_charge_on_target_force[axis - 1]

                        elif target_charge_properties[axis] > point_charge_properties[axis] and not repel: # opposite sign and target charge has a greater value on the axis than other point
                            summed_components[axis - 1] -= point_charge_on_target_force[axis - 1]

                        elif target_charge_properties[axis] < point_charge_properties[axis] and not repel: # opposite sign and target charge has a lesser value on the axis than other point
                            summed_components[axis - 1] += point_charge_on_target_force[axis - 1]
                        axis += 1

                    i = 0


            if not components:
                return math.sqrt(summed_components[0]**2 + summed_components[1]**2 +summed_components[2]**2)
            elif components:
                return summed_components

