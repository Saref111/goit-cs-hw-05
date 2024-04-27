import requests
import matplotlib.pyplot as plt
import operator
from mr import map_reduce

def visualize_top_words(word_freqs, top_n=10):
    top_words = dict(sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)[:top_n])
    plt.bar(top_words.keys(), top_words.values())
    plt.show()


if __name__ == '__main__':
    url = 'http://google.com'
    response = requests.get(url)
    text = response.text

    word_freqs = map_reduce(text)
    visualize_top_words(word_freqs)