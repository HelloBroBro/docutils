.. include:: ../header.rst

=======================
ODT Writer for Docutils
=======================

:Author: Dave Kuhlman
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This document has been placed in the public domain.

:abstract: This document describes the Docutils writer for
           OpenDocument Text (.odt) documents.

.. sectnum::

.. contents::


Introduction
============

The Docutils front end rst2odt_ translates reStructuredText_ into an
`OpenDocument Text`_ (.odt) file.
OpenDocument files `can be opened by most modern office software`__.
It is the native file format for LibreOffice_ Writer.

__ https://en.wikipedia.org/wiki/OpenDocument#Software


Requirements
============

In addition to the Docutils standard requirements, ``odtwriter``
requires:

- Optional -- `Pygments`_ is required if you want syntax
  highlighting of code in literal blocks.  See section `Syntax
  highlighting`_.

- Optional -- `Python Imaging Library`_ (PIL/Pillow_) is required if
  you use the image or figure directive but don't specify ``width``
  and ``height``.  See section `Images and figures`_.



How to Use It
=============

Run it from the command line as follows::

    $ rst2odt myinput.rst > myoutput.odt

To see usage information and to learn about command line options
that you can use, run the following::

    $ rst2odt --help

Examples::

    $ rst2odt -s -g python_comments.rst > python_comments.odt

    $ rst2odt --source-url=odtwriter.rst --generator \
        --stylesheet=/myconfigs/styles.odt odtwriter.rst > odtwriter.odt


Configuration file
------------------

The options described below can also be set in a `configuration file`_.
Use section `[odf_odt writer]`_ to set options specific to the
``odtwriter``.  For example::

    [odf_odt writer]
    stylesheet: styles1.odt

See the `Docutils Configuration`_ document for more information on
Docutils configuration files, including locations which are
searched.

.. _Docutils Configuration: config.html
.. _configuration file: config.html#configuration-files
.. _[odf_odt writer]: config.html#odf-odt-writer


Command line options
--------------------

The following command line options are specific to ``odtwriter``:

--stylesheet=<URL>      Specify a stylesheet URL, used verbatim.
                        Default: writers/odf_odt/styles.odt in the
                        installation directory.
--odf-config-file=<file>
                        Specify a configuration/mapping file relative to the
                        current working directory for additional ODF options.
                        In particular, this file may contain a section named
                        "Formats" that maps default style names to names to be
                        used in the resulting output file allowing for
                        adhering to external standards. For more info and the
                        format of the configuration/mapping file, see the
                        odtwriter doc.
--cloak-email-addresses
                        Obfuscate email addresses to confuse harvesters while
                        still keeping email links usable with standards-
                        compliant browsers.
--no-cloak-email-addresses
                        Do not obfuscate email addresses.
--table-border-thickness=TABLE_BORDER_THICKNESS
                        Specify the thickness of table borders in thousands of
                        a cm.  Default is 35.
--add-syntax-highlighting
                        Add syntax highlighting in literal code blocks.
--no-syntax-highlighting
                        Do not add syntax highlighting in literal code blocks.
                        (default)
--create-sections       Create sections for headers.  (default)
--no-sections           Do not create sections for headers.
--create-links          Create links.
--no-links              Do not create links.  (default)
--endnotes-end-doc      Generate endnotes at end of document, not footnotes at
                        bottom of page.
--no-endnotes-end-doc   Generate footnotes at bottom of page, not endnotes at
                        end of document. (default)
--generate-list-toc     Generate a bullet list table of contents, not an
                        ODF/``oowriter`` table of contents.
--generate-oowriter-toc
                        Generate an ODF/``oowriter`` table of contents,
                        not a bullet list.  (default) **Note:**
                        ``odtwriter`` is not able to determine page
                        numbers, so you will need to open the
                        generated document in ``oowriter``, then
                        right-click on the table of contents and
                        select "Update" to insert page numbers.
--custom-odt-header=CUSTOM_HEADER
                        Specify the contents of an custom header line.  See
                        odf_odt writer documentation for details about special
                        field character sequences.  See section
                        `Custom header/footers: inserting page numbers, date, time, etc`_
                        for details
