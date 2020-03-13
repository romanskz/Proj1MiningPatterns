class Dataset:
    """Utility class to manage a dataset stored in a external file."""
    def __init__(self, filepath):
        """reads the dataset file and initializes files"""
        self.transactions = list()
        self.items = set()

        try:
            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            for line in lines:
                transaction = list(map(int, line.split(" ")))
                self.transactions.append(transaction)
                for item in transaction:
                    self.items.add(item)

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


class TrieNode:
    def __init__(self, value):
        """counter used in counting candidates"""
        self.support_counter = 0
        self.value = value
        self.children = []
        self.item_set = []
        self.support_ratio = -1

    def insert(self, value):
        child = TrieNode(value)
        new_item_set = list(self.item_set)
        new_item_set.append(value)
        child.item_set = new_item_set
        child.value = value
        self.children.append(child)

    def get_child(self, value):
        for child in self.children:
            if child.value == value:
                return child
        return None

    def is_leaf(self):
        return  not self.children

    def getValue(self):
        return self.value


def generate_candidates(items, root_node: TrieNode, k):
    if k == 1:
        for value in items:
            root_node.insert(value)

    else:
        generate_candidates_from__trie(root_node, k, 0)


def generate_candidates_from__trie(root_node: TrieNode, k, curr_level):
    father_leaves_level = k - 2
    if curr_level < father_leaves_level:
        #not reached the father's level iterate to reach them
        for child in root_node.children:
            generate_candidates_from__trie(child,k, curr_level+1)
    else:
        #on the father's level we merge the children
        for i in range(0, len(root_node.children)):
            for j in range(i + 1, len(root_node.children)):
                root_node.children[i].insert(root_node.children[j].value)


def generate_candidates_from__trie2(root_node: TrieNode, k):
    # the idea is to merge the leaves of the same parent
    # we will jump to the fathers of the leaves
    # had to iterate each level like bfs. store the current level in a node

    #TODO this can be improved by always store the last level frequent nodes and their parents

    father_leaves_level = k - 2
    curr_level_nodes = []

    curr_level = 0

    if not root_node.is_leaf():
        curr_level_nodes = [root_node]

    while curr_level < father_leaves_level:
        temp = []
        for node in curr_level_nodes:
            for child in node.children:
                temp.append(child)
        curr_level_nodes = temp
        curr_level += 1

    #for each node in the fathers leave merge their children as in slides
    curr_iter = list(curr_level_nodes)
    for idx in range(0, len(curr_iter)):
        father = curr_iter[idx]
        for i in range(0, len(father.children)):
            for j in range(i+1, len(father.children)):
                curr_level_nodes[idx].children[i].insert(father.children[j].value)


def count_support(transactions, root_node: TrieNode):
    for trans in transactions:
        count_support_in_one_transaction(trans, 0, root_node)


def count_support_in_one_transaction(transaction, current_el_in_trans, root_node: TrieNode):
        if root_node.is_leaf():
            root_node.support_counter += 1
        else:
            for el in range(current_el_in_trans, len(transaction)):
                child = root_node.get_child(transaction[el])
                if child:
                    count_support_in_one_transaction(transaction, current_el_in_trans+1, child)


result_dict = dict()
resultString = ""

def filter_unfrequent_items(root_node: TrieNode, minFrequency, nbTransactions, itemSetList):
    children = list(root_node.children) #iterate on a copy so that we can remove unfrequent children from the trie.
    for child in children:
        if not child.is_leaf():
            itemSetList.append(child.value)
            filter_unfrequent_items(child, minFrequency,nbTransactions, itemSetList)
        else:
            freq = child.support_counter / nbTransactions
            if freq < minFrequency:
                root_node.children.remove(root_node.get_child(child.value))
            else:
                if root_node.get_child(child.value).support_ratio == -1: #node not yet computed
                    root_node.get_child(child.value).support_ratio = freq
                    itemSetList.append(child.value)
                    if not result_dict.get(str(itemSetList)):
                        result_dict[str(itemSetList)] = freq
                    print(str(root_node.get_child(child.value).item_set) + "  (" + str(freq) + ")")
                        #print(str(itemSetList) + "  (" + str(freq) + ")")
                    itemSetList.clear()



