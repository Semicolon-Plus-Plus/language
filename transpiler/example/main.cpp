#include <iostream>
void say(std::string txt) { std::cout << txt; }


int adder(int a, int b) 
	{
return (a + b);
}


int main() 
	{
say("Testing...\n");
if ((adder(2, 2) == 4)) { say("Adder works!\n");
 } else { say("Adder doesn't work\n");
 }
return 0;
}
