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
			matrix = np.array([[int(self.data_dict[prefix])]])
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
		img = Image.new( 'RGB', (256,256), "white")
		pixels = img.load()
		r,c=0,0
		mat_extent=256//np.shape(matrix)[0]
		for i in range(img.size[0]):
		    for j in range(img.size[1]):
		        #print(r,c)
		        pixels[i,j] = (self.colors_dict[matrix[r,c]][0], self.colors_dict[matrix[r,c]][1], 100)
		        c+=(j%mat_extent)//(mat_extent-1)
		    c=0
		    r+=(i%mat_extent)//(mat_extent-1)

		img.save(self.tiles_folder+self.quad_prefix+prefix+".jpg")

generate_tiles('02301023020111','files/map_data.csv','tiles/')