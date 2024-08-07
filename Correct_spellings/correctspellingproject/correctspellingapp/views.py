from django.shortcuts import render, redirect
from .sustain import vocab, probs
from .string_manupulation import edit_two_letters


def handler(request):
    result = None
    if request.method == 'POST':
        my_word = request.POST['Name']
        result = get_corrections(my_word, probs, vocab, verbose=False)
    else:
        redirect('homepage')
    return render(request, "index.html", {'response': result})


# suggest spelling suggestions
def get_corrections(word, probs, vocab, verbose=False):
    suggestions = []
    n_best = []
    suggestions = list(edit_two_letters(word).intersection(vocab))
    # suggestions = list(edit_two_letters(word, False).intersection(vocab))
    n_best = [[s, probs.get(s, -1)] for s in list(reversed(suggestions))]

    if verbose:
        print("suggestions = ", suggestions)

    return n_best