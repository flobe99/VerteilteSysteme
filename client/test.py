#!/usr/bin/env python3
import subprocess
from sys import stdout
import unittest

def call(args):
    result = subprocess.run( ["./client.py"] + args, stdout=subprocess.PIPE )
    return result.stdout.decode("ascii").strip(), result.returncode

class IntegrationTest( unittest.TestCase ):
    def setUp(self):
        # 1. Delete all
        text, status = call([ "delete", "--all", "." ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        # 2. Empty list
        text, status = call([ "list" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

    def test_create_blackboard_normal(self):
        text, status = call([ "create", "test", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

    def test_create_blackboard_already_exists(self):
        text, status = call([ "create", "test_exists", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "create", "test_exists", "5" ])
        self.assertEqual( text, "ERROR: (409) Blackboard already exists" )
        self.assertEqual( status, 1 )

    def test_create_blackboard_invalid_param(self):
        text, status = call([ "create", "test_invalid", "no_number" ])
        self.assertEqual( text, "ERROR: (400) Invalid parameters" )
        self.assertEqual( status, 1 )

    def test_display_blackboard_normal(self):
        text, status = call([ "create", "test", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "display", "test", "Hallo was geht" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

    def test_display_blackboard_not_found(self):
        text, status = call([ "display", "test", "Hallo was geht" ])
        self.assertEqual( text, "ERROR: (404) Blackboard not found" )
        self.assertEqual( status, 1 )

    def test_clear_blackboard(self):
        text, status = call([ "create", "test", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "clear", "test" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

    def test_clear_blackboard_not_found(self):
        text, status = call([ "clear", "test" ])
        self.assertEqual( text, "ERROR: (404) Blackboard does not exists" )
        self.assertEqual( status, 1 )

    def test_read_blackboard_normal(self):
        text, status = call([ "create", "test", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "display", "test", "test" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "read", "test" ])
        self.assertEqual( text, "test" )
        self.assertEqual( status, 0 )

    def test_read_blackboard_not_found(self):
        text, status = call([ "read", "test" ])
        self.assertEqual( text, "ERROR: (404) Blackboard does not exists" )
        self.assertEqual( status, 1 )

    def test_read_blackboard_empty(self):
        text, status = call([ "create", "test", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "read", "test" ])
        self.assertEqual( text, "ERROR: (444) Blackboard is empty" )
        self.assertEqual( status, 1 )

    def test_status_blackboard_empty(self):
        text, status = call([ "create", "test", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

    def test_status_blackboard_valid(self):
        pass

    def test_status_blackboard_expired(self):
        pass

    def test_status_blackboard_not_found(self):
        pass

    def test_list_blackboards(self):
        text, status = call([ "create", "test1", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "create", "test2", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "create", "test3", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "list" ])
        self.assertEqual( text, "test1,test2,test3" )
        self.assertEqual( status, 0 )

    def test_delete_blackboard_success(self):
        text, status = call([ "create", "test1", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "create", "test2", "5" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "delete", "test1" ])
        self.assertEqual( text, "" )
        self.assertEqual( status, 0 )

        text, status = call([ "list" ])
        self.assertEqual( text, "test2" )
        self.assertEqual( status, 0 )

    def test_delete_blackboard_not_found(self):
        text, status = call([ "delete", "test1" ])
        self.assertEqual( text, "ERROR: (404) Blackboard not found" )
        self.assertEqual( status, 1 )

if __name__ == "__main__":
    unittest.main()