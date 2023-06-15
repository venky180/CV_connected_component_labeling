from PIL import Image
import numpy as np
files = ["face.bmp","gun.bmp","test.bmp","face_old.bmp"]
# loop through each file in the files list
for file in files:
    # open the image file
    im = Image.open(file)
    # convert the image to a numpy array
    p = np.array(im)
    # create a new numpy array with the same shape as p and data type int
    a=np.zeros_like(p,dtype=int)
    # initialize variables
    L=0
    sets = []
    xy=0
    up = 0
    left = 0
    # loop through each row and column in p
    for i,x in enumerate(p):
        for j,y in enumerate(x):
            # if the pixel is True (i.e. white)
            if y == True:
                # determine the value of the pixel based on its neighbors
                if j != 0 and i==0:
                    up = 0
                    left = a[i,j-1]
                elif j == 0 and i!=0:
                    up = a[i-1,j]
                    left = 0
                elif j != 0 and i!=0:
                    up = a[i-1,j]
                    left = a[i,j-1]

                # if the pixel has the same value as its neighbors, set its value to the neighbor value
                if up == left and left !=0 and up !=0:
                    a[i,j] = up
                    xy=xy+1
                # if the pixel has a different value than its neighbors and only one of its neighbors is non-zero, set its value to the non-zero neighbor value
                elif left != up and (left*up == 0):
                    a[i,j] = max(left,up)
                # if the pixel has a different value than its neighbors and both of its neighbors are non-zero, set its value to the minimum neighbor value and merge the neighbor sets
                elif left != up and (left*up != 0):
                    a[i,j] = min(left,up)
                    newset = {left,up}
                    # check if the new set intersects with any existing sets and merge them if necessary
                    if len(sets) == 0:
                        sets.append(newset)
                    else:
                        for it,xx in enumerate(sets):
                            if newset & xx:
                                sets[it] = xx | newset
                                break
                            if it == len(sets)-1:
                                sets.append(newset)
                # if the pixel has no non-zero neighbors, assign it a new label value
                else:
                    L = L+1
                    a[i,j] = L
    # merge the last two sets if they intersect
    if sets[len(sets)-1] & sets[len(sets)-2] :
        sets[len(sets)-2] = sets[len(sets)-1] | sets[len(sets)-2]
        del sets[len(sets)-1]
    # assign label values to the pixels based on their set membership
    print(file," Components ",len(sets))
    for i,x in enumerate(a):
        for j,y in enumerate(x):
            if y !=0:
                for it,xx in enumerate(sets):
                    if y in xx:
                        a[i,j]= (it+1) * int(200/len(sets))
                        break
    # convert the numpy array back to an image and save it
    img = Image.fromarray(a.astype(np.uint8))
    filen = "result-"+file+".png"
    img.save(filen)