#include <Arduino.h>
#include <Adafruit_ST7735.h> 
#include <SD.h>
#include <mem_syms.h>

#include "map.h"
#include "serial_handling.h"

// #define DEBUG_SCROLLING
//#define DEBUG_PATH
#define DEBUG_MEMORY

// Pins and interrupt lines for the zoom in and out buttons.
const uint8_t zoom_in_interrupt = 1;     // Digital pin 3.
const uint8_t zoom_in_pin = 3;

const uint8_t zoom_out_interrupt = 0;    // Digital pin 2.
const uint8_t zoom_out_pin = 2;

// the pins used to connect to the AdaFruit display
const uint8_t sd_cs = 5;
const uint8_t tft_cs = 6;
const uint8_t tft_dc = 7;
const uint8_t tft_rst = 8;    

// Arduino analog input pin for the horizontal on the joystick.
const uint8_t joy_pin_x = 1;
// Arduino analog input pin for the vertical on the joystick.
const uint8_t joy_pin_y = 0;
// Digital pin for the joystick button on the Arduino.
const uint8_t joy_pin_button = 4;

// forward function declarations
void initialize_sd_card();
void initialize_screen();
void initialize_joystick();
uint8_t process_joystick(int16_t *dx, int16_t *dy);
void status_msg(char *msg);
void clear_status_msg();

// Interrupt routines for zooming in and out.
void handle_zoom_in();
void handle_zoom_out();

// global state variables

// globally accessible screen
Adafruit_ST7735 tft = Adafruit_ST7735(tft_cs, tft_dc, tft_rst);

// Map number (zoom level) currently selected.
extern uint8_t current_map_num;

// First time flag for loop, set to cause actions for the first time only
uint8_t first_time;

void setup() {
	Serial.begin(9600);
	Serial.println("Starting...");
	Serial.flush();    // There can be nasty leftover bits.

	initialize_screen();

	initialize_sd_card();

	initialize_joystick();

	initialize_map();

	// Want to start viewing window in the center of the map
	move_window(
		(map_box[current_map_num].W + map_box[current_map_num].E) / 2,
		(map_box[current_map_num].N + map_box[current_map_num].S) / 2
	);

	// with cursor in the middle of the window
	move_cursor_to( screen_map_x + display_window_width / 2
				  , screen_map_y + display_window_height / 2
	);

	// Draw the initial screen and cursor
	first_time = 1;

	// Now initialize and enable the zoom buttons.
	pinMode(zoom_out_pin, INPUT);    // Zoom out.
	digitalWrite(zoom_out_pin, HIGH);

	pinMode(zoom_in_pin, INPUT);    // Zoom in.
	digitalWrite(zoom_in_pin, HIGH);

	// Initialize interrupt routines attached to zoom buttons.
	attachInterrupt(zoom_in_interrupt, handle_zoom_in, FALLING);
	attachInterrupt(zoom_out_interrupt, handle_zoom_out, FALLING);

#ifdef DEBUG_MEMORY
	Serial.print("Available mem:");
	Serial.println(AVAIL_MEM);
#endif
}

const uint16_t screen_scroll_delta = 32;
const uint16_t screen_left_margin = 10;
const uint16_t screen_right_margin = 117;
const uint16_t screen_top_margin = 10;
const uint16_t screen_bottom_margin = 117;

// the path request, start and stop lat and lon
typedef enum {
	RS_WAIT_FOR_START = 0,
	RS_WAIT_FOR_STOP,
	RS_WAIT_LAST
} RequestState;

RequestState request_state = RS_WAIT_FOR_START;
LonLat32 start = LonLat32(0,0);
LonLat32 end = LonLat32(0,0);

// #define __SERVER

#ifndef __SERVER    
void debug_msg(char* str) {
	Serial.print(str);
}

void debug_msg(int num) {
	Serial.print(num);
}

void debug_msg(long num) {
	Serial.print(num);
}
#else
void debug_msg(char* str) {}
void debug_msg(int num)   {}
void debug_msg(long num)  {}
#endif

