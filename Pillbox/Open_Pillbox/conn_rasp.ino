void setup()
{
  Serial.begin(9600);
}
void loop()
{
  if(Serial.available())
  {
    char value = Serial.read();
    Serial.print(value);
  }
}