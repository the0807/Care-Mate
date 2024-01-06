int relay1 = 8;
int relay2 = 9;
 
void setup()
{
  Serial.begin(9600);
  pinMode(relay1,OUTPUT);
  pinMode(relay2,OUTPUT);
}
 
void loop()
{
  digitalWrite(relay1,HIGH);
  digitalWrite(relay2,HIGH);
  
  if(Serial.available())
  { 
    char value = Serial.read();
    Serial.println(value);
    if(value == '1')
    {
      digitalWrite(relay1,LOW);
      delay(10000);
      digitalWrite(relay1,HIGH);
    }
    else if(value == '2')
    {
      digitalWrite(relay2,LOW);
      delay(10000);
      digitalWrite(relay2,HIGH);
    }
  }
}