void loop() {
	while (1) {
		// Make sure we don't update the map tile on screen when we don't need to!
		uint8_t update_display_window = 0;

		if (first_time) {
			first_time = 0;
			update_display_window = 1;
		}

		// Joystick displacement.
		int16_t dx = 0;
		int16_t dy = 0;
		uint8_t select_button_event = 0;

		// If the map has been zoomed in or out we need to do a redraw,
		// and will center the display window about the cursor.
		// So a zoom in-out will re-center over a mis-positioned cursor!
		
		// if the map changed as a result of a zoom button press
		if (shared_new_map_num != current_map_num) {
	#ifdef DEBUG_SCROLLING
			Serial.print("Zoom from ");
			Serial.print(current_map_num);
			Serial.print(" x ");
			Serial.print(cursor_map_x);
			Serial.print(" y ");
			Serial.print(cursor_map_y);
	#endif

			// change the map and figure out the position of the cursor on
			// the new map.
			set_zoom();

			// center the display window around the cursor 
			move_window_to( cursor_map_x - display_window_width/2
						  , cursor_map_y - display_window_height/2
			);

	#ifdef DEBUG_SCROLLING
			Serial.print(" to ");
			Serial.print(current_map_num);
			Serial.print(" x ");
			Serial.print(cursor_map_x);
			Serial.print(" y ");
			Serial.print(cursor_map_y);
			Serial.println();
	#endif

			// Changed the zoom level, so we want to redraw the window
			update_display_window = 1;
		}


		// Now, see if the joystick has moved, in which case we want to
		// also want to move the visible cursor on the screen.

		// Process joystick input.
		select_button_event = process_joystick(&dx, &dy);

		// the joystick routine filters out small changes, so anything non-0
		// is a real movement
		if (abs(dx) > 0 || abs(dy) > 0) {
			// Is the cursor getting near the edge of the screen?  If so
			// then scroll the map over by re-centering the window.

			uint16_t new_screen_map_x = screen_map_x;
			uint16_t new_screen_map_y = screen_map_y;
			uint8_t need_to_move = 0;

			uint16_t cursor_screen_x;
			uint16_t cursor_screen_y;
			if (get_cursor_screen_x_y(&cursor_screen_x, &cursor_screen_y)) {
				// if the cursor is visible, then adjust the display to 
				// to scroll if near the edge.

				if (cursor_screen_x < screen_left_margin) {
					new_screen_map_x = screen_map_x - screen_scroll_delta;
					need_to_move = 1;
				}
				else if (cursor_screen_x > screen_right_margin) {
					new_screen_map_x = screen_map_x + screen_scroll_delta;
					need_to_move = 1;
				}

				if (cursor_screen_y < screen_top_margin) {
					new_screen_map_y = screen_map_y - screen_scroll_delta;
					need_to_move = 1;
				}
				else if (cursor_screen_y > screen_bottom_margin) {
					new_screen_map_y = screen_map_y + screen_scroll_delta;
					need_to_move = 1;
				}

				if (need_to_move) {
					// move the display window, leaving cursor at same lat-lon
					move_window_to(new_screen_map_x, new_screen_map_y);
					update_display_window = 1;
				} 
				else {
					// erase old cursor, move, and draw new one, no need to 
					// redraw the underlying map tile
					erase_cursor();
					move_cursor_by(dx, dy);
					draw_cursor();
				}
			}
		}

		// at this point the screen is updated, with a new tile window and
		// cursor position if necessary

		// will only be down once, then waits for a min time before allowing
		// pres again.
		if (select_button_event) {
			// Button was pressed, we are selecting a point!
			// which press is this, the start or the stop selection?

			// If we are making a request to find a shortest path, we will send out
			// the request on the serial port and then wait for a response from the
			// server.  While this is happening, the client user interface is
			// suspended.

			// if the stop point, then we send out the server request and wait.

			// This is a place holder for the code you need to write. This simply
			// prints the position of the cursor to the Serial port. 
			// Remove these lines and fill in your own code here.
			debug_msg("Button press @ ");
			debug_msg(cursor_lat);
			debug_msg(" ");
			debug_msg(cursor_lon);
			debug_msg("\n");
			// >>>>>>>>>>>>>>>>>>>> SERIAL >>>>>>>>>>>>>>>>>>>> 
			LonLat32 p(cursor_lon,cursor_lat);
			if (request_state==RS_WAIT_FOR_START) 
			{
				debug_msg("Stored start");
				start = p;
				request_state = RS_WAIT_FOR_STOP;
			} 
			else { // request_state==RS_WAIT_FOR_STOP
				debug_msg("Stored end");
				end = p;
				request_state = RS_WAIT_FOR_START;
				int path_len = srv_get_pathlen(start,end);

				if (path_len > 0) 
				{
					LonLat32 waypoints[path_len];
					if (srv_get_waypoints(waypoints,path_len)>=0) {
						debug_msg("Received properly.\n");
						
						// draw path on screen
						draw_path(waypoints, path_len); 
					}
				} 
				else 
				{
					debug_msg("Invalid path_len.\n");
					delay(1000);
					continue; 
				}				
				// Serial.println("Done with communication");

			}
			// <<<<<<<<<<<<<<<<<<<< SERIAL <<<<<<<<<<<<<<<<<<<< 
		} // end of select_button_event processing

		// do we have to redraw the map tile?  
		if (update_display_window) {
	#ifdef DEBUG_SCROLLING
			Serial.println("Screen update");
			Serial.print(current_map_num);
			Serial.print(" ");
			Serial.print(cursor_lon);
			Serial.print(" ");
			Serial.print(cursor_lat);
			Serial.println();
	#endif

			draw_map_screen();
			draw_cursor();

			// Need to redraw any other things that are on the screen. Hint: Path

			// force a redisplay of status message
			clear_status_msg();
		}

		// always update the status message area if message changes
		// Indicate which point we are waiting for
		if (request_state == RS_WAIT_FOR_START) {
			status_msg("FROM?");
		}
		else {
			status_msg("TO?");
		}
	}
}

char* prev_status_msg = 0;

void clear_status_msg() {
	status_msg("");
}

