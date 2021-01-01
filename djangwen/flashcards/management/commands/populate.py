import os
import re
from django.core.management import BaseCommand
from djangwen import settings
from flashcards.helpers import get_chinese
from flashcards.models import (
    Deck,
    Word
)


class Command(BaseCommand):
    def handle(self, **kwargs):
        path = settings.BASE_DIR + '/hsk_vocabulary/'
        full_path = os.path.abspath(path)
        for filename in os.listdir(full_path):
            file_path = os.path.join(full_path, filename)
            assert os.path.isabs(file_path)
            hsk = int(re.findall(r'\d+', filename)[0])
            with open(file_path, encoding='utf-8') as f:
                raw = f.read()
                lines = raw.split('\n')
                structures = set(len(l.split('\t')) for l in lines)
                assert len(structures) == 1
                for l in lines:
                    data = l.split('\t')
                    fields = {
                        'zi_simp': get_chinese(data[0]),
                        'zi_trad': get_chinese(data[1]),
                        'pinyin_number': data[2],
                        'pinyin_tone': data[3],
                        'english': data[4],
                        'hsk': hsk,
                    }
                    # w = Word(**fields)
            self.stdout.write('File "%s" processed.' % (filename))