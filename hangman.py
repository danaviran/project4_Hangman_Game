#################################################################
# FILE : ex4.py
# WRITER : Dana Aviran , dana.av , 211326608
# EXERCISE : intro2cs2 ex4 2022
# DESCRIPTION: Hangman game
#################################################################

import hangman_helper


def make_pattern(word):  # makes a pattern that is equal in length to word
    pattern = ""
    i = 0
    while i < len(word):
        pattern += '_'
        i += 1
    return pattern


def update_word_pattern(word, pattern, letter):  # updating the pattern
    i = 0
    while i < len(word):
        if word[i] == letter:  # if the index is a letter that is equal to letter
            pattern = pattern[:i] + letter + pattern[i + 1:]  # updating it
        i += 1
    return pattern


def filter_words_list(words, pattern, wrong_guess_lst):
    # returns all the words from thw word list that can be in the hint list
    new_lst = []
    i = 0
    while i < len(words):  # we go through all words in the list
        if len(pattern) == len(words[i]):  # if the length of words is equal
            j = 0  # we set an index for another loop
            boolean_val = True  # this value will tell us if the word is suited
            while j < len(words[i]):  # if it suits all the conditions
                if (pattern[j] != "_" and pattern[j] != words[i][j])\
                        or (pattern[j] == "_" and words[i][j] in pattern)\
                        or (words[i][j] in wrong_guess_lst):
                    boolean_val = False  # the word is not suited
                    break  # we break the inner loop
                j += 1  # else, we increase the index by one
            if boolean_val:
                new_lst.append(words[i])  # if the word is suited, we append it
        i += 1  # we increase the index by one
    return new_lst  # we return the list of all words that are suited


def make_short_hint_lst(hint_lst, length=hangman_helper.HINT_LENGTH):
    length_hint_list = len(hint_lst)
    short_hint_lst = []
    if length_hint_list > length:  # if the hint list is longer than length
        m = 0
        while len(short_hint_lst) < length:  # while the short one is shorter
            # we append to the short hint list the values of indexes
            # as written in the instructions file
            if (m * length_hint_list // length) < length_hint_list:
                if hint_lst[m * length_hint_list // length] \
                        not in short_hint_lst:
                    short_hint_lst.append(
                        hint_lst[m * length_hint_list // length])
            m += 1
        return short_hint_lst
    else:  # if the length of hint list and length value are equal
        return hint_lst


def run_single_game(word_list, score=hangman_helper.POINTS_INITIAL):
    if not word_list:  # if the word list is empty
        return score
    word = hangman_helper.get_random_word(word_list)  # we get a random word
    wrong_guess_list = []  # set the guess lists
    correct_guess_list = []
    msg = "good luck in your first game"
    pattern = make_pattern(word)  # we call the function to make a pattern
    while pattern != word and score > 0:
        # while the word was not found and the score is positive we start a
        # new round
        hangman_helper.display_state(pattern, wrong_guess_list, score, msg)
        # we display the state of round
        current_input = hangman_helper.get_input()
        # we take the input
        if current_input[0] == hangman_helper.HINT:  # if input is for a HINT
            score -= 1  # score goes down by one
            hint_lst = filter_words_list(word_list, pattern, wrong_guess_list)
            # use function the make a list of words that suit the hidden word
            short_hint_lst = make_short_hint_lst(hint_lst)
            # we make it shorter by calling another function
            hangman_helper.show_suggestions(short_hint_lst)
            # we show the short list to the player
        elif current_input[0] == hangman_helper.LETTER:
            # if the input is a letter - we check it carefully:
            if len(current_input[1]) > 1 or not current_input[1].islower():
                msg = "your input is not supported friend"
                continue
            elif current_input[1] in wrong_guess_list:
                msg = "you already tried this guess pal"
                continue
            elif current_input[1] in correct_guess_list:
                msg = "you are greedy. already tried this"
                continue
            else:  # if the letter is supported
                score -= 1  # score goes down by one
                if current_input[1] in word:  # if it is in the hidden word
                    pattern = update_word_pattern(word, pattern,  # update pattern
                                                  current_input[1])
                    # we calculate and update the score
                    num_success = word.count(current_input[1])
                    score += (num_success * (num_success + 1)) // 2
                    # we append the letter to the correct guess list
                    # it's not in instructions but it's important
                    correct_guess_list.append(current_input[1])
                    msg = "nice move sis"
                    continue  # we start another round
                else:  # if the letter is not in the hidden word
                    # we append the letter to the wrong guess list
                    wrong_guess_list.append(current_input[1])
                    msg = "the letter was not in the word bro"
                    continue  # we start another round
        elif current_input[0] == hangman_helper.WORD:  # if the input is a word
            score -= 1  # score goes down by one
            if current_input[1] == word:  # if the hidden word is the input
                num_success = pattern.count("_")  # we calculate score
                score += (num_success * (num_success + 1)) // 2  # add it
                pattern = word  # update pattern
                break  # break the loop (and the player wins)
            else:  # if the word is not correct
                msg = "the word you tried isn't correct"
    # the loop is done. there are two options:
    if pattern != word:  # pattern is different from word, the player loses
        msg = f"you lose the game. the word was {word}"
    elif score > 0 and pattern == word:  # the player wins
        msg = "we have a winner"
    # we display the state of the end of the game one lat time
    hangman_helper.display_state(pattern, wrong_guess_list, score, msg)
    return score


def main():  # the main function of the game
    word_list = hangman_helper.load_words()  # we load words from another file
    play_again = True  # we set a value
    # we set a value for the initial game score
    current_score = hangman_helper.POINTS_INITIAL
    num_of_games = 1  # we set the amount of one game
    while play_again:  # while the player asks to play again
        # we run a single game based on the current value of "current_score"
        current_score = run_single_game(word_list, current_score)
        # if the player won this game
        if current_score > 0:
            # we ask the player if he wants to play again
            play_again = hangman_helper.play_again \
                (f"number of games: {num_of_games} score: {current_score}"
                 f" do you want to play again?")
            if play_again:  # if he does, we increase the num of games by one
                num_of_games += 1
        else:  # if the player lost this games
            # we ask him if he wants to plat again
            play_again = hangman_helper.play_again \
                (f"number of games: {num_of_games} score: 0"
                 f" do you want to start a new round?")
            if play_again:  # if he does
                num_of_games = 1  # we set the initial value and score
                current_score = hangman_helper.POINTS_INITIAL
            # if he does not want another game, the function ends


if __name__ == '__main__':
    main()