--custom-odt-footer=CUSTOM_FOOTER
                        Specify the contents of an custom footer line.  See
                        odf_odt writer documentation for details about special
                        field character sequences.  See section
                        `Custom header/footers: inserting page numbers, date, time, etc`_
                        for details



Styles and Classes
==================

``odtwriter`` uses a number of styles that are defined in
``styles.xml`` in the default ``styles.odt``.  This section
describes those styles.

Note that with the ``--stylesheet`` command line option, you can
use either ``styles.odt`` or ``styles.xml``, as described below.
Use of ``styles.odt`` is recommended over ``styles.xml`` as, e.g.,
customizing `table styles`_ does not work with an ``*.xml``
stylesheet file.

You can modify the look of documents generated by ``odtwriter`` in
several ways:

- Open (a copy of) ``styles.odt`` in ``OpenOffice/oowriter`` and
  modify the style you wish to change. Now, save this document,
  then generate your documents using this modified copy of
  ``styles.odt``.

  In my version of ``oowriter``, to modify styles, either (1)
  press F11 or (2) use menu item "Format/Styles and Formatting",
  then right-click on the relevant style and select "Modify".
  Modify the style, then save your document.

- Open a document generated by ``odtwriter`` in `oowriter``.  Now,
  edit the style you are interested in modifying.  Now, you
  can extract the styles.xml file from your document and either
  (1) use this as your default styles file or (2) copy and paste
  the relevant style definition into your styles.xml.

- Extract ``styles.xml`` from ``styles.odt`` using your favorite
  ``zip/unzip`` tool.  Then modify ``styles.xml`` with a text
  editor.  Now re-zip it back into your own ``styles.odt``, or use
  it directly by specifying it with the ``--stylesheet`` command
  line option.  **Hint:** If you intend to extract ``styles.xml``
  from an ``.odt`` file (and then "re-zip" it), you should turn off
  XML optimization/compression in ``oowriter``.  In order to this
  in ``oowriter``, use Tools --> Options...  --> Load-Save -->
  General and turn off "Size optimization for XML format".

- Open an empty (or new) document in ``oowriter``.  Define all of
  the styles described in this section.  Then, use that document (a
  .odt file) as your stylesheet.  ``odtwriter`` will extract the
  ``styles.xml`` file from that document and insert it into the
  output document.

- Some combination of the above.


Styles used by odtwriter
------------------------

This section describes the styles used by ``odtwriter``.

Note that we do not describe the "look" of these styles.  That can
be easily changed by using ``oowriter`` to edit the document
``styles.odt`` (or a copy of it), and modifying any of the styles
described here.

To change the definition and appearance of these styles, open
``styles.odt`` in ``oowriter`` and open the Styles and Formatting
window by using the following menu item::

    Format --> Styles and Formatting

Then, click on the Paragraph Styles button or the Character Styles
button at the top of the Styles and Formatting window.  You may
also need to select "All Styles" from the drop-down selection list
at the bottom of the Styles and Formatting window in order to see
the styles used by ``odtwriter``.

Notice that you can make a copy of file ``styles.odt``, modify it
using ``oowriter``, and then use your copy with the
``--stylesheet=<file>`` command line option.  Example::

    $ rst2odt --stylesheet=mystyles.odt test2.rst > test2.odt


Paragraph styles
~~~~~~~~~~~~~~~~

rststyle-attribution
    The style for attributions, for example, the attribution in a
    ``.. epigraph::`` directive.  Derived from
    ``rststyle-blockquote``.

rststyle-blockindent
    An indented block.

rststyle-blockquote
    A block quote.

rststyle-blockquote-bulletitem
    The style for bullet list items inside block quote.

rststyle-blockquote-enumitem
    The style for enumerated list items inside block quote.

rststyle-bodyindent
    An indented block.

rststyle-bulletitem
    An item in an bullet list.

rststyle-caption
    The caption in a figure or image.  Also see
    ``rststyle-legend``.

rststyle-codeblock
    Literal code blocks -- A block of example code.  Created with
    double colon ("::") followed by an indented block or with the
    ``.. parsed-literal::`` directive.  Derived from the
    ``Preformatted Text`` style in ``oowriter``.

rststyle-enumitem
    An item in an enumerated list.

rststyle-epigraph
    The style for epigraphs, for example, the body of an
    ``.. epigraph::`` directive.  Derived from
    ``rststyle-blockquote``.

rststyle-epigraph-bulletitem
    The style for bullet list items inside epigraphs.

rststyle-epigraph-enumitem
    The style for enumerated list items inside epigraphs.

rststyle-footer
    The style for footers.  The footer content originates from the
    ``..footer::`` directive and in response to the command line
    flags for generator (``--generator``), date/time generated
    (``--date`` and ``--time``), and view source link
    (``--source-link`` and ``--source-url=URL``).

rststyle-header
    The style for headers.  The header content originates from the
    ``..header::`` directive.

rststyle-highlights
    The style for highlightss, for example, the body of an
    ``.. highlights::`` directive.  Derived from
    ``rststyle-blockquote``.

rststyle-highlights-bulletitem
    The style for bullet list items inside highlights.

rststyle-highlights-enumitem
    The style for enumerated list items inside highlights.

rststyle-horizontalline
    A horizontal line, e.g. used for transitions.

rststyle-legend
    The legend in a figure.  See the Docutils figure directive.  Also
    see ``rststyle-caption``.

rststyle-table-title
    The style for titles of tables.  See section `The table
    directive`_.

rststyle-textbody
    Normal text.  The style for paragraphs.  Derived from the ``Text
    body`` style in ``oowriter``.


Character styles
~~~~~~~~~~~~~~~~

rststyle-emphasis
    Emphasis.  Normally rendered as italics.

rststyle-inlineliteral
    An inline literal.

rststyle-strong
    Strong emphasis.  Normally rendered as boldface.

rststyle-quotation
    In-line quoted material.

rststyle-codeblock-classname
    Syntax highlighting in literal code blocks -- class names.

rststyle-codeblock-comment
    Syntax highlighting in literal code blocks -- comments.

rststyle-codeblock-functionname
    Syntax highlighting in literal code blocks -- function names.

rststyle-codeblock-keyword
    Syntax highlighting in literal code blocks -- Python language
    keywords.

rststyle-codeblock-name
    Syntax highlighting in literal code blocks -- other names, for
    example, variables.

rststyle-codeblock-number
    Syntax highlighting in literal code blocks -- literal numbers,
    including integers, floats, hex numbers, and octal numbers.

rststyle-codeblock-operator
    Syntax highlighting in literal code blocks -- Python operators.

rststyle-codeblock-string
    Syntax highlighting in literal code blocks -- literal strings.


List styles
~~~~~~~~~~~

rststyle-bulletlist
    Bullet lists (but not in the table of contents)

rststyle-blockquote-bulletlist
    Bullet lists in block quotes.

rststyle-blockquote-enumlist
    Enumerated lists in block quotes.

rststyle-enumlist-arabic
    Enumerated lists, arabic (but not in the table of contents)

rststyle-enumlist-loweralpha
    Enumerated lists, lower alpha (but not in the table of contents)

rststyle-enumlist-lowerroman
    Enumerated lists, lower roman (but not in the table of contents)

rststyle-enumlist-upperalpha
    Enumerated lists, upper alpha (but not in the table of contents)

rststyle-enumlist-upperroman
    Enumerated lists, upper roman (but not in the table of contents)

rststyle-epigraph-bulletlist
    Bullet lists in epigraphs.  See the ``.. epigraph::``
    directive.

rststyle-epigraph-enumlist
    Enumerated lists in epigraphs.  See the ``.. epigraph::``
    directive.

rststyle-highlights-bulletlist
    Bullet lists in highlights blocks.  See the ``.. highlights::``
    directive.

rststyle-highlights-enumlist
    Enumerated lists in highlights blocks.  See the ``.. highlights::``
    directive.

rststyle-tocbulletlist
    Lists in the table of contents when section numbering is off.

rststyle-tocenumlist
    Lists in the table of contents when section numbering is on.


Admonition styles
~~~~~~~~~~~~~~~~~

rststyle-admon-attention-hdr
    The style for the attention admonition header/title.

rststyle-admon-attention-body
    The style for the attention admonition body/paragraph.

rststyle-admon-caution-hdr
    The style for the caution admonition header/title.

rststyle-admon-caution-body
    The style for the caution admonition body/paragraph.

rststyle-admon-danger-hdr
    The style for the  admonition header/title.

rststyle-admon-danger-body
    The style for the danger admonition body/paragraph.

rststyle-admon-error-hdr
    The style for the error admonition header/title.

rststyle-admon-error-body
    The style for the error admonition body/paragraph.

rststyle-admon-hint-hdr
    The style for the hint admonition header/title.

rststyle-admon-hint-body
    The style for the hint admonition body/paragraph.

rststyle-admon-hint-hdr
    The style for the hint admonition header/title.

rststyle-admon-hint-body
    The style for the hint admonition body/paragraph.

rststyle-admon-important-hdr
    The style for the important admonition header/title.

rststyle-admon-important-body
    The style for the important admonition body/paragraph.

rststyle-admon-note-hdr
    The style for the note admonition header/title.

rststyle-admon-note-hdr
    The style for the note admonition header/title.

rststyle-admon-tip-body
    The style for the tip admonition body/paragraph.

rststyle-admon-tip-hdr
    The style for the tip admonition header/title.

rststyle-admon-warning-body
    The style for the warning admonition body/paragraph.

rststyle-admon-warning-hdr
    The style for the warning admonition header/title.

rststyle-admon-generic-body
    The style for the generic admonition body/paragraph.

rststyle-admon-generic-hdr
    The style for the generic admonition header/title.


Rubric style
~~~~~~~~~~~~

rststyle-rubric
    The style for the text in a rubric directive.

The rubric directive recognizes a "class" option.  If entered,
odtwriter uses the value of that option instead of the
``rststyle-rubric`` style.  Here is an example which which attaches
the ``rststyle-heading1`` style to the generated rubric::

    .. rubric:: This is my first rubric
       :class: rststyle-heading1


Table styles
~~~~~~~~~~~~

A table style is generated by ``oowriter`` for each table that you
create.  Therefore, ``odtwriter`` attempts to do something similar.
These styles are created in the ``content.xml`` document in the
generated ``.odt`` file.  These styles have names prefixed with
"rststyle-table-".

There are two ways in which you can control the styles of your
tables: one simple, the other a bit more complex, but more
powerful.

First, you can change the thickness of the borders of all tables
generated in a document using the "--table-border-thickness"
command line option.

Second, you can control additional table properties and you can
apply different styles to different tables within the same document
by customizing and using tables in your stylesheet: ``styles.odt``
or whatever you name your copy of it using the --stylesheet command
line option.  Then, follow these rules to apply a table style to
the tables in your document:

- The default table style -- Optionally, alter and customize the
  style applied by default to tables in your document by modifying
  table "rststyle-table-0" in your stylesheet (``styles.odt`` or a
  copy).  Caution: Do not change the name of this table.

- User-created table styles -- Add one or more new table styles to
  be applied selectively to tables in your document by doing the
  following:

  1. Using ``oowriter``, add a table to your stylesheet and give it
     a name that starts with the prefix "rststyle-table-", for
     example "rststyle-table-vegetabledata".  Customize the table's
     border thickness, border color, and table background color.

  2. In your reStructuredText document, apply your new table style
     to a specific table by placing the "..  class::" directive
     immediately before the table, for example::

         .. class:: rststyle-table-vegetabledata

The default table style will be applied to all tables for which you
do not specify a style with the "..  class::" directive.

Customize the table properties in ``oowriter`` using the table
properties dialog for the table (style) that you wish to customize.

Note that "--table-border-thickness" command line option overrides
the border thickness specified in the stylesheet.

The specific properties that you can control with this second
method are the following:

- Border thickness and border color.

- Background color -- When you change the background color of a
  table to be used as a style (in ``styles.odt`` or whatever you
  name it), make sure you change the background color for the
  *table* and *not* for a cell in the table.  ``odtwriter`` picks
  the background color from the table, not from a cell within the
  table.


Line block styles
~~~~~~~~~~~~~~~~~~

The line block styles wrap the various nested levels of line
blocks.  There is one line block style for each indent level.

rststyle-lineblock1
    Line block style for line block with no indent.

rststyle-lineblock2
    Line block style for line block indented 1 level.

rststyle-lineblock3
    Line block style for line block indented 2 levels.

rststyle-lineblock4
    Line block style for line block indented 3 levels.

rststyle-lineblock5
    Line block style for line block indented 4 levels.

rststyle-lineblock6
    Line block style for line block indented 5 levels.

Notes:

- ``odtwriter`` does not check for a maximum level of indents
  within line blocks.  Therefore, you can define additional line
  block styles for additional levels if you need them.  Define
  these styles with the names ``rststyle-lineblock7``,
  ``rststyle-lineblock8``, ...

- Since the line block style is used to create indentation, a line
  block that is inside a block quote will use
  ``rststyle-lineblock2`` as its first level of indentation.


Footnote and citation styles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

rststyle-footnote
    The style for footnotes.  This style affects the footnote
    content, *not* the footnote reference in the body of the document.

rststyle-citation
    The style for citations.  This style affects the citation
    content, *not* the citation reference in the body of the document.
    You might need to adjust the indentation in this style
    depending on the length of the label used in your citations.


Heading and title styles
~~~~~~~~~~~~~~~~~~~~~~~~~

rststyle-heading{1|2|3|4|5}
    The styles for headings (section titles and sub-titles).  Five
    levels of sub-headings are provided: rststyle-heading1 through
    rststyle-heading5.

rststyle-title
    The style for the document title.

rststyle-subtitle
    The style for the document sub-title.


Image and figure styles
~~~~~~~~~~~~~~~~~~~~~~~~~

rststyle-image
    The style applied to an image, either an image by itself or an
    image in a figure.

rststyle-figureframe
    The style applied to a figure (actually to the frame that
    surrounds a figure).



Defining and using a custom stylesheet
---------------------------------------

You can create your own custom stylesheet.  Here is how:

1. Make a copy of ``styles.odt``, which is in the distribution.

2. Open your copy of ``styles.odt`` in ``oowriter``.  Modify styles
   in that document.  Then, save it.

3. When you run ``rst2odt``, use the ``--stylesheet`` command
   line option to use your custom stylesheet.  Run ``rst2odt
   --help`` to learn more about these options.


Why custom stylesheets
~~~~~~~~~~~~~~~~~~~~~~~

Here are a few reasons and ideas:

- The `page size`_ is stored in the style sheet.  The default page
  size is ``US Letter``.  You can change the page size (for example,
  to ``A4``) in your custom stylesheet by opening it in
  ``oowriter``, then clicking on menu: ``Format/Page...``, then
  clicking on the ``Page`` tab.


Defining and using custom style names
-------------------------------------

[Credits: Stefan Merten designed and implemented the custom style names
capability.  Thank you, Stefan.]

You can also instruct ``odtwriter`` to use style names of your own
choice.


Why custom style names
~~~~~~~~~~~~~~~~~~~~~~

Here are a few reasons and ideas:

- Suppose that your organization has a standard set of styles in
  OOo ``oowriter`` and suppose that the use of these styles is
  required. You would like to generate ODF documents from
  reST text files, and you want the generated documents to contain
  these styles.

- Suppose that your company or organization has a policy of using a
  certain MS Word template for some set of documents.  You would
  like to generate ODF documents that use these custom style names,
  so that you can export these documents from ODF ``oowriter`` to MS
  Word documents that use these style names.

- Suppose that your documents are written in a language other than
  English.  You would like the style names visible in the "Styles
  and Formatting" window in OOo ``oowriter`` (menu item
  ``Format/Styles and Formatting``) to be understandable in the
  language of your users.

- ``odtwriter`` maps single asterisks/stars (for example, \*stuff\*)
  to emphasis and double stars to strong.  You'd like to reverse
  these.  Or, you would like to generate headings level 3 and 4
  where headings level 1 and 2 would normally be produced.


How to use custom style names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to define custom style names and to generate documents that
contain them, do the following:


1. Create a configuration file containing a "Formats" section.  The
   configuration file obeys the file format supported by the Python
   ConfigParser module:
   `ConfigParser -- Configuration file parser --
   https://docs.python.org/3/library/configparser.html
   <https://docs.python.org/3/library/configparser.html>`_.

