
#evaluate our algorithm by Map(Mean average precision)
from __future__ import division
import random
import linecache
from formula import CalcFormula2
import sys

#1.for a vac, randomly select 5 relevant photos and 5 irrelevant photos.
relevantCount = 5
irrelevantCount = 5

def CreateRelevantPhotoList(vj):
	ff = file("comment-newformat.txt")
	lines = ff.readlines()
	ff.close()
	out = open("relevantPhotos.txt", "w")
	list = []
	for line in lines:
		ret = line.lower().find(vj)
		if(ret != -1):
			#write file
			data = line.split("\t")
			list.append(data[0])
			#out.write(data[0]+"\n")
	print list
	slice = random.sample(list, relevantCount) 
	#print slice
	return slice
	
def CreateIrrelevantPhotoList():
	n = 1
	filename = "photometa.txt"
	count = len(open(filename,'rU').readlines())
	list = []
	while (n <= irrelevantCount):
		randomLine = random.randint(0, count-1)
		line = linecache.getline(filename, randomLine)
		data = line.split("\t")
		list.append(data[0])
		n += 1
	#print list
	return list

def CreateEvaluateList(vj):
	relevantList = CreateRelevantPhotoList(vj)
	print relevantList
	IrrelevantList = CreateIrrelevantPhotoList()
	print IrrelevantList
	#relevantList.extend(IrrelevantList)
	#list = relevantList 
	#print list
	filename = "EvaluateList-%s.txt" %vj
	out = open(filename, "w")

	flag = "1"
	for i in range(len(relevantList)):
		line = relevantList[i] + "\t" + flag +"\n"
		out.write(line)
		
	flag = "0"
	for i in range(len(IrrelevantList)):
		line = IrrelevantList[i] + "\t" + flag +"\n"
		out.write(line)
	out.close()
	
	
#vj = "interesting"
#CreateEvaluateList(vj)

#2.ranking the photos using our algorithm.
def RankPhotos(vj):
	
	filename = "EvaluateList-%s.txt" %vj
	ff = file(filename)
	lines = ff.readlines()
	ff.close()
	
	outfile = "result_map_%s.txt" %vj
	out = open(outfile, "w")
	list = []
	
	for line in lines:
		#di = line[0:len(line)-1]
		image = line.split("\t")
		di = image[0]
		flag = image[1] #end with a "\t"
		print "p(%s|%s) calculating..." %(di, vj)
		ret = CalcFormula2(di, vj)
		item = (di, vj, ret, flag)
		list.append(item)
		
	list.sort(key=lambda x:x[2], reverse = True)
	print list
	
	for item in list:
		line2write = "%s\t%s\t%f\t%s" %(item[0], item[1], item[2], item[3])
		out.write(line2write)
	out.close()
	
def TestList():
	ff = file("formula_2_result.txt")
	lines = ff.readlines()
	ff.close()
	list = []
	vj = "interesting"
	outfile = "result_map_%s.txt" %vj
	out = open(outfile, "w")
	
	for line in lines:
		data = line.split("\t")
		item = (data[0], data[1], float(data[2][0:len(data[2])-1]))
		print item
		list.append(item)
		list.sort(key=lambda x:x[2], reverse = True)
	print list
	
	for item in list:
		line2write = "%s\t%s\t%f\n" %(item[0], item[1], item[2])
		out.write(line2write)
	out.close()
	
#TestList()
#vj = "interesting"
#RankPhotos(vj)

#3.calculating the average precision.
def CalcAP(vj):
	ff = file("result_map_%s.txt" %vj)
	lines = ff.readlines()
	ff.close()
	count = 0
	relcount = 0
	totalPrecision = 0
	precision = 0
	for line in lines:
		data = line.split("\t")
		flag = int(data[3][0:len(data[3])-1])
		count += 1
		if(flag == 1):
			relcount += 1
			precision = 1/count
			totalPrecision +=  precision
	ap = totalPrecision / relcount
	print "The average precision of %s is %f\n" %(vj, ap)

def PerfEvaluationMAP():
	vj = sys.argv[1]
	CreateEvaluateList(vj)
	RankPhotos(vj)
	CalcAP(vj)

PerfEvaluationMAP()









