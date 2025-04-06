/**
 *
 */

const int baudrate = 9600;
const int acs712_analogIn = A0;
const int pHSensor_analogIn = A1;


void setup() {
  Serial.begin(baudrate);
}


void debug_read_DC_values()
{
  int milli_amps_dc = ACS712_readAveragedMilliAmpsDC();

  Serial.print("Watts: ");
  Serial.print( milli_amps_dc * readVcc() / 1e6 );
  Serial.print(" milliAmps DC : ");
  Serial.println( milli_amps_dc );

  /* -- measure DC current -- */

  int rawValue;
  long Vcc;
  double mV;
  double A;
  ACS712_readAveragedValuesDC( rawValue, Vcc, mV, A );

  Serial.print("rawValue : ");
  Serial.print( rawValue );
  Serial.print(" Vcc : ");
  Serial.print( Vcc );
  Serial.print(" mV : ");
  Serial.print( mV );
  Serial.print(" A : ");
  Serial.println( A );
}


void loop() 
{
/*
  long vcc = readVcc();
  Serial.print("Vcc : ");
  Serial.print( (float)vcc / 1000.0 );
  Serial.print(" ");
*/
/*
  int milli_amps_ac = ACS712_readAveragedMilliAmpsAC();
  Serial.print("Watts: ");
  Serial.print( milli_amps_ac * .230 );
  Serial.print(" milliAmps AC : ");
  Serial.println( milli_amps_ac );
*/

  float pH_value = pHSensor_readAveragedPHValue();
  Serial.print("pH ");
  Serial.println( pH_value );
}
