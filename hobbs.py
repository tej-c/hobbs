import sys
import nltk
from nltk.corpus import names
from nltk import Tree
import queue as Queue
#nltk.download('names')

# Labels for nominal heads
nominal_labels = ["NN", "NNS", "NNP", "NNPS", "PRP"]

def get_pos(tree, node):
    #print(tree.treepositions())
    for pos in tree.treepositions():
        if tree[pos] == node:
            return pos
    

def get_dom_np(sents, pos):
    # start with the last tree in sents
    tree = sents[-1]
    # get the NP's position by removing the last element from 
    # the pronoun's
    dom_pos = pos[:-1]
    return tree, dom_pos
    
def walk_to_np_or_s(tree, pos):
    path = [pos]
    still_looking = True
    while still_looking:
        # climb one level up the tree by removing the last element
        # from the current tree position
        pos = pos[:-1]
        path.append(pos)
        # if an NP or S node is encountered, return the path and pos
        if "NP" in tree[pos].label() or tree[pos].label() == "S":
            still_looking = False
    return path, pos

def bft(tree):
    lst = []
    queue = Queue.Queue()
    queue.put(tree)
    while not queue.empty():
        node = queue.get()
        lst.append(node)
        for child in node:
            if isinstance(child, nltk.Tree):
                queue.put(child)
    return lst

def count_np_nodes(tree):
    np_count = 0
    if not isinstance(tree, nltk.Tree):
        return 0
    elif "NP" in tree.label() and tree.label() not in nominal_labels:
        return 1 + sum(count_np_nodes(c) for c in tree)
    else:
        return sum(count_np_nodes(c) for c in tree)

def check_for_intervening_np(tree, pos, proposal, pro):
    bf = bft(tree[pos])
    bf_pos = [get_pos(tree, node) for node in bf]

    if count_np_nodes(tree[pos]) >= 3:
        for node_pos in bf_pos:
            if "NP" in tree[node_pos].label() \
            and tree[node_pos].label() not in nominal_labels: 
                if node_pos != proposal and node_pos != get_pos(tree, pro)[:-1]:
                    if node_pos < proposal:
                        return True
    return False

def traverse_left(tree, pos, path, pro, check=1):
    # get the results of breadth first search of the subtree
    # iterate over them
    breadth_first = bft(tree[pos])

    # convert the treepositions of the subtree rooted at pos
    # to their equivalents in the whole tree
    bf_pos = [get_pos(tree, node) for node in breadth_first]
    
    if check == 1:
        for p in bf_pos:
            if p<path[0] and p not in path:
                if "NP" in tree[p].label() and match(tree, p, pro):
                    if check_for_intervening_np(tree, pos, p, pro) == True:
                        return tree, p

    elif check == 0:
        for p in bf_pos:
            if p<path[0] and p not in path:
                if "NP" in tree[p].label() and match(tree, p, pro):
                    return tree, p

    return None, None

def traverse_right(tree, pos, path, pro):
    breadth_first = bft(tree[pos])
    bf_pos = [get_pos(tree, node) for node in breadth_first]

    for p in bf_pos:
        if p>path[0] and p not in path:
            if "NP" in tree[p].label() or tree[p].label() == "S":
                if "NP" in tree[p].label() and tree[p].label() not in nominal_labels:
                    if match(tree, p, pro):
                        return tree, p
                return None, None

def traverse_tree(tree, pro):
    # Initialize a queue and enqueue the root of the tree
    queue = Queue.Queue()
    queue.put(tree)
    while not queue.empty():
        node = queue.get()
        # if the node is an NP, return it as a potential antecedent
        if "NP" in node.label() and match(tree, get_pos(tree,node), pro):
            return tree, get_pos(tree, node)
        for child in node:
            if isinstance(child, nltk.Tree):
                queue.put(child)
    # if no antecedent is found, return None
    return None, None

def match(tree, pos, pro):
    if number_match(tree, pos, pro) and gender_match(tree, pos, pro):
        return True
    return False

def number_match(tree, pos, pro):
    m = {"NN":          "singular",
         "NNP":         "singular",
         "he":          "singular",
         "she":         "singular",
         "him":         "singular",
         "her":         "singular",
         "it":          "singular",
         "himself":     "singular",
         "herself":     "singular",
         "itself":      "singular",
         "NNS":         "plural",
         "NNPS":        "plural",
         "they":        "plural",
         "them":        "plural",
         "themselves":  "plural",
         "PRP":         None}
    
    # if the label of the nominal dominated by the proposed NP and 
    # the pronoun both map to the same number feature, they match 
    for c in tree[pos]:
        if isinstance(c, nltk.Tree) and c.label() in nominal_labels:
            if m[c.label()] == m[pro]:
                return True
    return False

def gender_match(tree, pos, pro):
    male_names = (name.lower() for name in names.words('male.txt'))
    female_names = (name.lower() for name in names.words('female.txt'))
    male_pronouns = ["he", "him", "himself"]
    female_pronouns = ["she", "her", "herself"]
    neuter_pronouns = ["it", "itself"]
    
    for c in tree[pos]:
        if isinstance(c, nltk.Tree) and c.label() in nominal_labels:
            # If the proposed antecedent is a recognized male name,
            # but the pronoun being resolved is either female or
            # neuter, they don't match
            if c.leaves()[0].lower() in male_names:
                if pro in female_pronouns:
                    return False
                elif pro in neuter_pronouns:
                    return False
            # If the proposed antecedent is a recognized female name,
            # but the pronoun being resolved is either male or 
            # neuter, they don't match
            elif c.leaves()[0].lower() in female_names:
                if pro in male_pronouns:
                    return False
                elif pro in neuter_pronouns:
                    return False
            # If the proposed antecedent is a numeral, but the 
            # pronoun being resolved is not neuter, they don't match
            elif c.leaves()[0].isdigit():
                if pro in male_pronouns:
                    return False
                elif pro in female_pronouns:
                    return False

    return True
    
def walk_to_s(tree, pos):
    path = [pos]
    still_looking = True
    while still_looking:
        # climb one level up the tree by removing the last element
        # from the current tree position
        pos = pos[:-1]
        path.append(pos)
        # if an S node is encountered, return the path and pos
        if tree[pos].label() == "S":
            still_looking = False
    return path, pos