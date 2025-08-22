package piscine

func BTreeMax(root *TreeNode) *TreeNode {
	if root == nil {
		return nil
	}

	// In a BST, the max value is always in the rightmost node
	current := root
	for current.Right != nil {
		current = current.Right
	}
	return current
}
