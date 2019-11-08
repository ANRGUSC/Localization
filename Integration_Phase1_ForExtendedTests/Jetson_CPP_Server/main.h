#pragma once

#define _USE_MATH_DEFINES
#include <cmath>

#include "conf.h"
#include <iostream>
#include <map>
#include <math.h>
#include <string>

extern std::map<char, int> ans_var;

extern Config *config;

extern double *likelihoodmatrix;

extern void printConfig();
extern void printLikelihoodToFile();
extern void printAns();

extern void kernelDriver(int);
extern double calculate_expected_cost(int, int);
extern void calculate_estimate();
extern void init_likelihood_indices();

extern std::string invokeGPUEngine(char*, int);
