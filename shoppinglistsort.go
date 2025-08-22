package piscine

func ShoppingListSort(slice []string) []string {
	n := len(slice)
	for i := 0; i < n; i++ {
		minIndex := i
		for j := i + 1; j < n; j++ {
			if len(slice[j]) < len(slice[minIndex]) {
				minIndex = j
			}
		}
		// Swap elements
		slice[i], slice[minIndex] = slice[minIndex], slice[i]
	}
	return slice
}
