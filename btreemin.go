package piscine

func BTreeMin(root *TreeNode) *TreeNode {
	if root == nil {
		return nil
	}

	// In a BST, the minimum value is in the leftmost node
	current := root
	for current.Left != nil {
		current = current.Left
	}
	return current
}
