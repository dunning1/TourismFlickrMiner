from __future__ import division
import random
import re

def IfPacExists(pk, image):
	ff = file("photometa.txt")
	lines = ff.readlines()
	ff.close()
	r = 0
	for line in lines:
		data = line.split("\t")#split the line with "tab"
		if (data[0] == image):
			p = re.compile(pk, re.IGNORECASE)
			#bug fix:not find pk in line, but in line[6,7,8]
			line = data[6] + data[7] + data[8]
			#print line
			r = p.findall(line.lower())
			break
	if r:
		return 1
	else:
		return 0
                
def calcVj4Image(vj, image):
	#vj appearance counting / image comments words counting
	ff = file("comment-newformat.txt")
	lines = ff.readlines()
	ff.close()
	appearance_count = 0
	comment_len = 0
	for line in lines:
		data = line.split("\t")#split the line with "tab"
		if (data[0] == image):
			##print "data[0] = %s, image = %s" %(data[0], image)
			#print line
			appearance_count = line.lower().count(vj)
			blanks = line.split(None)
			comment_len = len(blanks) - 1
			break

	#print "appearance_count = %d, comment_len = %d\n" %(appearance_count, comment_len)
	if(comment_len != 0):
		result = appearance_count / comment_len
	else:
		result = 0
	return result
	
	
def CalcFormula1(pk, vj):
	#for images
	ff = file("comment-newformat.txt")
	images = ff.readlines()
	ff.close()
	denominator = 0
	numerator = 0

	for image in images:
		data = image.split("\t")
		if(data[0].isdigit()):
			#print image
			Pvj = calcVj4Image(vj, data[0])
			#print "P(%s, %s) = %f" %(vj, data[0], Pvj)
			if(Pvj != 0):
				#print ("calcVj4Image(%s, %s) = %f" %(vj, data[0], Pvj))
				Bik = IfPacExists(pk, data[0])
				#print ("Bik(%s, %s) = %d" %(pk, data[0], Bik))
				numerator = numerator + Bik * Pvj
				denominator = denominator + Pvj
            
	if (denominator != 0):
		result = numerator / denominator
		#print "numerator = %f, denominator = %f" %(numerator, denominator)
		#print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxresult = %f\n" %result
		#print "denominator = %f\n" %denominator
	else:
		result = 0

	return result
	
	
def TestFormulaOne():
	pacfile = file("paclist.txt")
	paclist = pacfile.readlines()
	pacfile.close()  

	vacfile = file("vaclist.txt")
	vaclist = vacfile.readlines()
	vacfile.close()

	#vac = "lucky"
	#pac = "palace"
	#print "p(%s|%s) = %f\n" %(pac, vac, CalcFormula1(pac, vac))

	out = open("formula_1_result.txt", "w")

	for vac in vaclist:
		vac = vac[0:len(vac)-1]
		for pac in paclist:
			pac = pac[0:len(pac)-1]
			print vac
			print pac
			ret = CalcFormula1(pac, vac)
			print "p(%s|%s) = %f\n" %(pac, vac, ret)
			if(ret != 0):
				print "********************p(%s|%s) = %f**********************\n" %(pac, vac, ret)
				productResult = "p("+ pac + "," + vac +")=" + str(ret) + "\n"
				out.write(productResult)
					
	out.close()  

	
def CalcPkInImage(pac, di):
	#vj appearance counting / image comments words counting
	ff = file("photometa.txt")
	lines = ff.readlines()
	ff.close()
	appearance_count = 0
	comment_len = 0
	for line in lines:
		data = line.split("\t")#split the line with "tab"
		if (data[0] == di):
			line = data[6] + "\t" + data[7] + "\t"+ data[8]
			line = line.replace("+","\t")
			line = line.replace(",","\t")
			appearance_count = line.lower().count(pac)
			blanks = line.split(None)
			comment_len = len(blanks)
			break

	#print "appearance_count = %d, comment_len = %d\n" %(appearance_count, comment_len)
	if(comment_len != 0):
		result = appearance_count / comment_len
	else:
		result = 0
	return result
	
def CalcFormula2(di, vj):
	
	pacfile = file("paclist.txt")
	paclist = pacfile.readlines()
	pacfile.close() 
	ret = 1
	
	for pac in paclist:
		pac = pac[0:len(pac)-1]
		#print pac
		a = CalcPkInImage(pac, di)
		b = CalcFormula1(pac, vj)
		c = (a*b)+(1-a)*(1-b)
		#print "(a*b)+(1-a)*(1-b) = (%f*%f)+(1-%f)*(1-%f) = %f" %(a, b, a, b, c)
		if(c == 0):
			print "***************************************************************"
			print "a = %f, b = %f, di = %s, vj = %s, pac = %s" %(a, b, di, vj, pac)
		ret = ret * c
	ret = ret * 10000000
	print ">>>>>>>>>>>>>>>>>>>>>p(%s|%s) = %f>>>>>>>>>>>>>>>>>>>>\n" %(di, vj, ret)
	return ret


def CreateVacFileList(vj):
	ff = file("comment-newformat.txt")
	lines = ff.readlines()
	ff.close()
	out = open("candidatephotos.txt", "w")
	for line in lines:
		ret = line.find(vj)
		if(ret != -1):
			#write file
			data = line.split("\t")
			out.write(data[0]+"\n")
			

def TestFormulaTwo():
	vj = "interesting"
	ff = file("candidatephotos.txt")
	lines = ff.readlines()
	ff.close()
	out = open("formula_2_result.txt", "w")
	for line in lines:
		di = line[0:len(line)-1]
		print "p(%s|%s) calculating..." %(di, vj)
		ret = CalcFormula2(di, vj)
		line2write = "p(%s|%s) = %f\n" %(di, vj, ret)
		out.write(line2write)
	out.close()
	
#TestFormulaTwo()

    
    
    
    
    