def filter_unfrequent_items2(root_node: TrieNode, minFrequency, nbTransactions):
    #children = root_node.children #iterate on a copy so that we can remove unfrequent children from the trie.
    list_child_to_delete = []
    print("rooot : ", root_node.value)
    print(" root children: ", )
    for child in root_node.children:
        print("root : ", root_node.value, " child : ", str(child.value))
        if not child.is_leaf():
            filter_unfrequent_items2(child, minFrequency, nbTransactions)
        else:
            freq = child.support_counter / nbTransactions
            #print("freq", freq)
            if freq < minFrequency:
                #root_node.children.remove(root_node.get_child(child.value))
                print("freq Remove", freq)
                list_child_to_delete.append(child)
            else:
                print("freq take", freq)
                root_node.get_child(child.value).support_ratio = freq

    for x in list_child_to_delete:
        root_node.children.remove(x)

     #frequent set is empty then we can continue


def apriori(filepath, minFrequency):
    dataset = Dataset(filepath)
    items = list(dataset.items)
    transactions = dataset.transactions

    root_node = TrieNode(-1)
    k = 1
    while True:
        generate_candidates(items, root_node, k)
        count_support(transactions, root_node)

        before_freq_size = len(result_dict)

        filter_unfrequent_items(root_node, minFrequency, len(transactions),[])

        if len(result_dict) == before_freq_size:
            break
        k += 1

    #for key in result_dict.keys():
    #   print(key + "  (" + str(result_dict[key]) + ")")
    #print_trie5(root_node)
    #print_trie_bfs([root_node])




def print_trie_bfs(queue):
    if len(queue) == 0:
        return
    current = queue.pop()
    if current.support_ratio != -1:
        print(str(current.item_set) + "  (" + str(current.support_ratio) + ")")
    for child in current.children:
        queue.append(child)

    print_trie_bfs(list(queue))


from collections  import deque

def print_level_order(head, queue = deque()):
    if head is None:
        return
    print(str(head.item_set) + "  (" + str(head.support_ratio) + ")")
    [queue.append(node) for node in head.children if node]
    if queue:
        print_level_order(queue.popleft(), queue)


def print_trie(root_trie: TrieNode, nb):
    for x in root_trie.children:
        print_trie(x, nb)


def print_trie2(root_trie: TrieNode, nb):
    print(root_trie.value)
    for x in root_trie.children:
        for j in x.children:
            print("["+str(x.value)+ ", "+str(j.value)+"] ("+str(j.support_ratio)+")" + "- "+ str(j.support_counter/nb < 0.9))


def print_trie3(root_trie: TrieNode):
    print(root_trie.value)
    for x in root_trie.children:
        for j in x.children:
            for z in j.children:
                print("["+str(x.value)+ ", "+str(j.value)+ ", "+ str(z.value)+"]  ("+str(z.support_ratio)+")")


def print_trie4(root_trie: TrieNode):
    print(root_trie.value)
    for x in root_trie.children:
        for j in x.children:
            for z in j.children:
                for w in z.children:
                    print("("+str(x.value)+ " "+str(j.value)+ " "+ str(z.value)+ " "+ str(w.value)+")")


def print_trie5(root_trie: TrieNode):
    print(root_trie.value)
    for x in root_trie.children:
        for j in x.children:
            for z in j.children:
                for w in z.children:
                    for t in w.children:
                        print("("+str(x.value) + " "+str(j.value)+ " "+ str(z.value)+ " "+ str(w.value)+ " "+ str(t.value)+")")


def alternative_miner(filepath, minFrequency):
    """"""


if __name__ == '__main__':
	apriori("Datasets/chess.dat", 0.9)


