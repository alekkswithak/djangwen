from django.shortcuts import render
from flashcards.models import (
    Deck
)
from django.views.generic.list import ListView


class DeckListView(ListView):
    model = Deck
    template_name = 'deck_list.html'
    paginate_by = 12
