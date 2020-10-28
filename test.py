import file_op
import numpy as np

block = file_op.readPic("./alice.jpg")
block = block.reshape(-1)
print block
print block.shape
temp = block[block.shape[0]-1]
for  i in range(temp):
	block = np.delete(block,block.shape[0]-1)
	
print block
print block.shape
