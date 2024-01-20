#include <ESP8266WiFi.h>
String command;
String bot;
const char* ssid = "robotics_2";       // Replace with your local Wi-Fi network name
const char* password = "CLB422BFB0"; // Replace with your local Wi-Fi password
const char* server_ip = "192.168.1.77";   // Replace with your laptop's IP address
const int server_port = 12345;        // Choose a port number
String receivedMessage;
WiFiClient client;
const int t=0;
#define IN_1  14          // L298N in1 motors Right           
#define IN_2  12          // L298N in2 motors Right          
#define IN_3  13           // L298N in3 motors Left          
#define IN_4  15           // L298N in4 motors Left 
#define ena1 5
#define ena2 4 
void setup() 
{
  Serial.begin(115200);
 pinMode(IN_1, OUTPUT);
 pinMode(IN_2, OUTPUT);
 pinMode(IN_3, OUTPUT);
 pinMode(IN_4, OUTPUT); 
 digitalWrite(IN_1, LOW);
 digitalWrite(IN_2, LOW);
 digitalWrite(IN_3, LOW);
 digitalWrite(IN_4, LOW);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  // Connect to the server
  Serial.println("Connecting to server...");
  while (!client.connect(server_ip, server_port)) {
    Serial.println("Connection failed. Retrying...");
    delay(1000);
  }
  Serial.println("Connected to server");
}


void loop() {

  client.print("Hello Server!");
  // // Wait for a response from the server

 while (client.available() > 0) {
    receivedMessage += (char)client.read();
    Serial.print("recieved");
    Serial.println(receivedMessage);
  }
  bot =receivedMessage.substring(0, receivedMessage.indexOf("a"));
  command = receivedMessage.substring(2,receivedMessage.indexOf("b"));
  int t = receivedMessage.substring(receivedMessage.indexOf("b") + 1).toInt();
Serial.print(bot);
Serial.print(command);
Serial.print(t);
  receivedMessage="";
  delay(500);
  if(bot=="1") 
  {
    if (command == "F" || command == "f") 
    {

goAhead(); 
Serial.println("Moving Forward");
  delay(t);
    } 
    else if (command == "B" || command == "b")
    {

goBack();
Serial.println("Moving Backward");
  delay(t);
    }
    else if (command == "L" || command == "l")
    {

goLeft();
Serial.println("Moving Left");
  delay(t);
    }
    else if (command == "R" || command == "r")
    {

goRight();
Serial.println("Moving Right");
  delay(t);
    }
    else if (command == "S" || command == "s"){
stopRobot();
Serial.println("STOP!");
    }
  }
  else
  stopRobot();
}
void goLeft(){ 
  analogWrite(ena1,120);
 analogWrite(ena2,120);
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
         
  }

void goRight()
{ 
   analogWrite(ena1,120);
 analogWrite(ena2,120);
      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
          
 }

void goBack()
{ 
 analogWrite(ena1,100);
 analogWrite(ena2,100);
     digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      
  }

void goAhead()
{
   analogWrite(ena1,100);
 analogWrite(ena2,100);
      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);   
  }
void stopRobot()
{  
      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, HIGH);
      digitalWrite(IN_3, HIGH );
      digitalWrite(IN_4,HIGH);
}
