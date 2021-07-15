#include <Servo.h>
String entradaSerial = "";
bool entradaCompleta = false;
//PARA EL SERVO
Servo servo1;
int pulsoMin=600;
int pulsoMax=2600;
//mic QUE ACTIVARA EL SERVO DE ASPERSORES
int MIC = 5;
int VALOR ;


void setup()
{
  //PIN 3 t 4 se usan para activar los rele
  
  
   pinMode(3,OUTPUT);
   pinMode(4,OUTPUT);
   pinMode(MIC,INPUT);
   Serial.begin(9600);
   servo1.attach(2,pulsoMin,pulsoMax);
}

void loop()
{ 

  VALOR = digitalRead(MIC);
  if(VALOR == HIGH){
       servo1.write(0);
       delay(500);
       servo1.write(180);
        delay(500);
  }
 
  if(entradaCompleta){
    if(entradaSerial == "a\n"){
      digitalWrite(4,LOW);
      digitalWrite(3, HIGH);
      delay(400);
      
     
    }else if(entradaSerial == "b\n"){
      digitalWrite(3,LOW);
      digitalWrite(4, HIGH);
      delay(400);
      
      
    }else{Serial.println("El dato recibido es inválido!!");
    
    }
     entradaSerial = "";
    entradaCompleta = false;
  }
}

void serialEvent(){
  while (Serial.available()){

    char inChar = (char)Serial.read();
    entradaSerial += inChar;
     
    if(inChar == '\n'){
      entradaCompleta = true;
    }
  }
 }
