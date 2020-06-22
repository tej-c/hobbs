from nltk.tree import * 
#import hobbs
dp1 = Tree('dp', [Tree('d', ['the']), Tree('np', ['dog'])])
dp2 = Tree('dp', [Tree('d', ['the']), Tree('np', ['cat'])])
vp = Tree('vp', [Tree('v', ['chased']), dp2])
tree = Tree('s', [dp1, vp])
#print(tree)
t=tree.treepositions()
#print(t)
#for i in tree:
   # print('\n',i,'\n')
#tr=Tree.fromstring('(S(NP(DT the)(N castle)(PP in(NP (N camelot))))(VP remained(NP (DT the)(N residence(PP of(NP (DT the)(N king)))))(PP until(NP (CD 536)(WRB when(SBAR (-NONE- 0)(S (NP he)(VP moved (NP it)(PP to(NP (N london)))))))))))')
#tr.pretty_print()
trr=Tree.fromstring('(S (NP (PRP He)) (VP (VBD showed) (NP (PRP it)) \
        (PP (IN to) (NP (NNP Terrence)))))')
for pos in trr.treepositions():
    if trr[pos] == 'PRP him':
        print (pos)
#print(trr.productions())
#trr.pretty_print()
tree7 =Tree.fromstring('(S(NP (DT the) (N castle) (PP in (NP (N camelot))))(VP remained(NP (DT the) (N residence (PP of (NP (DT the) (N king)))))(PP until(NP (CD 536) (WRB when  (SBAR (S (NP he) (VP moved (NP it) (PP to (NP (N london)))))))))))')
print(trr.productions())
#for pos in tree7.treepositions():
    #if tree7[pos] == 'he':
        #print (pos)