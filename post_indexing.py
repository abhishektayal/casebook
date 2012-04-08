import string
import re


def stop_words(word_list,stop_words_list):
    line_stop_words = []
    #stop_words = "a","i","it","am","at","on","in","of","to","is","so","too","my","the","and","but","are","very","here","even","from","them","then","than","this","that","though"
    #this part removes the stop words for the list of inputs
    without_stop_words=[]
    sent = ""
    word = ""
    for word in word_list:
        if word  not in stop_words_list:
        #new_string = new_string + word + " "
            without_stop_words.append(word)
        print new_string
        #new_string = string.split(new_string)
        #line_stop_words = line_stop_words + [new_string]
    return(line_stop_words)
    
def RemovePunc(recv_line):
    line = []
    i = 0
    
    
    #This part removes the punctuation and converts input text to lowercase
        
    
    new_char_string = "" 
    for char in recv_line:
      if char in string.punctuation:
         char = " "
 
      new_char_string = new_char_string + char
    new_char_string=new_char_string.lower()
    broken_line=re.findall(r'\w+', new_char_string)
    #print broken_line
    #print recv_line
      
    return broken_line