2. In the "Formats" section of the configuration file, create one
   option (a name-value pair) for each custom style name that you
   wish to define.  The option name is the standard ``odtwriter``
   style name (without "rststyle-"), and the value is your custom
   style name.  Here is an example::

       [Formats]
       textbody: mytextbody
       bulletitem: mybulletitem
       heading1: myheading1
           o
           o
           o

3. Create a styles document that defines the styles generated by
   ``odtwriter``.  You can create and edit the styles in OOo
   ``oowriter``.  It may be helpful to begin by making a copy of the
   styles document that is part of the ``odtwriter`` distribution
   (``styles.odt``).

4. When you run ``odtwriter``, specify the ``--odf-config-file``
   option.  You might also want to specify your styles document
   using the ``--stylesheet`` option in order to include your
   custom style definitions.  For example::

       rst2odt --odf-config-file=mymappingfile.ini \
         --stylesheet=mystyles.odt mydoc.rst mydoc.odt


Classes
-------

``odtwriter`` uses the following Docutils class to provide additional
control of the generation of ODF content:

- Class ``wrap`` -- Use this to cause the wrapping of text around
  an image.  The default is *not* to wrap text around images.
  Here is an example::

      .. class:: wrap
      .. image:: images/flower01.png
          :alt: A bright yellow flower
          :height: 55
          :width: 60


