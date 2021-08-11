//DONNEE DE BRANCHEMENT DU ARDUINO

int inX = 0;
int inY = 0;
int LimitPin = 4;
int Sbutton = 7;
int delaiFlash = 100;
int LightPin = 6;
int LumiereReception = 5;


int PositionStepper = 0;

// dimension ECRAN
long DIMENSION_X = 800 ;
long DIMENSION_Y = 600;

//Dimension RAIL stepper
long LIMITtopRAIL = 0;
long LIMITbotRAIL = -6500;


long initial_homing=-2;
int inPosition = -10;
char remoteNum[20];

//PIN de branchement du JOYSTICK. 
const int x_pin = A3;
const int y_pin = A2;


const uint8_t ADR_NOEUD = 0x44; 
const uint8_t CMDXmax = 0xA1;
const uint8_t CMDXmin = 0xA2;
const uint8_t CMDYmax = 0xA3;
const uint8_t CMDYmin = 0xA4;

// PARAMETRE PHYSIQUE DU RAIL
const int CENTRErail = -3200;
float FacteurConversion = -(6400/DIMENSION_X);

const int PINservo = 12;

bool newData, runallowed = false;
long receivedSteps = 200;

uint16_t valeur1MSB = 0;
uint16_t valeur1LSB = 0;
uint16_t valeur2MSB = 0;
uint16_t valeur2LSB = 0;
uint16_t valeur3MSB = 0;
uint16_t valeur3LSB = 0;
uint16_t valeur4MSB = 0;
uint16_t valeur4LSB = 0;

uint16_t newPositionMSB90 = 0;
uint16_t newPositionLSB90 = 0;
uint16_t COMMANDE =0;

bool ModeManuel = false; 
long Xc = 0;
long xc = 0;
long Yc = 0;
long yc = 0;
volatile long newInPosition = 0;
volatile bool FlagDetection = 0; // bool de suivi si je reviens au main
volatile int inPourcentageSurLeRail = 0;
bool DeplacementManuel = 0; 
const int SERVO_ANGL_INF = 50;
const int SERVO_ANGL_SUP = 120;


