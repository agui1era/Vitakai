#include  <WiFi.h>
#include  <HTTPClient.h>
#include  <M5Stack.h>
 
const char* ssid = "mi9";
const char* password =  "qwertyqwerty";

int retry;
int pin_data2;
int pin_data5;
int httpResponseCode;

void setup() {

  M5.begin();

  /*
    Power chip connected to gpio21, gpio22, I2C device
    Set battery charging voltage and current
    If used battery, please call this function in your project
  */
  M5.Power.begin();

  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setCursor(10, 10);
  M5.Lcd.setTextColor(WHITE);
  M5.Lcd.setTextSize(2);

  pinMode(2,INPUT);
  pinMode(5,INPUT);

  Serial.begin(115200);
  delay(4000);   //Delay needed before calling the WiFi.begin
 
  WiFi.begin(ssid, password); 
 
  while (WiFi.status() != WL_CONNECTED) 
  
  { 
    delay(1000);
    Serial.println("Connecting to WiFi..");
    M5.Lcd.printf("Connecting to WiFi.. \r \n");
  }
 
  Serial.println("Connected to the WiFi network");
  M5.Lcd.printf("Connected to the WiFi network \r \n");
 
}
 
void loop() {
 
 
 if(WiFi.status()== WL_CONNECTED)
  {   


   M5.Lcd.fillScreen(BLACK);
   M5.Lcd.setTextColor(WHITE);
   M5.Lcd.setCursor(0, 0);
   M5.Lcd.printf("Detectando.. \r \n");
   delay(50);
  
   pin_data2 = digitalRead(2);  
   pin_data5 = digitalRead(5);
   Serial.println(pin_data2); 
   Serial.println(pin_data5); 

   if (pin_data2 == 0)

   {
       HTTPClient http;   
       retry = 0;
       http.begin("http://66.85.77.12:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry ");  //Specify destination for HTTP request
       http.addHeader("Content-Type", "application/json");             //Specify content-type header    
        
 
      while (retry < 9) 

      {
          
       if (pin_data5 == 1)
           {
           
              httpResponseCode = http.POST("{\"Saco10K\": 1}");   //Send the actual POST request
              M5.Lcd.fillScreen(BLACK);
              M5.Lcd.setTextColor(WHITE);
              M5.Lcd.setCursor(0, 0);
              M5.Lcd.printf("Post Saco10K \r \n");
           }
              else
           {
              httpResponseCode = http.POST("{\"Saco25K\": 1}");   //Send the actual POST request
              M5.Lcd.fillScreen(BLACK);
              M5.Lcd.setTextColor(WHITE);
              M5.Lcd.setCursor(0, 0);
              M5.Lcd.printf("Post Saco25K \r \n");
           };
           
        if(httpResponseCode>0){
 
            String response = http.getString();  //Get the response to the request
            Serial.println(httpResponseCode);   //Print return code
            Serial.println(response);           //Print request answer
            retry=9;
            delay(8000);

       }
       
       else
       
       {
 
       M5.Lcd.setTextColor(RED);
       Serial.print("Retry... ");
       Serial.println(httpResponseCode);
       M5.Lcd.printf("Retry... \r \n");
       retry=retry+1;
       delay(100);
 
       }

     }
   
   http.end();  //Free resources
 
    }
  }
 
 else
 {
 
    Serial.println("Error in WiFi connection");  
    M5.Lcd.printf("Error in WiFi connection \r \n"); 
    delay(1000);  //Send a request every 10 seconds
 
 }
 
 
}
