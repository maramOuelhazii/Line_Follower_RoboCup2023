#include <QTRSensors.h>
#include <Servo.h>

QTRSensors qtr;                                              
// --> Nombre des capteurs <--                          
const uint8_t SensorCount = 8;                               
                                                             
//      --> tableau des valeurs des capteurs <--             
uint16_t sensorValues[SensorCount];                          



float Kp = 0.5;                                                
float Ki = 0;                                                
float Kd = 0;                                                
//      --> les variables relatives a l'erreur calculé <--   
int P;                                                       
int I;                                                       
int D;                                                       
                                                             
int lastError = 0;                                           




//       --> Maximum vitesse <--                             
const uint8_t maxspeeda = 250;                               
const uint8_t maxspeedb = 250;                               
//       --> vitesse de base : initiale <--                  
const uint8_t basespeeda = 80;                              
const uint8_t basespeedb = 80;                              




//       --> Déclaration des pins des moteurs <--            
int moteurDroitePhase = 5;                                   
int moteurDroitePWM = 4;                                    
int moteurGauchePhase = 6;                                   
int moteurGauchePWM = 7;   

int capteurLeft=26;
int capteurRight=28;
int trig=24;
int echo=22;

int servoRemorquePin=48;
Servo servoRemorque;
int servoRemorqueUp=60;
int servoRemorqueDown=155;



int servoBrasPin=48;
Servo servoBras;


int servoPincePin=46;
Servo servoPince;



int coeff[8]={-1000,-600,-400,-200,200,400,600,1000};

int sumLeft=0;
int sumRight=0;
int sens=0;
void setup() {
  Serial.begin(115200);

//    --> Configuration de type de QTR <--                                                   
  qtr.setTypeRC();                                                                           
//      --> Configuration des pins de QTR <--                                                
  qtr.setSensorPins((const uint8_t[]){30, 32, 34, 36, 38, 40, 42, 44}, SensorCount);         
//    --> LEDON PIN <--                                                                      
  qtr.setEmitterPin(A0); 
                                                                       




//       --> Configuration des pins des moteurs <--          
  pinMode(moteurDroitePhase, OUTPUT);                        
  pinMode(moteurDroitePWM, OUTPUT);                          
  pinMode(moteurGauchePhase, OUTPUT);                        
  pinMode(moteurGauchePWM, OUTPUT);
  pinMode(capteurRight, INPUT);                        
  pinMode(capteurLeft, INPUT); 

  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);

//  servoRemorque.attach(servoRemorquePin);
//  
//  servoRemorque.write(servoRemorqueDown);
//  delay(1000);
//  servoRemorque.write(servoRemorqueUp);
//  delay(500);
//  servoRemorque.detach();

  
//  servoBrasL.attach(servoBrasLPin);
//  servoBrasR.attach(servoBrasRPin);
//  servoBras.attach(servoBrasPin);
//  delay(2000);

//servoBras.write(165);
//delay(2000);
//servoBras.detach();
//servoPince.attach(servoPincePin);
//servoPince.write(140);
//delay(2000);
//servoPince.write(170);
//delay(2000);

//  servoBras.attach(servoBrasPin);

//servoBras.write(30);
//  delay(2000);
//  servoBras.detach();
//servoPince.write(140);
//delay(2000);
//servoPince.detach();
//  delay(100000);

 
  

  forward(0, 0);


//  --> Confuguration de LED d'indication de calibrage <-- 
  pinMode(LED_BUILTIN, OUTPUT);                            
                                                           
// --> Calibrage des capteurs <--                          
  //calibration();                                           



}

float distance(){
  long duration, distance;
  
  // Send a pulse to the trig pin
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  
  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
  
}

//    --> Fonction de Calibrage <--                          
void calibration() {                                         
  digitalWrite(LED_BUILTIN, HIGH);                           
  for (uint16_t i = 0; i < 400; i++)                         
  {                                                          
    qtr.calibrate();                                         
  }                                                          
  digitalWrite(LED_BUILTIN, LOW);                            
} 

int getQTR(){
  qtr.read(sensorValues);
  int sum=0;
  for (int i=0;i<8;i++){
    int black=0;
    if(sensorValues[i]>1700){
      black=1;
    }
    sum+=coeff[i]*black;
   }
   return sum;
}


void calculHalf(){
  qtr.read(sensorValues);
  sumLeft=0;
  for (int i=0;i<4;i++){
    int black=0;
    if(sensorValues[i]>1700){
      black=1;
    }
    sumLeft+=black;
    Serial.print(black);
   }

   
  sumRight=0;
   for (int i=4;i<8;i++){
    int black=0;
    if(sensorValues[i]>1700){
      black=1;
    }
    sumRight+=black;
     Serial.print(black);
   }

}





                                                                                    
void forward(int pwmD, int pwmG) {                                                  
//  if faut régler les valeur de phase des moteurs pour un forward parfaite         
  analogWrite(moteurDroitePhase, 0 );                                               
  analogWrite(moteurGauchePhase, 0 );                                               
  analogWrite(moteurDroitePWM, pwmD);                                               
  analogWrite(moteurGauchePWM, pwmG);                                               
} 
void stoop() {                                                  
//  if faut régler les valeur de phase des moteurs pour un forward parfaite         
  analogWrite(moteurDroitePhase, 0 );                                               
  analogWrite(moteurGauchePhase, 0 );                                               
  analogWrite(moteurDroitePWM, 0);                                               
  analogWrite(moteurGauchePWM, 0);                                               
}                                                                                   




                                                                                    
void backward(int       vitesse ) {                                                  
//  if faut régler les valeur de phase des moteurs pour un forward parfaite         
  analogWrite(moteurDroitePhase, vitesse );                                               
  analogWrite(moteurGauchePhase, vitesse );                                               
  analogWrite(moteurDroitePWM, 0);                                               
  analogWrite(moteurGauchePWM, 0);                                               
}                                                                                   


