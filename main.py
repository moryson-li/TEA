from getopt import getopt
import sys
import tea
import math
import re



def print_help():
	msg = """
	-h,--help	print help menu

	-e,--encrypt	specifies encryption mode

	-d,--decrypt	specifies decryption mode

	-t,--type	specifies en/decrypt file type ,supporting Picture and Bianary file 
			using parameter pic,bin,file to sign out file type
			default file type is binary file

	-m,--mode	specifies en/decrypt mode ,support ECB,CBC and CTR ,but now it's just supporting ECB mode
			using parameter ECB CBC and CTR to sign en/decrypt mode
			default type is ECB

	-i,--input	necessary parameter, to specifies input file path

	-o,--output	necessary paremeter, to specifies output file path

 	-r,--round	specifies en/decrypt rounds,and rounds should be the power of 2
			default rounds is 32

	-k,--key	specifies en/decrypt key, and key should be hex string length of 32
			default key is 3ADA7521DBE2DBB311B44901A5C6EAD4

	-I,--IV		specifies init vector, and vector should be hex string length of 16
			default IV is 1234567812345678
"""
	print msg


opts,args = getopt(sys.argv[1:],"hedt:m:i:o:r:k:I:",["help","encrypt","decrypt","type=","mode=","in=","out=","round=","key=","IV="])


#supporting binary/picture
file_type ="bin"

#supporting ECB/CBC/CTR
key = "3ADA7521DBE2DBB311B44901A5C6EAD4"
en_de_mode ="ECB"
IV = "1234567812345678"
rou = 32
input_file = ""
output_file = ""
en = 0
de = 0

for o, a in opts:
	if o in ("-h","--help"):
		print_help()
		exit(0)

	if o in ("-e","--encrypt"):
		en = 1
		continue
	if o in ("-d","--decrypte"):
		de = 1
		continue
		

	if o in ("-t","--type"):
		file_type = a
		continue

	if o in ("-m","--mode"):
		en_de_mode = a
		continue
	if o in ("-r","--round"):
		rou = a
		continue
	if o in ("-k","--key"):
		key = a
		continue
	if o in ("-I","--IV"):
		IV = a
		continue

	if o in ("-i","--input","-o","--output"):
		if o in ("-i","--in"):
			input_file = a
			continue
		elif o in ("-o","--out"):
			output_file = a
			continue
	else:
		print("plese enter input/output file name")

if (en==0 and de==0) or (en==1 and de==1):
	print("chose encrypt or decrypt correctly")
	exit(0)

if file_type not in ("bin","pic"):
	print("error file type")
	exit(0)

if en_de_mode not in ("ECB","CBC","CTR"):
	print("error encrypt/decrypt mode")
	exit(0)

log_rou = int(math.log(int(rou),2))
if(2**log_rou != int(rou)):
	print("error round")
	exit()
if(len(key) != 32):
	print("error length of key")
	print len(key)
	exit(0)
if(not re.search('^[A-Fa-f0-9]+$',key)):
	print "error key"	
	exit()
if(len(IV) != 16):
	print("error length of IV")
	print len(key)
	exit(0)
if(not re.search('^[A-Fa-f0-9]+$',IV)):
	print "error IV"	
	exit()

key = re.findall(r'.{8}',key)
IV = re.findall(r'.{2}',IV)


if en==1 :
	tea.tea_en(file_type,en_de_mode,input_file,output_file,rou,key,IV)
elif de==1 :
	tea.tea_de(file_type,en_de_mode,input_file,output_file,rou,key,IV)





