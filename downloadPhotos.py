from flickr_api.api import flickr
import flickr_api
import re
import os
import sys

#input the vj as the parameter
vj = sys.argv[1] 
pdir = "rankedphotos\\" + vj + "\\"
downloadlist = "result_map_" + vj + ".txt"
print pdir

# import flickr_api as f
# p = f.Photo.search(tags="Parrot")[0]
# p.save("test.jpg", size_label="Square")
	# 'Square': 75x75
	# 'Thumbnail': 100 on longest side
	# 'Small': 240 on  longest side
	# 'Medium': 500 on longest side
	# 'Medium 640': 640 on longest side
	# 'Large': 1024 on longest side
	# 'Original': original photo (not always available)
def DownloadPhotos():
	ff = file(downloadlist)
	lines = ff.readlines()
	ff.close()
	order = 0
	for line in lines:
		order += 1
		data = line.split("\t")#split the line with "tab"
		p = flickr_api.Photo(id = data[0])
		if(not os.path.exists(pdir)):
			os.mkdir(pdir)
			print pdir
		# downloading the photo file()
		filename = pdir + str(order) + "." + data[0] + ".jpg"
		if(not os.path.exists(filename)):
			print filename
			try:
				p.save(filename, size_label = 'Medium')
			except Exception,e:
				print Exception, ":", e
				
			
		
DownloadPhotos()
