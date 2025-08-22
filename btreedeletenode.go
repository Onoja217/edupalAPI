package piscine

func BTreeDeleteNode(root, node *TreeNode) *TreeNode {
	if node == nil {
		return root
	}

	// Case 1: node has no left child
	if node.Left == nil {
		root = BTreeTransplant(root, node, node.Right)
	} else if node.Right == nil {
		// Case 2: node has no right child
		root = BTreeTransplant(root, node, node.Left)
	} else {
		// Case 3: node has two children
		// Get the minimum node in the right subtree (successor)
		successor := BTreeMin(node.Right)
		if successor.Parent != node {
			root = BTreeTransplant(root, successor, successor.Right)
			successor.Right = node.Right
			if successor.Right != nil {
				successor.Right.Parent = successor
			}
		}
		root = BTreeTransplant(root, node, successor)
		successor.Left = node.Left
		if successor.Left != nil {
			successor.Left.Parent = successor
		}
	}
	return root
}
