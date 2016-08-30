'''
Provides the TextSerial class to add a text-based interface for serial.Serial
based on TextIOWrapper. 

Created on Jan 11, 2015
Edited on Feb 14, 2015: 
- improved documentation
- new function get_port for an available serial port 
- timeout of TextSerial constructor defaults to None
- slightly changed test code
@author: csaba
'''
import io
import serial
import sys
import glob

class TextSerial(io.TextIOWrapper):
    '''Adds text-based interface for serial.Serial.
    
    This class simplifies text-based interaction
    with the serial port: The class makes the usual text based services 
    (writing a string, reading a line, reading strings, iterating through the 
    inputs using a for loop) available when working with serial ports.
    '''
    def __init__(self,*args, **kwargs):
        '''Constructs a TextSerial object. Two instances of serial.Serial
        are used; one for input and the other for output.

        The constructor can be called either with specifying the keyword
        argument ser which must then refer to an instance 
        of serial.Serial that will be used for both inputs and outputs, 
        or specifying arguments to be passed to the constructor of 
        serial.Serial for creating an input and and output instance.
        
        When the argument ser is not specified, the following arguments
        will be used to initialize the serial.Serial objects to be created.

        Args passed to serial.Serial (the first three are commonly used):
            port (str, int or None): Device name or port number number or None.
                Defaults to None.
            baudrate (int): Baud rate such as 9600 or 115200 etc.
                Defaults to 9600.
            timeout (float or None): Timeout for reading operations.
                It defaults to None, indefinite blocking. 
                The value of 0 means non-blocking mode.
                Unit is in seconds.
            bytesize (special): Number of data bits. 
                Default value: serial.EIGHTBITS.
            parity (special): Enable parity checking. 
                Default value: serial.PARITY_NONE.
            stopbits (special):  Number of stop bits.
                Default value: serial.STOPBITS_ONE.
            xonxoff (bool): Enable software flow control. Default value: False
            rtscts (bool): Enable hardware (RTS/CTS) flow control.
                Default value: False.
            writeTimeout (float or None): Set a write timeout value.
                Default value: None.
            dsrdtr (bool): Enable hardware (DSR/DTR) flow control.
                Default value: False.
            interCharTimeout (float): Inter-character timeout, None to disable.
                 Default value: None.

            See http://pyserial.sourceforge.net/pyserial_api.html            
            for extra information on these arguments
        
        Other args:
            encoding (str): The text encoding to be used. Defaults to 'ascii'.
            errors (str): How encoding and decoding errors should be handled.
                For details see the documentation of TextIOWrapper. 
                Defaults to None.
            newline (str, or None): Controls how line endings are handled. 
                For details see the documentation of TextIOWrapper; e.g.,
                https://docs.python.org/3/library/io.html#io.TextIOWrapper 
                Defaults to None (universal newline mode).
            line_buffering (bool): Whether upon seeing '\n' in the output,
                the stream will be flushed. 
                If this is set to False, it is the user's responsibility to call
                flush to make sure that the data is actually sent to the
                receiver. Defaults to True.
            write_through (bool): if True, calls to write() are guaranteed not 
                to be buffered. Defaults to False. Only in Python 3.3 or newer.
            ser (Serial): The serial object to be used, 
                for both input and output. This will work properly
                only with some serial objects, such as the loop back object.
                This is meant mainly for testing purposes.
        
        Raises:
            ValueError: Will be raised when parameter are out of range, e.g. 
                baud rate, data bits.
            SerialException: In case the device can not be found or can not be 
                configured.    
            
        '''
        # We initialize two Serial objects; one for the input, another
        # for the output. We need two objects, as upon the destruction
        # of this object, BufferedRWPair will attempt to close both 
        # the reader and the writer, leading to an exception.
        #
        # The documentation of BufferedRWPair at
        # https://docs.python.org/3/library/io.html#io.BufferedRWPair
        # mentions that one should not pass the same object to it both
        # as a reader and writer, but the suggestion there to use
        # BufferedRandom won't work for us as our stream (serial)
        # is non-seekable. Hence, we are forced to open the serial port
        # twice. 
        #
        def getkwarg(parname, defval, kwargs):
            v = defval            
            if parname in kwargs:
                v = kwargs[parname]
                del kwargs[parname]
            return v
          
        # get and remove TextIOWrapper specific arguments;
        # luckily for us these do not overlap with any of the serial arguments
        encoding       = getkwarg('encoding', 'ascii', kwargs)
        errors         = getkwarg('errors',None,kwargs)
        newline        = getkwarg('newline',None,kwargs)
        line_buffering = getkwarg('line_buffering',True,kwargs)
        write_through  = getkwarg('write_through',False,kwargs)
        
        if 'ser' in kwargs:
            self.ser_in = self.ser_out = kwargs.get('ser')
        else:
            self.ser_in  = serial.Serial(*args, **kwargs)
            self.ser_out = serial.Serial(*args, **kwargs)        
        
        # note: a try/catch won't work here, as a failing __init__
        # is kinda fatal, it will put the object into a failed
        # state and I don't know how to recover it from that state
        # otherwise I would prefer try/catch
        
        # note 2: We need to set BufferedRWPair's buffer size to 1;
        # BufferedRWPair forwards the read call to BuferredReader's
        # read function, which expects the
        # underlying stream to return None or b"" when there
        # is no more data available, rather than to block.
        # However, as of pyserial 2.7, Serial.read() blocks.
        # What would be needed is a non-blocking version of Serial.
        # This can be achieved by setting the timeout to zero on Serial,
        # but this kinda defeats the purpose of having nonzero timeouts.
        # Hence, we turn off buffering.
        if sys.version_info.major>=3 and sys.version_info.minor>=3:
            # This works in Python 3.3 and newer
            super().__init__( io.BufferedRWPair(self.ser_in, self.ser_out, 1)
                            , encoding = encoding
                            , errors = errors
                            , newline = newline
                            , line_buffering = line_buffering
                            , write_through = write_through
                            )
        else:
            # no write_through in earlier pythons
            super().__init__( io.BufferedRWPair(self.ser_in, self.ser_out, 1)
                            , encoding = encoding
                            , errors = errors
                            , newline = newline
                            , line_buffering = line_buffering
                            )
            
        # Explanation of the next line:
        # TextIOWrapper reads data in chunks, and NOT ONLY THROUGH 
        # BufferedRWPair's buffering interface, but it has its own chunk-based
        # processing. When the sender did not send data with size>=chunk size,
        # processing will block indefinitely (or as long as the timeout is).
        # The solution suggested here is to reset the chunk size to 1. 
        # The cons is that maybe data processing will not be the most
        # efficient, as data is obtained one byte at time.
        # Adding a timeout kind-of defeats the purpose of timeouts;
        # without changing the chunk size, the wrapper will always wait
        # until the timeout expires! This totally defeats the purpose of
        # timeouts (again).
        self._CHUNK_SIZE = 1
        
    def setTimeout(self,timeout):
        '''Resets the timeout for reading'''
        self.ser_in.setTimeout(timeout)
    def getTimeout(self):
        '''Gets the current timeout for reading'''
        return self.ser_in.setTimeout()

