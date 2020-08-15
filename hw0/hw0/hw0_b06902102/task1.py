# AI20S - HW0
# Student ID                :B06902102
# English Name              :Fernando Lopez
# Chinese Name (optional)   :羅費南


class Node(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    def sum_of_left_leaves(self, _root):
        """
        :type _root: Node
        :return type: int
        """
        # your code
        if _root is None:
            return 0
        a = 0
        b = 0
        if _root.left is None:
            a = 0
        else:
            if _root.left.left is None and _root.left.right is None:
                a = _root.left.val
            a += self.sum_of_left_leaves(_root.left)
        if _root.right is None:
            b = 0
        else:
            b = self.sum_of_left_leaves(_root.right)
        return a + b


if __name__ == '__main__':
    # build tree
    root = Node(3)
    root.left = Node(9)
    root.right = Node(20)
    root.right.left = Node(15)
    root.right.right = Node(7)
    root.right.right.left = Node(2)
    sol = Solution()
    print(sol.sum_of_left_leaves(root))


