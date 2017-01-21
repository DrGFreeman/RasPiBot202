#include <Servo.h>
#include <AStar32U4.h>
#include <PololuRPiSlave.h>
#include <FastGPIO.h>

/* Modified from example available for download at:
 *
 * https://github.com/pololu/pololu-rpi-slave-arduino-library
 */

// Custom data structure that we will use for interpreting the buffer.
// We recommend keeping this under 64 bytes total.  If you change the
// data format, make sure to update the corresponding code in
// a_star.py on the Raspberry Pi.

struct Data
{
  bool yellow, green, red;
  bool buttonA, buttonB, buttonC;

  int16_t leftMotor, rightMotor;
  uint16_t batteryMillivolts;
  uint16_t analog[6];

  bool resetEncoders;

  int16_t encoderLCount, encoderRCount;

  bool playNotes;
  char notes[14];
};

PololuRPiSlave<struct Data,5> slave;
PololuBuzzer buzzer;
AStar32U4Motors motors;
AStar32U4ButtonA buttonA;
AStar32U4ButtonB buttonB;
AStar32U4ButtonC buttonC;

// Encoders variables
const byte encoderLeftPinA = 8;    // PCINT4
const byte encoderLeftPinB = 16;   // PCINT2
const byte encoderRightPinA = 7;   // INT6
const byte encoderRightPinB = 0;   // INT2

static volatile bool lastLeftA;
static volatile bool lastLeftB;
static volatile bool lastRightA;
static volatile bool lastRightB;

volatile int16_t encoderLeftCount;
volatile int16_t encoderRightCount;

// ISRs
// ISR for left encoder pins A & B (PCINT4, 2)
ISR(PCINT0_vect)
{
  bool newLeftA = FastGPIO::Pin<encoderLeftPinA>::isInputHigh();
  bool newLeftB = FastGPIO::Pin<encoderLeftPinB>::isInputHigh();

  encoderLeftCount += (newLeftA ^ lastLeftB) - (lastLeftA ^ newLeftB);

  lastLeftA = newLeftA;
  lastLeftB = newLeftB;
}

// ISR for right encoder pins A & B (INT6 & INT2)
static void rightISR()
{
  bool newRightA = FastGPIO::Pin<encoderRightPinA>::isInputHigh();
  bool newRightB = FastGPIO::Pin<encoderRightPinB>::isInputHigh();

  encoderRightCount += (newRightA ^ lastRightB) - (lastRightA ^ newRightB);

  lastRightA = newRightA;
  lastRightB = newRightB;
}

void setup()
{  
  // Set up the slave at I2C address 20.
  slave.init(20);

  // Play startup sound.
  buzzer.play("v10>>g16>>>c16");

  // Setup encoders pins and attach ISRs
  FastGPIO::Pin<encoderLeftPinA>::setInputPulledUp();
  FastGPIO::Pin<encoderLeftPinB>::setInputPulledUp();
  FastGPIO::Pin<encoderRightPinA>::setInputPulledUp();
  FastGPIO::Pin<encoderRightPinB>::setInputPulledUp();
  PCMSK0 |= bit(PCINT4);
  PCMSK0 |= bit(PCINT2);
  PCIFR = (1 << PCIF0);
  PCICR = (1 << PCIE0);
  attachInterrupt(digitalPinToInterrupt(encoderRightPinA), rightISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderRightPinB), rightISR, CHANGE);

  // Initialize encoders variables
  lastLeftA = FastGPIO::Pin<encoderLeftPinA>::isInputHigh();
  lastLeftB = FastGPIO::Pin<encoderLeftPinB>::isInputHigh();
  encoderLeftCount = 0;
  lastRightA = FastGPIO::Pin<encoderRightPinA>::isInputHigh();
  lastRightB = FastGPIO::Pin<encoderRightPinB>::isInputHigh();
  encoderRightCount = 0;
}

void loop()
{
  // Call updateBuffer() before using the buffer, to get the latest
  // data including recent master writes.
  slave.updateBuffer();

  // Write various values into the data structure.
  slave.buffer.buttonA = buttonA.isPressed();
  slave.buffer.buttonB = buttonB.isPressed();
  slave.buffer.buttonC = buttonC.isPressed();

  // Change this to readBatteryMillivoltsLV() for the LV model.
  slave.buffer.batteryMillivolts = readBatteryMillivoltsSV();

  for(uint8_t i=0; i<6; i++)
  {
    slave.buffer.analog[i] = analogRead(i);
  }
  
  // Write encoder counts
  cli();
  slave.buffer.encoderLCount = encoderLeftCount;
  slave.buffer.encoderRCount = encoderRightCount;
  sei();

  // Reset encoder counts
  if (slave.buffer.resetEncoders)
  {
    slave.buffer.resetEncoders = 0;
    cli();
    encoderLeftCount = 0;
    encoderRightCount = 0;
    sei();
  }

  // READING the buffer is allowed before or after finishWrites().
  ledYellow(slave.buffer.yellow);
  ledGreen(slave.buffer.green);
  ledRed(slave.buffer.red);
  motors.setSpeeds(slave.buffer.leftMotor, slave.buffer.rightMotor);

  // Playing music involves both reading and writing, since we only
  // want to do it once.
  if(slave.buffer.playNotes)
  {
    buzzer.play(slave.buffer.notes);
    while(buzzer.isPlaying());
    slave.buffer.playNotes = false;
  }

  // When you are done WRITING, call finalizeWrites() to make modified
  // data available to I2C master.
  slave.finalizeWrites();
}
