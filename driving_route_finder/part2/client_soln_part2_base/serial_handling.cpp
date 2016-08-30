#include "serial_handling.h"

#include <Arduino.h>
#include <errno.h>
#include <assert13.h>
#include <stdio.h> // isdigit
#include <stdlib.h>
#include <string.h>


// server get path length
// return the path length as an integer
int srv_get_pathlen(LonLat32 start, LonLat32 end) 
{
	// make sure println prints the last thing
	Serial.println(""); 

	// send request line
	unsigned long startTime = millis();
	while (true) 
	{
		if (millis() - startTime > 1000) { 
			Serial.println("TIMEOUT");
			delay(1000);
			Serial.println("");
			startTime = millis();
			continue;
		}

		// if timeout does not occur, then send the request line (a string)
		Serial.print("R ");
		Serial.print(start.lat);
		Serial.print(" ");
		Serial.print(start.lon);
		Serial.print(" ");
		Serial.print(end.lat);
		Serial.print(" ");
		Serial.println(end.lon);
		
		break;
	}
	
	// wait for path length from server
	startTime = millis();
	String path_len;
	while (true) 
	{
		if (millis() - startTime > 10000) 
		{
			Serial.println("TIMEOUT");
			return false;
		}
		if (Serial.available()) 
		{
			path_len = Serial.readStringUntil('\n'); 
			if (path_len.substring(0,1) == "N") {
				break;
			}
		}
	}
	// print path_len 
	Serial.println(path_len.substring(2,3).toInt()); 

	return path_len.substring(2).toInt();
}

int srv_get_waypoints(LonLat32* waypoints, int path_len) 
{
	// make sure println prints the last thing
	Serial.println(""); 
	
	Serial.println("A"); 
	
	// store waypoint from server and acknowledge it
	int i = 0;
	unsigned long startTime = millis(); 
	while (true) 
	{
		if (millis() - startTime > 1000) 
		{
			Serial.println("TIMEOUT");
			return false;
		}
		if (Serial.available()) {
			String inLine = Serial.readStringUntil('\n');
			// session has ended 
			if (inLine.substring(0,1) == "E") {
				break;
			}
			// waypoint string
			if (inLine.substring(0,1) == "W") {
				// store the waypoint
				waypoints[i] = LonLat32(inLine.substring(10,19).toInt(),inLine.substring(2,9).toInt());
				// send acknowledgement
				Serial.println("A\n"); 
			}
	
			i += 1;
			startTime = millis(); 
		}
	}
	Serial.println(millis() - startTime); 

	return 0;
}

uint16_t serial_readline(char *line, uint16_t line_size) {
	int bytes_read = 0;    // Number of bytes read from the serial port.

	// Read until we hit the maximum length, or a newline.
	// One less than the maximum length because we want to add a null terminator.
	while (bytes_read < line_size - 1) {
		while (Serial.available() == 0) {
			// There is no data to be read from the serial port.
			// Wait until data is available.
		}

		line[bytes_read] = (char) Serial.read();

		// A newline is given by \r or \n, or some combination of both
		// or the read may have failed and returned 0
		if ( line[bytes_read] == '\r' || line[bytes_read] == '\n' ||
			 line[bytes_read] == 0 ) {
				// We ran into a newline character!  Overwrite it with \0
				break;    // Break out of this - we are done reading a line.
		} else {
			bytes_read++;
		}
	}

	// Add null termination to the end of our string.
	line[bytes_read] = '\0';
	return bytes_read;
}

uint16_t string_read_field(const char *str, uint16_t str_start
	, char *field, uint16_t field_size, const char *sep) {

	// Want to read from the string until we encounter the separator.

	// Character that we are reading from the string.
	uint16_t str_index = str_start;    

	while (1) {
		if ( str[str_index] == '\0') {
			str_index++;  // signal off end of str
			break;
		}

		if ( field_size <= 1 ) break;

		if (strchr(sep, str[str_index])) {
			// field finished, skip over the separator character.
			str_index++;    
			break;
		}

		// Copy the string character into buffer and move over to next
		*field = str[str_index];    
		field++;
		field_size--;
		// Move on to the next character.
		str_index++;    
	}

	// Make sure to add NULL termination to our new string.
	*field = '\0';

	// Return the index of where the next token begins.
	return str_index;    
}

int32_t string_get_int(const char *str) {
	// Attempt to convert the string to an integer using strtol...
	int32_t val = strtol(str, NULL, 10);

	if (val == 0) {
		// Must check errno for possible error.
		if (errno == ERANGE) {
			Serial.print("string_get_int failed: "); Serial.println(str);
			assert13(0, errno);
		}
	}

	return val;
}
