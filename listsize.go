package piscine

func ListSize(l *List) int {
	size := 0
	for current := l.Head; current != nil; current = current.Next {
		size++
	}
	return size
}
