""" myRIO_library - a library for working with NI myRIO in Python

This library is an improvement over nifpga, a Python library that
gives access to the FPGA registers of NI targets with FPGA.

In this library, we have created some support functions and a class
named MyRIO.
"""

from nifpga import Session
from typing import Tuple
import ctypes
import pkg_resources


# RGB constants

RED = 2
GREEN = 1
BLUE = 4
WHITE = 7
RGB_OFF = 0


# Support functions. They are not part of the class MyRIO, but they are used by it.
# Feel free to use them in your own programs.

def u8_to_bits (u8_number: int) -> [bool]:
    """ This function converts u8 values to an array of Booleans """
    mask = 1
    one_by_one = []
    for i in range(8):
        one_by_one.append(bool((u8_number & mask) != 0))
        mask = mask * 2
    return(one_by_one)

def only_one_bit_on (bit_number: int, input_number: int=0) -> int:
    """ This function switches on only one bit on a u8 integer """
    u8_number = 0
    if bit_number <= 7:
        u8_number = (1 << bit_number)
    return input_number | u8_number
    #TODO raise a warning if bit_number is too big

def only_one_bit_off (bit_number: int, input_number: int=0) -> int:
    """ This function switches on only one bit off a u8 integer """
    
    if bit_number <= 7:
        mask = ~(1 << bit_number)
        return input_number & mask
    else:
        return input_number        #TODO raise a warning if bit_number is too big

def raw_to_volts_AB (raw: int) -> float:
    """ This function converts the raw value 
    from myRIO MXP (ports A and B) Analog Input channels to volts
    """

    return raw * 0.001220703

def raw_to_volts_C (raw: int) -> float:
    """ This function converts the raw value 
    from myRIO MSP (port C) Analog Input channels to volts
    """
    
    return raw * 0.004882813

def raw_to_volts_audio (raw: int) -> float:
    """ This function converts the raw value 
    from myRIO Audio Input channels to volts
    """
    
    return raw * 0.001220703

def volts_to_raw_AB (volts: float) -> int:
    """ This function converts values in Volts 
    to raw values for myRIO MXP (ports A and B) Analog Output channels
    """
    
    return int(volts / 0.001220703)

def volts_to_raw_C (volts: float) -> int:
    """ This function converts values in Volts 
    to raw values for myRIO MSP (port C) Analog Output channels
    """ 

    signed_value = int(volts / 0.004882813)
    unsigned_value = ctypes.c_uint16(signed_value).value
    return unsigned_value

def volts_to_raw_audio (volts: float) -> int:
    """ This function converts values in Volts 
    to raw values for Audio Output channels
    """

    signed_value = int(volts / 0.001220703)
    unsigned_value = ctypes.c_uint16(signed_value).value
    return unsigned_value

def volts_to_temperature (volts: float) -> float:
    """ This function converts values in Volts 
    to temperature in Celsius degrees
    """
    return ((volts-1.7)*10/-0.3)+20

def volts_to_luminosity (volts: float) -> float:
    """ This function converts values in Volts 
    to luminosity in percentage (0-100%)
    """
    return 100-(volts*30.3)

def extract_waveform_from_csv_file(file_name: str) -> [int]:
    """ This function extracts a stereo waveform from a .csv file
    and returns it as a list of I16 integers.
    The .csv format is very basic for an audio file, but
    the myRIO has memory limitations, so the audio files
    must be mono and quite shorts.
    We have tried the wave library from Python, but it does not work
    properly with the myRIO, so we have used the csv format that 
    can be easily generated (we used a simple LabVIEW program for that).
    """
    # Open and read a csv file 
    with open(file_name, 'r') as file:
        data = file.readlines()     # Read all the lines of the file
        waveform = []               # Create an empty list for the waveform
        for line in data:           # Read line by line
            waveform.append(volts_to_raw_audio(float(line))) # Append the integer value to the list

    return waveform                # Return the list



