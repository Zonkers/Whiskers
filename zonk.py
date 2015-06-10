#!/usr/bin/env python

#
#
# Zonkers python command line toy
#
#
# Copyright (C) Whiplash 360, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# June 1, 2015
# Author: D.S.S.
#

import sys, getopt

from zonkers import *

def zonk_usage ():
    print 'zonkers.py'
    print '  -p/--port=portnum(1-8) : specify the A2D port number, default port is 1'
    print '  -t/--trig=hexval : trigger value '
    print '  -r/--read : read and print the A2D value for the given port'
    print '  -i/--ios  : read and print the input and output fields'
    print '  -o/--output=val  : value to set the output to'
    print '  -g/--gain=val  : value to set the gain to for the given port'
    print '  --showgain  : read and print the gain for the given port' 
    print '  -s/--iosetup=val : value to set the I/O setup field to for the given port'
    print '  --complow=lowval : value to set the Low compare field to for the given port'
    print '  --comphi=highval : value to set the High compare field to for the given port'
    print '  -d/--regdump : read and print hex dump of all register values'
    print '  --print : read and print all register values'
    print '  -l/--loop=count : repeat the given operation count times, must be first parameter'
    print '  --init : initialize GPIOs on beagle bone'

def main(argv):
   port = 1
   val = 0
   repeat = 1

   try:
      opts, args = getopt.getopt(argv,'dhp:t:rio:g:dl:s:',['init','port=','trig=','read','ios','output','gain=','regdump','print','loop=','iosetup=','comphi=','complow=','showgain'])
   except getopt.GetoptError:
       zonk_usage()
       sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         zonk_usage()
         sys.exit()
      elif opt in ('-p', '--port'):
         port = int(arg,0)
         if port<1 or port>8:
             zonk_usage()
             sys.exit(2)
      elif opt in ('-l','--loop'):
         repeat = int(arg,0)
      elif opt in ('-t', '--trigger'):
         val = int(arg,0)
         zonkers_set_trigger(val)
      elif opt in ('-r', '--read'):
         for x in range(0,repeat):
             zonkers_read_a2d(port)
      elif opt in ('-i', '--ios'):
         for x in range(0,repeat):
             zonkers_print_ios()
      elif opt in ('-o', '--output'):
         val = int(arg,0)
         zonkers_set_outputs(val)
      elif opt in ('-s', '--iosetup'):
         val = int(arg,0)
         zonkers_set_iosetup(val)
      elif opt in ('-g', '--gain'):
         val = int(arg,0)
         zonkers_set_gain(port,val)
      elif opt in ('--showgain'):
         zonkers_print_gain(port)
      elif opt in ('--comphi'):
         val = int(arg,0)
         zonkers_set_comphi(port,val)
      elif opt in ('--complow'):
         val = int(arg,0)
         zonkers_set_complow(port,val)
      elif opt in ('-d', '--regdump'):
         zonkers_dump_registers()
      elif opt in ('--print'):
         zonkers_print_registers()
      elif opt in ('--init'):
         zonkers_init_ios()

if __name__ == "__main__":
   main(sys.argv[1:])
