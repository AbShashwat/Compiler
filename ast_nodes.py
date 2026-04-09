class ASTNode:

    def __init__(self, node_type, value=None):
        self.type = node_type
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"ASTNode({self.type}, {self.value})"