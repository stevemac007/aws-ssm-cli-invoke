"""Basic tests for the addition code."""
from __future__ import absolute_import

import unittest

from ssm.main import SSMInvoke


class SSMInvokeTests(unittest.TestCase):
    def test_init(self):

        under_test = SSMInvoke()

        self.assertEqual([], under_test.targets)
        self.assertEqual(None, under_test.command)
        self.assertEqual(None, under_test.instances)
        self.assertEqual("", under_test.comment)
        self.assertEqual(None, under_test.ssm_client)
        self.assertEqual(False, under_test.wait)
        self.assertEqual(False, under_test.show_output)