Roles
-------

You can use a Docutils custom interpreted text role to attach a
character style to an inline area of text.  This capability also
enables you to attach a new character style (with a new name) that
you define yourself.  Do this by defining your role in a stylesheet
as a character style with "rststyle-" prefixed to your role name,
then use the ``role`` directive and inline markup to apply your
role.

In order to use this capability, do the following:

- Define the character style for your custom role in a stylesheet
  (a copy of ``styles.odt``) with the prefix "rststyle-".
  Remember: (1) If the name of your custom role is "pretty", then
  define a character style named "rststyle-pretty".  (2) Define the
  style as a *character* style, and *not*, for example as a
  paragraph style.

- Declare your role in the source reStructuredText document in a
  ``role`` directive.  Example::

      .. role:: pretty

- Use inline markup to apply your role to text.  Example::

      We have :pretty:`very nice` apples.

Here is another example::

    .. role:: fancy

    Here is some :fancy:`pretty text` that looks fancy.

For more on roles see:
`Custom Interpreted Text Roles --
https://docutils.sourceforge.io/docs/ref/rst/directives.html#custom-interpreted-text-roles
<https://docutils.sourceforge.io/docs/ref/rst/directives.html#custom-interpreted-text-roles>`_.

**Note:** The ability to base a role on another existing role is
*not* supported by ``odtwriter``.


