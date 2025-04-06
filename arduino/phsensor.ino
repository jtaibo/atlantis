extern const int pHSensor_analogIn;

#define NUM_PH_SAMPLES 5000

/**
 * Calibration values
 *
 *   The sensor is linear, so we estimate the formula y = m x + b, where y
 *   is the pH and x is the volts reading
 *
 */
// Awaiting the delivery of the calibration solutions in powders
float m = -4.9138;	// Computed from calibration solution powder (pH 4.01, pH 6.86)
float b = 18.702;	// Computed from calibration solution powder (pH 4.01, pH 6.86)
//float m = -5.7;
//float b = 21.34;


float pHSensor_readAveragedPHValue()
{ 
  int pH_values[NUM_PH_SAMPLES];

#if REMOVE_MIN_AND_MAX
  int min = 1023;
  int max = 0;

  for( int i = 0 ; i < NUM_PH_SAMPLES ; i++ ) {
    int val = analogRead( pHSensor_analogIn );
    if ( val < min )
      min = val;
    if ( val > max )
      max = val;
    pH_values[i] = val;
    delay(10);
  }
  int samples = 0;
  long accum = 0;
  bool min_removed = false;
  bool max_removed = false;
  for( int i = 0 ; i < NUM_PH_SAMPLES ; i++ ) {
    if ( !min_removed && pH_values[i] == min ) {
      min_removed = true;
      continue;
    }
    if ( !max_removed && pH_values[i] == max ) {
      max_removed = true;
      continue;
    }
    accum += pH_values[i];
    samples++;
  }
  int averaged_value = accum / samples;
#else
  float accum = 0;
  for( int i = 0 ; i < NUM_PH_SAMPLES ; i++ ) {
    accum += analogRead( pHSensor_analogIn );
  }
  float averaged_value = accum / NUM_PH_SAMPLES;
#endif

//return averaged_value;

  float vcc = (float)readVcc() / 1000.0;
  float volts = (float)averaged_value * vcc / 1023.0;

  float pH = volts * m + b;

  return pH;
}
