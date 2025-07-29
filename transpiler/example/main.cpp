#include <iostream>
void say(std::string txt) { std::cout << txt; }


int adder(int a, int b) { 
	return a + b;
 }

int main() { 
	say("test");
    adder(2, 4);
    return 0;
 }