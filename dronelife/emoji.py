""" Essentially a fork of fontawesome-markdown
"""

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree

class EmojiPattern(Pattern):
    def handleMatch(self, m):
        el = etree.Element('i')
        emoji_name = m.group(2)
        el.attrib = {'class':'emoji dronelife-{0}'.format(emoji_name)}

        return el

class EmojiExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        emoji = EmojiPattern(r'\(([\w]+)\)')
        md.inlinePatterns.add('emoji', emoji, '<reference')
