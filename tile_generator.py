import csv
import random
from PIL import Image
import numpy as np



class generate_tiles:
	def __init__(self,quad_prefix,filename,tiles_folder,bottom_level=18,max_image_prod=18):
		self.quad_prefix = quad_prefix
		self.max_image_prod = max_image_prod
		self.bottom_level = bottom_level
		self.tiles_folder = tiles_folder
		self.data_dict = self.read_map_csv(filename)
		self.colors_dict = [
			(204, 255, 255),
			(204, 102, 0),
			(51, 204, 51),
			(0, 102, 0),
			(0, 204, 102),
			(0, 0, 0),
			(255, 204, 0),
			(102, 255, 102),
			(255, 153, 255),
			(255, 0, 0),
			(51, 51, 153),
			(102, 204, 255),
		]
		self.generate_matrix('')

	def read_map_csv(self,filename):
		dic = {}
		with open(filename,'r') as data:
			for line in csv.reader(data):
				dic[line[1]]=line[2]
		del dic['path']
		return dic

	def generate_matrix(self,prefix):
		print(self.quad_prefix+prefix)
		if len(self.quad_prefix+prefix)==self.bottom_level:
			val = int(self.data_dict[prefix])
			matrix = np.array([[(self.colors_dict[val][0], self.colors_dict[val][1], self.colors_dict[val][2])]])
		else:
			zeroth = self.generate_matrix(prefix+'0')
			first = self.generate_matrix(prefix+'1')
			second = self.generate_matrix(prefix+'2')
			third = self.generate_matrix(prefix+'3')
			#print(zeroth)
			#print(first)
			#print(second)
			#print(third)
			matrix = np.concatenate((np.concatenate((zeroth, first), axis=1),np.concatenate((second, third), axis=1)),axis=0)

		if len(self.quad_prefix+prefix)<=self.max_image_prod:
			#print(matrix)
			self.generate_image(prefix,matrix)
		return matrix

	def generate_image(self,prefix,matrix):
		img = Image.fromarray(matrix.astype(np.uint8))
		img = img.resize((256,256),resample=Image.NEAREST)
		img.save(self.tiles_folder+self.quad_prefix+prefix+".jpg")


# airport 12330031112120
# railway 12330031113210
# highway 12330031113213
# slm&com 12330031112211 
# water   1233003111113  
# forest  12330031110130 

generate_tiles('1233003111213','files/3.csv','tiles/')