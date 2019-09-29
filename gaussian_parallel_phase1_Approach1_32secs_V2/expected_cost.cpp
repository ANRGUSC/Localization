#include "main.h"

void populate_expected_cost(int i, int j);
double calculate_expected_cost(int, int);
void init_likelihood_indices();
static int cost_MLE(int i, int j, int p, int q);
static double get_likelihood(int i, int j, int p, int q);

static int ifactor, jfactor, pfactor;

void init_likelihood_indices()
{
	ifactor = config->w * config->l * config->w;
	jfactor = config->l * config->w;
	pfactor = config->w;
}

void populate_expected_cost(int i, int j)
{
	double expect = 0.0;

	for (int p = 0; p < config->l; p++)
	{
		for (int q = 0; q < config->w; q++)
		{
			populate_likelihood(p, q);
		}
	}
}


double calculate_expected_cost(int i, int j)
{
	double expect = 0.0;

	for (int p = 0; p < config->l; p++)
	{
		for (int q = 0; q < config->w; q++)
		{
			expect += (config->prob[i][j] * get_likelihood(i, j, p, q))
				* cost_MLE(i, j, p, q);
		}
	}

	return expect;
}


double get_likelihood(int i, int j, int p, int q)
{
	size_t index = i * ifactor;
	index = index + (j * jfactor);
	index = index + (p * pfactor);
	index = index + q;
	return likelihoodmatrix[index];
}


int cost_MLE(int i, int j, int p, int q)
{
	return (
		((abs(p - i) < config->rad1) && (abs(q - j) < config->rad1)) ? -1 : 0
		);
}