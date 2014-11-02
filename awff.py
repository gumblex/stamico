#!/usr/bin/python
# vim:ts=8:sw=4:expandtab:encoding=utf-8
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
__version__ = '1.1'

import sys
import fontforge
import json

pointsize=48
thres=1
scalen=1024.0/pointsize-1	#32


with open('gwid_dict.json', 'r') as f:
	gwid = json.load(f)
avgwid = gwid['##avg']
fontlen = gwid['##len']

i=int(sys.argv[1])
afont=fontforge.open("MergedResized.sfd")
if fontlen-i<63:
	afont.selection.select(("encoding","ranges"),i,fontlen-1)
else:
	afont.selection.select(("encoding","ranges"),i,i+63)
print "Opened %s to %s ." % (str(i),str(i+63))
for aglyphp in afont.selection:
	aglyph=afont[aglyphp]
	thiswid=gwid[afont[aglyphp].glyphname]
	if thiswid:
		wid=avgwid-thiswid
		print "Glyph %s" % aglyph.glyphname
		if int(wid)!=0:
			if .005<wid<.8:
				aglyph.stroke("circular",int(abs(wid*scalen)),'round','round',('removeinternal','cleanup'))
			elif -1<wid<-0.005:
				aglyph.stroke("circular",int(abs(wid*scalen)),'round','round',('removeexternal','cleanup'))
		aglyph.removeOverlap()
		aglyph.simplify(1.1,('ignoreslopes','smoothcurves','removesingletonpoints'))
afont.save()
afont.close()
afont=None
