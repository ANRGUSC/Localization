#include "main.h"

double likelihood(int p, int q);

double likelihood(int p, int q)
{
	std::vector<double> obs_r;
	std::vector<double>::iterator Tx_iter = config->Tx.begin();
	std::vector<double>::iterator Ty_iter = config->Ty.begin();
	double likelihood = 1.0;

	for (; Tx_iter != config->Tx.end(); ++Tx_iter, ++Ty_iter)
	{
		double dist = sqrt((pow(((*Tx_iter) - p), 2)) +
							(pow(((*Ty_iter) - q), 2)));

		if (dist == 0) continue;
		obs_r.push_back((-10 * config->eta * log(dist)));
	}

	for (int i = 0; i < obs_r.size(); i++)
	{
		likelihood *= gaussian_func(config->obs[i], obs_r[i], config->sigma);
	}

	return likelihood;
}