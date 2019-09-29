#pragma once

#include <vector>

class Config
{
public:
	std::vector<double> obs;
	std::vector<double> Tx;
	std::vector<double> Ty;
	int l;
	int w;
	double total_area;
	double sigma;
	double eta;
	double rad1;
	double **prob;
	Config();
};

bool isValid(int, int);