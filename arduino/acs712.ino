extern const int acs712_analogIn;

//const int mVperAmp = 185;	// 5A sensor
const int mVperAmp = 120;	// Empirical measurements

const int ACFreq = 50;	// 50 Hz
const int samplingTimeInMilliSecs = 2 * 1000 / ACFreq;

//int zeroOffset = 512 - 508;	// 508 was the mean value read with zero current
//int zeroOffset = 0;	// It seems that each execution the offset is different, so I will let it as 0 for now :-/
int zeroOffset = -1;

/**
 *
 */
void ACS712_readAveragedValuesDC( int &rawValue, long &vcc, double &milliVolts, double &amps )
{
  int num_samples = 1000;
  long accum = 0;
  for( int i=0 ; i < num_samples ; i++ ) {
    accum += analogRead(acs712_analogIn);
  }
  rawValue = accum / num_samples;
  vcc = readVcc();
  milliVolts = ((double)(rawValue + zeroOffset) / 1024.0) * vcc;	// mV
  amps = (milliVolts - (vcc/2.)) / mVperAmp;
}

int ACS712_readMilliAmpsDC()
{
  int rawValue = analogRead(acs712_analogIn);
  long vcc = readVcc();
  double milliVolts = ((double)(rawValue + zeroOffset) / 1024.0) * vcc;	// mV
  double amps = (milliVolts - (vcc/2.)) / mVperAmp;
  return amps * 1000.0;
}

int ACS712_readAveragedMilliAmpsDC(int num_samples = 1000)
{
  long accum = 0;
  for ( int i = 0 ; i < num_samples ; i++ ) {
    accum += ACS712_readMilliAmpsDC();
  }
  return accum / num_samples;
}

int ACS712_readMilliAmpsAC()
{
  int sample_min = 1023;
  int sample_max = 0;
  unsigned long start_time = millis();
  while ( ( millis() - start_time ) < samplingTimeInMilliSecs ) {
    int raw_value = analogRead(acs712_analogIn);
    if ( raw_value < sample_min )
      sample_min = raw_value;
    if ( raw_value > sample_max )
      sample_max = raw_value;
  }
  long vcc = readVcc();
  double vp = (( sample_max - sample_min ) * vcc ) / 2048;
  double mVrms = .707 * vp;
  return 1000. * mVrms / mVperAmp;
}

int ACS712_readAveragedMilliAmpsAC( int num_cycles = 50 /* 1 second */ )
{
  long accum = 0;
  for ( int i = 0 ; i < num_cycles ; i++ ) {
    accum += ACS712_readMilliAmpsAC();
  }
  return accum / num_cycles;
}
