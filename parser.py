import bz2, re

path = '/home/han/Documents/zhwiki.xml.bz2'
path2 = 'sample.xml'


class Buffer:
    """
    A buffer for one wiki page
    """
    def __init__(self, fp):
        self.content = ''
        self.full = False
        self.loading = False
        self.path = fp

    def reset(self):
        self.content = ''
        self.full = False

    def fetch_line(self, l):
        if bool(re.search(r'\<page', l)):
            self.content += l.strip()
            self.loading = True
        elif bool(re.search(r'\<\/page', l)):
            self.content += l.strip()
            self.loading = False
            self.full = True
        elif self.loading:
            self.content += l.strip()

    def fetch(self):
        a = []
        with open(self.path, 'r') as f:
            for l in f:
                self.fetch_line(l)
                if self.full:
                    a += [self.dump()]
        return a

    def dump(self):
        c = self.content
        self.reset()
        return c


class Corpus:
    """
    Indexed text
    """
    def __init__(self, s, p=0):
        self.t = s
        self.pos = (p, p+len(s))

    def slice(self, n):
        """
        divide corpus into two substrings
        :param n: breakpoint
        :return: substrings
        """
        return Corpus(self.t[:n]), Corpus(self.t[n:], n)

    def concat(self):
        """
        concatenate two Corpus objects
        :return: Corpus object
        """
        pass


class Page:
    """
    An instance of wiki page
    """
    def __init__(self, s):
        self.title = re.findall('(?<=\<title\>).*(?=\<\/title\>)', s)[0]
        self.ns = re.findall('(?<=\<ns\>).*(?=\<\/ns\>)', s)[0]
        self.raw_text = re.findall('(?<=\<text xml:space\=\"preserve\"\>).*(?=\<\/text\>)', s)[0]\
            .replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>')
        self.text = Corpus(self.raw_text)

        # optional fields
        self.file = []
        self.category = []
        self.meta = []
        self.link = []

    def get_meta(self):
        """
        get all {{meta}}
        :return:
        """
        text = self.text.t
        while bool(self._get_meta(text)):
            tmp = self._get_meta(text)
            self.meta += [tmp]
            text = text.replace(tmp, '')

    def get_link(self):
        """
        get all [[link]]
        :return:
        """
        text = self.text.t
        while bool(self._get_link(text)):
            tmp = self._get_link(text)
            self.link += [tmp]
            text = text.replace(tmp, '')

    def _get_meta(self, text):
        """
        get one {{meta}}
        :return:
        """
        if bool(re.search(r'{{', text)) and bool(re.search(r'}}', text)):
            tmp = re.findall(r'{{.*', text)[0]
            k = 2
            for i in range(2, len(tmp)):
                if tmp[i] == '{':
                    k += 1
                if tmp[i] == '}':
                    k -= 1
                if k == 0:
                    return tmp[:i+1]
            if k!=0:
                text = text[:text.find(tmp)]+text[text.find(tmp)+2:]
                self._get_meta(text)

    def _get_link(self, text):
        if bool(re.search(r'\[\[', text)) and bool(re.search(r'\]\]', text)):
            tmp = re.findall(r'\[\[.*', text)[0]
            k = 2
            for i in range(2, len(tmp)):
                if tmp[i] == '[':
                    k += 1
                if tmp[i] == ']':
                    k -= 1
                if k == 0:
                    return tmp[:i+1]
            if k!=0:
                text = text[:text.find(tmp)]+text[text.find(tmp)+2:]
                self._get_meta(text)

    def _erase(self, s):
        pass

# b = Buffer(path2)
# a = [Page(x) for x in b.fetch()]
# for i in a:
#     i.get_meta()
#     print(i.meta)

a = Corpus('基于单内核的操作系统通常有着较长的历史渊源')
b = a.slice(5)
for i in b:
    print(i.t, i.pos)
