#include "conf.h"
#include <iostream>

using namespace std;

Config::Config()
{
	obs = { -120.40999999999991, -126.28899999999972, -125.26200000000017 };
	Tx = { 1, 2, 3 };
	Ty = { 5, 5, 5 };
	l = 15;
	w = 100;
	sigma = 16.16;
	eta = 3.93;
	rad1 = 0.1;
	//total_area = (double)(this->l * this->w);
	total_area = 109.0;

	prob = new double*[this->l];
	for (int i = 0; i < this->l; i++)
	{
		prob[i] = new double[this->w];
	}

	for (int i = 0; i < this->l; i++)
	{
		for (int j = 0; j < this->w; j++)
		{
			if (isValid(i, j))
			{
				prob[i][j] = 1.0 / this->total_area;
			}
			else 
			{
				prob[i][j] = 0.0;
			}
		}
	}
}

Config::Config(std::string inputStr)
{
	obs.clear();
	Tx.clear();
	Ty.clear();

	std::string::iterator start = inputStr.begin();
	std::string::iterator constEnd = inputStr.end();
	std::string::iterator travEnd = constEnd;
	int extractionMode = 0;

	for(;;)
	{
		for(; *start != '['; start++);
		travEnd = start;
		for(; *travEnd != ']'; travEnd++);
		switch(extractionMode)
		{
		    case 0:
		    {
		        start++;
		        int count = 3;
		        std::string::iterator commaIterStart = start;
		        for(int i = 0; i < count; i++)
		        {
		            std::string::iterator commaIterEnd = commaIterStart;
		            for(; *commaIterEnd != ','; commaIterEnd++);
		            auto temp = std::string(commaIterStart, commaIterEnd);
		            obs.push_back(std::stod(temp));
		            commaIterStart = commaIterEnd;
		            commaIterStart++;
		        }
		        extractionMode++;
		        break;
		    }
		    
		    case 1:
		    {
		        start++;
		        int count = 3;
		        std::string::iterator commaIterStart = start;
		        for(int i = 0; i < count; i++)
		        {
		            std::string::iterator commaIterEnd = commaIterStart;
		            for(; *commaIterEnd != ','; commaIterEnd++);
		            auto temp = std::string(commaIterStart, commaIterEnd);
		            Tx.push_back(std::stod(temp));
		            commaIterStart = commaIterEnd;
		            commaIterStart++;
		        }
		        extractionMode++;
		        break;
		    }
		    
		    case 2:
		    {
		        start++;
		        int count = 3;
		        std::string::iterator commaIterStart = start;
		        for(int i = 0; i < count; i++)
		        {
		            std::string::iterator commaIterEnd = commaIterStart;
		            for(; *commaIterEnd != ','; commaIterEnd++);
		            auto temp = std::string(commaIterStart, commaIterEnd);
		            Ty.push_back(std::stod(temp));
		            commaIterStart = commaIterEnd;
		            commaIterStart++;
		        }
		        extractionMode++;
		        goto End;
		    }
		}
		
		start = travEnd;
		start++;
	}
	
	End:

		l = 15;
		w = 100;
		sigma = 16.16;
		eta = 3.93;
		rad1 = 0.1;
		total_area = 109.0;

		prob = new double*[this->l];
		for (int i = 0; i < this->l; i++)
		{
			prob[i] = new double[this->w];
		}

		for (int i = 0; i < this->l; i++)
		{
			for (int j = 0; j < this->w; j++)
			{
				if (isValid(i, j))
				{
					prob[i][j] = 1.0 / this->total_area;
				}
				else 
				{
					prob[i][j] = 0.0;
				}
			}
		}

	//     std::cout.precision(17);
	//     for(std::vector<double>::iterator i = obs.begin(); i != obs.end(); i++)
	//         std::cout << *i << " ";
	    
	//     std::cout << std::endl;
	//     for(std::vector<double>::iterator i = Tx.begin(); i != Tx.end(); i++)
	//         std::cout << *i << " ";
	    
	//     std::cout << std::endl;    
	//     for(std::vector<double>::iterator i = Ty.begin(); i != Ty.end(); i++)
	//         std::cout << *i << " ";

	// std::cout << l << std::endl;
	// std::cout << w << std::endl;
	// std::cout << sigma << std::endl;
	// std::cout << eta << std::endl;
	// std::cout << rad1 << std::endl;
	// std::cout << total_area << std::endl;

	return;
}

bool isValid(int x, int y)
{
	(void)x;
	(void)y;
	return true;
}