#include "main.h"

void printConfig();
void printAns();
std::map<char, int> ans_var;
Config* config;
double **kudaTransferKernelMatrix;
std::vector<int> likelihood_indices;
int kudaTransferKernelMatrix_iter;
size_t kernelnumRows;
size_t kernelnumCols;
double *kudaOutMatrix;
double *likelihoodmatrix;
double *expectmatrix;

void ansInit()
{
	ans_var.insert({ 'i', -1 });
	ans_var.insert({ 'j', -1 });
}

int main(void)
{
	config = (Config*) new Config();

	kernelnumRows = (config->l * config->l * config->w * config->w * config->Tx.size())
							+ (3000 - ((config->l * config->l * config->w * config->w * config->Tx.size()) % 3000));
	kernelnumCols = 3;
	kudaOutMatrix = (double*) new double[(uint64_t)kernelnumRows];

	kudaTransferKernelMatrix = (double**) new double*[(uint64_t)kernelnumRows];
	for (size_t i = 0; i < kernelnumRows; i++)
	{
		kudaTransferKernelMatrix[i] = new double[kernelnumCols];
	}
	kudaTransferKernelMatrix_iter = 0;
	
	likelihoodmatrix = (double*) new double[(uint64_t)(config->l * config->l * config->w * config->w)];
	expectmatrix = (double*) new double[(uint64_t)(config->l * config->w)];

	populate_estimate();
	calculate_likelihood();
	calculate_estimate();
	printAns();

	return 0;
}