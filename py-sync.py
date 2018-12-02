'''
Authors: Daniel Frederick and Evan Trowbridge
Date: 12-1-2018
---------------------------------------------
TO DO -
-
Port 12480
Split File - cmd$ split -b 100000000 {filename}
Reassemble File - cmd$ cat x* > {outputFilename}
'''

import os
import datetime

class sync:
	def __init__(self, folder1, folder2, pInfo=False):

		self.folder1 = folder1
		self.folder2 = folder2

		self.dif1 = self.check(self.folder1, self.folder2)
		self.dif2 = self.check(self.folder2, self.folder1)

		if pInfo:
			self.printInfo()

	def printDiffs(self):
		print("Files in folder 1 that aren't in folder 2:\n{}".format(self.dif1))
		print("Files in folder 2 that aren't in folder 1:\n{}".format(self.dif2))

	def printInfo(self):
		print('\nOriginal contents of folder 1:\n')
		self.folder1.printContents()
		print("\nFiles in folder 1 that aren't in folder 2:\n")
		self.dif1.printContents()

		print('\nOriginal contents of folder 2:\n')
		self.folder2.printContents()
		print("Files in folder 2 that aren't in folder 1:\n")
		self.dif2.printContents()

	# 
	def check(self, f1, f2):
		folder1 = f1
		folder2 = f2
		ans = []

		for i in folder1.contents:
			if type(i) is file:
				if not folder2.contains(i):
					ans.append(i)
			elif type(i) is folder:
				if not folder2.contains(i):
					try:
						k = self.check(i, folder2.contents[folder2.posOf(i)])
						if k != []:
							ans.append(k)
					except TypeError:
						pass
		t = container('diff_in_{}'.format(f1.name))
		t.contents = ans
		return t


class folder:
	def __init__(self, path, name):
		self.contents = []
		self.path = path
		self.name = name
		for i in os.listdir(path):
			if '.' not in i:
				self.contents.append(folder('{}\{}'.format(path, i), i))
			else:
				self.contents.append(file('{}\{}'.format(path, i), i))

	def __str__(self):
		return self.printContents(0, False)

	def posOf(self, f):
		for i in range(0, len(self.contents) - 1):
			if self.contents[i].name == f.name:
				return i
		return 'null'

	def printContents(self, level=0, p=True):
		ans = '\t'*level + self.name + '-->\n'
		for i in self.contents:
			if type(i) is file:
				x = level + 1
				ans += ('\t--') * x + i.name + '\n'
			else:
				ans += i.printContents(level + 1, False)
		if p:
			print(ans)
		else:
			return ans

	def contains(self, f):
		for i in self.contents:
			if i.name == f.name:
				return True
		return False

	def removeFolder(self, f):
		try:
			print('Removing folder {} from folder {}'.format(f, self.name))
			self.contents.remove(f)
		except ValueError:
			print('Error. There is no folder {} in folder {}'.format(f.name, self.name))

	def removeFile(self, f):
		try:
			print('Removing file {} from folder {}'.format(f, self.name))
			self.contents.remove(f)
		except ValueError:
			print('Error. There is no file {} in folder {}'.format(f.name, self.name))

class container(folder):
	def __init__(self, name):
		self.contents = []
		self.name = name

class file:
	def __init__(self, path, name):
		self.path = path
		self.name = name

	def __str__(self):
		return self.name

dir1 = 'C:\sync\dir1'
dir2 = 'C:\sync\dir2'

folder1 = folder(dir1, 'dir1')
folder2 = folder(dir2, 'dir2')

# folder1.printContents()

temp = sync(folder1, folder2, True)