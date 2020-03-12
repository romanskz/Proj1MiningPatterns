"""
Skeleton file for the project 1 of the LINGI2364 course.
Use this as your submission file. Every piece of code that is used in your program should be put inside this file.

This file given to you as a skeleton for your implementation of the Apriori and Depth
First Search algorithms. You are not obligated to use them and are free to write any class or method as long as the
following requirements are respected:

Your apriori and alternativeMiner methods must take as parameters a string corresponding to the path to a valid
dataset file and a double corresponding to the minimum frequency.
You must write on the standard output (use the print() method) all the itemsets that are frequent in the dataset file
according to the minimum frequency given. Each itemset has to be printed on one line following the format:
[<item 1>, <item 2>, ... <item k>] (<frequency>).
Tip: you can use Arrays.toString(int[] a) to print an itemset.

The items in an itemset must be printed in lexicographical order. However, the itemsets themselves can be printed in
any order.

Do not change the signature of the apriori and alternative_miner methods as they will be called by the test script.

__authors__ = "<write here your group, first name(s) and last name(s)>"
"""
import re

class Dataset:
	"""Utility class to manage a dataset stored in a external file."""

	def __init__(self, filepath):
		"""reads the dataset file and initializes files"""
		self.transactions = list()
		self.items = set()
		self.transactionsString = list()

		try:
			lines = [line.strip() for line in open(filepath, "r")]
			lines = [line for line in lines if line]  # Skipping blank lines
			for line in lines:
				transaction = list(map(int, line.split(" ")))
				self.transactions.append(transaction)
				trans_string = ""
				for item in transaction:
					self.items.add(item)
					trans_string += str(item) + " "

				self.transactionsString.append(trans_string)
		except IOError as e:
			print("Unable to read dataset file!\n" + e)

	def trans_num(self):
		"""Returns the number of transactions in the dataset"""
		return len(self.transactions)

	def items_num(self):
		"""Returns the number of different items in the dataset"""
		return len(self.items)

	def get_transaction(self, i):
		"""Returns the transaction at index i as an int array"""
		return self.transactions[i]


class ItemSet:
	def __init__(self, keys):

		self.keys = keys

		# regex string to find the set in a transaction
		# https://regex101.com/r/teyF5J/9/
		regexStr = "^(\d+ )*"
		strItems = "" # write item set as a string help in sorting
		for nb in self.keys:
			strItems += str(nb) + " "
			regexStr += str(nb)+" (\d+ )*"

		self.regex_pattern = regexStr
		self.keys_string = strItems

	def __cmp__(self, other):
		return self.keys_string <= other.keys_string

	def __eq__(self, other):
		return self.keys_string.__eq__(other.keys_string)

	def __str__(self):
		return self.keys.__str__()

	def __repr__(self):
		return str(self)


def filter_freqset(transanctionsString, candidates, minFrequency, nbTransactions):
	ret_freq_sets = list()
	ret_freq_printed_set = ""
	for candi in candidates:
		counter = 0.0
		for trans in transanctionsString:
			if re.compile(candi.regex_pattern).search(trans) is not None:
				counter += 1.0
		freq = counter / nbTransactions
		if freq >= minFrequency:
			ret_freq_sets.append((candi, freq))
			ret_freq_printed_set += str(candi) + " ("+str(freq)+")\n"

	return ret_freq_sets, ret_freq_printed_set


def generate_candidates(items, k, freq_items_k_1):
	if k == 1:
		candidates = [ItemSet([nb]) for nb in items]
	elif k == 2:
		candidates = list()
		for i in range(freq_items_k_1.__len__()):
			for j in range(i+1, freq_items_k_1.__len__()):
				candidates.append(ItemSet(freq_items_k_1[i][0].keys + freq_items_k_1[j][0].keys))
	else:
		candidates = list()
		for i in range(freq_items_k_1.__len__()):
			prefix_i = freq_items_k_1[i][0].keys[:-1]
			for j in range(i + 1, freq_items_k_1.__len__()):
				prefix_j = freq_items_k_1[j][0].keys[:-1]
				if prefix_i.__str__().__eq__(prefix_j.__str__()):
					prefix_j.extend([freq_items_k_1[i][0].keys[-1], freq_items_k_1[j][0].keys[-1]])
					candidates.append(ItemSet(prefix_j))

	return candidates


def apriori(filepath, minFrequency):
	"""Runs the apriori algorithm on the specified file with the given minimum frequency"""
	# TODO: implementation of the apriori algorithm
	dataset = Dataset(filepath)
	items = list(dataset.items)
	frequent_sets = ([], "")
	k = 1
	result_printed = ""
	while frequent_sets[0] or k == 1:
		candidates = generate_candidates(items, k, frequent_sets[0])
		frequent_sets = filter_freqset(dataset.transactionsString, candidates, minFrequency, len(dataset.transactions))
		k += 1
		result_printed += frequent_sets[1]
	print(result_printed)


def alternative_miner(filepath, minFrequency):
	"""Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency"""
	# TODO: either second implementation of the apriori algorithm or implementation of the depth first search algorithm
	print("Not implemented")


if __name__ == '__main__':
	apriori("Datasets/chess.dat", 0.9)