Hints and Suggestions and Features
==================================

Table of contents
-----------------

The ``..contents::`` directive causes ``odtwriter`` to generate
either:

1. A static, outline style table of contents, if the
   ``--generate-list-toc`` command line option is specified, or

2. An ODF/``oowriter`` style table of contents containing
   dynamically updated page numbers and with the formatting control
   that ``oowriter`` gives you.  This is the default, or use the
   command line option ``--generate-list-toc``.  **Note:**
   ``odtwriter`` is not able to determine page numbers, so you will
   need to open the generated document in ``oowriter``, then
   right-click on the table of contents and select "Update" to
   insert correct page numbers.


Syntax highlighting
-------------------

``odtwriter`` can add syntax highlighting to code in code
blocks.  In order to activate this, do all of the following:

1. Install `Pygments`_ and ...

2. Use the command line option ``--add-syntax-highlighting``.
   Example::

       $ rst2odt --add-syntax-highlight test.rst > test.odt

The following styles are defined in styles.odt and are used for
literal code blocks and syntax highlighting:

- Paragraph styles:

  - rststyle-codeblock -- The style for the code block as a whole.

- Character styles:

  - rststyle-codeblock-classname -- class names.

  - rststyle-codeblock-comment -- comments.

  - rststyle-codeblock-functionname -- function names.

  - rststyle-codeblock-keyword -- Python language keywords.

  - rststyle-codeblock-name -- other names, for example,
    variables.

  - rststyle-codeblock-number -- literal numbers, including
    integers, floats, hex numbers, and octal numbers.

  - rststyle-codeblock-operator -- Python operators.

  - rststyle-codeblock-string -- literal strings.

