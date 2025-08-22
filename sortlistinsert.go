package piscine

func SortListInsert(l *NodeI, data_ref int) *NodeI {
	newNode := &NodeI{Data: data_ref}

	// Case 1: List is empty or new node should be inserted at the beginning
	if l == nil || data_ref < l.Data {
		newNode.Next = l
		return newNode
	}

	// Case 2: Traverse and find the correct insertion point
	curr := l
	for curr.Next != nil && curr.Next.Data < data_ref {
		curr = curr.Next
	}

	newNode.Next = curr.Next
	curr.Next = newNode
	return l
}
