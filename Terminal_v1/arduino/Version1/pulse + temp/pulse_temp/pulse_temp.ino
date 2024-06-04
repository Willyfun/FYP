#define sensor_pin A0
#define pulse_pin A1
#define USE_ARDUINO_INTERRUPTS true
#include <PulseSensorPlayground.h> 

int Threshold = 550;      
const int LED = LED_BUILTIN;  
int myBPM = 0;
int bpm = 0;
int temp = 0;
                               
PulseSensorPlayground pulseSensor;  


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  pulseSensor.analogInput(pulse_pin);   
  pulseSensor.blinkOnPulse(LED);       
  pulseSensor.setThreshold(Threshold);   

  if (pulseSensor.begin()) {
    Serial.println("We created a pulseSensor Object !");
  }
}

void loop() {

  bpm = read_pulse_sensor_value();
  temp = read_temp_sensor_value();

  Serial.print("BPM = ");
  Serial.println(bpm);
  Serial.print("Temperature =");
  Serial.print(temp);
  Serial.println("*C");

  delay(3000);
 
}

int read_pulse_sensor_value(){
  if (pulseSensor.sawStartOfBeat()) {            
    myBPM = pulseSensor.getBeatsPerMinute();  
  }

  delay(20);  
  return myBPM;
                      

}


int read_temp_sensor_value(){
  // put your main code here, to run repeatedly:
 //Read Raw ADC Data
  int adcData = analogRead(sensor_pin);
  // Convert that ADC Data into voltage
  float voltage = adcData * (5.0 / 1024.0);
  // Convert the voltage into temperature 
  float temperature = voltage * 100;
  
  delay(20);
  return temperature;
}
