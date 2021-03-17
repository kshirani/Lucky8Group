# Python Activity
#define a function count_threes(n)
#Part A (count_threes) now needs to return the multiple of three that occurs the most in a string.
# For example, 0939639 would return 9 since it appeared 3 times while the other multiple of three appeared less than that.
# You only need to worry about single digit multiples of 3 (3, 6, 9). You must use a dictionary to accomplish this.

def count_threes(n):
    multiples={                 # since there are only three single digit multiples of 3 we set up dictionary with initial count 0
        3:0,
        6:0,
        9:0
    }
    for number in n:            # iterate over the string to get each number
        if int(number)%3==0 and number!='0' :      # check if number is a non-zero multiple of 3
            multiples[int(number)]= multiples[int(number)] + 1  #increment count if it is
    return max(multiples,key=multiples.get)             # return key with maximum value


#define a function longest_consecutive_repeating_char(s)
#Part B (longest_consecutive_repeating_char) now needs to account for the edge case where two characters have
# the same consecutive repeat length. The return value should now be a list containing all characters with the longest
# consecutive repeat. For example, the longest_consecutive_repeating_char('aabbccd') would return ['a', 'b', 'c'] (order doesn't matter).
# You must use a dictionary to accomplish this.

def longest_consecutive_repeating_char(s):
    characters={}           # set up dictionary to keep count
    last_char=None          # keep track of last character
    for character in s:     # iterate over all the characters in string
        if character not in characters.keys():  # if character not in dictionary set it up
            characters[character]=1             # initial value of 1
        if character==last_char:                # if consequtive i.e. matches last character
            characters[character]=characters[character]+1   # increment count
        last_char=character                     # set current character as last character for next run
    #print(characters)
    results=[]                                  # list of results to be returned
    max_value=max(characters.values())          # find maximum value in dictionary
    for character in s:                         # iterate over all the characters in string
        if characters[character]==max_value and character not in results:   # if character is with maximum count and not included
            results.append(character)                                       # include it
    return results                              # return result

def is_palindrome(s):
    string=s.replace(' ','').lower()            # remove spaces and convert to lower case for comparison
    for i in range(0, int(len(string)/2)):      # set mid-point and iterate
        if string[i] != string[len(string)-i-1]:# check if nth character from beginning and end do not match
            return False                        # well then it's not a palindrome. Return false
    return True                                 # didn't fail any check so it is a palindrome. Return true
