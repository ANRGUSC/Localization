#pragma once

#include <vector>
#include <string>

using namespace std;
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
	Config(std::string inputStr);
};

bool isValid(int, int);

#define NUMTHR_STD_CONF		1400
