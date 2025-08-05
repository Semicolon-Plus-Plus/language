#include <iostream>
#include <vector>
void say(std::string txt, std::string lastAdd = "\n") { std::cout << txt << lastAdd; }


int adder(int a, int b) 
	{
return a + b;
}


void fastFunc (std::string msg) { say("Welcome, " + msg + "!");
 }

bool boolCheck(int a, int b, int exp) 
	{
return (a + b) == exp;
}


int main() 
	{
say("Testing...");
if (adder(2, 2) == 4) { say("Adder works!");
 } else { say("Adder doesn't work");
 }
if (1 != 1) { say("1 isn't 1?!");
 } else if (3 == 3) { say("Three is three.");
 }

int res = adder(2, 4);
if (res == 6) { say("One.", "");
say("Two");
 }
bool test234 = boolCheck(2, 2, 4);
std::string marf = "test123";
if (res != 7) { say("res isn't 7! (OK)");
 }
fastFunc("wwwqr");
std::vector<int> listTest = { 1, 2, 3 };
listTest.push_back(3);
return 0;
}
