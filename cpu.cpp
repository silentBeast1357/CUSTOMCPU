#include <iostream>
#include <vector>
#include <inttypes.h>
#include <fstream>
#include <string>

using namespace std;

int32_t main(int32_t argc, char** argv)
{
    if (argc != 2)
    {
        cout << "Error: No file provided" << endl; 
        return 1;
    }

    ifstream File(argv[1]);
    if (!File.is_open())
    {
        cout << "Error: File not found" << endl;
    }

    string fileContents, line;
    while(getline(File,line))
        fileContents += line;
    File.close();
    return 0;
}