from django.shortcuts import render
from flashcards.models import (
    Deck,
    Word
)
from django.views.generic.list import ListView


class DeckListView(ListView):
    model = Deck
    template_name = 'deck_list.html'
    paginate_by = 12


class DeckWordsListView(ListView):
    model = Word
    template_name = 'browse_deck.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = Deck.objects.get(id=self.kwargs.get('deck_id'))
        return context

    def get_queryset(self):
        return Word.objects.filter(deck__id=self.kwargs.get('deck_id'))
