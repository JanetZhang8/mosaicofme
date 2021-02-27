#COMMENT: graph super wrong lol. here i'm testing closest match to see if that was the problem, but I dont think so. Probably the way I calculate profile picture brightness

import numpy as np

#helper function to find the closest match in a list to a number
#returns index of list
def closest_match(list, target):
    curr = list[0][0]
    ans = 0
    for i in range (len(list)):
        if abs(target - list[i][0]) < abs(target - curr):
            curr = list[i][0]
            ans = i
    return ans
"""
allimg = [[3.1, 3.2, 8.2],
        [4.1, 2.0, 2.1],
        [1.0, 1.1, 5.1]]"""

allimg = [(1.1, 'jpg'), (2.1, 'jpg'),(3.1, 'jpg'), (4.1, 'jpg')]
profile_brightness = [[2.1, 6.2, 3.2],
                     [7.1, 3.0, 3.1],
                     [2.0, 4.1, 1.1]]

#create a placement_ref array whos values are the allimg index that best matches the profile image brightness at each coordinate
placement_ref = np.zeros((3,3))
for i in range(3):
    for j in range(3):
        placement_ref[i][j] = closest_match(allimg, profile_brightness[i][j])
placement_ref = placement_ref.astype(int)

print(placement_ref)


"""
0 - 1
1 - 2
2 - 3
3 - 5
4 - 7




"""
