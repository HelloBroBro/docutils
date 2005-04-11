# Author: Chris Liechti
# Contact: cliechti@gmx.net
# Revision: $Revision: $
# Date: $Date: $
# Copyright: This module has been placed in the public domain.

"""
S5/HTML Slideshow Writer.
"""

__docformat__ = 'reStructuredText'


import random
import sys
import docutils
from docutils import frontend, nodes, utils
from docutils.writers import html4css1
from docutils.parsers.rst import directives
from docutils.transforms import Transform
try:
    import optparse
except ImportError:
    import optik as optparse


class Writer(html4css1.Writer):

    settings_spec = html4css1.Writer.settings_spec + (
        'S5 Slideshow Specific Options',
        """The HTML --footnote-references option's default is set to """
        '"brackets".',
        (('Specify a S5 design directory. Overrides the theme selected'
          'by the document. Default is "ui" if thisoption is absent and the'
          'document does not redefine it.',
          ['--theme'],
          {'default': None, 'metavar': '<file>'}),
    ))

    settings_default_overrides = {'footnote_references': 'brackets'}

    relative_path_settings = (html4css1.Writer.relative_path_settings
                              + ('template',))

    config_section = 's5 writer'
    config_section_dependencies = ('writers', 'html4css1 writer')

    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = HTMLTranslator


class HTMLTranslator(html4css1.HTMLTranslator):
    def __init__(self, *args):
        html4css1.HTMLTranslator.__init__(self, *args)
        #get theme from document substitutions, or use the default
        if self.document.substitution_defs.has_key('s5 theme'):
            theme = self.document.substitution_defs['s5 theme'].astext()
        else:
            theme = 'ui'
        #the command line overrides the theme setting
        if self.document.settings.theme is not None:
            theme = self.document.settings.theme
        #insert S5 styleshet and script stuff in the HTML header info
        self.body_prefix.insert(0, '''
            <meta name="version" content="S5 1.0" />
            <link rel="stylesheet" href="%(s5_theme_dir)s/slides.css" type="text/css" media="projection" id="slideProj" />
            <link rel="stylesheet" href="%(s5_theme_dir)s/opera.css" type="text/css" media="projection" id="operaFix" />
            <link rel="stylesheet" href="%(s5_theme_dir)s/print.css" type="text/css" media="print" id="slidePrint" />
            <script src="%(s5_theme_dir)s/slides.js" type="text/javascript"></script>\n''' % {
            's5_theme_dir': theme,
        })

    def visit_document(self, node):
        # empty or untitled document?
        if not len(node) or not isinstance(node[0], nodes.title):
            # for XHTML conformance, modulo IE6 appeasement:
            self.head.insert(0, '<title></title>\n')
        
        #try to get the presentation title
        if isinstance(node[0], nodes.title):
            title = '<h1>%s</h1>' % node[0].astext()
        else:
            title = ''
        #additional footer information can be set trough document substitutions
        if self.document.substitution_defs.has_key('s5 location'):
            location = '<h2>%s</h2>' % self.document.substitution_defs['s5 location'].astext()
        else:
            location = ''
        #insert the slide layout master once in the HTML body
        self.body_prefix.append('''
            <div class="layout">
                <div id="currentSlide"></div>
                <div id="header"></div>
                <div id="footer">
                    %s %s
                    <div id="controls"></div>
                </div>
            </div>\n''' % (title, location)
        )


    def depart_document(self, node):
        self.fragment.extend(self.body)
        self.body_prefix.append(self.starttag(node, 'div', CLASS='presentation'))
        self.body_suffix.insert(0, '</div>\n')


    def visit_section(self, node):
        self.section_level += 1
        if node.has_key('s5'):
            self.body.append(self.starttag(node, 'div', CLASS='handout'))
        else:
            if self.section_level > 1:
                self.body.append(self.starttag(node, 'div', CLASS='section')) #dummy for matching div's
            else:
                self.body.append(self.starttag(node, 'div', CLASS='slide'))

#extra directive for handouts

def handout_directive(name, arguments, options, content, lineno,
                      content_offset, block_text, state, state_machine):
    text = '\n'.join(content)
    if not text:
        warning = state_machine.reporter.warning(
            'The handout is empty; content required.'
            % (name), '',
            nodes.literal_block(block_text, block_text), line=lineno)
        return [warning]
    #~ node = nodes.compound(text)
    node = nodes.section(text)
    node['s5'] = 'handout'
    if options.has_key('class'):
        node.set_class(options['class'])
    state.nested_parse(content, content_offset, node)
    return [node]

handout_directive.content = 1
#~ handout_directive.options = {'class': directives.class_option}
directives.register_directive('handout', handout_directive)
