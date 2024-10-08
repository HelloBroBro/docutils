.. include:: ../header.rst

==========================
 Docutils_ Hacker's Guide
==========================

:Author: Lea Wiemann
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This document has been placed in the public domain.

:Abstract: This is the introduction to Docutils for all persons who
    want to extend Docutils in some way.
:Prerequisites: You have used reStructuredText_ and played around with
    the `Docutils front-end tools`_ before.  Some (basic) Python
    knowledge is certainly helpful (though not necessary, strictly
    speaking).

.. _Docutils: https://docutils.sourceforge.io/
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _Docutils front-end tools: ../user/tools.html

.. contents::


Overview of the Docutils Architecture
=====================================

To give you an understanding of the Docutils architecture, we'll dive
right into the internals using a practical example.

Consider the following reStructuredText file::

    My *favorite* language is Python_.

    .. _Python: https://www.python.org/

Using the ``rst2html`` front-end tool, you would get an HTML output
which looks like this::

    [uninteresting HTML code removed]
    <body>
    <div class="document">
    <p>My <em>favorite</em> language is <a class="reference" href="https://www.python.org/">Python</a>.</p>
    </div>
    </body>
    </html>

While this looks very simple, it's enough to illustrate all internal
processing stages of Docutils.  Let's see how this document is
processed from the reStructuredText source to the final HTML output:


Reading the Document
--------------------

The **Reader** reads the document from the source file and passes it
to the parser (see below).  The default reader is the standalone
reader (``docutils/readers/standalone.py``) which just reads the input
data from a single text file.  Unless you want to do really fancy
things, there is no need to change that.

Since you probably won't need to touch readers, we will just move on
to the next stage:


Parsing the Document
--------------------

The **Parser** analyzes the the input document and creates a **node
tree** representation.  In this case we are using the
**reStructuredText parser**:

.. code:: python

    from docutils import frontend, utils
    from docutils.parsers.rst import Parser
    settings = frontend.get_default_settings(Parser)
    with open('test.rst', encoding='utf-8') as file:
        document = utils.new_document(file.name, settings)
        Parser().parse(file.read(), document)

Let us now examine the node tree.
With ``print(document.pformat())`` we get::

    <document source="test.rst">
        <paragraph>
            My
            <emphasis>
                favorite
             language is
            <reference name="Python" refname="python">
                Python
            .
        <target ids="python" names="python" refuri="https://www.python.org/">

The top-level node is ``document``.  It has a ``source`` attribute
whose value is ``text.rst``.  There are two children: A ``paragraph``
node and a ``target`` node.  The ``paragraph`` in turn has children: A
text node ("My "), an ``emphasis`` node, a text node (" language is "),
a ``reference`` node, and again a ``Text`` node (".").

These node types (``document``, ``paragraph``, ``emphasis``, etc.) are
all defined in ``docutils/nodes.py``.  The node types are internally
arranged as a class hierarchy (for example, both ``emphasis`` and
``reference`` have the common superclass ``Inline``).  To get an
overview of the node class hierarchy, use epydoc (type ``epydoc
nodes.py``) and look at the class hierarchy tree.

.. tip:: While rst2pseudoxml_ shows the node tree after `transforming the
   document`_, the script quicktest.py_ (in the ``tools/dev/`` directory
   of the Docutils distribution) shows the direct result of parsing a
   reStructuredText sample.

.. _quicktest.py: https://docutils.sourceforge.io/tools/dev/quicktest.py


Transforming the Document
-------------------------

In the node tree above, the ``reference`` node does not contain the
target URI (``https://www.python.org/``) yet.

Assigning the target URI (from the ``target`` node) to the
``reference`` node is *not* done by the parser (the parser only
translates the input document into a node tree).

Instead, it's done by a **Transform**.  In this case (resolving a
reference), it's done by the ``ExternalTargets`` transform in
``docutils/transforms/references.py``.

