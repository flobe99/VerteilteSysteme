#!/usr/bin/env python3
import argparse
import sys
import requests
import json
from requests import status_codes

class APIError( Exception ):

    def __init__(self, status_code, description):
        self.status_code = status_code

        super().__init__( "(" + str(status_code) + ") " + description )

# Wrapper for the REST API
class API:

    def __init__(self, host, debug=False):
        self.host = host
        self._debug = debug

    def debug(self, string):
        if not self._debug:
            return

        print( string )

    def call(self, method, path, data):
        self.debug( "[DEBUG] Send {} request to {} with data {}".format( method, self.host + path, data ) )
        r = requests.request( method, self.host + path, params=data )
        self.debug( "[DEBUG] Got response with code {} and data {}".format( r.status_code, r.text ) )

        return r.status_code, r.text

    def create_blackboard(self, name, valid_time):
        status_code, text = self.call( "POST", "/blackboard/create", { "name": name, "validityTime": valid_time } )
        if status_code == 200:
            pass
        elif status_code == 400:
            raise APIError( 400, "Invalid parameters" )
        elif status_code == 404:
            raise APIError( 404, "Blackboard not found" )
        elif status_code == 409:
            raise APIError( 409, "Blackboard already exists" )
        else:
            raise APIError( status_code, "Unkown error")

    def display_blackboard(self, name, message):
        status_code, text = self.call( "GET", "/blackboard/display", { "name": name, "message": message } )
        if status_code == 200:
            pass
        elif status_code == 400:
            raise APIError( 400, "Invalid parameters" )
        elif status_code == 404:
            raise APIError( 404, "Blackboard not found" )
        elif status_code == 500:
            raise APIError( 500, "Internal error" )
        else:
            raise APIError( status_code, "Unkown error")

    def clear_blackboard(self, name):
        status_code, text = self.call( "GET", "/blackboard/clear", { "name": name } )
        if status_code == 200:
            pass
        elif status_code == 400:
            raise APIError( 400, "Invalid parameters" )
        elif status_code == 404:
            raise APIError( 404, "Blackboard does not exists" )
        elif status_code == 500:
            raise APIError( 500, "Internal error" )
        else:
            raise APIError( status_code, "Unkown error")

    def read_blackboard(self, name):
        status_code, text = self.call( "GET", "/blackboard/read", { "name": name } )
        if status_code == 200:
            return json.loads( text )
        elif status_code == 400:
            raise APIError( 400, "Invalid parameters" )
        elif status_code == 404:
            raise APIError( 404, "Blackboard not found" )
        elif status_code == 444:
            raise APIError( 444, "Blackboard is empty" )
        elif status_code == 500:
            raise APIError( 500, "Internal error" )
        else:
            raise APIError( status_code, "Unkown error")

    def status_blackboard(self, name):
        status_code, text = self.call( "GET", "/blackboard/getStatus", { "name": name } )
        if status_code == 200:
            return json.loads( text )
        elif status_code == 400:
            raise APIError( 400, "Invalid parameters" )
        elif status_code == 404:
            raise APIError( 404, "Blackboard not found" )
        elif status_code == 500:
            raise APIError( 500, "Interal Error" )
        else:
            raise APIError( status_code, "Unkown error")

    def list_blackboards(self):
        status_code, text = self.call( "GET", "/blackboard/list", {} )
        if status_code == 200:
            return json.loads( text )
        elif status_code == 500:
            raise APIError( 500, "Internal error" )
        else:
            raise APIError( status_code, "Unkown error")

    def delete_blackboard(self, name):
        status_code, text = self.call( "DELETE", "/blackboard/delete", { "name": name } )
        if status_code == 200:
            pass
        elif status_code == 400 :
            raise APIError( 400, "Invalid parameters" )
        elif status_code == 404:
            raise APIError( 404, "Blackboard not found")
        elif status_code == 500:
            raise APIError( 500, "Internal error")
        else:
            raise APIError( status_code, "Unkown error")

    def delete_blackboard_all(self):
        status_code, text = self.call( "DELETE", "/blackboard/deleteAll", {} )
        if status_code == 200:
            pass
        elif status_code == 500:
            raise APIError( 500, "Internal error" )
        else:
            raise APIError( status_code, "Unkown error" )


class Option:

    def __init__(self, name, help, suboptions=[] ):
        self.name = name
        self.help = help
        self.suboptions = suboptions

# Setup options
############################
options = [
    Option( "create", "Create a new blackboard", [
        Option( "name", "Blackboard name" ),
        Option( "valid_time", "Time until a message gets invalid" )
    ]),
    Option( "display", "Displays a new message on the blackboard", [
        Option( "name", "Blackboard name" ),
        Option( "message", "Message content" )
    ]),
    Option( "clear", "Clears a blackboard", [
        Option( "name", "Blackboard name" )
    ]),
    Option( "read", "Prints the current message on a blackboard", [
        Option( "name", "Blackboard name" )
    ]),
    Option( "status", "Checks if message on blackboard is valid or invalid", [
        Option( "name", "Blackboard name" )
    ]),
    Option( "list", "List all blackboards" ),
    Option( "delete", "Delete a blackboard", [
        Option( "name", "Blackboard name" ),
        Option( "--all", "Delete all blackboards" )
    ])
]

parser = argparse.ArgumentParser( description='Command line tool for viewing and manipulating distributed blackboards' )
parser.add_argument( "--debug", help="Enables debug output", action="store_true" )
subparser = parser.add_subparsers(  help="subcommand" )

for option in options:
    p = subparser.add_parser( option.name, help=option.help )
    p.set_defaults( option=option.name )

    for suboption in option.suboptions:
        if "--" in suboption.name:
            p.add_argument( suboption.name, help=suboption.help, action="store_true" )
        else:
            p.add_argument( suboption.name, help=suboption.help )

args = parser.parse_args()
if not( "option" in vars(args) ):
    parser.print_help()
    sys.exit( 1 )
############################

api = API( "http://localhost:5000", args.debug )

try:

    if args.option == 'create':
        api.create_blackboard( args.name, args.valid_time )
        print( "Created blackboard '{}' with a valid time of {}".format( args.name, args.valid_time ) )

    elif args.option == "display":
        api.display_blackboard( args.name, args.message )
        print( "Displayed '{}' to blackboard '{}'".format( args.message, args.name ) )

    elif args.option == "clear":
        api.clear_blackboard( args.name )
        print( "Cleared blackboard '{}'".format( args.name ) )

    elif args.option == "read":
        bb = api.read_blackboard( args.name )

        valid = "valid" if bb['validity'] else "invalid"
        content = bb['content']

        print( "Blackboard data ({}):".format( valid ) )
        print( content )

    elif args.option == "status":
        result = api.status_blackboard( args.name )

        print( "Blackboard '{}' status:" )
        print( " - Empty:", result['empty'] )
        print( " - Valid: ", result['validity'] )
        print( " - Last message timestamp:", result['timestamp'] )

    elif args.option == "list":
        blackboards = api.list_blackboards()

        print( "Available blackboards:" )
        [print( " -", bb["name"] ) for bb in blackboards]

    elif args.option == "delete":
        if args.all:
            api.delete_blackboard_all()
            print( "Deleted all blackboards" )
        else:
            api.delete_blackboard( args.name )
            print( "Deleted blackboard '{}'".format( args.name) )

except APIError as e:
    print( "ERROR:", e )
    sys.exit( 1 )