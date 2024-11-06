#ifndef SINUSOIDAL_GENERATOR_H
#define SINUSOIDAL_GENERATOR_H

#include <cmath>
#include <chrono>

class SinusoidalGenerator {
public:
    SinusoidalGenerator(double amplitude, double frequency);
    double generateValue(double interval_ms);
    
private:
    double amplitude;
    double frequency;
    double time;
};

#endif // SINUSOIDAL_GENERATOR_H

