#include "main.h"
#include <fstream>

void printConfig();
void printAns();
void printLikelihoodToFile();

void printConfig()
{
	std::vector<double>::iterator i;

	std::cout << "obs[]:";
	for (i = config->obs.begin(); i != config->obs.end(); i++)
	{
		std::cout << *i << " ";
	}
	std::cout << std::endl;

	std::cout << "Tx[]:";
	for (i = config->Tx.begin(); i != config->Tx.end(); i++)
	{
		std::cout << *i << " ";
	}
	std::cout << std::endl;

	std::cout << "Ty[]:";
	for (i = config->Ty.begin(); i != config->Ty.end(); i++)
	{
		std::cout << *i << " ";
	}
	std::cout << std::endl;

	std::cout << "l:" << config->l << std::endl;
	std::cout << "w:" << config->w << std::endl;
	std::cout << "total_area:" << config->total_area << std::endl;
	std::cout << "sigma:" << config->sigma << std::endl;
	std::cout << "eta:" << config->eta << std::endl;
	std::cout << "rad1:" << config->rad1 << std::endl;

	for (int i = 0; i < config->l; i++)
	{
		for (int j = 0; j < config->w; j++)
		{
			std::cout << config->prob[i][j] << " ";
		}
		std::cout << std::endl;
	}
	return;
}

void printAns()
{
	std::cout << ans_var['i'] << " " << ans_var['j'];
}

void printLikelihoodToFile()
{
	std::ofstream outfile;
	outfile.open("outfile_likelihood.txt");
	for (int p = 0; p < (config->l * config->l * config->w * config->w); p++)
	{
		outfile << likelihoodmatrix[p] << "\n";
	}
	outfile.close();
}