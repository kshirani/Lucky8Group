import pythonBasics2

# main() is already set up to call the functions
# we want to test with a few different inputs,
# printing 'OK' when each function is correct.
# the simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.

def test(got, expected):
    prefix = ' OK ' if got == expected else '  X '
    print ('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))

def main():
    # set which functions to test
    check_count_threes = True
    check_longest_consecutive_repeating_char = False
    check_is_palindrome = False

    if check_count_threes:
        print('Testing count_threes:')
        test(pythonBasics2.count_threes(0), 0)
        test(pythonBasics2.count_threes(2), 0)
        test(pythonBasics2.count_threes(3), 1)
        test(pythonBasics2.count_threes(6), 2)
        test(pythonBasics2.count_threes(24), 8)

    if check_longest_consecutive_repeating_char:
        print("---------------------------------------------------------")
        print('longest_consecutive_repeating_charater')
        test(pythonBasics2.longest_consecutive_repeating_char('aaa'), 'a')
        test(pythonBasics2.longest_consecutive_repeating_char('abba'), 'b')
        test(pythonBasics2.longest_consecutive_repeating_char('caaddda'), 'd')
        test(pythonBasics2.longest_consecutive_repeating_char('aaaffftttt'), 't')
        test(pythonBasics2.longest_consecutive_repeating_char('aaababbacccca'), 'c')
        test(pythonBasics2.longest_consecutive_repeating_char('ddabab'), 'd')
        test(pythonBasics2.longest_consecutive_repeating_char('caac'), 'a')

    if check_is_palindrome:
        print("-------------------------------------------------------")
        print('Testing is_palindrome')
        test(pythonBasics2.is_palindrome("Hello"), False)
        test(pythonBasics2.is_palindrome("civic"), True)
        test(pythonBasics2.is_palindrome("Civic"), True)
        test(pythonBasics2.is_palindrome("Racecar"), True)
        test(pythonBasics2.is_palindrome("Dont nod"), True)
        test(pythonBasics2.is_palindrome("was it a cat I saw"), True)
        test(pythonBasics2.is_palindrome("It was not a cat"), False)


if __name__ == '__main__':
  main()
