hobbs.py
________

Enter `python hobbs.py demo` to see a demo.

Otherwise, enter a file containing parsed sentences to search, with
one sentence per line, and then enter the pronoun you'd like to resolve, e.g., 

	python hobbs.py demosents.txt "He"
	python hobbs.py demosents.txt "it"
	python hobbs.py demorefl.txt "herself"

The sentences must use Treebank tags and be parsed such that they can be converted into
NLTK Trees. The pronoun must be in the last sentence of the file.

This program uses Hobbs’ algorithm to find the antecedent of a pronoun.
It has also been expanded to handle reflexive pronouns. The algorithm is given below:

1.	Begin at the NP node immediately dominating the pronoun
2.	Go up the tree to the first NP or S node encountered. 
	Call this node X and the path used to reach it p.
3.	Traverse all branches below node X to the left of path p in a
	left-to-right, breadth-first fashion. Propose as an antecedent
	any NP node that is encountered which has an NP or S node between
	it and X. 
4.	If node X is the highest S node in the sentence, traverse the
	surface parse trees of previous sentences in the text in order of
	recency, the most recent first; each tree is traversed in a
	left-to-right, breadth-first manner, and when an NP node is 
	encountered, it is proposed as an antecedent. If X is not the highest
	S node in the sentence, continue to step 5.
5.	From node X, go up the tree to the first NP or S node encountered. 
	Call this new node X, and call the path traversed to reach it p. 
6.	If X is an NP node and if the path p to X did not pass through the 
	Nominal node that X immediately dominates, propose X as the antecedent.
7.	Traverse all branches below node X to the left of path p in a 
	left-to-right, breadth-first manner. Propose any NP node encountered 
	as the antecedent.
8.	If X is an S node, traverse all the branches of node X to the right 
	of path p in a left-to-right, breadth-first manner, but do not go 
	below any NP or S node encountered. Propose any NP node encountered 
	as the antecedent. 
9.	Go to step 4. 

    """get_pos()Given a tree and a node, return the tree position
    of the node. 
    """ 

	"""get_dom_np()Finds the position of the NP that immediately dominates 
    the pronoun.

    Args:
        sents: list of trees (or tree) to search
        pos: the tree position of the pronoun to be resolved
    Returns:
        tree: the tree containing the pronoun
        dom_pos: the position of the NP immediately dominating
            the pronoun
    """

    """walk_to_np_or_s()Takes the tree being searched and the position from which 
    the walk up is started. Returns the position of the first NP
    or S encountered and the path taken to get there from the 
    dominating NP. The path consists of a list of tree positions.

    Args:
        tree: the tree being searched
        pos: the position from which the walk is started
    Returns:
        path: the path taken to get the an NP or S node
        pos: the position of the first NP or S node encountered
    """

    """bft()Perform a breadth-first traversal of a tree.
    Return the nodes in a list in level-order.

    Args:
        tree: a tree node
    Returns:
        lst: a list of tree nodes in left-to-right level-order
    """

	"""count_np_nodes()Function from class to count NP nodes.
    """

	"""check_for_intervening_np()Check if subtree rooted at pos contains at least 
    three NPs, one of which is: 
        (i)   not the proposal,
        (ii)  not the pronoun, and 
        (iii) greater than the proposal

    Args:
        tree: the tree being searched
        pos: the position of the root subtree being searched
        proposal: the position of the proposed NP antecedent
        pro: the pronoun being resolved (string)
    Returns:
        True if there is an NP between the proposal and the  pronoun
        False otherwise
    """

    """traverse_left()Traverse all branches below pos to the left of path in a
    left-to-right, breadth-first fashion. Returns the first potential
    antecedent found. 
    
    If check is set to 1, propose as an antecedent any NP node 
    that is encountered which has an NP or S node between it and pos. 

    If check is set to 0, propose any NP node encountered as the antecedent.

    Args:
        tree: the tree being searched
        pos: the position of the root of the subtree being searched
        path: the path taked to get to pos
        pro: the pronoun being resolved (string)
        check: whether or not there must be an intervening NP 
    Returns:
        tree: the tree containing the antecedent
        p: the position of the proposed antecedent
    """

    """traverse_right()Traverse all the branches of pos to the right of path p in a 
    left-to-right, breadth-first manner, but do not go below any NP 
    or S node encountered. Propose any NP node encountered as the 
    antecedent. Returns the first potential antecedent.

    Args:
        tree: the tree being searched
        pos: the position of the root of the subtree being searched
        path: the path taken to get to pos
        pro: the pronoun being resolved (string)
    Returns:
        tree: the tree containing the antecedent
        p: the position of the antecedent
    """

    """traverse_tree()Traverse a tree in a left-to-right, breadth-first manner,
    proposing any NP encountered as an antecedent. Returns the 
    tree and the position of the first possible antecedent.

    Args:
        tree: the tree being searched
        pro: the pronoun being resolved (string)
    """

    """match()Takes a proposed antecedent and checks whether it matches
    the pronoun in number and gender
    
    Args:
        tree: the tree in which a potential antecedent has been found
        pos: the position of the potential antecedent
        pro: the pronoun being resolved (string)
    Returns:
        True if the antecedent and pronoun match
        False otherwise
    """

    """number_match()Takes a proposed antecedent and pronoun and checks whether 
    they match in number.
    """

    """gender_match()Takes a proposed antecedent and pronoun and checks whether
    they match in gender. Only checks for mismatches between singular
    proper name antecedents and singular pronouns.
    """

    """hobbs()The implementation of Hobbs' algorithm.

    Args:
        sents: list of sentences to be searched
        pos: the position of the pronoun to be resolved
    Returns:
        proposal: a tuple containing the tree and position of the
            proposed antecedent
    """

    """resolve_reflexive()Resolves reflexive pronouns by going to the first S
    node above the NP dominating the pronoun and searching for
    a matching antecedent. If none is found in the lowest S
    containing the anaphor, then the sentence probably isn't 
    grammatical or the reflexive is being used as an intensifier.
    """

    """walk_to_s()Takes the tree being searched and the position from which 
    the walk up is started. Returns the position of the first S 
    encountered and the path taken to get there from the 
    dominating NP. The path consists of a list of tree positions.

    Args:
        tree: the tree being searched
        pos: the position from which the walk is started
    Returns:
        path: the path taken to get the an S node
        pos: the position of the first S node encountered
    """