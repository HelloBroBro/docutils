.. include:: ../header.rst

======================
 Python Source Reader
======================
:Author: David Goodger
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This document has been placed in the public domain.

This document explores issues around extracting and processing
docstrings from Python modules.

For definitive element hierarchy details, see the "Python Plaintext
Document Interface DTD" XML document type definition, pysource.dtd_
(which modifies the generic docutils.dtd_).  Descriptions below list
'DTD elements' (XML 'generic identifiers' or tag names) corresponding
to syntax constructs.


.. contents::


Model
=====

The Python Source Reader ("PySource") model that's evolving in my mind
goes something like this:

1. Extract the docstring/namespace [#]_ tree from the module(s) and/or
   package(s).

   .. [#] See `Docstring Extractor`_ below.

2. Run the parser on each docstring in turn, producing a forest of
   doctrees (per nodes.py).

3. Join the docstring trees together into a single tree, running
   transforms:

   - merge hyperlinks
   - merge namespaces
   - create various sections like "Module Attributes", "Functions",
     "Classes", "Class Attributes", etc.; see pysource.dtd_
   - convert the above special sections to ordinary doctree nodes

4. Run transforms on the combined doctree.  Examples: resolving
   cross-references/hyperlinks (including interpreted text on Python
   identifiers); footnote auto-numbering; first field list ->
   bibliographic elements.

   (Or should step 4's transforms come before step 3?)

5. Pass the resulting unified tree to the writer/builder.

I've had trouble reconciling the roles of input parser and output
writer with the idea of modes ("readers" or "directors").  Does the
mode govern the transformation of the input, the output, or both?
Perhaps the mode should be split into two.

For example, say the source of our input is a Python module.  Our
"input mode" should be the "Python Source Reader".  It discovers (from
``__docformat__``) that the input parser is "reStructuredText".  If we
want HTML, we'll specify the "HTML" output formatter.  But there's a
piece missing.  What *kind* or *style* of HTML output do we want?
PyDoc-style, LibRefMan style, etc.  (many people will want to specify
and control their own style).  Is the output style specific to a
particular output format (XML, HTML, etc.)?  Is the style specific to
the input mode?  Or can/should they be independent?

I envision interaction between the input parser, an "input mode" , and
the output formatter.  The same intermediate data format would be used
between each of these, being transformed as it progresses.


Docstring Extractor
===================

We need code that scans a parsed Python module, and returns an ordered
tree containing the names, docstrings (including attribute and
additional docstrings), and additional info (in parentheses below) of
all of the following objects:

- packages
- modules
- module attributes (+ values)
- classes (+ inheritance)
- class attributes (+ values)
- instance attributes (+ values)
- methods (+ formal parameters & defaults)
- functions (+ formal parameters & defaults)

(Extract comments too?  For example, comments at the start of a module
would be a good place for bibliographic field lists.)

In order to evaluate interpreted text cross-references, namespaces for
each of the above will also be required.

See python-dev/docstring-develop thread "AST mining", started on
2001-08-14.


Interpreted Text
================

DTD elements: package, module, class, method, function,
module_attribute, class_attribute, instance_attribute, variable,
parameter, type, exception_class, warning_class.

To classify identifiers explicitly, the role is given along with the
identifier in either prefix or suffix form::

    Use :method:`Keeper.storedata` to store the object's data in
    `Keeper.data`:instance_attribute:.

The role may be one of 'package', 'module', 'class', 'method',
'function', 'module_attribute', 'class_attribute',
'instance_attribute', 'variable', 'parameter', 'type',
'exception_class', 'exception', 'warning_class', or 'warning'.  Other
roles may be defined.

.. _pysource.dtd: pysource.dtd
.. _docutils.dtd: ../ref/docutils.dtd


.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   fill-column: 70
   End:
