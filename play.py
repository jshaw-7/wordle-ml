import numpy as np 
import pandas as pd 
import random

import string
import re

import colorama
from colorama import Fore
import helpers

with open('wordle-allowed-guesses.txt', 'r') as f:
    allowed = f.read().splitlines()
with open('wordle-answers-alphabetical.txt','r') as f:
    answers = f.read().splitlines()
allowed += answers

top_starting_words = helpers.getTopWords()

def get_guess(words, answers):
    guess = ''
    correct = 0
    while correct == 0:
        guess = input(Fore.RESET + 'input a 5-letter word: ')
        if len(guess) != 5:
            print(Fore.RESET + 'word must be 5 letters.')
        elif (guess not in words):
            print(Fore.RESET + 'please input a real word.')
        else:
            correct = 7
    return guess
    
def check_word(guess, status, choice):
    for i in range(5):
        for x in range(5):
            if guess[i] == choice[x] and x == i:
                status[i] = 2
                break
            elif guess[i] == choice[x]:
                status[i] = 1
                break
    return sum(status)

def print_word(guess, status):
    for i in range(5):
        if status[i] == 2:
            print(Fore.GREEN + guess[i], end = '')
        elif status[i] == 1:
            print(Fore.YELLOW + guess[i], end = '')
        else:
            print(Fore.RED + guess[i], end = '')
    print()

def play(choice):
    attempts = 0
    guesses = 6
    won = False
    
    print(Fore.GREEN + "this is WORDLE!")
    print(Fore.RESET + "you have 6 tries to guess the 5-letter word i'm thinking of ... ")

    for i in range(6):
        attempts +=1
        guess = get_guess(allowed, answers)
        status = [0, 0, 0, 0, 0]
        score = check_word(guess, status, choice)
        print('guess ' + str(i+1) + ": ")
        print_word(guess, status)
        if (score >= 10) or (choice == guess):
            won = True
            break
    if won:
        print(Fore.GREEN + "you won! the correct word was " + choice)
    else:
        print(Fore.RED + "you lost. the correct word was " + choice)
    return attempts, won

def solve(choice):
    possible = allowed
    guesses = 0
    while True:
        guesses +=1
        guess = make_guess(possible, guesses)
        print(Fore.RESET + "bot guess " + str(guesses) + ": "+ guess.upper())
        result = get_result(guess, choice)
        if result == "!!!!!":
            break
        possible = update_possible(possible, guess, result)
    return guesses

def get_result(guess, answer):
    result = ""
    for pos, ch_guess, ch_answer in zip(range(5), guess, answer):
        if ch_guess == ch_answer:
            result += "!"
        elif ch_guess not in answer:
            result += "_"
        else:
            result += "?"
    return result
  
def update_possible(possible, guess, result):
    return [word for word in possible if get_result(guess, word) == result]

def make_guess(possible, guess):
    for i in range(len(top_starting_words)):
        if top_starting_words[i] in possible:
            return top_starting_words[i]
    return random.choice(possible)


choice = answers[random.randint(0, len(answers))]
print(choice)

player, won = play(choice)
bot = solve(choice)

if not won:
    print(Fore.RED + ('you did not get the word "' + choice +'", and it took the ai ' + str(bot) + ' guesses. better luck next time!'))
elif (player < bot) and (player == 1):
    print(Fore.GREEN + ('the word "' + choice +'" took you ' + str(player) + ' guess and took the ai ' + str(bot) + ' guesses. good job!'))
elif(player <= bot):
    print(Fore.GREEN + ('the word "' + choice +'" took you ' + str(player) + ' guesses and took the ai ' + str(bot) + ' guesses. good job!'))
else:
    print(Fore.RED + ('the word "' + choice +'" took you ' + str(player) + ' guesses and took the ai ' + str(bot) + ' guesses. better luck next time!'))