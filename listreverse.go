package piscine

// ListReverse reverses the order of elements in a linked list
func ListReverse(l *List) {
	if l == nil || l.Head == nil {
		return
	}

	var prev *NodeL
	current := l.Head
	l.Tail = l.Head // The original head becomes the new tail

	for current != nil {
		next := current.Next
		current.Next = prev
		prev = current
		current = next
	}

	l.Head = prev // The last node processed becomes the new head
}
