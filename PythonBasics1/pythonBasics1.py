# Python Activity
#
# Fill in the code for the functions below.
# The starter code for each function includes a 'return'
# which is just a placeholder for your code. Make sure to add what is going to be returned.

# Part A. count_char
# Define a function count_char(s, char) that takes a string and a character
# and returns the number of times the given character appears in the string
def count_char(s, char):
    #start by initializing the count variable
  count = 0

  #iterating over the string s

  for ch in s:
    #checking if current character matches with the given character
    if ch==char:
      count+=1 #increment the count

  #return count of char in s
  return count


# Part B. is_power_of
# Define a function is_power_of(i,j) that takes 2 ints i and j
# and checks if i is a power of j or not
# the function should return True indicating that i is a power of j
# otherwise return False
def is_power_of(i,j):
  # YOUR CODE HERE
  #check for base condition
  if j==1 and i!=0:
    return True
  if j==1 and i==0 :
    return False
  if i==1 and j!=1:
    return False


  #finding the correct power

  # take absoute value for easy calculation
  base = abs(i)
  num = abs(j)
  power = 1

  if base<num:
    #if i is smaller then j
    #getting the positive power
    while base<num:
      power +=1
      #increment power

      #getting new base
      base = abs(i)**power

  else :
    #if i is bigger then j
    #getting negative power
    while base<num:
      #increment power
      power -= 1


      base = abs(i)**power

  #rasing i to the power to required power
  # & check if it is equal or not
  return i**power == j


# Part C. longest_word
# Define a function longest_word(s) that takes a string s
# where s is a sentence made up of words separated by a single space " "
# and returns the longest word in this sentence
# if 2 or more words are tied as longest then return the one that occurs LAST in the sentence
# if s is an empty string return an empty string
def longest_word(s):
  # YOUR CODE HERE
  ans = ""

  #creating the list of all the words
  words = s.split(" ")

  #check Every word in words

  for word in words:
    #check if length of current word is more or the same
    if length(word)>=length(ans):

      #update answer
      ans = word

  return ans

