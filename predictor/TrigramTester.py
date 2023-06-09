import argparse
import codecs
from collections import defaultdict
from tqdm import tqdm
import string


class TrigramTester:

    def __init__(self):

        # The mapping from words to identifiers.
        self.w2i = {}

        # The mapping from identifiers to words.
        self.i2w = {}

        # An array holding the unigram counts.
        self.unigram_count = defaultdict(int)

        # An array holding the bigram counts.
        self.bigram_prob = defaultdict(lambda: defaultdict(int))

        # An array holding the trigram counts.
        self.trigram_prob = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        # Number of unique words (i2w forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0

        self.lower = True

        self.CHARS = list(" abcdefghijklmnopqrstuvwxyz.'")
        self.CAP_CHARS = list(" abcdefghijklmnopqrstuvwxyz'ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.ALL_CHARS = [' ', '’', '—', '–', '“', '”', 'é', '‘'] + list(string.punctuation) + list(
            string.ascii_letters) + list(string.digits)

    def read_model(self, filename):
        """
        Reads the contents of the language model file into the appropriate data structures.

        :param filename: The name of the language model file.
        :return: true if the entire file could be processed, false otherwise.
        """
        print('reading model...')
        try:
            with codecs.open('./models/' + filename, 'r', 'utf-8') as f:
                metadata = f.readline().strip().split()
                self.unique_words, self.total_words = map(int, metadata[:2])
                self.lower = metadata[2]

                for i in range(self.unique_words):
                    index, word, count = f.readline().strip().split()
                    self.w2i[word] = int(index)
                    self.i2w[i] = word
                    self.unigram_count[i] = int(count)
                self.unigram_count = sorted(self.unigram_count.items(), key=lambda x: x[1], reverse=True)

                f.readline()

                for line in f:
                    if line.strip() == "-2":
                        break
                    i, j, log_p = line.strip().split()
                    self.bigram_prob[int(i)][int(j)] = float(log_p)
                for i in self.bigram_prob.keys():
                    # sort in reverse to get decreasing probabilities
                    self.bigram_prob[i] = sorted(self.bigram_prob[i].items(), key=lambda x: x[1], reverse=True)

                for line in f:
                    if line.strip() == "-3":
                        break
                    i, j, k, log_p = line.strip().split()
                    self.trigram_prob[int(i)][int(j)][int(k)] = float(log_p)
                for i, w1 in self.trigram_prob.items():
                    for j, w2 in w1.items():
                        # sort in reverse to get decreasing probabilities
                        self.trigram_prob[i][j] = sorted(self.trigram_prob[i][j].items(), key=lambda x: x[1],
                                                         reverse=True)

                return True
        except IOError:
            print("Couldn't find bigram probabilities file {}".format(filename))
            return False

    def predict(self, w0="", w1=None, w2=None):
        """
        Gives the top 3 predictions from the model given, if available, the current word and the previous two
        """
        predictions = []
        options = None

        if w1:
            key = self.w2i.get(w1, -1)
            options = self.bigram_prob.get(key, None) if not w2 else self.trigram_prob.get(self.w2i.get(w2, -1),
                                                                                           {}).get(key, None)

        options = options or self.unigram_count

        if options:
            predictions = [self.i2w[i] for (i, _) in options if self.i2w[i].startswith(w0)][:3]

        return predictions


    def interactive_word_predictor(self):
        print("Interactive word predictor session started...")

        while True:
            inp_string = input()
            if inp_string.strip().lower() == "exit":
                break
            elif inp_string == "":
                continue

            if inp_string.endswith(" "):
                last_word = ""
            else:
                last_word = inp_string.split()[-1]

            words = inp_string.strip().split()
            seq_size = len(words)
            if seq_size == 0:
                continue

            predictions = []
            w1 = words[seq_size - 2] if seq_size >= 2 else None
            w2 = words[seq_size - 3] if seq_size >= 3 else None

            predictions = self.predict(w0=last_word, w1=w1, w2=w2)

            l = len(predictions)
            for i in range(l - 1):
                print(predictions[i], end=' | ')
            print(predictions[l - 1])

    def clean_line(self, line):
        dirty = line.split(" ")
        cleaned = []
        for w in dirty:
            if self.lower:
                cleaned.append(w.lower())
            else:
                cleaned.append(w)
        return cleaned

    def text_gen(self, f):
        with open(f, encoding='utf8', errors='ignore') as f:
            for line in f:
                yield self.clean_line(line)

    def verify_prediction(self, prefix="", word1=None, word2=None):
        """
        Verify the top predictions from the model, return the length of the prediction - length of prefix if matched
        """
        for prediction in self.predict(prefix, word1, word2):
            if prediction.startswith(prefix):
                return len(prediction) - len(prefix)
        return 0

    def compute_keystrokes(self, test_filename):
        """
        Calculate and display the proportion of saved keystrokes for a test file
        """
        saved_keystrokes, total_keystrokes = 0, 0

        for line in tqdm(self.text_gen(test_filename), desc="computing proportion of saved keystrokes", total=1000):
            for i, word in enumerate(line):
                prev_word1 = line[i - 1] if i >= 1 else None
                prev_word2 = line[i - 2] if i >= 2 else None

                for j in range(len(word) + 1):
                    prefix = word[:j]
                    saved_keystrokes += self.verify_prediction(prefix, prev_word1, prev_word2)
                    total_keystrokes += len(word)

        saved_proportion = saved_keystrokes / total_keystrokes if total_keystrokes else 0
        print(f"Proportion of saved keystrokes: {saved_proportion:.6f}")


def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Word Predictor')
    parser.add_argument('--interactive', '-i', action='store_true')
    parser.add_argument('--model', '-m', type=str, default='trigram_twitter.txt', help='file with language model')
    parser.add_argument('--keystrokes', '-k', type=str, required=False,
                        help='input a test file to compute the average number of saved keystrokes on')
    arguments = parser.parse_args()

    predictor = TrigramTester()
    predictor.read_model(arguments.model)

    if arguments.interactive:
        predictor.interactive_word_predictor()

    if arguments.keystrokes:
        predictor.compute_keystrokes(arguments.keystrokes)


if __name__ == "__main__":
    main()