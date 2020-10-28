import file_op
import re
import math
import numpy as np



def tea_en(file_type,en_de_mode,input_file,output_file,rou,key,IV):
	#supporting file/binary/picture
	#supporting ECB/CBC/CTR
	blocks = file_op.file_read(file_type,input_file)

	#padding blocks
	temp = 8 - blocks.shape[0]%8
	for i in range(temp-1):
		blocks = np.append(blocks,0)
	blocks = np.append(blocks,temp)
	blocks = blocks.reshape(-1,8)

	for i in range(len(IV)):
		IV[i] = int(IV[i],16)
	IV = np.array(IV)
	print blocks
	for i in range(blocks.shape[0]):
		if(en_de_mode == "CBC"):
			blocks[i] = XOR(blocks[i],IV)
		elif(en_de_mode == "CTR"):
			temp = TEA_block_encode(IV,key,rou)
			blocks[i] = XOR(blocks[i],temp)
			#IV++
			continue

		blocks[i] = TEA_block_encode(blocks[i],key,rou)

		if(en_de_mode == "CBC"):
			IV = blocks[i]
	print blocks
	blocks = blocks.reshape(-1)
	file_op.file_write(input_file,file_type,output_file,blocks)
	
	

def tea_de(file_type,en_de_mode,input_file,output_file,rou,key,IV):
	blocks = file_op.file_read(file_type,input_file)
	blocks = blocks.reshape(-1,8)
	for i in range(len(IV)):
		IV[i] = int(IV[i],16)
	
	IV = np.array(IV)
	for i in range(blocks.shape[0]):
		if(en_de_mode == "CBC"):
			temp = np.array([])
			for j in range(len(blocks[i])):
				temp = np.append(temp,blocks[i][j])
		elif(en_de_mode == "CTR"):
			temp = TEA_block_encode(IV,key,rou)
			blocks[i] = XOR(blocks[i],temp)
			continue
			#IV++

		blocks[i] = TEA_block_decode(blocks[i],key,rou)

		if(en_de_mode == "CBC"):
			blocks[i] = XOR(blocks[i],IV)
			IV = temp

	blocks = blocks.reshape(-1)
	temp = blocks[blocks.shape[0]-1]
	for i in range(temp):
		blocks = np.delete(blocks,blocks.shape[0]-1)
	file_op.file_write(input_file,file_type,output_file,blocks)



def TEA_block_encode(block ,key,rou):

	k0 = int(key[0],16)
	k1 = int(key[1],16)
	k2 = int(key[2],16)
	k3 = int(key[3],16)
	block = block.reshape(-1,4)
	L = int(npencode(block[0]),2)
	R = int(npencode(block[1]),2)

	delta = 0x9e3779b9
	summ = 0
	
	for i in range(int(rou)):
		summ += delta
		L += ((R<<4)+k0)^(R+summ)^((R>>5)+k1)
		L &= 0xffffffff
		R += ((L<<4)+k2)^(L+summ)^((L>>5)+k3)
		R &= 0xffffffff

	L = bin(L).replace('0b','')
	R = bin(R).replace('0b','')
	for i in range(32-len(L)):
		L = '0'+L
	for i in range(32-len(R)):
		R = '0'+R

	L = re.findall(r'.{8}',L)
	R = re.findall(r'.{8}',R)

	for i in range(4):
		block[0][i] = int(L[i],2)
		block[1][i] = int(R[i],2)
	block = block.reshape(-1)
	return block
	

def TEA_block_decode(block ,key,rou):
	k0 = int(key[0],16)
	k1 = int(key[1],16)
	k2 = int(key[2],16)
	k3 = int(key[3],16)


	
	block = block.reshape(-1,4)
	L = int(npencode(block[0]),2)
	R = int(npencode(block[1]),2)

	delta = 0x9e3779b9
	log_rou = int(math.log(int(rou),2))
	summ = delta<<log_rou
	
	for i in range(int(rou)):
		R -= ((L<<4)+k2)^(L+summ)^((L>>5)+k3)
		R &= 0xffffffff
		L -= ((R<<4)+k0)^(R+summ)^((R>>5)+k1)
		L &= 0xffffffff
		summ -= delta
		
	L = bin(L).replace('0b','')
	R = bin(R).replace('0b','')
	for i in range(32-len(L)):
		L = '0'+L
	for i in range(32-len(R)):
		R = '0'+R

	L = re.findall(r'.{8}',L)
	R = re.findall(r'.{8}',R)

	for i in range(4):
		block[0][i] = int(L[i],2)
		block[1][i] = int(R[i],2)
	block = block.reshape(-1)
	return block
	
def npencode(s):
	result = ""
	for c in s:
		temp = bin(c).replace('0b', '') 
		for i in range (8-len(temp)):
			temp = '0'+temp
		result += temp
	return result

def XOR(a,b):
	for i in range(len(a)):
		a[i] = int(a[i])^int(b[i])
	return a
