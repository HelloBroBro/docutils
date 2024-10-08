#!/usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for Null writer.
"""

from pathlib import Path
import sys
import unittest

if __name__ == '__main__':
    # prepend the "docutils root" to the Python library path
    # so we import the local `docutils` package.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docutils.core import publish_string
from docutils.writers import null


class WriterPublishTestCase(unittest.TestCase):
    def test_publish(self):
        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    output = publish_string(
                        source=case_input,
                        writer=null.Writer(),
                        settings_overrides={
                            '_disable_config': True,
                            'strict_visitor': True,
                        },
                    )
                    if isinstance(output, bytes):
                        output = output.decode('utf-8')
                    self.assertEqual(case_expected, output)


totest = {}

totest['basic'] = [
["""\
This is a paragraph.
""",
'']
]

if __name__ == '__main__':
    unittest.main()
