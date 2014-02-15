'''Auto adjust stroke width.
Copyright Gumble <abcdoyle888@gmail.com> 2013-2014

#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 3 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.
'''
import sys,os,shutil
from subprocess import Popen

import bdflib
import k3m
import json

def simpscale(x,B,D):
	'''Scale x in [0,B] to [0,D]'''
	return int(D*(float(x)/B))

def CountPix(img):
	black=0
	for aline in img:
		black+=aline.count(1)
	return black

pointsize=48

print 'Mersuring pen widths...'
gwid={}
if len(sys.argv)>1:
	print 'Generating bdf...'
	Popen(u"fontforge -script genbdf.pe %s >/dev/null 2>&1" % str(pointsize), shell=True, cwd=os.getcwdu()).wait()
	srcfile = open('MergedFont-%s.bdf' % pointsize, 'r')
	bdffile = srcfile.readlines()
	srcfile.close()
	fontd = bdflib.read_bdf(iter(bdffile))
	bdffile = []
	ratiosum = 0.0
	gcount=0
	toolbar_width = 60
	fontlen=len(fontd.glyphs)
	print "Length %s" % fontlen

	k=0
	sys.stdout.write("/%s\\\n" % ("-" * toolbar_width))
	sys.stdout.flush()
	#sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
	sys.stdout.write("[")
	lastprg=0

	for aglyph in fontd.glyphs:
		bitmap = aglyph.bitmap()
		corig = CountPix(bitmap)
		if corig>0:
			#k3mskeletize(bitmap)
			#ck3m = CountPix(bitmap)
			ck3m = k3m.k3mcount(bitmap)
			gwid[aglyph.name]=corig/float(ck3m)
			ratiosum+=corig/float(ck3m)
			gcount+=1
		else:
			gwid[aglyph.name]=0
		k+=1
		nprg=simpscale(k,fontlen,toolbar_width)
		if nprg-lastprg>0:
			sys.stdout.write("="*(nprg-lastprg))
			lastprg=nprg
			sys.stdout.flush()
	sys.stdout.write("]\n")
	avgwid=ratiosum/gcount
	gwid['##count']=gcount
	gwid['##avg']=avgwid
	gwid['##len']=len(fontd.glyphs)
	print "Pen width avg.= " + str(avgwid)
	print "Vector pen width avg.= " + str(1024.0/pointsize*avgwid)
	with open('gwid_dict.json', 'w') as f:
		json.dump(gwid, f)
else:
	with open('gwid_dict.json', 'r') as f:
		gwid = json.load(f)
	avgwid = gwid['##avg']
	fontlen = gwid['##len']
gwid={}

shutil.copy2("MergedFont.sfd", "MergedResized.sfd")
print "Auto changing width..."
proc=Popen(u"python -u autowidth.py >aw.log 2>&1", shell=True, cwd=os.getcwdu())
print 'Process started. shell pid %s' % str(proc.pid)
proc.wait()
lastgl=''
print "Killed or completed."
gnum=0
enumb=0
errd={}
with open('aw.log','r') as fp:
	for line in fp:
		st = line.split(' ')
		if st[0]=='Glyph':
			lastgl=st[1]
			gnum+=1
		elif st[0]=='Opened':
			gnum=int(st[1])
		elif st[0]=='OK.':
			pass
		elif st[0]=='':
			pass
		else:
			errd[lastgl]=line
			enumb+=1
errd[lastgl]='Terminated.'
print 'Processed %s glyphs with %s errors.' % (str(gnum),str(enumb))
for k in errd:
	print k
	print ' ' + errd[k].strip()
print 'Done %s%%.' % (str(float(gnum*100)/fontlen))
# with open('errstat.json', 'r') as f:
	# errstat = json.load(f)
# errstat['err']+=len(errd)
# errstat['count']+=gnum
# print 'Problem ~=' + str(errstat['err']/float(errstat['count'])*fontlen)
# with open('errstat.json', 'w') as f:
	# json.dump(errstat, f)
if gnum!=fontlen:
	#proc=Popen(u"fontforge MergedFont.sfd", shell=True, cwd=os.getcwdu())
	print 'Fontforge started. shell pid %s' % str(proc.pid)
else:
	#os.chdir('../')
	#proc=Popen(u"python autoadjust.py", shell=True, cwd=os.getcwdu())
	#print 'python started. shell pid %s' % str(proc.pid)
	print 'Done.'
