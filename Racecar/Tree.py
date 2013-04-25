class Tree:
    def __init__(self):
        self.children = []
        self.value = None
        self.type = None
        self.errors = []

    def printTree_old(self):
        print "(value: ", self.value,
        print ", children: [ ",
        for tree in self.children:
            if type(tree) == type(self):
                tree.printTree()
            else:
                print tree,
            print ", ",
        print " ] ) ",

    def printTree(self):
        if self.value != "empty" and len(self.children) != 0:
            print self.value, "(", self.type, ") -> ",
            for child in self.children:
                if type(child) == type(self):
                    print child.value, "(", child.type, ") ",
                else:
                    print child, " ",
            print
            for child in self.children:
                if type(child) == type(self):
                    child.printTree()
