package piscine

func LoafOfBread(str string) string {
	runes := []rune(str)
	n := len(runes)
	i := 0
	words := []string{}

	for {
		wordRunes := []rune{}
		// Collect 5 non-space characters
		for i < n && len(wordRunes) < 5 {
			if runes[i] != ' ' {
				wordRunes = append(wordRunes, runes[i])
			}
			i++
		}

		if len(wordRunes) == 0 {
			break
		}

		// If first word has less than 5 chars, return Invalid Output
		if len(words) == 0 && len(wordRunes) < 5 {
			return "Invalid Output\n"
		}

		words = append(words, string(wordRunes))

		// Skip next character (if any)
		if i < n {
			i++
		}
	}

	// Join words with space and add newline
	output := ""
	for idx, w := range words {
		if idx > 0 {
			output += " "
		}
		output += w
	}
	output += "\n"
	return output
}