class MyRIO:
    """ Class MyRIO: class for accessing NI myRIO inputs and outputs using nifgpa

    NI myRIO is a programmable device with digital and analog inputs and outputs.
    It is usually programmed in LabVIEW, but it can be programmed in Python too.
    """

    __session = None

    def __init__(self, session_bitfile="", session_resource = "RIO0"):
        """ when an instance is created, an nifpga session is created. """
        if session_bitfile == "":
            session_bitfile = pkg_resources.resource_filename('myRIO_base', 'data/Default.lvbitx')

        self.__session = Session(session_bitfile, session_resource)
        sys_handler = self.__session.registers['SYS.RDY']
        while not sys_handler.read():       #TODO: What if the system is never ready?
            time.sleep(0.1)

    def check_if_ready(self) -> bool:
        """ checks if system is ready """
        sys_handler = self.__session.registers['SYS.RDY']
        return sys_handler.read()

    def __del__(self):
        """ This function closes the session with the myRIO FPGA """
        self.__session.close()

    def set_DIO_mask(self, mask_low: int =7, mask_high: int =0, port: str ='A'):
        """ sets the DIO mask for defining the direction (IN/OUT) of the channels

        low 7, high 0 is the default for the design of our current MXP cards
        """

        dir_string_low = 'DIO.' + port + '_' + '7:0' + '.DIR'
        dir_string_high = 'DIO.' + port + '_' + '15:8' + '.DIR'
        mask_handler_low = self.__session.registers[dir_string_low]
        mask_handler_high = self.__session.registers[dir_string_high]
        mask_handler_low.write(mask_low)    # 7 is 00000111 where 1 is OUT
        mask_handler_high.write(mask_high)    # 0 is 00000000 where 0 is IN


    def read_analog_input(self, channel: int, port: str ='A') -> float:
        """ returns the value in volts of one of the AI channels (default port: A) """
    
        channel_string = 'AI.' + port + '_' + str(channel) + '.VAL'
        channel_handler = self.__session.registers[channel_string]
        if port=='A' or port == 'B':
            return raw_to_volts_AB(channel_handler.read())
        elif port=='C':
            return raw_to_volts_C(channel_handler.read())
        elif port=='AudioIn_L' or port =='AudioIn_R':
            return raw_to_volts_audio(channel_handler.read())
        else:
            #TODO how to report the exception (port name error)
            return None

    def read_MXP_temperature(self, channel: int=0, port: str ='A') -> float:
        """ returns the temperature in Celsius degrees of one of the 
            AI channels (default channel:0, default port: A)
        """
        channel_string = 'AI.' + port + '_' + str(channel) + '.VAL'
        channel_handler = self.__session.registers[channel_string]
        if port=='A' or port == 'B':
            return volts_to_temperature(raw_to_volts_AB(channel_handler.read()))
        else:
            #TODO how to report the exception (port name error)
            return None

    def read_MXP_luminosity(self, channel: int =1, port: str ='A') -> float:
        """ returns the luminosity in percentage of one of the 
            AI channels (default channel:1, default port: A)
        """
        channel_string = 'AI.' + port + '_' + str(channel) + '.VAL'
        channel_handler = self.__session.registers[channel_string]
        if port=='A' or port == 'B':
            return volts_to_luminosity(raw_to_volts_AB(channel_handler.read()))
        else:
            #TODO how to report the exception (port name error)
            return None

    def read_digital_input(self, channel: int, port: str ='A') -> bool:
        """ returns the Boolean value of one of the DIO input channels (default port: A) """

        # First, check if the function is asking for a channel 
        # in the low byte (7:0) or in the high byte (15:8)
        if channel<8 :
            channel_string = 'DIO.' + port + '_7:0.IN'
            array_index = int(channel)
        else:
            channel_string = 'DIO.' + port + '_15:8.IN'
            # The length of the array is 8, so the index should be in the 7:0 range
            array_index = channel-8

        channel_handler = self.__session.registers[channel_string]
        raw_value = channel_handler.read()
        bool_array = u8_to_bits(raw_value)
        return bool_array[array_index]

    def read_digital_port(self, port: str ='A') -> [bool]:
        """ returns the Boolean values of the whole port (default port: A) """

        channel_string_low = 'DIO.' + port + '_7:0.IN'
        channel_string_high = 'DIO.' + port + '_15:8.IN'
        channel_handler_low = self.__session.registers[channel_string_low]
        channel_handler_high = self.__session.registers[channel_string_high]
        raw_value_low = channel_handler_low.read()
        raw_value_high = channel_handler_high.read()
        bool_array = u8_to_bits(raw_value_low) + u8_to_bits(raw_value_high)
        return bool_array

    def read_MXP_button(self, button: int =1, port: str ='A') -> bool:
        """ returns the Boolean value of one of the MXP buttons (default port: A) 
            We spect 1 for the first button, 2 for the second one.
            Most of our cards have a black button first, a white button second.
        """
        channel_string = 'DIO.' + port + '_7:0.IN'
        array_index = int(button+2)
        channel_handler = self.__session.registers[channel_string]
        raw_value = channel_handler.read()
        bool_array = u8_to_bits(raw_value)
        return bool_array[array_index]

    def read_button(self) -> bool:
        """ returns the Boolean value of the myRIO onboard button """

        channel_string = 'DI.BTN'
        channel_handler = self.__session.registers[channel_string]
        raw_value = channel_handler.read()
        return bool(raw_value)

    def read_analog_accelerometer(self) -> Tuple[float, float, float]:
        """ returns the x, y, and z values in Gs of the onboard Accelerometer """
    
        channel_string_x = 'ACC.X.VAL'
        channel_string_y = 'ACC.Y.VAL'
        channel_string_z = 'ACC.Z.VAL'
        channel_handler_x = self.__session.registers[channel_string_x]
        channel_handler_y = self.__session.registers[channel_string_y]
        channel_handler_z = self.__session.registers[channel_string_z]
        raw_value_x = channel_handler_x.read()
        raw_value_y = channel_handler_y.read()
        raw_value_z = channel_handler_z.read()

        if raw_value_x & (1 << 15):
        # Perform two's complement conversion for negative numbers
            raw_value_x = raw_value_x - (1 << 16)
        x_value = float(raw_value_x) / 256.0

        if raw_value_y & (1 << 15):
        # Perform two's complement conversion for negative numbers
            raw_value_y = raw_value_y - (1 << 16)
        y_value = float(raw_value_y) / 256.0

        if raw_value_z & (1 << 15):
        # Perform two's complement conversion for negative numbers
            raw_value_z = raw_value_z - (1 << 16)
        z_value = float(raw_value_z) / 256.0

        return x_value, y_value, z_value

    def write_leds_integer(self, raw_value: int):
        """ changes the state of the myRIO onboard LEDs using an integer value """

        value = max(0, min(raw_value, 15))      #TODO: raising a warning when out of range?
        channel_string = 'DO.LED3:0'
        channel_handler = self.__session.registers[channel_string]
        channel_handler.write(value)

    def write_leds_booleans(self, boolean_values: [bool]):
        """ changes the state of the myRIO onboard LEDs using Booleans """

        raw_value = 0
        j = 1
        for i in range(4):
            raw_value = raw_value + boolean_values[i]*j
            j = j*2

        channel_string = 'DO.LED3:0'
        channel_handler = self.__session.registers[channel_string]
        channel_handler.write(raw_value)
        return None

    def write_digital_output(self,
                             channel: int,
                             value: bool,
                             port: str ='A',
                             mask_low: int =7,
                             mask_high: int =0):
        """ writes a Boolean value on one of the DIO output channels (default port: A)
        The defaults are set for the design of our current MXP cards: 
        RGB LEDs at channels 0,1,2 (G,R,B) and buttons at channels 3,4. Rest unused.
        """
        self.set_DIO_mask(port=port, mask_low=mask_low, mask_high=mask_high)

        # Check if the function is asking for a channel 
        # in the low byte (7:0) or in the high byte (15:8)
        if 0 <= channel <= 7 :
            channel_string = 'DIO.' + port + '_7:0.OUT'
            mask_string = 'DIO.' + port + '_7:0.DIR'
        elif 8 <= channel <= 15:
            channel_string = 'DIO.' + port + '_15:8.OUT'
            mask_string = 'DIO.' + port + '_15:8.DIR'
            channel = channel-8
        else:
            #TODO raise an error if channel is out of range
            return None

        mask_handler = self.__session.registers[mask_string]
        saved_mask = mask_handler.read()
        new_mask = only_one_bit_on(channel, saved_mask)
        mask_handler.write(new_mask)

        channel_handler = self.__session.registers[channel_string]
        saved_value = channel_handler.read()

        if value:
            value_to_be_written = only_one_bit_on(channel,saved_value)
        else:
            value_to_be_written = only_one_bit_off(channel,saved_value)

        channel_handler.write(value_to_be_written)

        mask_handler.write(saved_mask)   # restore original DIR mask

    def write_digital_port(self, 
                           value_low: int, 
                           value_high: int=255, 
                           port: str ='A',
                           mask_low: int =7,
                           mask_high: int =0):
        """ writes integer low and high values on DIO output channels (default port: A)
        The defaults are set for the design of our current MXP cards: 
        RGB LEDs at channels 0,1,2 (G,R,B) and buttons at channels 3,4. Rest unused.
        """
        
        self.set_DIO_mask(port=port, mask_low=mask_low, mask_high=mask_high)

        channel_string_low = 'DIO.' + port + '_7:0.OUT'
        channel_string_high = 'DIO.' + port + '_15:8.OUT'
        channel_handler_low = self.__session.registers[channel_string_low]
        channel_handler_high = self.__session.registers[channel_string_high]
        channel_handler_low.write(value_low)
        channel_handler_high.write(value_high)
 
    def write_MXP_RGB_LED(self, color: int, port: str ='A'):
        """ writes a color on the myRIO MXP RGB LED (default port: A) """

        self.set_DIO_mask(port=port)    # default mask is OK for the RGB LED
        channel_string_low = 'DIO.' + port + '_7:0.OUT'
        channel_handler_low = self.__session.registers[channel_string_low]
        channel_handler_low.write(color)
 
    def write_analog_output(self, channel: int, value: float, port: str ='A'):
        """ writes a value (in volts) on an AO channel (default port: A) """
    
        channel_string = 'AO.' + port + '_' + str(channel) + '.VAL'
        channel_handler = self.__session.registers[channel_string]
        if port=='A' or port == 'B':
            raw_value = volts_to_raw_AB(value)
        elif port=='C':
            raw_value = volts_to_raw_C(value)
        elif port=='AudioOut_L' or port =='AudioOut_R':
            raw_value = volts_to_raw_audio(value)
        else:
            #TODO how to report the exception (port name error)
            raw_value = 0
        channel_handler.write(raw_value)
        go_handler = self.__session.registers['AO.SYS.GO']
        go_handler.write(True)

    def play_waveform(self, waveform: [int]):
        """ plays a waveform on the myRIO Audio Output channels """
    
        channel_string_left = 'AO.AudioOut_L.VAL'
        channel_string_right = 'AO.AudioOut_R.VAL'
        channel_handler_left = self.__session.registers[channel_string_left]
        channel_handler_right = self.__session.registers[channel_string_right]

        go_handler = self.__session.registers['AO.SYS.GO']

        for i in range(len(waveform)):
            channel_handler_left.write(waveform[i])
            channel_handler_right.write(waveform[i])
            go_handler.write(True)

