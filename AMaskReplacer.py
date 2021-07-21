import os
import re

from OldAlfaM import OldSymbol, OldImage


if __name__ == "__main__":
	# path to project
	path = "masks"
	#list of *.c files
	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(path):
		#find all *.c
		for file in f:
			if '.c' in file or '.h' in file:
				files.append(os.path.join(r, file))


	#read all files
	for file in files:	
		read = open(file,"r")
		alfafile = "".join(read.readlines())
		read.close()
		#try find alfa
		regular = r"u8\s*\w+\s*\[\]\s*=\s*\{[\n,\w,\s,\,]*\};"

		masks = re.findall(regular, alfafile)
		

		if(len(masks) > 0):
			sourcePath = file + "new.c"
			headerPath = file + "new.h"
			H = ""
			name = os.path.basename(file)
			H = (name[:-2]).upper()
			print(name, H)
			source = open(sourcePath, "w+")
			header = open(headerPath, "w+")
			
			header.write(f"#ifndef {H}_H\n#define {H}_H\n#include\"graphics.h\"\n\n")
			source.write(f"#include\"arch.h\"\n\n")
			#all finded mask convert to new alfa and write to new file
			for i,s in enumerate(masks):
				if(s[0] == "S"):
					alfa = OldSymbol(s)
				else:
					alfa = OldImage(s)
				
				newAlfa = alfa.toNewAlfa()
				newExtern = alfa.CreExtern();
				
				header.write(newExtern)
				source.write(newAlfa)


			header.write(f"#endif//{H}_H")
			source.close()
			header.close()

	
	




