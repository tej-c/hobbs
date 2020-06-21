from nltk.tree import *
import hobbs
dp1 = Tree('dp', [Tree('d', ['the']), Tree('np', ['dog'])])
dp2 = Tree('dp', [Tree('d', ['the']), Tree('np', ['cat'])])
vp = Tree('vp', [Tree('v', ['chased']), dp2])
tree = Tree('s', [dp1, vp])
#print(tree)
t=tree.treepositions()
#print(t)
for i in tree:
    print('\n',i,'\n')