if __name__ == "__main__":
    print("This is a library for working with NI myRIO in Python")
    print("It is not intended to be run directly, but to be imported in other programs.")
    print("Please, see the documentation for more information.")
    from time import sleep
    myrio1 = MyRIO()

    
    print("Read digital port A:")
    print(myrio1.read_digital_port(port='A'))
    print("Read temperature from MXP port A, channel 0:")
    print(myrio1.read_MXP_temperature())
    print("Read luminosity from MXP port A, channel 1:")
    print(myrio1.read_MXP_luminosity())
    print("RGB LED in MXP port A: RED")
    myrio1.write_MXP_RGB_LED(RED)
    sleep(1)
    print("RGB LED in MXP port A: GREEN")
    myrio1.write_MXP_RGB_LED(GREEN)
    sleep(1)
    print("RGB LED in MXP port A: BLUE")
    myrio1.write_MXP_RGB_LED(BLUE)
    sleep(1)
    print("RGB LED in MXP port A: OFF")
    myrio1.write_MXP_RGB_LED(RGB_OFF)

    
    # Play a simple waveform (2024/04/10)
    print("Playing a simple waveform")
    csv_file = pkg_resources.resource_filename('myRIO_base', 'examples/PinkPanther.csv')
    my_waveform = extract_waveform_from_csv_file(csv_file)
    myrio1.play_waveform(my_waveform)



        
""" TODO

There are some extra features that we do not cover.
They are interesting, but are not so commonly used, and given
their complexity, we leave them for future development.
The features we did not cover are:
1.-PWM and ENC
2.-I2C and SPI
3.-IRQs

It would be interesting too to improve the audio functions.
"""

""" Credits
This library has been developed from scratch by Aitzol Ezeiza Ramos
from the University of the Basque Country (UPV/EHU)
It is strongly based on nifpga the basic library for accessing the
FPGA on NI RIO devices.

https://github.com/ni/nifpga-python/

We also use typing and ctypes.

First version: 2024/02/28
Current version: 2024/03/14
"""
