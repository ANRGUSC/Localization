#include "main.h"
#include <chrono>

void printConfig();
void printAns();
std::map<char, int> ans_var;
Config* config;

void ansInit()
{
	ans_var.insert({ 'i', -1 });
	ans_var.insert({ 'j', -1 });
}

int main(void)
{
	auto start = std::chrono::steady_clock::now();
	config = (Config*) new Config();

	estimate();
	// printConfig();
	printAns();

	auto end = std::chrono::steady_clock::now();

	std::cout << "Execution Time : " << std::endl;
	std::cout << "Seconds: " << std::chrono::duration_cast<std::chrono::seconds>(end - start).count() << std::endl;
	std::cout << "MilliSeconds: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << std::endl;
	std::cout << "MicroSeconds: " << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() << std::endl;
	std::cout << "NanoSeconds: " << std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() << std::endl;

	return 0;
}