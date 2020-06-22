from hobbs import *
from nltk.parse.chart import BottomUpLeftCornerChartParser
import nltk
r = ["Himself", "himself", "Herself", "herself",
     "Itself", "itself", "Themselves", "themselves"]
p = ["He", "he", "Him", "him", "She", "she", "Her",
    "her", "It", "it", "They", "they",'he','He']
def convert_to_treebank(sentence):
    grammar = nltk.CFG.fromstring("""
S -> NP VP
NP -> NNP|DT JJ NN|DT NN
DT -> 'a'|'the'
JJ -> 'flashy'
NN -> 'hat'|'store'
PP -> IN NP
IN -> 'at'|'to'
NNP -> 'John'|'Mary'|'Tej'|'Terrence'
VP -> VBD SBAR
VBD -> 'said'
SBAR -> NONE S|S
NONE -> '.'
S -> NP VP
NP -> PRP
PRP -> 'he'|'herself'|'him'|'her'|'himself'|'she'|'He'|'it'
VP -> VBD NP|VBD NP PP
VBD -> 'likes'|'loves'|'knows'|'saw'|'showed'
NP -> NNS
NNS -> 'dogs'
 """)
    a=BottomUpLeftCornerChartParser(grammar)
    chart=a.chart_parse(sentence.split())
    parses = list(chart.parses(grammar.start()))
    #print("Total Edges :", len(chart.edges()))
    for parse in parses: 
        #print(parse.treepositions())
        parse.pretty_print()
        return parse
def resolve_reflexive(sents, pro):
    """ Resolves reflexive pronouns by going to the first S
    node above the NP dominating the pronoun and searching for
    a matching antecedent. If none is found in the lowest S
    containing the anaphor, then the sentence probably isn't 
    grammatical or the reflexive is being used as an intensifier.
    """
    pos=get_pos(sents[-1],pro)
    tree, pos = get_dom_np(sents, pos)

    pro = tree[pos].leaves()[0].lower()

    # local binding domain of a reflexive is the lowest clause 
    # containing the reflexive and a binding NP
    path, pos = walk_to_s(tree, pos)

    proposal = traverse_tree(tree, pro)

    return proposal
def hobbs(sents, pro):
    """ The implementation of Hobbs' algorithm.

    Args:
        sents: list of sentences to be searched
        pos: the position of the pronoun to be resolved
    Returns:
        proposal: a tuple containing the tree and position of the
            proposed antecedent
    """
    pos=get_pos(sents[-1],pro)
    # The index of the most recent sentence in sents
    sentence_id = len(sents)-1
    # The number of sentences to be searched
    num_sents = len(sents)
    
    # Step 1: begin at the NP node immediately dominating the pronoun
    tree, pos = get_dom_np(sents, pos)

    # String representation of the pronoun to be resolved
    pro = tree[pos].leaves()[0].lower()

    # Step 2: Go up the tree to the first NP or S node encountered
    path, pos = walk_to_np_or_s(tree, pos)
    
    # Step 3: Traverse all branches below pos to the left of path
    # left-to-right, breadth-first. Propose as an antecedent any NP
    # node that is encountered which has an NP or S node between it and pos
    proposal = traverse_left(tree, pos, path, pro)

    while proposal == (None, None):
        
        # Step 4: If pos is the highest S node in the sentence, 
        # traverse the surface parses of previous sentences in order
        # of recency, the most recent first; each tree is traversed in
        # a left-to-right, breadth-first manner, and when an NP node is
        # encountered, it is proposed as an antecedent
        if pos == ():
            # go to the previous sentence
            sentence_id -= 1
            # if there are no more sentences, no antecedent found
            if sentence_id < 0:
                return None
            # search new sentence
            proposal = traverse_tree(sents[sentence_id], pro)
            if proposal != (None, None):
                return proposal

        # Step 5: If pos is not the highest S in the sentence, from pos,
        # go up the tree to the first NP or S node encountered. 
        path, pos = walk_to_np_or_s(tree, pos)
        
        # Step 6: If pos is an NP node and if the path to pos did not pass 
        # through the nominal node that pos immediately dominates, propose pos 
        # as the antecedent.
        if "NP" in tree[pos].label() and tree[pos].label() not in nominal_labels:
            for c in tree[pos]:
                if isinstance(c, nltk.Tree) and c.label() in nominal_labels:
                    if get_pos(tree, c) not in path and match(tree, pos, pro):
                        proposal = (tree, pos)
                        if proposal != (None, None):
                            return proposal

        # Step 7: Traverse all branches below pos to the left of path, 
        # in a left-to-right, breadth-first manner. Propose any NP node
        # encountered as the antecedent.
        proposal = traverse_left(tree, pos, path, pro, check=0)
        if proposal != (None, None):
            return proposal

        # Step 8: If pos is an S node, traverse all the branches of pos
        # to the right of path in a left-to-right, breadth-forst manner, but
        # do not go below any NP or S node encountered. Propose any NP node
        # encountered as the antecedent.
        if tree[pos].label() == "S":
            proposal = traverse_right(tree, pos, path, pro)
            if proposal != (None, None):
                return proposal

    return proposal
sents = [convert_to_treebank(sents) for sents in input("Enter multiple sents: ").split(",")]
pros = [(pros) for pros in input("Enter multiple pros: ").split(",")] 
for i in range(len(pros)):
    if pros[i] in p:
        tree,pos=hobbs(sents,pros[i])
        print ("Proposed antecedent for '"+pros[i]+"':", tree[pos])
    elif pros[i] in r:
        tree,pos=resolve_reflexive(sents,pros[i])
        print ("Proposed antecedent for '"+pros[i]+"':", tree[pos])