void status_msg(char *msg) {
	// messages are strings, so we assume constant, and if they are the
	// same pointer then the contents are the same.  You can force by
	// setting prev_status_msg = 0

	if (prev_status_msg != msg) {
		prev_status_msg = msg;
		tft.fillRect(0, 148, 128, 12, GREEN);

		tft.setTextSize(1);
		tft.setTextColor(MAGENTA);
		tft.setCursor(0, 150);
		tft.setTextSize(1);

		tft.println(msg);
	}
}


void initialize_screen() {

	tft.initR(INITR_REDTAB);

	tft.setRotation(0);

	tft.setCursor(0, 0);
	tft.setTextColor(0x0000);
	tft.setTextSize(1);
	tft.fillScreen(BLUE);    
}

void initialize_sd_card() {
	if (!SD.begin(sd_cs)) {
#ifdef DEBUG_SERIAL
		Serial.println("Initialization has failed. Things to check:");
		Serial.println("* Is a card inserted?");
		Serial.println("* Is your wiring correct?");
		Serial.println("* Is the chipSelect pin the one for your shield or module?");

		Serial.println("SD card could not be initialized");
#endif

		while (1) {};    // Just wait, stuff exploded.
	}
	else {
#ifdef DEBUG_SERIAL

		Serial.println("Wiring is correct and a card is present.");

#endif
	}
}


// Center point of the joystick - analog reads from the Arduino.
int16_t joy_center_x = 512;
int16_t joy_center_y = 512;

void initialize_joystick() {
	// Initialize the button pin, turn on pullup resistor
	pinMode(joy_pin_button, INPUT);
	digitalWrite(joy_pin_button, HIGH);

	// Center Joystick
	joy_center_x = analogRead(joy_pin_x);
	joy_center_y = analogRead(joy_pin_y);
}


// button state: 0 not pressed, 1 pressed
uint8_t prev_button_state = 0;

// time of last sampling of button state
uint32_t button_prev_time = millis();

// only after this much time has passed is the state sampled.
uint32_t button_sample_delay = 200;

/*
Read the joystick position, and return the x, y displacement from the zero
position.  The joystick has to be at least 4 units away from zero before a
non-zero displacement is returned.  This filters out the centering errors that
occur when the joystick is released.

Also, return 1 if the joystick button has been pushed, held for a minimum
amount of time, and then released.  That is, a 1 is returned if a button
select action has occurred.  

*/
uint8_t process_joystick(int16_t *dx, int16_t *dy) {
	int16_t joy_x;
	int16_t joy_y;
	uint8_t button_state;

	joy_x = (analogRead(joy_pin_y) - joy_center_x);
	joy_y = (analogRead(joy_pin_x) - joy_center_y);

	if (abs(joy_x) <= 4) {
		joy_x = 0;
	}

	if (abs(joy_y) <= 4) {
		joy_y = 0;
	}

	// set cursor moving direction correspond to joystick moving direction 
	*dx = -joy_x / 128;
	*dy = -joy_y / 128;

	uint8_t button_press_event = 0; // no event by default
	// check for suitable time delay since the last time we read the joystick
	uint32_t cur_time = millis();
	// time inversion caused by wraparound?
	if (cur_time < button_prev_time) {
		// this is a hack.. but first this happens once in a million years
		// and the user won't notice either (but this could be made nicer; TODO)
		button_prev_time = cur_time;
	}
	if (cur_time > button_prev_time + button_sample_delay) {
		button_prev_time = cur_time;
		button_state = (LOW == digitalRead(joy_pin_button)); // true if button is pressed
		// if a press is followed by a release, we will have an event:
		button_press_event = (prev_button_state && !button_state);
		prev_button_state = button_state;
	}
	return button_press_event;
}


// Zooming in and out button handlers

extern volatile uint8_t shared_new_map_num;

/*
n mS debounce delay - ignore any further interrupts until this interval has
passed.    Although this works in isolations, you should not be hammering on an
interrupt line like this, so also make sure that there is debouncing on the
switches as per the course notes.
*/

const uint32_t bounce_delay = 500;

volatile uint32_t in_prev_intr_time = 0;
void handle_zoom_in() {
	uint32_t cur_intr_time = millis();
	if (cur_intr_time < in_prev_intr_time) {
		// time inversion caused by wraparound, so reset
		in_prev_intr_time = cur_intr_time;
	}
	if (in_prev_intr_time == 0 || 
	in_prev_intr_time + bounce_delay < cur_intr_time) {

		zoom_in();
		in_prev_intr_time = cur_intr_time;
	}
}

volatile uint32_t out_prev_intr_time = 0;
void handle_zoom_out() {
	uint32_t cur_intr_time = millis();
	if (cur_intr_time < out_prev_intr_time) {
		// time inversion caused by wraparound, so reset
		out_prev_intr_time = cur_intr_time;
	}
	if (out_prev_intr_time == 0 || 
	out_prev_intr_time + bounce_delay < cur_intr_time) {

		zoom_out();
		out_prev_intr_time = cur_intr_time;
	}
}

