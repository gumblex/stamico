N = ((32,64,128), (16,0,1), (8,4,2))
A0 = [3,6,7,12,14,15,24,28,30,31,48,56,60,62,63,96,112,120,124,\
	  126,127,129,131,135,143,159,191,192,193,195,199,207,223,224,\
	  225,227,231,239,240,241,243,247,248,249,251,252,253,254]
A1 = [7, 14, 28, 56, 112, 131, 193, 224]
A2 = [7, 14, 15, 28, 30, 56, 60, 112, 120, 131, 135, 193, 195, 224, 225, 240]
A3 = [7, 14, 15, 28, 30, 31, 56, 60, 62, 112, 120, 124, 131, 135, 143, 193, 195, 199, 224, 225, 227, 240, 241, 248]
A4 = [7, 14, 15, 28, 30, 31, 56, 60, 62, 63, 112, 120, 124, 126, 131, 135, 143, 159, 193, 195, 199, 207, 224, 225, 227, 231, 240, 241, 243, 248, 249, 252]
A5 = [7, 14, 15, 28, 30, 31, 56, 60, 62, 63, 112, 120, 124, 126, 131, 135, 143, 159, 191, 193, 195, 199, 207, 224, 225, 227, 231, 239, 240, 241, 243, 248, 249, 251, 252, 254]
A1pix = [3, 6, 7, 12, 14, 15, 24, 28, 30, 31, 48, 56, 60, 62, 63, 96, 112, 120, 124, 126, \
 127, 129, 131, 135, 143, 159, 191, 192, 193, 195, 199, 207, 223, 224, 225, 227, \
 231, 239, 240, 241, 243, 247, 248, 249, 251, 252, 253, 254]
A1pfix = [21,69,81,84]

def simpscale(x,B,D):
	'''Scale x in [0,B] to [0,D]'''
	return int(D*(float(x)/B))

def k3mskeletize(img):

	# initialize the regions and get their contents into arrays:
	srcWidth, srcHeight = len(img), len(img[0])
	
	plist = []
	flag = True
	c = 0
	B = []

	def thinner(W):
		for x in range(1,srcWidth-1):
			for y in range(1,srcHeight-1):
				if getpixel(x,y)==0: continue
				weight = 0
				for i in range (-1,2):
					for j in range (-1,2):
						weight += N[i+1][j+1] * getpixel(x+i,y+j)
				if weight in W:
					putpixel(x,y)
				if weight in A1pfix:
					img[x][y] = 1

	def phase(B, W):
		for b in B:
			weight = 0
			for i in range (-1,2):
				for j in range (-1,2):
					weight += N[i+1][j+1] * getpixel(b[0]+i,b[1]+j)
			if weight in W:
				putpixel(b[0],b[1])
				B.remove(b)
		return B

	def border(A0):
		B = {}
		for x in range(1,srcWidth-1):
			for y in range(1,srcHeight-1):
				bit = getpixel(x,y)
				if bit==0: continue
				# Weight
				weight = 0
				for i in range (-1,2):
					for j in range (-1,2):
						weight += N[i+1][j+1] * getpixel(x+i,y+j)
				if weight in A0:
					B[(x,y)]=1
					# B.append((x,y))
		return B

	def putpixel(x, y):
		#if not (x<0 or x>srcWidth-1 or y<0 or y>srcHeight-1):
		img[x][y]=0

	def getpixel(x, y):
		if x<0 or x>srcWidth-1 or y<0 or y>srcHeight-1:
			return 0
		else:
			return img[x][y]

	while flag:
		c += 1
		B = border(A0)
		Bp1 = phase(list(B), A1)
		Bp2 = phase(Bp1, A2)
		Bp3 = phase(Bp2, A3)
		Bp4 = phase(Bp3, A4)
		Bp5 = phase(Bp4, A5)
		plist = Bp5
		if len(B) == len(plist): flag=False
	thinner(A1pix)
	
def CountPix(img):
	black=0
	for aline in img:
		black+=aline.count(1)
	return black

def k3mcount(img):
	bitmap=img[:]
	k3mskeletize(bitmap)
	ck3m = CountPix(bitmap)
	return ck3m
