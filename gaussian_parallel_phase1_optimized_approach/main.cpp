#include "main.h"
#include <chrono>

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
	auto start = std::chrono::steady_clock::now();

	config = (Config*) new Config();
	likelihoodmatrix = (double*) new double[(uint64_t)(config->l * config->l * config->w * config->w)];
	init_likelihood_indices();
	kernelDriver();
	calculate_estimate();
	printAns();
	// printLikelihoodToFile();

	auto end = std::chrono::steady_clock::now();

	std::cout << "Execution Time : " << std::endl;
	std::cout << "Seconds: " << std::chrono::duration_cast<std::chrono::seconds>(end - start).count() << std::endl;
	std::cout << "MilliSeconds: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << std::endl;
	std::cout << "MicroSeconds: " << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() << std::endl;
	std::cout << "NanoSeconds: " << std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() << std::endl;

	return 0;
}