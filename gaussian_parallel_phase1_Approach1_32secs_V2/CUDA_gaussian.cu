#include "main.h"
#include <stdio.h>
#include "cuda_runtime.h"
#include "cuda.h"

// #define __TESTMODE__

#ifndef __TESTMODE__
#define IN_MAT_ROWS		3000
#define NUM_BLOCKS		10
#else
#define IN_MAT_ROWS		9
#define NUM_BLOCKS		3
#endif

#define IN_MAT_COLS			3
#define OUT_MAT_COLS		1
#define OUT_MAT_ROWS		IN_MAT_ROWS
#define NUM_THRDS_PER_BLK	((IN_MAT_ROWS/NUM_BLOCKS) * IN_MAT_COLS)


void kernelDriver(size_t);


__global__ void cuda_hello() {
	int thrId_Act = blockIdx.x * blockDim.x + threadIdx.x;
	printf("Hello World from GPU!\t%d\t%lu\n", blockIdx.x, thrId_Act);
}


__global__ void cuda_gaussian(double *outArr, double *inArr) {
	int thrId_Blk = threadIdx.x;
	int thrId_Act = blockIdx.x * blockDim.x + threadIdx.x;
	int opmode = thrId_Blk % IN_MAT_COLS;
	double comp_a_factor = sqrt(2 * M_PI);
	__device__ __shared__ double gaussianIntrComp_t[NUM_THRDS_PER_BLK];

	switch (opmode)
	{
		case 0:
		{
			gaussianIntrComp_t[thrId_Blk] = -pow((inArr[thrId_Act] - inArr[thrId_Act + 1]), 2.0);
			break;
		}

		case 1:
		{
			gaussianIntrComp_t[thrId_Blk] = 2 * pow(inArr[thrId_Act + 1], 2.0);
			break;
		}

		case 2:
		{
			gaussianIntrComp_t[thrId_Blk] = 1.0 / (comp_a_factor * inArr[thrId_Act]);
			break;
		}

		default:
			break;
	}

	__syncthreads();
	if (opmode == 2)
	{
		double comp_d;
		comp_d = pow(M_E, (gaussianIntrComp_t[thrId_Blk - 2] / gaussianIntrComp_t[thrId_Blk - 1]));
		outArr[thrId_Act / IN_MAT_COLS] = gaussianIntrComp_t[thrId_Blk] * comp_d;
	}
	return;
}

__global__ void simplecudaAdd(double* out, double* in)
{
	printf("Hello World from GPU!\n");
	for (int i = 0; i < (IN_MAT_ROWS * IN_MAT_COLS); i++)
	{
		printf("%f\n", in[i]);
	}
	for (int i = 0; i < 9; i++)
	{
		out[i] = 10.0;
		printf(" %d\t\t%d\t\t%d\t\t%d\n", (blockIdx.x * blockDim.x + threadIdx.x), blockIdx.x, blockDim.x, threadIdx.x);
	}

}

 void kernelDriver(size_t curIter) 
 {
	 size_t outer_var = curIter;
	//for (size_t outer_var = 0; outer_var < kernelnumRows; outer_var+=3000)
	//{
		double *inputGPUXferArr = (double*) new double[IN_MAT_ROWS * IN_MAT_COLS];
		double *outputGPUXferArr = (double*) new double[OUT_MAT_ROWS * OUT_MAT_COLS];
		double *kern_inputArr;
		double *kern_outputArr;
		cudaError_t error;
		double *kernOutputArrPtr = &kudaOutMatrix[0];

		if ((error = cudaMalloc((void**)&kern_outputArr, OUT_MAT_ROWS * OUT_MAT_COLS * sizeof(double))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel outputArr" << std::endl;
		}

		if ((error = cudaMalloc((void**)&kern_inputArr, IN_MAT_ROWS * IN_MAT_COLS * sizeof(double))) != cudaSuccess)
		{
			std::cout << "cudaMalloc returned error for kernel inputArr" << std::endl;
		}

		for (size_t i = outer_var, counter_i = 0; i < (outer_var + 3000); i++)
		{
			for (size_t j = 0; j < IN_MAT_COLS; j++, counter_i++)
				inputGPUXferArr[counter_i] = kudaTransferKernelMatrix[i][j];
		}

		error = cudaMemcpy(kern_inputArr, inputGPUXferArr, IN_MAT_ROWS * IN_MAT_COLS * sizeof(double), cudaMemcpyHostToDevice);
		if (error != cudaSuccess)
		{
			std::cout << "cudaMemcpy returned error for copying kernel size" << std::endl;
		}

		cudaDeviceSynchronize();

		cuda_gaussian << <NUM_BLOCKS, NUM_THRDS_PER_BLK >> > (kern_outputArr, kern_inputArr);
		cudaMemcpy(kernOutputArrPtr + outer_var, kern_outputArr, OUT_MAT_ROWS * sizeof(double), cudaMemcpyDeviceToHost);
	//}
}