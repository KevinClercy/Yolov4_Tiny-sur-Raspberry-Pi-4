#include "AccelStepper.h"
#include "OneButton.h"
#include "Servo.h"
#include <Wire.h>
#include "VALEUR.h"
#include "coordonne.h"
#include "cordo.h"

AccelStepper MyStepper(2,2,3);
AccelStepper* ptrStepper = &MyStepper;
Coordonne MyCoord(0,0,0,0);
Coordonne* ptrMyCoord = &MyCoord;
Servo mServo;
Servo* ptrMyServo = &mServo;
cordo CordoChef(ptrStepper, ptrMyCoord, ptrMyServo); 

//flag pour indiquer lorsque le PI veux simplement indiquer une position sur le rail 

//Fonction de mise en place
void setup()
{  
    
    pinMode(LightPin,OUTPUT);
    pinMode(LimitPin,INPUT_PULLUP);
    pinMode(Sbutton,INPUT);
    pinMode(LumiereReception,OUTPUT);
    
    Serial.begin(9600);
    MyStepper.setMaxSpeed(1000);
    MyStepper.setAcceleration(1000); //ACCELERATION = Steps /(second)^2
    pinMode(10,OUTPUT);
    //Setup du bus I2c
    Wire.begin(ADR_NOEUD);
    
    Wire.onReceive(receiveEvent);
    MyStepper.setCurrentPosition(0);
    CordoChef.HomingStepper();
    CordoChef.initServo();
    // Homing3();
    // initServo2();
    allumeLumiere();

      // telephone number to send sms
   //readSerial(remoteNum);
      
}

void loop()
{   
    
    while(digitalRead(Sbutton)){ 
      if(ModeManuel){
        allumeLumiere();
        CordoChef.DeplacementJoystick();
      }
    // 
    // Serial.print(digitalRead(LimitPin));
    if (FlagDetection){
        CordoChef.ActualiserPosition();
        CordoChef.Deplacement();
        if(CordoChef.isONtarget()){
          FlagDetection = false;
        }
    }
    }
    

}



void receiveEvent(int TailleList){

    
    Serial.print("\n Taille : ");
    Serial.println(TailleList);
    //LECTURE DU TABLEAU DE 8BIT QUI ARRIVE DU RPI
    if (TailleList == 9 ){
    COMMANDE = Wire.read();
    valeur1MSB = Wire.read();
    valeur1LSB = Wire.read();
    valeur2MSB = Wire.read();
    valeur2LSB = Wire.read();
    valeur3MSB = Wire.read();
    valeur3LSB = Wire.read();
    valeur4MSB = Wire.read();
    valeur4LSB = Wire.read();
    }

    
    Serial.println(COMMANDE);
    switch (COMMANDE){
    //Cas de fonctionnement normal

    
    case 0xA7:
    //Je transforme les  MSB et LSB avant de les envoyer dans la classe COORDO
      Xc = valeur1MSB*256+valeur1LSB;
      xc = valeur2MSB*256+valeur2LSB;
      Yc = valeur3MSB*256+valeur3LSB;
      yc = valeur4MSB*256+valeur4LSB;
      MyCoord.setCoord(Xc,xc,Yc,yc);
      MyCoord.printCo();
      Serial.print("Flag");
      FlagDetection = 1;
      break;
    
      case 0xA8: //fonction pas fini pour depalcer sur le rail 
      DeplacementManuel = 1;
      Serial.println("MovePosition"); 
      inPourcentageSurLeRail = valeur1LSB;
      
      break;
    
    case 0xA0:
      Serial.println("ModeManuel OFF");
      ModeManuel = false;
      
      CordoChef.setAngleServo(90);
      break;

    case 0xA1:
      Serial.println("ModeManuel ON");
      ModeManuel = true;
      break;

    default:
      break;
  }


}

// FONCTION UTILITAIRE : Permet de controller les lumiere de la LightPin. dans notre cas, nous l<utilisons pour prevenir quand le systeme est en mode manuel 
void allumeLumiere(){
  digitalWrite(LightPin,HIGH);
  delay(delaiFlash);
  digitalWrite(LightPin,LOW);
  delay(delaiFlash);
  digitalWrite(LightPin,HIGH);
  delay(delaiFlash);
  digitalWrite(LightPin,LOW);
  digitalWrite(LumiereReception,HIGH);
  delay(delaiFlash);
  digitalWrite(LumiereReception,LOW);
  delay(delaiFlash);
  digitalWrite(LumiereReception,HIGH);
  delay(delaiFlash);
    

}


