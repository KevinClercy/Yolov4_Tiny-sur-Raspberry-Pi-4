'''Cette classe permet de stocker les traiter les informations de coordonnée envoyer vers le ARDUINO

Permet de trouver les centre lorsquon recoit des coordooné
Imprimer les informations utiles 

Maxence Le Vergos 
'''



class Coordonne {
    private:

    int Xmax,Xmin, Ymax,Ymin;


    public:
    double CentreX, CentreY;
    
    Coordonne(){
        Xmax = 0;
        Xmin = 0;
        Ymax = 0; 
        Ymin = 0; 
        CentreX = 1.0;
        CentreY = 1.0;
    }
    Coordonne(uint16_t inX,uint16_t inx,uint16_t inY,uint16_t iny){
        Xmax = inX;
        Xmin = inx;
        Ymax = inY; 
        Ymin = iny; 
    }

    void returnCentre(double & positionX, double & positionY) {
        positionX = CentreX;
        positionY = CentreY;
    }

    void setCoord (int inXmax,int inXmin,int inYmax,int inYmin){
    Xmax  = inXmax;
    Xmin  = inXmin;
    Ymax  = inYmax;
    Ymin  = inYmin;
    CentreCoordonne();

    }  

    void CentreCoordonne(){
    //Serial.println("CalculCentre");
    CentreX = (Xmax+Xmin)/2;
    CentreY = (Ymax+Ymin)/2;
    }

    void printCo(){
    Serial.println(Xmax);
    Serial.println(Xmin);
    Serial.println(Ymax);
    Serial.println(Ymin);
    Serial.println("CentreX");
    Serial.println(CentreX);
    Serial.println("CentreY");
    Serial.println(CentreY);

    
    }


};


#endif