The Transforms are applied after parsing.  To see how the node tree
has changed after applying the Transforms, we use the
rst2pseudoxml_ tool [#]_::

    $ rst2pseudoxml test.rst
    <document source="test.rst">
        <paragraph>
            My
            <emphasis>
                favorite
             language is
            <reference name="Python" **refuri="https://www.python.org/"**>
                Python
            .
        <target ids="python" names="python" ``refuri="https://www.python.org/"``>

For our small test document, the only change is that the ``refname``
attribute of the reference has been replaced by a ``refuri``
attribute |---| the reference has been resolved.

While this does not look very exciting, transforms are a powerful tool
to apply any kind of transformation on the node tree.
In fact, there are quite a lot of Transforms, which do various useful
things like creating the table of contents, applying substitution
references or resolving auto-numbered footnotes. For details, see
`Docutils Transforms`_.

.. [#] You can also get a standard XML representation of the
       node tree by using rst2xml_ instead of rst2pseudoxml_.

.. _Docutils Transforms: ../api/transforms.html
.. _rst2pseudoxml: ../user/tools.html#rst2pseudoxml
.. _rst2xml: ../user/tools.html#rst2xml


Writing the Document
--------------------

To get an HTML document out of the node tree, we use a **Writer**, the
HTML writer in this case (``docutils/writers/html4css1.py``).

The writer receives the node tree and returns the output document.
For HTML output, we can test this using the ``rst2html`` tool::

    $ rst2html --link-stylesheet test.rst
    <?xml version="1.0" encoding="utf-8" ?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "https://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="https://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="generator" content="Docutils 0.3.10: https://docutils.sourceforge.io/" />
    <title></title>
    <link rel="stylesheet" href="../docutils/writers/html4css1/html4css1.css" type="text/css" />
    </head>
    <body>
    <div class="document">
    <p>My <em>favorite</em> language is <a class="reference" href="https://www.python.org/">Python</a>.</p>
    </div>
    </body>
    </html>

So here we finally have our HTML output.  The actual document contents
are in the fourth-last line.  Note, by the way, that the HTML writer
did not render the (invisible) ``target`` node |---| only the
``paragraph`` node and its children appear in the HTML output.


Extending Docutils
==================

Now you'll ask, "how do I actually extend Docutils?"

First of all, once you are clear about *what* you want to achieve, you
have to decide *where* to implement it |---| in the Parser (e.g. by
adding a directive or role to the reStructuredText parser), as a
Transform, or in the Writer.  There is often one obvious choice among
those three (Parser, Transform, Writer).  If you are unsure, ask on
the Docutils-develop_ mailing list.

In order to find out how to start, it is often helpful to look at
similar features which are already implemented.  For example, if you
want to add a new directive to the reStructuredText parser, look at
the implementation of a similar directive in
``docutils/parsers/rst/directives/``.


Modifying the Document Tree Before It Is Written
------------------------------------------------

You can modify the document tree right before the writer is called.
One possibility is to use the publish_doctree_ and
publish_from_doctree_ functions.

To retrieve the document tree, call::

    document = docutils.core.publish_doctree(...)

Please see the docstring of publish_doctree for a list of parameters.

.. XXX Need to write a well-readable list of (commonly used) options
   of the publish_* functions.  Probably in api/publisher.rst.

``document`` is the root node of the document tree.  You can now
change the document by accessing the ``document`` node and its
children |---| see `The Node Interface`_ below.

When you're done with modifying the document tree, you can write it
out by calling::

    output = docutils.core.publish_from_doctree(document, ...)

.. _publish_doctree: ../api/publisher.html#publish_doctree
.. _publish_from_doctree: ../api/publisher.html#publish_from_doctree


The Node Interface
------------------

As described in the overview above, Docutils' internal representation
of a document is a tree of nodes.  We'll now have a look at the
interface of these nodes.

(To be completed.)


What Now?
=========

This document is not complete.  Many topics could (and should) be
covered here.  To find out with which topics we should write about
first, we are awaiting *your* feedback.  So please ask your questions
on the Docutils-develop_ mailing list.

.. _Docutils-develop: ../user/mailing-lists.html#docutils-develop

.. |---| unicode:: 8212 .. em-dash
   :trim:

.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
