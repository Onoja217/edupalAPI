package piscine

func ListPushFront(l *List, data interface{}) {
	newNode := &NodeL{
		Data: data,
		Next: l.Head,
	}

	if l.Head == nil {
		l.Tail = newNode
	}

	l.Head = newNode
}
