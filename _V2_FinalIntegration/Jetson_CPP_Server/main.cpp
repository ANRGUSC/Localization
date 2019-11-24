#include "main.h"
#include <chrono>
#include <sstream>

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
std::string invokeGPUEngine(char*, int);

void ansInit()
{
	ans_var.insert({ 'i', -1 });
	ans_var.insert({ 'j', -1 });
}

std::string invokeGPUEngine(char* incVal, int numThr)
{
	std::string incStr(incVal);
	if(incStr.find("(l!=N| REQ: ") == std::string::npos)
	{
		if(incStr.find("$35V35 OUTPUT") == std::string::npos)
			return "";
		return "$35V35 OUTPUT: NOK - INVALID INPUT";
	}
	
	config = (Config*) new Config(incStr);
	auto start = std::chrono::steady_clock::now();
	
	likelihoodmatrix = (double*) new double[(uint64_t)(config->l * config->l * config->w * config->w)];
	init_likelihood_indices();
	kernelDriver(numThr);
	calculate_estimate();
	std::cout << "Obtained Answer: ";
	printAns();
	
	auto end = std::chrono::steady_clock::now();
	std::cout << "\n-----Statisics-----\nExecution Time : " << std::endl;
	std::cout << "Seconds: " << std::chrono::duration_cast<std::chrono::seconds>(end - start).count() << std::endl;
	std::cout << "MilliSeconds: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << std::endl;
	std::cout << "MicroSeconds: " << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() << std::endl;
	std::cout << "NanoSeconds: " << std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() << std::endl;

	std::string outStr("$35V35 OUTPUT: OK; ");
	outStr += '[';
	outStr += std::to_string(ans_var['i']);
	outStr += ',';
	outStr += std::to_string(ans_var['j']);
	outStr += ']';
	return outStr;
}
