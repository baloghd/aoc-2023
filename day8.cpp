#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <string>
#include <regex>

using namespace std;

struct node
{
    int data;
    node *left;
    node *right;
};

int main()
{

    ifstream infile("day8.input");
    string line;
    size_t found;

    vector<string> instructions;
    vector<node> nodes = {};

    regex word_regex("(\\w+)");

    while (std::getline(infile, line))
    {
        istringstream iss(line);

        if (line.find("=") != string::npos)
        {
            cout << line << endl;
            string value;
                }
    }

    return 0;
}