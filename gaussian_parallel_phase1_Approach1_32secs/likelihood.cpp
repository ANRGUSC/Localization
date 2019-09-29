#include "main.h"

void populate_likelihood(int p, int q);
void calculate_likelihood();

void populate_likelihood(int p, int q)
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

	likelihood_indices.push_back((int)obs_r.size());
	for (int i = 0; i < obs_r.size(); i++)
	{
		kudaTransferKernelMatrix[kudaTransferKernelMatrix_iter][0] = config->obs[i];
		kudaTransferKernelMatrix[kudaTransferKernelMatrix_iter][1] = obs_r[i];
		kudaTransferKernelMatrix[kudaTransferKernelMatrix_iter][2] = config->sigma;
		kudaTransferKernelMatrix_iter++;
	}
}

void calculate_likelihood()
{
	kernelDriver();
	double* kudaOutMatrixPtr = &kudaOutMatrix[0];
	for (int i = 0; i < likelihood_indices.size(); i++)
	{
		double depositVal = 0.0;
		for (int j = 0; j < likelihood_indices[i]; j++)
		{
			depositVal += (*kudaOutMatrixPtr);
			kudaOutMatrixPtr++;
		}
		likelihoodmatrix[i] = depositVal;
	}
}