def get_port(ports=[]):
    '''Attempts to find out the port to be used, based on the operating system.
    
    Args:
        ports (list of strings): recommended port names to be checked first.
            Default value is []
            
    Returns 
        str or None: The name of a port that was successfully accessed and
            which could be used in further communications, or None
            if no appropriate was found.
    '''
    ports = ports[:] # make a copy of the list
    if sys.platform.startswith('darwin'):
        ports += glob.glob('/dev/tty.usbmodem*')
    elif sys.platform.startswith('win32'):
        ports += ['COM3','COM2','COM1']
    else: # linux and variants
        ports += glob.glob('/dev/ttyACM*')
        
    for port in ports:
        try:
            with TextSerial(port) as ser:
                pass
            return port
        except serial.SerialException as exc: # errors on MacOS
            pass
        except OSError as exc: # errors on Linux
            if exc.errno!=2:
                raise

    return None

def __main():
    '''Testing the interface'''
    
    print("Using a loopback simulator:")
    with TextSerial(ser=serial.serial_for_url('loop://',timeout=0)) as ser:
        # send 'hello'
        print("hello",file=ser)
        # as this is a loop back, we receive hello:
        line = ser.readline() 
        # an empty line sent back has actually its new line character
        print("Received:",line.rstrip('\r\n'))
        # demonstrate a for loop:
        lno = 0
        print(lno,file=ser)
        for line in ser:
            print("Received:",line.rstrip('\r\n'))
            if lno>=10:
                break
            lno += 1
            print(lno,file=ser)
    try:
        # if one has an echo program:
        baud = 9600
        port = get_port()
        if port==None:
            print("No suitable port found, exiting")
            return
        print("Attempting to use an 'echo' program on",port)
        # We use a single newline character when communicating with the Arduino
        # to mark the end of lines. We are setting the newline parameter to ''.
        # As a result, inputs lines can end in '\n','\r', or '\r\n'.
        # No end of line translation takes place in either reading or
        # writing. Note that print will print '\n' to mark the end of lines.
        #

        def test(timeout=0):
            with TextSerial(port,baud,newline='',timeout=timeout) as ser:
                for i in range(50):
                    msg = 'hello'+" "+str(i)
                    print("Sending:",msg)
                    print(msg,file=ser)
                    line = ser.readline()
                    if line and line[-1]!='\n':
                        # partial lines are possible when using a very short
                        # timeout
                        print("Got partial line:",line)
                    else:
                        print("Got:", line.rstrip('\r\n'))
                print("Cleaning the input buffer")
                ser.setTimeout(1) # set timeout to one second
                for line in ser:
                    print("Got:", line.rstrip('\r\n'))
        timeout = None # blocking mode
        # call the test function
        test(timeout)                    
        print("Closed serial port.")
        timeout = 1 # ridiculously small timeout; likely causing broken comm.
        print("Re-running the test with a timeout of %s seconds" % timeout)
        print("First.. waiting for 5 seconds..")
        import time
        for i in range(5):
            time.sleep(1)
            print('.',end='') # this won't flush
            sys.stdout.flush()
        print()
        print("Starting..")
        time.sleep(1)
        # call the test function
        test(timeout)        
    except serial.SerialException as exc:
        print("Failure. \n",exc)
    except OSError as exc: # error on Linux
        if exc.errno!=2:
            raise
        print("Failure. \n",exc)
            
    print("bye!")
            
if __name__=="__main__":
    __main()            
