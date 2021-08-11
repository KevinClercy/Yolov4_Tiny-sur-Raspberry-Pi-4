#ifndef __CORDO__
#define __CORDO__
#include "coordonne.h"
#include <Servo.h>
#include <AccelStepper.h>

//CLASS PRINCIPALE QUI COORDONE LES ACTIONS DES MOTEURS QU<ON LUI PR/SENTE.

class cordo
{
private:
  long ouAllerX;
  long AngleServo = 50;
  // long LIMITtopRAIL= 0;     //limit sup du rail
  // long LIMITbotRAIL = -6500; //limit inferieur du rail

  //Pointeur vers des class qui aide au controle des moteurs
  AccelStepper *ptrStepper = nullptr;
  Coordonne *ptrCoordo = nullptr;
  Servo *ptrServo = nullptr;

public:
  //CONSTRUCTEUR
  cordo()
  {
    ouAllerX = 0;
    // LIMITbotRAIL = -6500;
    // LIMITtopRAIL= 0;
    AngleServo = 0;
  }
  //constructeur d"un coordo avec 1 stepper 1 servo et 1 set de coordonne
  cordo(AccelStepper *inPtr, Coordonne *inPtrCoordonne, Servo *inPtrServo)
  {
    ptrStepper = inPtr;
    ptrCoordo = inPtrCoordonne;
    ptrServo = inPtrServo;
  } //pointeur vers le stepper qu<il doit controler

  void PF(const char *inText)
  {
    Serial.println(inText);
    Serial.print(ouAllerX);
    Serial.print("<-ouAllerX_______Current ->");
    Serial.print(ptrStepper->currentPosition());
  }

  bool isONtarget()
  {
    if (ptrStepper->currentPosition() == ouAllerX)
    {
      return true;
    }
    else
    {
      return false;
    }
  };

  void HomingStepper()
  {
    Serial.println("Homing Ref");
    int stop = 0;
    ptrStepper->moveTo(10000);
    ptrStepper->setSpeed(10000);
    ptrStepper->setAcceleration(10000);
    Serial.print("......");
    while (!stop)
    { // va jusq'au stopper du homing
      stop = digitalRead(LimitPin);
      ptrStepper->run();
    }
    ptrStepper->setCurrentPosition(0);
    ptrStepper->runToNewPosition(-100);
    Serial.print(".....COMPLETE");
  }

  void setAngleServo(int inAngle) { ptrServo->write(inAngle); };

  void initStepperSpeedAndAcceleration(int inSpeed, int inAcceleration)
  {
    ptrStepper->setAcceleration(inAcceleration);
    ptrStepper->setSpeed(inSpeed);
  }

  void initServo()
  {
    Serial.print("initServo");
    ptrServo->attach(PINservo);
    ptrServo->write(90);
    Serial.print("testServoinit");
    Serial.print(ptrServo->read());
    //ptrServo->write(135);
    delay(1000);
  }

  long getOuAllerX() { return ouAllerX; }
  long GetPositionStepper() { return ptrStepper->currentPosition(); }

  void SetDeplacement(long inOuAller) { ouAllerX = inOuAller; }
  //FONCTION POUR DEPLACER LE STEPPER

  void SeDeplacerAlaPosition(long inPosition)
  {
    ptrStepper->runToNewPosition(-inPosition);
  }
  // se deplace au pourcentage demandé. meme si le rail change de dimension
  void SeDeplacerPourcentage(long inPourcentage)
  {

    Serial.print(ouAllerX = inPourcentage * (LIMITbotRAIL / 100));
    ouAllerX = inPourcentage * (LIMITbotRAIL / 100);
  }
  //Donne le nouvelle objectif
  void Deplacement()
  {
    PF("Deplacement");
    // Serial.print("IS ON TARGET ^^ : ");
    // Serial.print(isONtarget());
    while (!isONtarget())
    {
      ptrStepper->run();
    }
    ptrServo->write(AngleServo);
  }

  //FONCTION POUR ACTUALISER LES OBJECTIFS DU STEPPER
  void deplacementAgauche()
  {
    ptrStepper->moveTo(-10000);
    ptrStepper->setSpeed(-1000);
  }
  void deplacementADroite()
  {
    ptrStepper->moveTo(10000);
    ptrStepper->setSpeed(1000);
  }
  void ActualiserPosition()
  {
    CalculDeplacementX();
    CalculServo();
  }

  void Print() { Serial.println(ptrStepper->currentPosition()); }

  //Calcul le deplacement pour mettre le centre du carre au centre de l<image (400, 300)
  void CalculDeplacementX()
  {
    Serial.println("Calcul DeplacementX >>> ProchaineCible");
    Serial.print(ptrStepper->currentPosition());
    Serial.print("<-----Position____CentreX----->");
    Serial.println(ptrCoordo->CentreX);
    long deplacement = (((DIMENSION_X / 2) - ptrCoordo->CentreX) * FacteurConversion);
    
    if (abs(deplacement) > 300){
    Serial.println("ValeurDuDeplacement:");
    Serial.println(deplacement);
    ouAllerX = ptrStepper->currentPosition() - deplacement;
    Serial.print(ouAllerX);
    //Limite le déplacement de la camera dans les limites physique du rail
    if (ouAllerX < LIMITbotRAIL)
    {
      ouAllerX = LIMITbotRAIL;
    }
    if (ouAllerX > LIMITtopRAIL)
    {
      ouAllerX = LIMITtopRAIL;
    }

    //permet de calmer le mouvement de la camera

    ptrStepper->moveTo(ouAllerX);
    Serial.print(ouAllerX);
    }else {
      Serial.print("trop petit deplacement");
    }
  }

  //PETIT FONCTION POUR LIRE LE INPUT DUN JOYSTICK LORSQUON A LE MODE MANUEL ALLUME

  int ReadJoystick()
  {
    inX = analogRead(x_pin);
    inY = analogRead(y_pin);
    // inY = map(inY, 0, 1023, 140, 45);     // scale it to use it with the servo (value between 0 and 180)
  }

  void CalculServo()
  {
    // Mapping du ServoMoteur pour limiter l'angle
    //  0      = angle0%
    //  200    = 50 %
    //  400    = angle 100%
    AngleServo = map(ptrCoordo->CentreY, 0, DIMENSION_Y, SERVO_ANGL_INF, SERVO_ANGL_SUP);
  }
  //PETIT FONCTION POUR CONTROLER LE ROBOT AVEC UN JOYSTICK
  void DeplacementJoystick()
  {
    ReadJoystick();
    if (inY > 1000)
    {
      ptrServo->write(ptrServo->read() + 10);
    }
    if (inY < 100)
    {
      ptrServo->write(ptrServo->read() - 10);
    }
    if (inX > 700 and ptrStepper->currentPosition() > LIMITbotRAIL)
    {
      while (inX > 1000)
      {
        deplacementAgauche();
        ptrStepper->run();
        ReadJoystick();
      }
    }
    if (inX < 200 and ptrStepper->currentPosition() < LIMITtopRAIL)
    {
      while (inX < 200)
      {
        deplacementADroite();
        ptrStepper->run();
        ReadJoystick();
      }
    }
  }

};

#endif