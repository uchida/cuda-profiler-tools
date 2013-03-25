#!/usr/bin/env python

# Author: Javier Cabezas <javier.cabezas@bsc.es>
#
# Copyright (c) 2013 Barcelona Supercomputing Center
#                    IMPACT Research Group
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cudaprof
from datetime import datetime

def now():
    time = datetime.time(datetime.now())
    return time.strftime("%H:%M:%S")

# Used for debugging purposes
def shell():
    from IPython import embed
    embed()

if __name__=="__main__":
    import argparse
    import subprocess as proc

    parser = argparse.ArgumentParser(description = 'Profile CUDA programs')
    parser.add_argument('cmdline', metavar='cmdline', type = str,
                        help = 'Program to be profiled')
    parser.add_argument('args', metavar='arg', type = str, nargs = '*',
                        help = 'Argument to be passed to the program')
    parser.add_argument('-g', '--graphical', dest = 'graphical', action='store_const',
                        const = True, default = False,
                        help = 'Show the graphical interface')
    parser.add_argument('-c', '--conf', metavar='CONF_FILE', dest = 'conf', action='store',
                        default = None,
                        help = 'Configuration file')
    parser.add_argument('-o', '--out', metavar='OUT_FILE_PATTERN', dest = 'out', action='store',
                        default = 'cuda_profile_%d_%p.log',
                        help = 'Output file pattern')

    args = vars(parser.parse_args())

    OPTION_CMD       = args['cmdline']
    OPTION_CMD_ARGS  = ' '.join(args['args'])

    OPTION_GRAPHICAL = args['graphical']
    OPTION_CONF_FILE = args['conf'] 
    OPTION_OUT_FILE_PATTERN = args['out'] 

    # Initialize CUDA
    cudaprof.cuda.init()

    # Create counters
    options = cudaprof.cuda.get_options()
    # Create counters
    counters = cudaprof.cuda.get_counters(False)
    # Read counters from configuration file
    options_conf, counters_conf = cudaprof.io.get_conf_from_file(OPTION_CONF_FILE)

    # Merged options with configuration file
    cudaprof.init_options(options, options_conf)
    # Merged counters with configuration file
    cudaprof.init_counters(counters, counters_conf)

    if OPTION_GRAPHICAL == False:
        # Collect enabled options
        enabled_options = [ option for option in options if option.active == True ]
        # Collect enabled events
        enabled_counters = [ counter for domain, _counters in counters.items()
                                     for counter in _counters if counter.active == True ]

        groups = core.cuda.get_event_groups(enabled_counters)

        def print_progress(n):
            i = 1
            while i <= n:
                print "%s: Run %d/%d" % (now(), i, n)
                i +=1
                yield

        progress = print_progress(len(groups))

        core.runner.launch_groups(OPTION_CMD, OPTION_CMD_ARGS, enabled_options, groups, progress)
    else:
        import cudaprof.gui as gui

        gui.start(options, counters, OPTION_CONF_FILE, OPTION_CMD, OPTION_CMD_ARGS)
