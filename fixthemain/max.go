package piscine

func Max(a []int) int {
	if len(a) == 0 {
		return 0
	}
	max := a[0]
	for _, num := range a[1:] {
		if num > max {
			max = num
		}
	}
	return max
}
