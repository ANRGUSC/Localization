#include "main.h"

double expected_cost(int i, int j);
static int cost_MLE(int i, int j, int p, int q);

double expected_cost(int i, int j)
{
	double expect = 0.0;

	for (int p = 0; p < config->l; p++)
	{
		for (int q = 0; q < config->w; q++)
		{
			expect += (config->prob[i][j] * likelihood(p, q)) 
						* cost_MLE(i, j, p, q);
		}
	}

	return expect;
}

int cost_MLE(int i, int j, int p, int q)
{
	return (
		((abs(p - i) < config->rad1) && (abs(q - j) < config->rad1)) ? -1 : 0
		);
}