import csv
from collections import defaultdict


class SatorFinder:

    def __init__(self, file_path):

        self._char_0 = defaultdict(set)
        self._char_1 = defaultdict(set)
        self._char_2 = defaultdict(set)
        self._char_3 = defaultdict(set)
        self._char_4 = defaultdict(set)
        self._palindrome = []
        self._words = []
        self.solutions = []

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row[0]) == 5:
                    self.add_word(row[0])

    def add_word(self, word: str):
        word_idx = len(self._words)
        self._words.append(word)
        self._char_0[word[0]].add(word_idx)
        self._char_1[word[1]].add(word_idx)
        self._char_2[word[2]].add(word_idx)
        self._char_3[word[3]].add(word_idx)
        self._char_4[word[4]].add(word_idx)

        if word == word[::-1]:
            self._palindrome.append(word)

    def find(self):
        for palindrome in self._palindrome:
            first_row_words = self._find_reversible_words_with_middle_char(palindrome[0])

            self._find_solutions(first_row_words, palindrome)

        print("----------------")

        with open('solutions.txt', 'w') as f:
            for solution in self.solutions:
                for word in solution:
                    print(word)
                    f.write(word)
                    f.write('\n')

                print("----------------")
                f.write("--------------\n")
            msg = f"Total solutions: {len(self.solutions)}"
            print(msg)
            f.write(msg)

    def _find_reversible_words_with_middle_char(self, char):
        words_idx = self._char_2.get(char)
        result_words = []
        for idx in words_idx:
            word = self._words[idx]
            reversed_word = word[::-1]
            if reversed_word in self._words and reversed_word not in result_words:
                result_words.append(self._words[idx])
        return result_words

    def _find_solutions(self, first_row_words, palindrome):
        middle_char = palindrome[1]
        for first_row_word in first_row_words:
            first_char = first_row_word[1]
            last_char = first_row_word[3]
            second_row_candidates = self._char_2[middle_char].intersection(
                self._char_0[first_char]).intersection(self._char_4[last_char])

            if not second_row_candidates:
                continue

            for word_idx in second_row_candidates:
                word = self._words[word_idx]
                reversed_word = word[::-1]
                if reversed_word in self._words:
                    reversed_first_row_word = first_row_word[::-1]
                    self.solutions.append(
                        [
                            first_row_word,
                            word,
                            palindrome,
                            reversed_word,
                            reversed_first_row_word
                        ]
                    )


if __name__ == '__main__':

    print('Calculando Sator squares')
    finder = SatorFinder('es.txt')
    finder.find()

