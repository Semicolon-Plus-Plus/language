#include <iostream>
void say(std::string txt) { std::cout << txt; }


int adder(int a, int b) 
	{
return a + b;
}


void fastFunc (std::string msg) { say("Welcome, " + msg + "!\n");
 }

bool boolCheck(int a, int b, int exp) 
	{
return (a + b) == exp;
}


int main() 
	{
say("Testing...\n");
if (adder(2, 2) == 4) { say("Adder works!\n");
 } else { say("Adder doesn't work\n");
 }
if (1 != 1) { say("1 isn't 1?!\n");
 } else if (3 == 3) { say("Three is three.\n");
 }

int res = adder(2, 4);
if (res == 6) { say("one");
say("Two");
 }
bool test234 = boolCheck(2, 2, 4);
std::string marf = "test123";
return 0;
}
