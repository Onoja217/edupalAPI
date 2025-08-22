package piscine

type NodeI struct {
	Data int
	Next *NodeI
}

func ListSort(l *NodeI) *NodeI {
	// Base case: empty list or single element
	if l == nil || l.Next == nil {
		return l
	}

	// Split the list into two halves
	middle := getMiddle(l)
	nextToMiddle := middle.Next
	middle.Next = nil

	// Recursively sort both halves
	left := ListSort(l)
	right := ListSort(nextToMiddle)

	// Merge the sorted halves
	return merge(left, right)
}

// Helper function to get the middle node of a list
func getMiddle(head *NodeI) *NodeI {
	if head == nil {
		return head
	}

	slow, fast := head, head
	for fast.Next != nil && fast.Next.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}
	return slow
}

// Helper function to merge two sorted lists
func merge(a, b *NodeI) *NodeI {
	if a == nil {
		return b
	}
	if b == nil {
		return a
	}

	var result *NodeI
	if a.Data <= b.Data {
		result = a
		result.Next = merge(a.Next, b)
	} else {
		result = b
		result.Next = merge(a, b.Next)
	}
	return result
}