Each of the above styles has a default appearance that is defined
in ``styles.odt``.  To change that definition and appearance, open
``styles.odt`` in ``oowriter`` and use menu item::

    Format --> Styles and Formatting

Then, click on the Paragraph Styles button or the Character Styles
button at the top of the Styles and Formatting window.  You may
also need to select "All Styles" from the drop-down selection list
at the bottom of the Styles and Formatting window.



The container directive
-----------------------

There is limited support for the ``container`` directive.  The
limitations and rules for the container directive are the following:

- Only the first class in the list of classes (arguments) is used.

- That class/style must be a paragraph style and not (for example) a
  character style.

- The style/class given to the container directive will have a
  "rststyle-" prefix in the odt file.

So, for example::

    .. container:: style-1 style-2 style-3

        a block of text

- Only ``style-1`` is used; ``style-2`` and ``style-3`` are ignored.

- ``rststyle-style-1`` must be defined.  It should be an existing,
  predefined style, or you should define it in your stylesheet
  (``styles.odt`` or the argument to the ``--stylesheet`` command
  line option).

- ``rststyle-style-1`` must be a paragraph style.

To define a paragraph style, use the following menu item in
``oowriter``::

    Format --> Styles and Formatting

Then, click on the Paragraph Styles button.

The following example attaches the ``rststyle-heading2`` style (a
predefined style) to each paragraph/line in the container::

    .. container:: heading2

       Line 1 of container.

       Line 2 of container.

