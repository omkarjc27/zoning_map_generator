import csv
import random
from PIL import Image
import numpy as np



class generate_tiles:
	def __init__(self,quad_prefix,filename,tiles_folder,bottom_level=19,max_image_prod=18):
		self.quad_prefix = quad_prefix
		self.max_image_prod = max_image_prod
		self.bottom_level = bottom_level
		self.tiles_folder = tiles_folder
		self.data_dict = self.read_map_csv(filename)
		self.colors_dict = {}
		for i in range(20):self.colors_dict[i]=(random.randint(0,225),random.randint(0,225))
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
			matrix = np.array([[(self.colors_dict[val][0], self.colors_dict[val][1], 100)]])
		else:
			zeroth = self.generate_matrix(prefix+'0')
			first = self.generate_matrix(prefix+'1')
			second = self.generate_matrix(prefix+'2')
			third = self.generate_matrix(prefix+'3')
			
			matrix = np.concatenate((np.concatenate((zeroth, first), axis=1),np.concatenate((second, third), axis=1)),axis=0)

		if len(self.quad_prefix+prefix)<=self.max_image_prod:
			self.generate_image(prefix,matrix)
		return matrix

	def generate_image(self,prefix,matrix):
		img = Image.fromarray(matrix.astype(np.uint8))
		img = img.resize((256,256))
		img.save(self.tiles_folder+self.quad_prefix+prefix+".jpg")

generate_tiles('02301023020111','files/map_data.csv','tiles/')