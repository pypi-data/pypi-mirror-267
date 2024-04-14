#****************************************************************************
#* __main__.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
import argparse
from .impl.cmd.cmd_gen_sv import CmdGenSV

def getparser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)
    gen_sv = subparsers.add_parser("gen-sv",
        help="Generate one or more SV classes, optionally enclosed in a package")
    gen_sv.add_argument("-m", "--module",
        action="append",
        required=True,
        help="Specify a Python module to load for API discovery")
    gen_sv.add_argument("-uvm", action="store_true",
        help="Generates UVM-friendly interface classes")
    gen_sv.add_argument("-i", "--include",
        action="append",
        help="Specify a pattern for API inclusion")
    gen_sv.add_argument("-e", "--exclude",
        action="append",
        help="Specify a pattern for API exclusion")
    gen_sv.add_argument("-p", "--package",
        help="Place the generated class APIs in a package")
    gen_sv.add_argument("-o", "--output",
        default="hdl_call_if_api.svh",
        help="Specifies the output filename")
    gen_sv.set_defaults(func=CmdGenSV())

    return parser

def main():
    parser = getparser()
    args = parser.parse_args()

    args.func(args)

if __name__ == "__main__":
    main()


