#include "main.h"
#include <stdio.h>
#include "cuda_runtime.h"
#include "cuda.h"

// Use a multiple of 4
#define MAX_THREADS 8

void kernelDriver();


__global__ void cuda_gaussian(double *out_likelihood, double *in_obs, double *in_Tx, double *in_Ty, double *in_eta, 
								double *in_sigma, int *in_lmax, int *in_wmax, int *in_totthreads) 
{
	int thrId = blockIdx.x * blockDim.x + threadIdx.x;
	
	if (thrId >= *in_totthreads)
		return;

	// printf("Hello World from GPU!\t%lu\n", thrId); return;

	int inmr = thrId, idnr = ((*in_totthreads)/ (*in_lmax));
	int jnmr = (inmr%idnr), jdnr = (idnr / (*in_wmax));
	int pnmr = (jnmr%jdnr), pdnr = (jdnr / (*in_lmax));
	int p = pnmr / pdnr;
	int q = pnmr % pdnr;

	double obs_r[3];
	double likelihood = 1.0;
	int iter;
	int obsr_iter;

	for (iter = 0, obsr_iter = 0; iter < 3; iter++)
	{
		double dist = sqrt((pow(((in_Tx[iter]) - p), 2)) +
			(pow(((in_Ty[iter]) - q), 2)));

		if (dist == 0) continue;
		obs_r[obsr_iter++] = -10 * (*in_eta) * log(dist);
	}

	for (iter = 0; iter < obsr_iter; iter++)
	{
		double temp_likelihood = (1.0 / ((sqrt(2 * M_PI)) * (*in_sigma))) *
									(exp((-pow(in_obs[iter] - obs_r[iter], 2.0)) /
									(2 * pow((*in_sigma), 2.0))));
		likelihood *= temp_likelihood;
	}
	out_likelihood[thrId] =  likelihood;
	return;
}

 void kernelDriver(int args_numThr) 
 {	
		double *kern_inputobs;
		double *kern_inputTx;
		double *kern_inputTy;
		double *kern_inputeta;
		double *kern_inputsigma;
		int *kern_inputlmax;
		int *kern_inputwmax;
		int *kern_inputtotthreads;

		double *kern_outputArr;
		cudaError_t error;

		// Malloc Session
		if ((error = cudaMalloc((void**)&kern_outputArr, (config->l * config->l * config->w * config->w) * sizeof(double))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel outputArr" << std::endl;
		}

		if ((error = cudaMalloc((void**)&kern_inputobs, 3 * sizeof(double))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel inputObs" << std::endl;
		}

		if ((error = cudaMalloc((void**)&kern_inputTx, 3 * sizeof(double))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel inputTx" << std::endl;
		}

		if ((error = cudaMalloc((void**)&kern_inputTy, 3 * sizeof(double))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel inputTy" << std::endl;
		}

		if ((error = cudaMalloc((void**)&kern_inputeta, sizeof(double))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel inputeta" << std::endl;
		}

		if ((error = cudaMalloc((void**)&kern_inputsigma, sizeof(double))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel inputsigma" << std::endl;
		}

		if ((error = cudaMalloc((void**)&kern_inputlmax, sizeof(int))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel inputlmax" << std::endl;
		}

		if ((error = cudaMalloc((void**)&kern_inputwmax, sizeof(int))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel inputwmax" << std::endl;
		}

		if ((error = cudaMalloc((void**)&kern_inputtotthreads, sizeof(int))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel inputtotthreads" << std::endl;
		}


		// Memcpy Session
		double* obs_arr = &config->obs[0];
		error = cudaMemcpy(kern_inputobs, obs_arr, 3 * sizeof(double), cudaMemcpyHostToDevice);
		if (error != cudaSuccess)
		{
			std::cout << "cudaMemcpy returned error for copying kern_inputobs" << std::endl;
		}

		double* Tx_arr = &config->Tx[0];
		error = cudaMemcpy(kern_inputTx, Tx_arr, 3 * sizeof(double), cudaMemcpyHostToDevice);
		if (error != cudaSuccess)
		{
			std::cout << "cudaMemcpy returned error for copying kern_inputTx" << std::endl;
		}

		double* Ty_arr = &config->Ty[0];
		error = cudaMemcpy(kern_inputTy, Ty_arr, 3 * sizeof(double), cudaMemcpyHostToDevice);
		if (error != cudaSuccess)
		{
			std::cout << "cudaMemcpy returned error for copying kern_inputTy" << std::endl;
		}

		error = cudaMemcpy(kern_inputeta, &config->eta, sizeof(double), cudaMemcpyHostToDevice);
		if (error != cudaSuccess)
		{
			std::cout << "cudaMemcpy returned error for copying kern_inputeta" << std::endl;
		}

		error = cudaMemcpy(kern_inputsigma, &config->sigma, sizeof(double), cudaMemcpyHostToDevice);
		if (error != cudaSuccess)
		{
			std::cout << "cudaMemcpy returned error for copying kern_inputsigma" << std::endl;
		}

		error = cudaMemcpy(kern_inputlmax, &config->l, sizeof(int), cudaMemcpyHostToDevice);
		if (error != cudaSuccess)
		{
			std::cout << "cudaMemcpy returned error for copying kern_inputlmax" << std::endl;
		}

		error = cudaMemcpy(kern_inputwmax, &config->w, sizeof(int), cudaMemcpyHostToDevice);
		if (error != cudaSuccess)
		{
			std::cout << "cudaMemcpy returned error for copying kern_inputwmax" << std::endl;
		}

		int totthreads = config->l * config->w * config->l * config->w;
		error = cudaMemcpy(kern_inputtotthreads, &totthreads, sizeof(int), cudaMemcpyHostToDevice);
		if (error != cudaSuccess)
		{
			std::cout << "cudaMemcpy returned error for copying kern_inputtotthreads" << std::endl;
		}

		unsigned int numBlocks = ((unsigned int)floor((config->l * config->l * config->w * config->w) / args_numThr) + 1) * 4;
		int numThreads = args_numThr/4;
		cudaDeviceSynchronize();
		cuda_gaussian << <numBlocks, numThreads >> > (kern_outputArr, kern_inputobs, kern_inputTx, kern_inputTy, kern_inputeta,
														kern_inputsigma, kern_inputlmax, kern_inputwmax, kern_inputtotthreads);
		cudaDeviceSynchronize();

		cudaMemcpy(likelihoodmatrix, kern_outputArr, (config->l * config->l * config->w * config->w) * sizeof(double), cudaMemcpyDeviceToHost);

}
