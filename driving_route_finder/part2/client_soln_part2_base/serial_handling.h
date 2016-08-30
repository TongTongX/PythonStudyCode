#ifndef SERIAL_HANDLING_H
#define SERIAL_HANDLING_H

#include <stdint.h>
#include "core_types.h"
// >>>>>>>>>>>>>>>>>>>> CUT >>>>>>>>>>>>>>>>>>>> 

/** Gets the length of the path between start and end.
    The function sends a request to the server listening 
    on the serial port and waits for the server responding
    with the number of waypoints along the path from start to end.
  */
int srv_get_pathlen(LonLat32 start, LonLat32 end);

/** Gets the waypoints on the path from start to end
    corresponding to a previously requested path.
    This function can be called only once after every call
    to srv_get_pathlen, which iniates the request.
  */
int srv_get_waypoints(LonLat32* waypoints, int path_len);
// <<<<<<<<<<<<<<<<<<<< CUT <<<<<<<<<<<<<<<<<<<< 


/*
    Function to read a single line from the serial buffer up to a specified
  length (length includes the null termination character that must be
  appended onto the string).  This function is blocking. The newline
  character sequence is given by CRLF, or "\r\n".

  Arguments:
  buffer: Pointer to a buffer of characters where the string will be stored.

  length: The maximum length of the string to be read.

  Preconditions:  None.

  Postconditions: Function will block until a full newline has been read, or the
    maximum length has been reached.  Afterwards the new string will be stored 
    in the buffer passed to the function.

  Returns: the number of bytes read

*/
uint16_t serial_readline(char *line, uint16_t line_size);

/*
    Function to read a portion of a string into a buffer, up to any given
  separation characters.  This will read up to the specified length of the
  character buffer if a separation character is not encountered, or until the 
  end of the string which is being copied.  A starting index of the string 
  being copied can also be specified.

  Arguments:
  str:  The string which is having a portion copied.
  str_start:  The index of the string to start at. (Less than str's length).
  buf:  The buffer to store the copied chunk of the string into.
  buf_len:  The length of the buffer.
  sep:  String containing characters that will be used as separators.

  Preconditions:  Make sure str_start does *NOT* exceed the size of str.

  Postconditions: Stores the resulting string in buf, and returns the
    position where reading was left off at.  The position returned will skip
    separation characters.

*/

uint16_t string_read_field(const char *str, uint16_t str_start, 
    char *field, uint16_t field_size, const char *sep);

/*
 Function to convert a string to an int32_t.

 Arguments:
 str:  The string to convert to an integer.

 Preconditions:  The string should probably represent an integer value.

 Postconditions: Will return the equivalent integer.  If an error occured
     the blink assert may be triggered, and sometimes zero is just returned
    from this function because EINVAL does not exist for the Arduino strtol.

 */

int32_t string_get_int(const char *str);

#endif
