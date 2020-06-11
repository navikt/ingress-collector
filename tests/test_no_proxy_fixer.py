import unittest
import os
from collector.nais import remove_no_proxy_domain


class BasicsTest(unittest.TestCase):

    def test_no_proxy(self):
        envvarname = "wuba_duba_dup_dup"
        os.environ[envvarname] = ".something.no,.nais.no,.something-else.com"
        remove_no_proxy_domain(".nais.no", envvarname)
        self.assertEqual(os.environ[envvarname], ".something.no,.something-else.com")
