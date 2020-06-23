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
trr=Tree.fromstring("(S(NP I)(VP(VP (V shot) (NP (Det an) (N elephant)))(PP (P in) (NP (Det my) (N pajamas)))))")
for pos in trr.treepositions():
    if trr[pos] == 'PRP him':
        print (pos)
#ṇprint(trr.productions())
trr.pretty_print()
tree7 =Tree.fromstring('(S(NP (DT the) (N castle) (PP in (NP (N camelot))))(VP remained(NP (DT the) (N residence (PP of (NP (DT the) (N king)))))(PP until(NP (CD 536) (WRB when (S (NP he) (VP moved (NP it) (PP to (NP (N london))))))))))')
print(tree7.productions())
tree7.pretty_print()
#for pos in tree7.treepositions():
    #if tree7[pos] == 'he':
        #print (pos)

#(S(NP (DT the)(JJ little)(JJ yellow)(NN dog))(VBD barked)(IN at)(NP (DT the)(NN cat)))