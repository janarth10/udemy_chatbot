#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 12:00:47 2019

@author: janarth
"""

# Building Deep NLP chatbot trained on movie dialogue

import numpy as np
import tensorflow as tf
import re
import time

# PART 1: DATA PREPROCESSING

lines = open('movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
conv_lines = open('movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

id2line = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]
        
conversations = [ ]
for line in conv_lines[:-1]:
    _line = line.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    conversations.append(_line.split(','))
    
# Sort the sentences into questions (inputs) and answers (targets)
questions = []
answers = []

for conv in conversations:
    for i in range(0, len(conv)-1, 2):
        questions.append(id2line[conv[i]])
        answers.append(id2line[conv[i+1]])
        

def clean_text(text):
    '''Clean text by removing unnecessary characters and altering the format of words.'''

    text = text.lower()
    
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"n'", "ng", text)
    text = re.sub(r"'bout", "about", text)
    text = re.sub(r"'til", "until", text)
    text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    
    return text

# Clean the data
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))
    
clean_answers = []    
for answer in answers:
    clean_answers.append(clean_text(answer))
    
    
# Create a dictionary for the frequency of the vocabulary
word2count = {}
for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
            
for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
            
            
#  Remove words below a certain frequency (aiming to remove 5% of words) 
#   and encode each word by mapping it to an integer
threshold = 20
question_words_to_int = {}
word_num = 0
for word, count in word2count.items():
    if count >= threshold:
        question_words_to_int[word] = word_num
        word_num += 1
        
answer_words_to_int = {}
word_num = 0
for word, count in word2count.items():
    if count >= threshold:
        answer_words_to_int[word] = word_num
        word_num += 1
        
        
# Add the unique tokens to the dictionaries. Order is important for Seq2Seq.
#   <PAD> - not sure
#   <EOS> - end of string
#   <OUT> - filtered out
#   <SOS> - start of string
        
tokens = ['<PAD>','<EOS>','<OUT>','<SOS>']

for code in tokens:
    questions_vocab_to_int[code] = len(questions_vocab_to_int)+1
    
for code in tokens:
    answers_vocab_to_int[code] = len(answers_vocab_to_int)+

# get inverse of answer_words_to_int
answer_ints_to_word = { word_int: word for word, word_int in answer_words_to_int.items()}

# add <EOS> to end of every answer
#   we add a space before <EOS> so the decode can differentiate between the 
#   last word in the sentence and the <EOS> token
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'


# Translate words in clean_questions/answers into integers
encoded_questions = []
for question in clean_questions:
    translation = []
    for word in question.split():
        if word not in question_words_to_int:
            translation.append(question_words_to_int['<OUT>'])
        else:
            translation.append(question_words_to_int[word])
    encoded_questions.append(translation)

encoded_answers = []
for answer in clean_answers:
    translation = []
    for word in answer.split():
        if word not in answer_words_to_int:
            translation.append(answer_words_to_int['<OUT>'])
        else:
            translation.append(answer_words_to_int[word])
    encoded_answers.append(translation)


# sort questions and answers by length of questions. removing questions over
#   length 25 to improve training.
sorted_questions = []
sorted_answers = []
for length in range(1, 26):
    for i in enumerate(encoded_questions):
        if len(i[1]) == length:
            sorted_questions.append(encoded_questions[i[0]])
            sorted_questions.append(encoded_answers[i[0]])




































