package piscine

func ListAt(l *NodeL, pos int) *NodeL {
	current := l
	count := 0

	for current != nil {
		if count == pos {
			return current
		}
		current = current.Next
		count++
	}
	return nil
}