More information on how to define a new style (for example, in your
``styles.odt``) can be found in section
`Defining and using custom style names`_.



The table directive
-------------------

The ``table`` directive can be used to add a title to a table.
Example::

    .. table:: A little test table

        =========== =============
        Name        Value
        =========== =============
        Dave        Cute
        Mona        Smart
        =========== =============

The above will insert the title "A little test table" at the top of the
table.  You can modify the appearance of the title by modifying the
paragraph style ``rststyle-table-title``.


Footnotes and citations
-----------------------

Footnotes and citations are supported.

There are additional styles ``rststyle-footnote`` and
``rststyle-citation`` for footnotes and citations. See
`Footnote and citation styles`_.

You may need to modify the citation style to fit the length of your
citation references.

Endnotes -- There are command line options that control whether
``odtwriter`` creates endnotes instead of footnotes.  Endnotes
appear at the end of the document instead of at the bottom of the
page.  See flags ``--endnotes-end-doc`` and
``--no-endnotes-end-doc`` in section `Command line options`_.


Images and figures
------------------

The ODT Writer only supports fixed `length units`_ ("cm", "mm", "in",
"pc", "pt", "px) for the size attributes "width", and "height".
The fallback unit (used for attribute values without unit) is "px".

If on the image or the figure directive you do not provide the width
and height options, then ``odtwriter`` will attempt to determine the
size of the image using the Python Imaging Library (PIL/Pillow_).
If ``odtwriter`` cannot find and import the
Python Imaging Library, it will raise an exception.  If this
ocurrs, you can fix it by doing one of the following:

- Install the Python Imaging Library or

- Add both the ``width`` and the ``height`` options.

For more information about PIL, see: `Python Imaging Library`_.


The raw directive
-----------------

The ``raw`` directive is supported.  Use output format type "odt".

You will need to be careful about the formatting of the raw
content.  In particular, introduced whitespace might be a problem.

In order to produce content for the raw directive for use by
``odtwriter``, you might want to extract the file ``content.xml``
from a ``.odt`` file (using some Zip tool), and then clip, paste,
and modify a selected bit of it.

Here is an example::

    .. raw:: odt

        <text:p text:style-name="rststyle-textbody">Determining
        <text:span text:style-name="rststyle-emphasis">which</text:span>
        namespace a name is in is static.  It can be determined by a
        lexical scan of the code.  If a variable is assigned a value
        <text:span text:style-name="rststyle-emphasis">anywhere</text:span>
        in a scope (specifically within a function or method body),
        then that variable is local to that scope.  If Python does
        not find a variable in the local scope, then it looks next
        in the global scope (also sometimes called the module scope)
        and then in the built-ins scope.  But, the
        <text:span text:style-name="rststyle-inlineliteral">global</text:span>
        statement can be used to force Python to find and use a global
        variable (a variable defined at top level in a module) rather
        than create a local one.</text:p>


The meta directive
------------------

``odtwriter`` supports the ``meta`` directive.  "keywords"
and "description" are set in their respective odt fields.
Other meta fields are set as "Custom Properties".
Here is an example::

    .. meta::
       :keywords: reStructuredText, docutils, formatting
       :description lang=en: A reST document, contains formatted
           text in a formatted style.
       :custom_var: Value

To see the results of the ``meta`` directive in ``oowriter``,
select menu item "File/Properties...", then click on the
"Description" tab ("keywords" and "description" fields) and the
"Custom Properties" tab.


Footnote references inside footnotes
------------------------------------

Not supported.

Get a grip.  Be serious.  Try a dose of reality.

``odtwriter`` ignores them.

They cause ``oowriter`` to croak.


Page size
---------

The default page size, in documents generated by the ODT writer is
"US Letter".  You can change this (for example to ``A4``) by using a
custom stylesheet.  See `Defining and using a custom stylesheet`_
for instructions on how to do this.

On machines which support ``paperconf``, the ODT writer can insert
the default page size for your locale.  In order for this to work,
the following conditions must be met:

1. The program ``paperconf`` must be available on your system.
   ``odtwriter`` uses ``paperconf -s`` to obtain the paper size.
   See ``man paperconf`` for more information.

2. The page height and width settings must be absent from the stylesheet
   used to generate the document.

   You can use the Python script ``prepstyles.py`` distributed with
   Docutils to remove the page height and width settings from a
   stylesheet file ``STYLES.odt`` with ::

       $ python3 -m docutils.writers.odf_odt.prepstyles STYLES.odt

   (the command changed in Docutils 0.20.1).

.. warning:: If you edit your stylesheet in ``oowriter`` and then
    save it, ``oowriter`` automatically inserts a page height and
    width in the styles for that (stylesheet) document.  If that is
    not the page size that you want and you want ``odtwriter`` to
    insert a default page size using ``paperconf``, then you will
    need to strip the page size from your stylesheet each time you
    edit that stylesheet with ``oowriter``.



Custom header/footers: inserting page numbers, date, time, etc
----------------------------------------------------------------

You can specify custom headers and footers for your document from
the command line.  These headers and footers can be used to insert
fields such as the page number, page count, date, time, etc.  See
below for a complete list.

To insert a custom header or footer, use the "--custom-odt-header"
or "--custom-odt-footer" command line options.  For example, the
following inserts a footer containing the page number and page
count::

    $ rst2odt --custom-odt-footer="Page %p% of %P%" f1.rst > f1.odt


Field specifiers
~~~~~~~~~~~~~~~~~~

You can use the following field specifiers to insert ``oowriter``
fields in your custom headers and footers:

%p%
    The current page number.

%P%
    The number of pages in the document.

%d1%
    The current date in format 12/31/99.

%d2%
    The current date in format 12/31/1999.

%d3%
    The current date in format Dec 31, 1999.

%d4%
    The current date in format December 31, 1999.

%d5%
    The current date in format 1999-12-31.

%t1%
    The current time in format 14:22.

%t2%
    The current time in format 14:22:33.

%t3%
    The current time in format 02:22 PM.

%t4%
    The current time in format 02:22:33 PM.

%a%
    The author of the document (actually the initial creator).

%t%
    The document title.

%s%
    The document subject.


**Note:** The use of the above field specifiers in the body of your
reStructuredText document is **not** supported, because these
specifiers are not standard across Docutils writers.



Credits
=======

Stefan Merten designed and implemented the custom style names
capability.  Thank you, Stefan.

Michael Schutte supports the Debian GNU/Linux distribution of
``odtwriter``.  Thank you, Michael, for providing and supporting
the Debian package.

Michael Schutte implemented the fix that enables ``odtwriter`` to
pick up the default paper size on platforms where the program
``paperconf`` is available.  Thank you.



.. _rst2odt:
    tools.html#rst2odt
.. _reStructuredText:
    ../ref/rst/restructuredtext.html
.. _length units:
    ../ref/rst/restructuredtext.html#length-units
.. _`OpenDocument Text`:
    https://en.wikipedia.org/wiki/OpenDocument
.. _LibreOffice:
    https://libreoffice.org/
.. _`Pygments`:
    https://pygments.org/
.. _`Python Imaging Library`:
    https://en.wikipedia.org/wiki/Python_Imaging_Library
.. _`Pillow`: https://pypi.org/project/pillow/
