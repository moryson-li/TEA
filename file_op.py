from PIL import Image
import numpy as np
import re
import struct


def file_read(file_type,input_file):
	if(file_type == "pic"):
		return readPic(input_file)
	elif(file_type == "bin"):
		return readBin(input_file)


def file_write(input_file,file_type,output_file,blocks):
	if(file_type == "pic"):
		return writePic(input_file,output_file,blocks)
	elif(file_type == "bin"):
		return writeBin(output_file,blocks)

#write blocks into picture
def writePic(input_f,filename,blocks):		
	p = Image.open(input_f).convert('L')
	leng,wid = p.size
	p.close()
	my_p = Image.new("L",(leng,wid))
	
	for x in range(leng):
		for y in range(wid):
			my_p.putpixel((x,y),blocks[y*leng+x])
	
	my_p.save(filename)


#write blocks into binary file
def writeBin(filename,blocks):
	out = file(filename,"wb")
	for i in blocks:
		temp = struct.pack('B',i)
		out.write(temp)


#read picture as block
def readPic(filename):
	#picture convert
	p = Image.open(filename).convert('L')
	leng,wid = p.size
	temp = 8 - (leng*wid)%8
	blocks = np.array(p).reshape(-1)
	p.close()

	return blocks

#read binary file as block
def readBin(input_file):
	f = open(input_file,'rb')
	data = f.read()
	f.close()
	blocks = np.array([])
	blocks.dtype = int
	for i in data:
		blocks = np.append(blocks,ord(i))

	return blocks


