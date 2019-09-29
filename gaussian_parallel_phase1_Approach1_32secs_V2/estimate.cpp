#include "main.h"

void populate_estimate();
void calculate_estimate();

void populate_estimate()
{	
	init_likelihood_indices();
	for (int i = 0; i < config->l; i++)
	{
		for (int j = 0; j < config->w; j++)
		{
			populate_expected_cost(i, j);
		}
	}
	return;
}


void calculate_estimate()
{
	double run_cost = std::numeric_limits<double>::max();
	double temp_cost = 0.0;

	for (int i = 0; i < config->l; i++)
	{
		for (int j = 0; j < config->w; j++)
		{
			temp_cost = calculate_expected_cost(i, j);
			if (temp_cost < run_cost)
			{
				run_cost = temp_cost;
				ans_var['i'] = i;
				ans_var['j'] = j;
			}
		}
	}
	return;
}