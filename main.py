from pointChargeEngine import *
'''
Created by Maximo Xavier DeLeon
2/24/2021
'''

# create point charges
q1 = PointCharge(1e-9,[0.03,0.01,0.00],0)
q2 = PointCharge(-10e-9,[0.03,0.00,0.00],0)
q3 = PointCharge(10e-9,[0.00,0.00,0.00],0)

point_charge_list = [q1,q2,q3]

# create space object
field_space = Space()
# Iterate through list of charges and add them to field space object
for i in range(len(point_charge_list)):
    charge_name = 'q' + str(i + 1)
    field_space.add_charge(point_charge_list[i],charge_name)

# calculate the net force acting on the charge named q2
print(field_space.summate_forces('q2',components=False),'N')






