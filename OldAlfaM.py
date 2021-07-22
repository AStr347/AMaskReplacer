import re

class OldAlfa:
	#			a8			a16			a24				a32
	#max for width and height
	wsizes = [0b111,	0b1111111, 0b1111111111,	0b11111111111111]
	hsizes = [0b1111,	0b1111111, 0b11111111111,	0b11111111111111]
	
	#keys in bin
	keys = ["0b1",		"0b10",	   "0b100",			"0b1000"]
	#count of bit for width and height 
	wbit = [3,			7,			10,				14]
	hbit = [4,			7,			11,				14]
	keybit = [1,          2,          3,              4]
	#default init values
	def __init__(self) :
		self.symbol = ""
		self.width = 0
		self.height = 0
		self.payload = ""
		self.type = 0
		self.size = 0


class OldSymbol (OldAlfa):
	

	def __init__(self, s):
		super().__init__()
		#get name of symbol
		self.symbol = (re.findall(r",\w+\)", s)[0])[1 : -1]
		#get font
		self.font = (re.findall(r"\(\w+,", s)[0])[1 : -1]
		#get width, 0, height, 0,
		sizes = re.findall(r"\s*(\d+),\n*\s*0,\n", s)
		if(2 > len(sizes)):
			return None
		#get width
		width = re.findall(r"\d+",(sizes[0]))[0]
		#get height
		height = re.findall(r"\d+",(sizes[1]))[0]
		self.width = int(width) - 1
		self.height = int(height) - 1
		#get payload without sizes
		payload = re.search(r"0x[\n,\w,\s,\,]+\};",s)[0][:-3]
		#to 1 string
		payload = payload.replace("\n","")
		self.payload = payload
		

		#find type of alfa
		wtype, htype = 0, 0
		
		for i,w in enumerate(OldSymbol.wsizes):
			if(self.width < w):
				wtype = i
				break
		
		for i,h in enumerate(OldSymbol.hsizes):
			if(self.height < h):
				htype = i
				break
		
		self.type = max(wtype,htype)

		#get size of payload
		self.size = len(re.findall(r"0x", self.payload))


	def toNewAlfa(self):
		t = self.type
		O = OldAlfa;
		#finaly struct for write
		newalfa = ["const struct {\n\t",
					f"unsigned key : {O.keybit[t]};\n\t",
					f"unsigned width : {O.wbit[t]};\n\t",
					f"unsigned height : {O.hbit[t]};\n\t",
					f"u8 payload[{self.size}];\n",
					"} ",
						self.symbol, " __attribute__((section (\"",self.font,"\"))) = {\n\t",
						".key = ",  str(O.keys[self.type]), ",\n\t",
						".width = ", str(self.width), ",\n\t",
						".height = ", str(self.height), ",\n\t",
						".payload = {", self.payload ,"},\n"
						"};\n"]

		return "".join(newalfa) + "\n\n\n"

	def CreExtern(self):
		#finaly extern struct for write
		newalfa = ["extern const amask_t " , self.symbol, ";"
						]
		return "".join(newalfa) + "\n\n"


class OldImage (OldAlfa):
	def __init__(self, s):
		super().__init__()
		#get name of symbol
		regular = re.findall(r"u8\s*(\w+)\s*\[\]\s*=", s)
		self.symbol = (regular[0])
		
		#get width, 0, height, 0,
		sizes = re.findall(r"\n*\s*(\d+),\n*\s*0,\n*", s)
		if(2 > len(sizes)):
			return None
		#get width
		width = re.findall(r"\d+",(sizes[0]))[0]
		#get height
		height = re.findall(r"\d+",(sizes[1]))[0]
		self.width = int(width) - 1
		self.height = int(height) - 1
		#get payload without sizes
		payload = re.search(r"0x[\n,\w,\s,\,]+\};",s)[0][:-3]
		#to 1 string
		payload = payload.replace("\n","")
		self.payload = payload
		

		#find type of alfa
		wtype, htype = 0, 0
		
		for i,w in enumerate(OldSymbol.wsizes):
			if(self.width < w):
				wtype = i
				break
		
		for i,h in enumerate(OldSymbol.hsizes):
			if(self.height < h):
				htype = i
				break
		
		self.type = max(wtype,htype)

		#get size of payload
		self.size = len(re.findall(r"0x", self.payload))


	def toNewAlfa(self):
		t = self.type
		O = OldAlfa;
		#finaly struct for write
		newalfa = ["const struct {\n\t",
					f"unsigned key : {O.keybit[t]};\n\t",
					f"unsigned width : {O.wbit[t]};\n\t",
					f"unsigned height : {O.hbit[t]};\n\t",
					f"u8 payload[{self.size}];\n",
					"} ",
						self.symbol, " = {\n\t",
						".key = ",  str(O.keys[self.type]), ",\n\t",
						".width = ", str(self.width), ",\n\t",
						".height = ", str(self.height), ",\n\t",
						".payload = {", self.payload ,"},\n"
						"};\n"]

		return "".join(newalfa) + "\n\n\n"

	def CreExtern(self):
		#finaly extern struct for write
		newalfa = ["extern const amask_t " , self.symbol, ";"
						]
		return "".join(newalfa) + "\n\n"