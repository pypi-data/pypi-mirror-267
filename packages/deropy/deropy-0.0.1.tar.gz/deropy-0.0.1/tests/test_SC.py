from SC import SC
import unittest

class TestSC(unittest.TestCase):

    def setUp(self):
        self.SC = SC()


    def test_initialize(self):
        # ---- Expected response or SC content
        expected_response = {
            "jsonrpc": "2.0",
            "id": "1",
        }

        # ---- Invoke the SC function (use the commented line if you need to setup fee)
        response_json = SC.initialize()
        #response_json = SC.initialize_fee(1000)

        # ---- Read the smart contract (could be needed to check variables)
        sc_content = self.sc.read()

        # ---- Your test here
        self.assertEqual(1, 1)

    def test_append_code(self):
        params = {
            "code": "string",
        }

        # ---- Expected response or SC content
        expected_response = {
            "jsonrpc": "2.0",
            "id": "1",
        }

        # ---- Invoke the SC function (use the commented line if you need to setup fee)
        response_json = SC.append_code(**params)
        #response_json = SC.append_code_fee(1000, **params)

        # ---- Read the smart contract (could be needed to check variables)
        sc_content = self.sc.read()

        # ---- Your test here
        self.assertEqual(1, 1)
