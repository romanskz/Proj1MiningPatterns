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
		self.last_item = max(self.items)

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
		strItems = ""  # write item set as a string help in sorting
		for nb in self.keys:
			strItems += str(nb) + " "
			regexStr += str(nb) + " (\d+ )*"

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
			ret_freq_printed_set += str(candi) + " (" + str(freq) + ")\n"

	return ret_freq_sets, ret_freq_printed_set


def generate_candidates(items, k, freq_items_k_1):
	if k == 1:
		candidates = [ItemSet([nb]) for nb in items]
	elif k == 2:
		candidates = list()
		for i in range(len(freq_items_k_1)):
			for j in range(i + 1, len(freq_items_k_1)):
				candidates.append(ItemSet(freq_items_k_1[i][0].keys + freq_items_k_1[j][0].keys))
	else:
		candidates = list()
		for i in range(len(freq_items_k_1)):
			prefix_i = freq_items_k_1[i][0].keys[:-1]
			for j in range(i + 1, len(freq_items_k_1)):
				prefix_j = freq_items_k_1[j][0].keys[:-1]
				if str(prefix_i).__eq__(str(prefix_j)):
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


# Alternative miner (DFS)


def print_output(set_i: set, transactions_with_set, nb_transactions):
	str1 = str(sorted(list(set_i))[1:])
	# print(transactions_with_set, nb_transactions)
	str2 = " (" + str(float(transactions_with_set / nb_transactions)) + ")"
	print(str1 + str2)


def dfs(set_i: set, vertical_rep_db, last_item, min_freq, nb_transactions, nb_transactions_of_the_set,
		vertical_rep_empty_set):
	"""
	:param set_i: set of the current frequent items
	:param vertical_rep_db: the vertical representation of the projected database under set_i
	:param last_item: the biggest item in the transactions
	:param min_freq: the minimal frequency
	:param nb_transactions: the total number of transactions of the basic database
	:param nb_transactions_of_the_set: the total number of transactions of set_i
	:param vertical_rep_empty_set: the set of all the number of transactions
	:return: Print all the itemset more or equally frequent than min_freq
	"""
	if 0 not in set_i:
		return
	if len(set_i) > 1 and float(nb_transactions_of_the_set / nb_transactions) >= min_freq:
		print_output(set_i, nb_transactions_of_the_set, nb_transactions)
	for item in vertical_rep_db:
		set_i2 = set_i.copy()
		set_i2.add(item)
		vert_proj_D_I_U_i, all_transactions = \
			get_vert_projected_db(set_i2, vertical_rep_db, last_item, nb_transactions, min_freq, vertical_rep_empty_set)
		dfs(set_i2, vert_proj_D_I_U_i, last_item, min_freq, nb_transactions, len(all_transactions),
			vertical_rep_empty_set)


def get_vertical_rep(transactions):
	"""
	:param transactions: list of all the transactions of the database
	:return: Vertical representation of the initial database (with the element 0 corresponding to the empty set)
	"""
	vertical_rep = dict()
	vertical_rep[0] = set()
	for i in range(len(transactions)):
		vertical_rep[0].add(i + 1)
		for elem in transactions[i]:
			if elem not in vertical_rep:
				vertical_rep[elem] = set()
			vertical_rep[elem].add(i + 1)
	return vertical_rep


def get_vert_projected_db(elems: set, vertical_rep, last_item, nb_initial_transactions, min_frequency,
						  vertical_rep_empty_set):
	"""
	:param elems: items I
	:param vertical_rep: the vertical representation of the database D
	:param last_item: the greatest item in the transactions
	:param nb_initial_transactions: the total number of transactions of the basic database
	:param min_frequency: the minimal frequency
	:param vertical_rep_empty_set: the set of all the number of transactions
	:return: The vertical representation of the projected database D under items I
	"""
	vertical_rep_res = dict()
	set_of_elem = vertical_rep_empty_set
	for e in elems:
		if e in vertical_rep:
			set_of_elem = set_of_elem.intersection(vertical_rep[e])
	all_transactions = set_of_elem.copy()
	for i in range(max(elems) + 1, last_item + 1):
		if i in vertical_rep:
			res_elem_i = set_of_elem.intersection(vertical_rep[i])
			all_transactions = all_transactions.union(res_elem_i)
			if res_elem_i and float(len(res_elem_i) / nb_initial_transactions) >= min_frequency:
				vertical_rep_res[i] = res_elem_i
	return vertical_rep_res, all_transactions


def alternative_miner(filepath, minFrequency):
	"""Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency

		Depth first search algorithm
	"""
	dataset = Dataset(filepath)
	# set with all the transaction number
	vertical_rep_empty_set = set([x for x in range(1, len(dataset.transactions) + 1)])
	vert_proj_db = get_vert_projected_db({0}, get_vertical_rep(dataset.transactions), dataset.last_item,
										 len(dataset.transactions), minFrequency, vertical_rep_empty_set)[0]
	dfs({0}, vert_proj_db, dataset.last_item, minFrequency, len(dataset.transactions),
		len(dataset.transactions), vertical_rep_empty_set)



if __name__ == '__main__':
	# apriori("Datasets/chess.dat", 0.9)
	alternative_miner("Datasets/accidents.dat", 0.8)
