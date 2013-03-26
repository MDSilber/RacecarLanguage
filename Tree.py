class Tree:
  def __init__(self):
    self.children = []
    self.value = None

  def printTree(self):
    print "(value: ", self.value,
    print ", children: [ ",
    for tree in self.children:
      if type(tree) == type(self):
        tree.printTree()
      else:
        print tree
      print ", ",
    print " ] ) ",
