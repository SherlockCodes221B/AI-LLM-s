from django.core.cache import cache
import pickle

vocab_cache_key = 'vocab_cache'
probs_cache_key = 'probs_cache'
# this key is used to `set` and `get` your trained model from the cache

vocab = cache.get(vocab_cache_key)
probs = cache.get(probs_cache_key)

if vocab is None and probs is None:
    # your model isn't in the cache
    # so `set` it
    # load the pickle file
    vocab = pickle.load(open('correctspellingapp/vocab-spellings.pkl', 'rb'))
    cache.set(vocab_cache_key, vocab, None)
    probs = pickle.load(open('correctspellingapp/word-probability-spellings.pkl', 'rb'))
    cache.set(probs_cache_key, probs, None)
