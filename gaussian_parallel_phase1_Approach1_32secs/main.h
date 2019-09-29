#pragma once

#define _USE_MATH_DEFINES
#include <cmath>

#include "conf.h"
#include <iostream>
#include <map>
#include <math.h>

extern std::map<char, int> ans_var;

extern Config *config;

extern std::vector<int> likelihood_indices;

extern int kudaTransferKernelMatrix_iter;
extern double **kudaTransferKernelMatrix;
extern double *kudaOutMatrix;
extern double *likelihoodmatrix;
extern double *expectmatrix;

extern size_t kernelnumRows;
extern size_t kernelnumCols;

extern void printConfig();
extern void populate_estimate();
extern void populate_expected_cost(int, int);
extern void populate_likelihood(int, int);
extern double gaussian_func(double, double, double);

extern void kernelDriver();
extern void calculate_likelihood();
extern double calculate_expected_cost(int, int);
extern void calculate_estimate();
extern void init_likelihood_indices();