#include <iostream>
#include <vector>
#include <inttypes.h>
#include <fstream>
#include <string>
#include <converters.h>

using namespace std;

template<typename t>
void printVector(vector<t> a)
{
    for (int32_t i=0;i<a.size();i++)
        cout << a[i] << ", ";
    cout << "\n";
}

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
        return 1;
    }

    string fileContents, line;
    while(getline(File,line))
        fileContents += line;
    File.close();

    int64_t filelength = fileContents.length();
    if (filelength % 16 != 0)
    {
        cout << "Error: File is of incorrect length" << endl;
        return 1;
    }

    vector<string> instructions;
    string tmpStr;
    for (int64_t i=0;i<filelength;i++)
    {
        tmpStr += fileContents[i];
        if ((i+1)%16 == 0)
        {
            instructions.push_back(tmpStr);
            tmpStr = "";
        }
    }

    printVector(instructions);
    return 0;
}