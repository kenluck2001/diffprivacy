'''
Adapted from https://albertauyeung.github.io/2020/06/15/python-trie.html/
'''
MAXDEPTH = 20
class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        # a counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.counter = 0

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}

class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")

    def __insert (self, node, char):
        if char in node.children:
            node = node.children[char]
        else:
            # If a character is not found,
            # create a new node in the trie
            new_node = TrieNode(char)
            node.children[char] = new_node
            node = new_node

        return node

    def insert2(self, word):
        """Insert a word into the trie"""
        node = self.root
        
        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char == "*":
                for c in ("0", "1"):
                    node = self.__insert (node, c)
            else:
                node = self.__insert (node, char)
        
        # Mark the end of a word
        node.is_end = True

        # Increment the counter to indicate that we see this word once more
        node.counter += 1

    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root
        
        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            node = self.__insert (node, char)
        
        # Mark the end of a word
        node.is_end = True

        # Increment the counter to indicate that we see this word once more
        node.counter += 1

    def find(self, word):
        """find a word into the trie"""
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                break

        return node.is_end

    def remove(self, word):
        """remove a word into the trie"""
        node = self.root
        for letter in word[:-1]:
            if letter not in node.children:
                return False
            node = node.children[letter]

        # check last element
        if word[-1] in node.children:
            node.counter -= 1
            del node.children[word[-1]]
            return True

        return False

    def remove2(self, word):
        """remove a word into the trie. """
        node = self.root
        for letter in word[:-1]:
            if letter =="*":
                for c in ('0', '1'):
                    if c not in node.children:
                        return False
                    node = node.children[c]
            else:
                if letter not in node.children:
                    return False
                node = node.children[letter]

        # check last element
        if word[-1] in node.children:
            if word[-1] =="*":
                for c in ('0', '1'):
                    node.counter -= 1
                    del node.children[c]
            else:
                node.counter -= 1
                del node.children[word[-1]]
            return True

        return False
        
    def dfs(self, node, prefix, depth = 0):
        """Depth-first traversal of the trie
        
        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if depth == MAXDEPTH:
            return
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))
        
        for child in node.children.values():
            self.dfs(child, prefix + node.char, depth+1)
        
    def query(self, x):
        """Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by the number of 
        times they have been inserted
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        self.output = []
        node = self.root
        
        # Check if the prefix is in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []
        
        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1])

        # Sort the results in reverse order and return
        return sorted(self.output, key=lambda x: x[1], reverse=True)

if __name__ == '__main__':
    t = Trie()
    text = "was"
    print ("without saving text: {} is found: {}".format(text, t.find(text)))

    t.insert("***")
    t.insert("was")
    t.insert("word")
    t.insert("war")
    t.insert("what")
    t.insert("where")
    t.insert("zzzzz")
    print ("result match wh: {}".format(t.query("wh")) )

    text = "was"
    print ("text: {} is found: {}".format(text, t.find(text)))

    text = "ken"
    print ("text: {} is found: {}".format(text, t.find(text)))

    text = "zzzzz"
    print ("text: {} is found: {}".format(text, t.find(text)))
    t.remove(text)
    print ("text: {} is found: {}".format(text, t.find(text)))

    text = "zzz"
    t.remove(text)
    print ("text: {} is found: {}".format(text, t.find(text)))

    print ("result match wh: {}".format(t.query("wh")) )


