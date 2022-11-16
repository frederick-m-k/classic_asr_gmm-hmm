import numpy


class WagnerFischer:
	"""
	Class for computing and processing distance matrecies.

	Define two lists:
		>>>list1 = ["af", "aa", "i:", "0"]
		>>>list2 = ["af", "aa", "cc", "0"]
		Initialize the instance of WagnerFischer class, e.g.
		>>>wf = wagnerfischer.WagnerFischer()

		Outputs number of deletions, insertions and substitution on console
		>>>wf.sumOccurencies(list)
		(Deletions: 1
		Substitutions: 0
		Insertions: 1)

		Calculates and puts into a variable distance
		>>>list = wf.calculateWagnerFischer(list1, list2)
	"""

	def __init__(self):
		self.deletions = 0
		self.substitutions = 0
		self.insertions = 0
		self.log_file = "data_analysis/logFile.txt"
		open(self.log_file, 'w', encoding="utf-8").close() # clear the file

	def printDistances(self, dist, l1length, l2length):
		"""
		Prints distances matrix
		:param dist:
		:param l1Length:
		:param l2Length:
		:return:
		"""
		for t1 in range(l1length + 1):
			for t2 in range(l2length + 1):
				print(int(dist[t1][t2]), end=" ")
			print()

	def calculateWagnerFischer(self, list1, list2, tg_id, insertion=1, deletion=1, substitution=1):
		"""
		Strings are input as A and B. Costs can be optionally given. Matches are
		always free. Returns list of changes including symbols for deletion, insertion, substitution and match.

		Default substitution weights set to compensate for free match weight.
		Weights can be changed although mind the proper values.
		"""
		n_l1 = len(list1)
		n_l2 = len(list2)
		# compute distance matrix
		distances = numpy.zeros((n_l1 + 1, n_l2 + 1))
		for i in range(n_l1):  # cost of deletion
			distances[i + 1][0] = distances[i][0] + deletion
		for j in range(n_l2):  # cost of insertion
			distances[0][j + 1] = distances[0][j] + insertion

		for i in range(n_l1):  # fill out middle of matrix
			for j in range(n_l2):  # fill out matrix # 1
				if list1[i] == list2[j]:  # match
					distances[i + 1][j + 1] = distances[i][j]  # aka, it's free.
				else:  # no match
					distances[i + 1][j + 1] = min(distances[i + 1][j] + insertion,
												  distances[i][j + 1] + deletion,
												  distances[i][j] + substitution)
		# traceback
		change = []
		while n_l1 > 0 and n_l2 > 0:
			s_cost = distances[n_l1 - 1][n_l2 - 1]  # substitute or match
			d_cost = distances[n_l1 - 1][n_l2]  # delete
			i_cost = distances[n_l1][n_l2 - 1]  # insert
			if s_cost < d_cost:
				if s_cost < i_cost:
					if s_cost == distances[n_l1][n_l2]:  # match
						change.append('=')
					else:  # substitution
						change.append('*')
					n_l1 -= 1
					n_l2 -= 1
				else:  # insertion
					change.append('^')
					list1.insert(n_l1, '*')
					n_l2 -= 1
			else:  # deletion
				change.append('v')
				list2.insert(n_l2, '*')
				n_l1 -= 1
		with open(self.log_file, 'a', encoding="utf-8") as log_fd:
			log_fd.write(tg_id + '\n')
			log_fd.write(' '.join(list1) +"\n")
			log_fd.write(' '.join(list2) +"\n")
			log_fd.write(' '.join(change[::-1]) + "\n")
			log_fd.write('\n')
		return change[::-1]

	def sumOccurencies(self, inlist):
		"""
		Sums all occurencies of deletions, insertions and substitutions.
		:param inlist:
		:return:
		"""
		self.deletions = inlist.count('v')
		self.substitutions = inlist.count('*')
		self.insertions = inlist.count('^')

		#print("Deletions: " + str(self.deletions) + "\n" +
		#	  "Substitutions: " + str(self.substitutions) + "\n" +
		#	  "Insertions: " + str(self.insertions) + "\n")

	def getDeletions(self):
		return self.deletions

	def getSubstitutions(self):
		return self.substitutions

	def getInsertions(self):
		return self.insertions
