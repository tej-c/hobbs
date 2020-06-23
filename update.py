from hobbs import *
from nltk.parse.chart import BottomUpLeftCornerChartParser
import nltk
r = ["Himself", "himself", "Herself", "herself",
     "Itself", "itself", "Themselves", "themselves"]
p = ["He", "he", "Him", "him", "She", "she", "Her",
    "her", "It", "it", "They", "they",'he','He']
def convert_to_treebank(sentence):
    grammar = nltk.CFG.fromstring("""
S -> NP VP|IN NP|NP VBD RP NP|NP VBD IN NP|PP NP PP NP NP VP NP
RP -> 'down' 
NP -> NNP|DT JJ NN|DT NN|DT NNS|NP VP|DT JJ JJ NN|NN|NNP NNP|NP NN|PRP NN
PRP -> 'my'
DT -> 'a'|'the'|'an'
JJ -> 'flashy'|'long'|'golden'|'little'|'yellow'
NN -> 'hat'|'store'|'dog'|'cat'|'hair'|'cup'|'coffee'|'story'|'mat'|'rabbit'|'elephant'|'pajamas'|'market'
PP -> IN NP |IN | NP IN
IN -> 'at'|'to'|'in'|'of'|'until'|'that'|'over'|'on'|'and'
NNP -> 'john'|'mary'|'tej'|'terrence'|'rapunzel'|'mr.'|'stone'|'alice'
VP -> VBD SBAR
VBD -> 'said'
SBAR -> S
NP -> 'he'|'herself'|'him'|'her'|'himself'|'she'|'He'|'it'|'his'|'i'|'they'
VP -> VBD NP|VBD NP PP|VRB PP|VRB|VP PP|VBD
VBD -> 'likes'|'loves'|'knows'|'saw'|'showed'|'liked'|'dumped'|'loved'|'let'|'barked'|'told'|'sit'|'chased'|'shot'|'went'|'drank'|'gave'|'is'|'going'|'was'|'buy'|'has'|'scared'|'went'
NP -> NNS|NP JJ JJ NN
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
    pos=get_pos(sents[-1],pro)
    tree, pos = get_dom_np(sents, pos)

    pro = tree[pos].leaves()[0].lower()

    # local binding domain of a reflexive is the lowest clause 
    # containing the reflexive and a binding NP
    path, pos = walk_to_s(tree, pos)

    proposal = traverse_tree(tree, pro)

    return proposal
def hobbs(sents, pro):
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
sents = [convert_to_treebank(sents.lower()) for sents in input("you can Enter multiple sents, (,) seperated: ").split(",")]
pros = [(pros.lower()) for pros in input("you can Enter multiple pros, (,) seperated: ").split(",")] 
for i in range(len(pros)):
    if pros[i] in p:
        tree,pos=hobbs(sents,pros[i])
        print ("Proposed antecedent for '"+pros[i]+"':", tree[pos])
    elif pros[i] in r:
        tree,pos=resolve_reflexive(sents,pros[i])
        print ("Proposed antecedent for '"+pros[i]+"':", tree[pos])

