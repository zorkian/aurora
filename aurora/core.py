'''aurora core -- provides the main classes

This mostly implements the Articles class that does all of the iteration
on the articles. It also implements the individual Article class.

'''

import os
import re

class Articles:
    '''Keeps track of all of the individual articles that exist.

    '''
    def __init__(self, path, formatter):
        self.by_slug = {}  # Slug -> Article
        self.by_recent = []  # [ Art, Art, Art... ] where 0 is oldest, -1 is most recent
        self.by_date = {}  # Yr -> { Mo -> [ ... ] }
        self.on_index = []  # [ Art, Art, Art... ]

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
            art = Article(yr, mo, da, slug, ffn, formatter)
            if not art.publish:
                continue
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

        # Construct the index of the most recent N.
        self.on_index = self.by_recent[-3:]
        self.on_index.reverse()


class Article:
    '''A single Article.

    '''
    def __init__(self, yr, mo, da, slug, ffn, formatter):
        self.time = '%d-%d-%d' % (yr, mo, da)
        self.year = yr
        self.month = mo
        self.day = da
        self.slug = slug
        self.filename = ffn
        self.props = {}
        self.content = ''
        self.raw_content = ''
        self.title = 'no title'
        self.publish = True
        self.date = '%04d-%02d-%02d' % (yr, mo, da)
        self.time = '00:00'
        self.categories = []
        self.subtitle = ''

        with open(self.filename, 'r') as f:
            header = True
            for line in f:
                tline = line.strip()
                if not header or len(tline) <= 0 or not re.match(r'^.+?:.+?$', line):
                    self.raw_content += line.rstrip() + '\n'
                    header = False
                else:
                    k, v = tline.split(':', 1)
                    self._set_prop(k, v)
        self.content = formatter(self.raw_content)

    def _set_prop(self, prop, val):
        '''Given a property (such as from a post), set that on
        ourselves.  This is an internal method.

        '''
        prop = prop.lower().strip()
        val = val.strip()

        if prop == 'publish':
            self.publish = True if val == 'yes' else False
        elif prop == 'time':
            self.time = val
        elif prop == 'categories':
            self.categories = [x.strip() for x in val.split(',')]
        elif prop == 'subtitle':
            self.subtitle = val
        elif prop == 'title':
            self.title = val

    def __lt__(self, other):
        '''Internal: for sorting these objects.

        '''
        if self.date == other.date:
            return self.time < other.time
        return self.date < other.date

