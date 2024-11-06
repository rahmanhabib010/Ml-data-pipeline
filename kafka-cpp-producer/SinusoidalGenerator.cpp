#include "SinusoidalGenerator.h"

SinusoidalGenerator::SinusoidalGenerator(double amplitude, double frequency)
    : amplitude(amplitude), frequency(frequency), time(0.0) {}

double SinusoidalGenerator::generateValue(double interval_ms) {
    // Update time based on the interval in seconds
    time += interval_ms / 1000.0;  // Convert milliseconds to seconds
    return amplitude * sin(2 * M_PI * frequency * time);
}

