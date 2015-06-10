#
# Zonkers python support library
#
#
# Copyright (C) Whiplash 360, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# June 1, 2015
# Author: D.S.S.
#


from smbus import SMBus
import time
import Adafruit_BBIO.GPIO as GPIO
 
zonk_smb=SMBus(1);
zonk_slaveaddr=0x48;
zonk_verbose=0

# I2C register definitions
_ZONKERS_REG_OFFSET = 0x100
_ZONKERS_A2D_READ = 0 + _ZONKERS_REG_OFFSET           # 8 channels
_ZONKERS_IN_PORT = 16 + _ZONKERS_REG_OFFSET
_ZONKERS_OUT_PORT = 18 + _ZONKERS_REG_OFFSET
_ZONKERS_GAIN_PORT = 20  + _ZONKERS_REG_OFFSET
_ZONKERS_A2D_COMPARE_LOW = 36 + _ZONKERS_REG_OFFSET   # 8 channels
_ZONKERS_A2D_COMPARE_HIGH = 52 + _ZONKERS_REG_OFFSET  # 8 channels
_ZONKERS_CONVERT_ON_READ = 68 + _ZONKERS_REG_OFFSET
_ZONKERS_IO_SETUP = 70 + _ZONKERS_REG_OFFSET          # 8 channels   
_ZONKERS_CONTROL = 86 + _ZONKERS_REG_OFFSET

#def swap16(x):
#    """Swaps the byte order of a 16-bit value."""
#    return ((x << 8 & 0xFF00) | (x >> 8 & 0x00FF))

def zonkers_set_current_address(addr):
    """Sets I2C address in slave."""
    a1=addr/256
    a0=addr%256
    zonk_smb.write_i2c_block_data(zonk_slaveaddr,a1,[a0])

def zonkers_write_block(addr,data):
    """Writes a block sequence to i2c at given address."""
    a1=addr/256
    a0=addr%256

    data.insert(0,a0)
    zonk_smb.write_i2c_block_data(zonk_slaveaddr,a1,data)
    
    # DSS - i2c EEProm example code had this section, it does not seem to be needed for zonkers. Leaving it in for reference    
    # wait until acknowledged
    #ready=0
    #while not ready:
    #	try:
    #		zonk_smb.read_byte(zonk_slaveaddr)
    #		ready=1
    #	except IOError:
    #		ready=0

def zonkers_read_byte(addr):
    """Read a byte from i2c at the given address."""
    zonkers_set_current_address(addr)
    time.sleep(0.050) 
    return zonk_smb.read_byte(zonk_slaveaddr)

def zonkers_read_word(addr):
    """Read 2 bytes (word) from i2c at the given address"""
    zonkers_set_current_address(addr)
    # DSS - I was unable to get this to work without this delay, this works for 400KHz i2c, I think it needs to be longer for 100KHz (default)
    time.sleep(0.050) 
    return zonk_smb.read_byte(zonk_slaveaddr) | zonk_smb.read_byte(zonk_slaveaddr) << 8 # bytes are swapped! line data is BE, we are LE

def zonkers_set_trigger(val):
    """Set zonkers trigger field."""
    blk1=[val/256,val%256] 
    zonkers_write_block(_ZONKERS_CONVERT_ON_READ,blk1)
    if zonk_verbose == 1: 
        print "trigger set to ",format(val,'04x')

def zonkers_read_trigger():
    """Read and return zonkers trigger field."""
    return zonkers_read_word(_ZONKERS_CONVERT_ON_READ)

def zonkers_print_trigger():
    """Read and print zonkers trigger field."""
    val = zonkers_read_trigger()
    if zonk_verbose == 1: 
        print "trigger=",format(val,'04x')

def zonkers_read_a2d(port):
    """Read and return the A2D value of the given port (1-8), value is in mV."""
    val = zonkers_read_word(_ZONKERS_A2D_READ + ((port - 1) * 2))
    if zonk_verbose == 1: 
        print "A2D Value[", port, "]=", format(val,'04x'), " ", format(val,'04d'), " mV"
    return val;

def zonkers_read_inputs ():
    """Read (via i2c) and return zonkers input register field."""
    return zonkers_read_word(_ZONKERS_IN_PORT)

def zonkers_read_outputs ():
    """Read (via i2c) and return zonkers output register field."""
    return zonkers_read_word(_ZONKERS_OUT_PORT)


def zonkers_set_outputs(val):
    """Set the zonkers output register field."""
    blk=[val]
    zonkers_write_block(_ZONKERS_OUT_PORT+1,blk)
    if zonk_verbose == 1: 
        print "outputs set to ",format(val,'02x')

def zonkers_print_ios():
    """Read and print zonkers input and output register fields."""
    print "Inputs=", format(zonkers_read_inputs(),'04x')
    print "Outputs=",format(zonkers_read_outputs(),'04x')


