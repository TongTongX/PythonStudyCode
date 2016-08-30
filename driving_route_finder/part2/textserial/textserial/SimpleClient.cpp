#include <Arduino.h>

/*
Test read and write to arduino through minicom.
The program, running on the Arduino, reads data on the serial 0 port
and echos it back on the same port. The program also demonstrates
how to detect new lines.

You can test this program with serial-mon, serial-test.py

Use <CTRL>-A Q to quit.

*/

bool waiting_for_eol = false;
String buffer;

void setup() {
   Serial.begin(9600); // 115200 can be used with Python, but not with serial-mon
   Serial.print("PHASE01\r\n\r\n\r\n\r\n\r\n\r\n");
   Serial.print("The program waits for input on the serial port.\r\n"
      "When a full line is received, it is sent back on the serial port\r\n"
      "to the sender, with three dots (...) appended.\r\n"
      "When running this code in the serial-monitor, use Ctrl+A and Q to exit\r\n"
      "if you had enough fun.\r\n"
      "The code can also be used to test serial_test.py\r\n"
   );
   buffer = "PHASE02";
}

void loop() {
   if (!waiting_for_eol) {
      // print what's in the buffer:
      Serial.print(buffer);
      buffer = "";
      Serial.println("...");
      waiting_for_eol = true;
   }
   else if (Serial.available()) {
      // read the incoming byte:
      int in_char = Serial.read();
      // if end of line is received, waiting for line is done:
      if (in_char == '\n' || in_char == '\r') {
         waiting_for_eol = false;
         // this would be a good time to process the buffer
      }
      else {
         buffer += char(in_char);
      }
   }
}


