package piscine

// ListClear deletes all nodes from the linked list
func ListClear(l *List) {
	if l == nil {
		return
	}
	l.Head = nil
	l.Tail = nil
}
