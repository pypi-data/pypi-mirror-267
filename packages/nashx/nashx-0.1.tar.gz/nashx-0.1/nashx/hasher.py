def hasher(words, length):
    asci = []
    for char in words:
        asci.append(ord(char))

    for i in range(len(asci)):
        newVal = asci[i]
        newVal = 3 * newVal + 1
        asci[i] = newVal

    for i in range(len(asci)):
        newVal = asci[i]
        newVal = newVal / 2.45
        asci[i] = newVal

    def normalize_to_range(numbers, target_min, target_max):
        min_val = min(numbers)
        max_val = max(numbers)

        normalized_numbers = [
            int(((num - min_val) / (max_val - min_val)) * (target_max - target_min) + target_min)
            for num in numbers
        ]

        return normalized_numbers

    final_asci = normalize_to_range(asci, 33, 126)

    final_asci1 = []

    for i in range(length):
        new_element = (final_asci[i % len(final_asci)] + i) % 94 + 33
        final_asci1.append(new_element)

    array_sum = sum(final_asci1)
    digit_sum = sum(int(digit) for digit in str(array_sum))

    final_asci2 = []
    if digit_sum % 7 == 0:
        for i in range(length):
            new_element = (final_asci[i % len(final_asci)] * (i + 1)) % 94 + 33
            final_asci2.append(new_element)
    elif digit_sum % 7 == 1 or digit_sum % 7 == 3 or digit_sum % 7 == 5:
        for i in range(length):
            new_element = (final_asci[i % len(final_asci)] ** (i + 2)) % 94 + 33
            final_asci2.append(new_element)
    else:
        for i in range(length):
            new_element = (abs(final_asci[i % len(final_asci)] - i)) % 94 + 33
            final_asci2.append(new_element)

    hashedWord = []

    for i in range(len(final_asci2)):
        character = chr(final_asci2[i])
        hashedWord.append(character)

    finalHash = ''.join(hashedWord)

    return finalHash