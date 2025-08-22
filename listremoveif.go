package piscine

func ListRemoveIf(l *List, data_ref interface{}) {
	// Remove all matching nodes from the head
	for l.Head != nil && l.Head.Data == data_ref {
		l.Head = l.Head.Next
	}

	// If list became empty
	if l.Head == nil {
		l.Tail = nil
		return
	}

	// Remove matching nodes in the middle
	current := l.Head
	for current.Next != nil {
		if current.Next.Data == data_ref {
			current.Next = current.Next.Next
			// If we removed the last node, update Tail
			if current.Next == nil {
				l.Tail = current
			}
		} else {
			current = current.Next
		}
	}
}
