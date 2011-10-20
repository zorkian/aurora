'''aurora core -- provides the main classes

This mostly implements the Articles class that does all of the iteration
on the articles. It also implements the individual Article class.

'''

import os
import re

class Articles:
    '''Keeps track of all of the individual articles that exist.

    '''
    def __init__(self, path):
        self.by_slug = {}  # Slug -> Article
        self.by_recent = []  # [ Art, Art, Art... ] where 0 is oldest, -1 is most recent
        self.by_date = {}  # Yr -> { Mo -> [ ... ] }

        if not os.path.isdir(path):
            return
        for fn in os.listdir(path):
            ffn = os.path.join(path, fn)
            if not os.path.isfile(ffn):
                continue
            match = re.match(r'^(\d\d\d\d)-(\d\d)-(\d\d)-(.+)\.md$', fn)
            if match is None:
                continue
            yr, mo, da, slug = match.groups()
            if slug in self.by_slug:
                continue
            yr, mo, da = int(yr), int(mo), int(da)

            # Now we have an article, store it.
            art = Article(yr, mo, da, slug, ffn)
            self.by_slug[slug] = art
            self.by_recent.append(art)
            if yr not in self.by_date:
                self.by_date[yr] = {}
            if mo not in self.by_date[yr]:
                self.by_date[yr][mo] = []
            self.by_date[yr][mo].append(art)

        # Do a bunch of sorting.
        self.by_recent.sort()
        for yr in self.by_date:
            for mo in self.by_date[yr]:
                self.by_date[yr][mo].sort()
            

class Article:
    '''A single Article.

    '''
    def __init__(self, yr, mo, da, slug, ffn):
        self.time = '%d-%d-%d' % (yr, mo, da)
        self.year = yr
        self.month = mo
        self.day = da
        self.slug = slug
        self.filename = ffn
        self.props = {}
        self.content = ''

        with open(self.filename, 'r') as f:
            header = True
            for line in f:
                line = line.strip()
                if not header or len(line) <= 0 or not re.match(r'^.+?:.+?$', line):
                    self.content += line + '\n'
                    header = False
                else:
                    k, v = line.split(':', 1)
                    self.props[k.strip()] = v.strip()

    def __lt__(self, other):
        return self.time < other.time


