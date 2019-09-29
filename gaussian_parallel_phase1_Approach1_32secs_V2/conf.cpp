#include "conf.h"

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

bool isValid(int x, int y)
{
	(void)x;
	(void)y;
	return true;
}