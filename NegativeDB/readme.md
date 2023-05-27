This is an project on creating negative databases that are hard to reverse-engineer at scale. Each record is a binary strings and created using the satisfiability of a 3-SAT problem which is NP-hard, making it harder to reverse engineer. I have taken care to use CRC code (with custom generator to handle errors in 1024 bit string) to reduce superfluous string which can be created in the random process. We have adapted core ideas in the [paper](Paper: https://crypto.stanford.edu/portia/papers/HardNDBFinal.pdf). Our DB uses trie (prefix tree) to make retrieval easy.

The implementation is in Python.

The list of code files.
- crc.py: This is the source code for the cyclic redundancy checks.

- db.py: the actual database source code.

- trie.py: This is the source code for the prefix tree for string search.

- textProcessing.py: This is used for managing textual input.

Run the code
$ python db.py

blog link: https://kenluck2001.github.io/blog_post/privacy_at_your_fingertips.html

