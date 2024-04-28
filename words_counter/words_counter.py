import requests
import matplotlib.pyplot as plt
import operator
import queue
import threading
from mr import map_reduce

def count_words(text, q):
    word_freqs = map_reduce(text)
    q.put(word_freqs)

def visualize_top_words(word_freqs, top_n=10):
    top_words = dict(sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)[:top_n])
    plt.bar(top_words.keys(), top_words.values())
    plt.show()


if __name__ == '__main__':
    url = 'http://google.com'
    response = requests.get(url)
    text = response.text

    num_threads = len(text) // 1000 
    text_chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]

    q = queue.Queue()
    threads = []

    for chunk in text_chunks:
        t = threading.Thread(target=count_words, args=(chunk, q))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

    word_freqs = {}
    while not q.empty():
        chunk_freqs = q.get()
        for word, freq in chunk_freqs.items():
            if word in word_freqs:
                word_freqs[word] += freq
            else:
                word_freqs[word] = freq

    visualize_top_words(word_freqs)