#include "main.h"


double gaussian_func(double, double, double);

double gaussian_func(double x, double mu, double sigma)
{
		double comp_a_factor = sqrt(2 * M_PI);
		double a = 1.0 / (comp_a_factor * config->sigma);
		double b = -pow(x - mu, 2.0);
		double c = 2 * pow(config->sigma, 2.0);
		double d = exp(b / c);
		double e = a * d;
		return e;
}