def zonkers_set_gain(port,val):
    """Set the gain setting for the given A2D port."""
    blk=[val]
    zonkers_write_block(_ZONKERS_GAIN_PORT+((port-1)*2)+1,blk)
    if zonk_verbose == 1: 
        print "gain[",port,"] set to ",format(val,'02x')

def zonkers_read_gain (port):
    """Read and return the gain setting for the given A2D port."""
    return zonkers_read_word(_ZONKERS_GAIN_PORT + ((port-1)*2))


def zonkers_print_gain (port):
    """Read and print the gain setting for the given A2D port."""
    val = zonkers_read_gain(port)
    print "Gain[", port, "]=", format(val,'04x')

def zonkers_print_a2d_compare (port):
    """Read and print the A2D gain setting for the given A2D port."""
    val = zonkers_read_word(_ZONKERS_A2D_COMPARE_LOW + ((port-1)*2))
    val2 = zonkers_read_word(_ZONKERS_A2D_COMPARE_HIGH + ((port-1)*2))
    print "A2D Compare[", port, "]=", format(val,'04x'),"-",format(val2,'04x')

def zonkers_print_iosetup(port):
    """Read and print the A2D i/o setup setting for the given A2D port."""
    val = zonkers_read_word(_ZONKERS_IO_SETUP + ((port - 1) * 2))
    print "IO Setup[", port, "]=", format(val,'04x')

def zonkers_set_iosetup(port,val):
    """Read and print the A2D gain setting for the given A2D port."""
    blk=[val]
    zonkers_write_block(_ZONKERS_IO_SETUP+((port-1)*2)+1,blk)
    if zonk_verbose == 1: 
        print "IOSetup[",port,"] set to ",format(val,'02x')

def zonkers_set_complow(port,val):
    """Set the zonkers compare-low register field for the given A2D port."""
    blk1=[val/256] 
    blk2=[val%256]
    zonkers_write_block(_ZONKERS_A2D_COMPARE_LOW+((port-1)*2),blk2)
    zonkers_write_block(_ZONKERS_A2D_COMPARE_LOW+((port-1)*2)+1,blk1)
    if zonk_verbose == 1: 
        print "CompareLow[",port,"] set to ",format(val,'04x')

def zonkers_set_comphi(port,val):
    """Set the zonkers compare-high register field for the given A2D port."""
    blk1=[val/256] 
    blk2=[val%256]
    zonkers_write_block(_ZONKERS_A2D_COMPARE_HIGH+((port-1)*2),blk2)
    zonkers_write_block(_ZONKERS_A2D_COMPARE_HIGH+((port-1)*2)+1,blk1)
    if zonk_verbose == 1: 
        print "CompareHigh[",port,"] set to ",format(val,'04x')

def zonkers_init_ios():
    """Set the I/O pins to inputs on the beagle bone, so that the zonker board can control them."""

    # The input bits 7 -> 0 are on P8 pins 18  -> 11.
    # The output bits 7 -> 0 are on P8 pins 25 -> 32.

    GPIO.setup("P8_18", GPIO.IN)
    GPIO.setup("P8_17", GPIO.IN)
    GPIO.setup("P8_16", GPIO.IN)
    GPIO.setup("P8_15", GPIO.IN)
    GPIO.setup("P8_14", GPIO.IN)
    GPIO.setup("P8_13", GPIO.IN)
    GPIO.setup("P8_12", GPIO.IN)
    GPIO.setup("P8_11", GPIO.IN)

    GPIO.setup("P8_25", GPIO.IN)
    GPIO.setup("P8_26", GPIO.IN)
    GPIO.setup("P8_27", GPIO.IN)
    GPIO.setup("P8_28", GPIO.IN)
    GPIO.setup("P8_29", GPIO.IN)
    GPIO.setup("P8_30", GPIO.IN)
    GPIO.setup("P8_31", GPIO.IN)
    GPIO.setup("P8_32", GPIO.IN)

    GPIO.cleanup()
   

def zonkers_dump_registers():
    """Read and print hex values of entire zonkers register space"""
    for x in range(_ZONKERS_A2D_READ,_ZONKERS_A2D_READ+88,2):
        print "[",x,"]",format(zonkers_read_word(x),'04x')

def zonkers_print_registers ():
    """Read and print all zonkers registers."""
    print "--A2D--"
    for x in range(1,9):
        zonkers_read_a2d(x)
    zonkers_print_ios()
    print "--Gain--"
    for x in range(1,9):
        zonkers_print_gain(x)
    print "--A2D Compare--"
    for x in range(1,9):
        zonkers_print_a2d_compare(x)
    zonkers_print_trigger()
    print "--IO Setup--"
    for x in range(1,9):
        zonkers_print_iosetup(x)




