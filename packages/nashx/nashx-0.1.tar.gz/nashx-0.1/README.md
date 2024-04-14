This custom-made hashing algorithm is ASCII based Algorithm, where set of operations are performed onto the ASCII value of the input string and then once those operations are completed the resulting values are converted back into printable characters by mapping the value (modified ASCII) to its corresponding character.

1.	Working of this Hashing Algorithm:
ASCII Conversion: The function first converts each character in the input string to its ASCII value and stores these values in a list called asci.
2.	Transformation Step 1: Each ASCII value is then transformed by multiplying it by 3 and adding 1.
3.	Transformation Step 2: Each resulting value from the previous step is divided by 2.45.
4.	Normalization: The normalize_to_range function normalizes the transformed ASCII values to a specified range (33 to 126 in this case, corresponding to printable ASCII characters). This ensures that the final ASCII values can be converted back to printable characters.
5.	Length Adjustment and Modulation: The code then creates a new list, final_asci1, by looping over the normalized ASCII values. It ensures the list has the same length as specified by the length parameter. For each index, it calculates a new value by adding the index to the corresponding ASCII value, modulo 94 (to keep it within the printable ASCII range), and then adding 33 to shift it back into the printable range.
6.	Summation and Condition: The sum of the elements in final_asci1 is calculated. Then the sum of the digits of this sum is found (digit_sum). Depending on the value of digit_sum modulo 7, one of three different transformations is applied to create a new list, final_asci2:
•	If digit_sum % 7 is 0, each value is multiplied by its index (plus one), modulo 94, plus 33.
•	If digit_sum % 7 is 1, 3, or 5, each value is raised to the power of (index + 2), modulo 94, plus 33.
•	Otherwise, the absolute difference between each value and its index is taken, modulo 94, plus 33.
7.	Character Conversion: The values in final_asci2 are converted back to characters using the chr function.
8.	Final Hash Generation: The characters are concatenated to form the final hashed string, which is returned by the function.



Examples:
1.	Input: Naman, 15
Output: “Xc:;C89n3K:]t}k”

2.	Input: naman, 15
Output: “AA7?=<<2:877-53”

3.	Input: MMCOE, 15
Output: “10@>M,+;9H'&64C”

4.	Input: mMMCoE, 15
Output: “h/%|CR$3A0=*bSe”


Above are few Examples of the Hashes generated for the given input of the data. Also, the examples show the Avalanche Effect, which is that changing of one-character results in generation of entirely new hash even if its just a difference of uppercase and lowercase.
