#pragma once

#define _USE_MATH_DEFINES
#include <cmath>

#include "conf.h"
#include <iostream>
#include <map>
#include <math.h>

extern std::map<char, int> ans_var;

extern double **kudaTransferKernelMatrix;
extern Config *config;

extern void printConfig();
extern void estimate();
extern double expected_cost(int, int);
extern double likelihood(int, int);
extern double gaussian_func(double, double, double);