void right(int       vitesse ) {                                                  
//  if faut régler les valeur de phase des moteurs pour un forward parfaite         
  analogWrite(moteurDroitePhase, vitesse );                                               
  analogWrite(moteurGauchePhase, 0 );                                               
  analogWrite(moteurDroitePWM, 0);                                               
  analogWrite(moteurGauchePWM, vitesse+50);                                               
}

void left(int       vitesse ) {                                                  
//  if faut régler les valeur de phase des moteurs pour un forward parfaite         
  analogWrite(moteurDroitePhase, 0);                                               
  analogWrite(moteurGauchePhase, vitesse );                                               
  analogWrite(moteurDroitePWM, vitesse+50);                                               
  analogWrite(moteurGauchePWM, 0);                                               
}

//    --> Fonction Principale <--                                                            
void PID_control() {                                                                         
  int error = getQTR();;                                                               
  P = error;                                                                                 
  I = I + error;  //Accumulatoin d'erreur                                                    
  D = error - lastError; // Dérivée => différence                                            
//   Mise à jour de dernier erreur                                                           
  lastError = error;                                                                         
//   calcul de vitesse de sortie => application de PID                                       
  int motorspeed = P*Kp + I*Ki + D*Kd;                                                       
                                                                                             
//   Calcul des nouveau valeurs de pwm                                                       
  int motorSpeedDroite = basespeeda + motorspeed;                                            
  int motorSpeedGauche = basespeedb - motorspeed;                                            
                                                                                             
//   Saturation                                                                              
                                                                                             
  if (motorSpeedDroite > maxspeeda) {                                                        
    motorSpeedDroite = maxspeeda;                                                            
  }                                                                                          
  if (motorSpeedGauche > maxspeedb) {                                                        
    motorSpeedGauche = maxspeedb;                                                            
  }                                                                                          
  if (motorSpeedDroite < 0) {                                                                
    motorSpeedDroite = 0;                                                                    
  }                                                                                          
  if (motorSpeedGauche < 0) {                                                                
    motorSpeedGauche = 0;                                                                    
  }                                                                                          
                                                                                             
  Serial.print(motorSpeedDroite);Serial.print(" ");Serial.println(motorSpeedGauche);       
                                                                                             
//  Application de correction aux moteurs                                                    
  forward(motorSpeedDroite, motorSpeedGauche);                                               
}  

int sens0Compt=0;


//  ****************** LOOP ****************
void loop() {
//
//  qtr.read(sensorValues);
//  for (int i=0;i<8;i++){
//    Serial.print(sensorValues[i]);Serial.print("-");    
//   }
//   Serial.print(digitalRead(capteurLeft));
//    Serial.print(digitalRead(capteurRight));
//   Serial.println("\n");
//  

  
//  Serial.println(getQTR());
//  forward(70,70);
//  delay(2000);
//  backward(70);
//  delay(2000);
//  right(70);
//  delay(2000);
//  left(70);
//  delay(2000);
  
//  while(true){
//    Serial.println(distance());
//  }
  
//   Serial.print(digitalRead(capteurLeft));
//   Serial.print("-");
//   Serial.print(digitalRead(capteurRight));
//  Serial.println(getQTR());
  //PID_control();
  //backward(150);
  
  calculHalf();
// 
  int err=sumLeft-sumRight;
  Serial.println(sumLeft);
  if(!digitalRead(capteurLeft) && digitalRead(capteurRight)){
    sens=1;
    
  }
  else if(!digitalRead(capteurRight) && digitalRead(capteurLeft)){
    sens=-1;
    
  }
  else if(err==0 && digitalRead(capteurRight) && digitalRead(capteurLeft) && (sumLeft+sumRight)>0){
    sens0Compt++;
    if(sens0Compt>200){
      sens=0; 
      sens0Compt=0;
    
    }
    
 
    }
//  Serial.println(err);
//  if(!digitalRead(capteurLeft)){
//    left(120);
//  }
//  else 
//  if(!digitalRead(capteurRight)){
//    right(120);
//  }

//if(sens==1 ){
//  while(err!=0){
//    calculHalf();
//    err=sumLeft-sumRight;
//    left(80);
//  }
//}else 
//
//if(sens==-1){
//  while(err!=0){
//    calculHalf();
//    err=sumLeft-sumRight;
//    right(80);
//  }
//}

if(sumLeft+sumRight==0){
      if(sens==1){
      left(120);
    }else if (sens==-1){
      right(120);
    }else{
      forward(100,100);
    }
}
  else 
  if(err>0){
    left(120);
  }else if(err<0){
    right(120);
  }else{
//    if(sens==1){
//      left(90);
//    }else if (sens==-1){
//      right(90);
//    }else{
          forward(150,150);

//    }
  }

if (Serial.available() > 0) {
    String str = Serial.readStringUntil('\n');
    if(str="0100"){
      right(120);
  }
  else if(str="0001"){
      left(120);
  }
  
  }
}



}
