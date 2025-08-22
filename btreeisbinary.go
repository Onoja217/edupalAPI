package piscine

func BTreeIsBinary(root *TreeNode) bool {
	return isBSTHelper(root, "", "\uffff") // Using empty string as min, max as max Unicode char
}

func isBSTHelper(node *TreeNode, min, max string) bool {
	if node == nil {
		return true
	}
	// node.Data must be strictly greater than min and strictly less than max
	if node.Data <= min || node.Data >= max {
		return false
	}
	return isBSTHelper(node.Left, min, node.Data) && isBSTHelper(node.Right, node.Data, max)
}
