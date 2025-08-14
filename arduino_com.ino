void setup() {
  Serial.begin(115200);
}
void loop() {
  if (Serial.available() > 0) {
    String str = Serial.readStringUntil('\n');
    int index = 0;
    
int substrings[3]; 
int id=0;
while (str.length() > 0) {
  int index = str.indexOf('-');
  
  if (index == -1) {
    substrings[id] = str.toInt();
    break;
  }
  substrings[id] = str.substring(0, index).toInt();
  str = str.substring(index+1);
  id++;
}




  
  }
}
