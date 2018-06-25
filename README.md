# Compile


 Running the tests:

- The program needs 3 arguments for its operation. These are the names of the train data, test data and output file.


 Sample run code:

$ python3 assignment3.py train-S1.pos test-S1.pos out.txt



 Explanation of functions:

 main():
 
- The Main function reads the train and test data and sends it to other functions.


 read_test_data(array,word_dictionary,tag_dictionary,count):
 
 
- This function calculates which class the test data belongs to.

- This function prints the results in the output file.

 read_input(array,p):
 
 
- This function parse the train data and keep the words in the dictionary according to the positions.

- This function parse tags in train data and keep them in dictionary.

 calculate_tag(word):
 
 
- This function calculates the tag.


 calculate_probability(word_dictionary,tag_dictionary,x,k,temp,tag4,lex):
 
 
- This function calculates which sense_id belongs to the input read.

 

 Average duration of the program:
 
- It takes about 3-4 seconds to do all the operations.
 
Authors: Sergen Topcu




