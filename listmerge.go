package piscine

func ListMerge(l1 *List, l2 *List) {
	// If l1 is empty, just take l2's elements
	if l1.Head == nil {
		l1.Head = l2.Head
		l1.Tail = l2.Tail
		return
	}

	// If l2 is empty, nothing to do
	if l2.Head == nil {
		return
	}

	// Connect l1's tail to l2's head
	l1.Tail.Next = l2.Head
	// Update l1's tail to be l2's tail
	l1.Tail = l2.Tail

	// Clear l2 to avoid unexpected behavior
	l2.Head = nil
	l2.Tail = nil
}
