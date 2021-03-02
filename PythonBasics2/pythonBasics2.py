# Python Activity
#
# Fill in the code for the functions below.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code. Make sure to add what is going to be returned.


# Part A. count_threes
# Define a function count_threes(n) that takes an int and

def count_threes(n):
  # YOUR CODE HERE:
  return int(n/3) #returns number of multiples of 3 in the range drom 0 to n including n



# Part B. longest_consecutive_repeating_char
# Define a function longest_consecutive_repeating_char(s) that takes
# a string s and returns the character that has the longest consecutive repeat.
def longest_consecutive_repeating_char(s):
  # YOUR CODE HERE:
  a=len(s)
  #declaring
  char=1
  consec=s[0]
  max= 1

  for i in range(0, a-1):
    if s[i] == s[i + 1]:
      char += 1

    else:
      if char > max:
        max = char
        consec=s[i]
      char = 1

  if char > max:
    max = char
    consec= s[i]
  return consec
#returns the character that has the longest consecutive repeat.





# Part C. is_palindrome
# Define a function is_palindrome(s) that takes a string s
# and returns whether or not that string is a palindrome.
# A palindrome is a string that reads the same backwards and
# forwards. Treat capital letters the same as lowercase ones
# and ignore spaces (i.e. case insensitive).
def is_palindrome(s):
  #YOUR CODE HERE:
  i = 0
  pa = len(s)-1 #(similar to circles activity)
 #declare

  while i <= pa:
    if s[i] == ' ':
      i += 1
      continue

    if s[pa] == ' ':
      pa -= 1
      continue

    #Treat capital letters the same as lowercase ones
    if s[i].lower() != s[pa].lower():
      return False
    i += 1
    pa -= 1
  return True #returns whether or not that string is a palindrome


