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
	def __init__(self, folder1, folder2):
		# self.path1 = path1
		# self.path2 = path2

		self.folder1 = folder1
		self.folder2 = folder2

		# self.folder1 = folder(self.path1, 'folder1')
		# self.folder2 = folder(self.path2, 'folder2')

		self.diffs = self.check(self.folder1, self.folder2)

	def printDiffs(self):
		print("Files in folder 1 that aren't in folder 2:\n{}".format(self.diffs[0]))
		print("Files in folder 2 that aren't in folder 1:\n{}".format(self.diffs[1]))

	def printInfo(self):
		print('\nOriginal contents of folder 1:\n{}'.format(self.folder1.printContents))
		print("\nFiles in folder 1 that aren't in folder 2:\n{}".format(self.diffs[0]))

		print('\nOriginal contents of folder 2:\n{}'.format(self.folder2.printContents))
		print("Files in folder 2 that aren't in folder 1:\n{}".format(self.diffs[1]))
				
	def check(self, folder1, folder2):
		for i in folder1.contents:
			if '.' in i.name:
				print('{} is a file'.format(i.name))
				if i in folder2.contents:
					folder1.removeFile(i)
			else:
				print('{} is a folder'.format(i.name))
				if i not in folder2.contents:
					break
				else:
					self.check(i, folder2[folder2.index(i)])
					if i.contents == []:
						folder1.removeFolder(i)

		for i in folder2.contents:
			if '.' in i.name:
				print('{} is a file'.format(i.name))
				if i in folder1.contents:
					folder2.removeFile(i)
			else:
				print('{} is a folder'.format(i.name))
				if i not in folder1.contents:
					break
				else:
					self.check(i, folder1[folder1.index(i)])
					if i.contents == []:
						folder1.removeFolder(i)

		return [folder1.contents, folder2.contents]
		
				

class folder:
	def __init__(self, path, name):
		self.contents = os.listdir(path)
		self.path = path
		self.name = name
		# print('Pre- contents of {}: {}'.format(self.name, self.contents))
		for i in self.contents:
			if '.' not in i:
				x = self.contents.index(i)
				self.contents[x] = folder('{}\{}'.format(path, i), i)
			else:
				x = self.contents.index(i)
				self.contents[x] = file('{}\{}'.format(path, i), i)
		# print('Post- contents of {}: {}'.format(self.name, self.contents))

	def __str__(self):
		return self.name
		
		'''
		ans = '{}\n'.format(self.name)
		for i in self.contents:
			if type(i) is file:
				ans += '\t{}\n'.format(i.name)
			elif type(i) is folder:
				ans += i.__str__()
		return ans
		'''
		'''
	def __repr__(self):
		return self.name
		'''

	def printContents(self):
		print('\nContents of folder {}\n'.format(self.name))
		for i in self.contents:
			if type(i) is file:
				print('\t{}\n'.format(i.name))
			elif type(i) is folder:
				i.printContents()

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

class file:
	def __init__(self, path, name):
		self.path = path
		self.name = name

	def __str__(self):
		return self.name

dir1 = 'C:\sync\dir1'
dir2 = 'C:\sync\dir2'

folder1 = folder(dir1, 'folder1')
folder2 = folder(dir1, 'folder2')

# folder1.printContents()

temp = sync(folder1, folder2)
temp.printInfo()