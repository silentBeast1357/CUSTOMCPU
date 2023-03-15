#include <iostream>
#include <vector>
#include <inttypes.h>
#include <fstream>
#include <string>

using namespace std;

template<typename t>
void printVector(vector<t> a)
{
    for (int32_t i=0;i<a.size();i++)
        cout << a[i] << ", ";
    cout << "\n";
}



string reverse(string text)
{
    string output = "";
    for (int32_t i=0;i<text.length();i++)
        output += text[i];
    return output;
}


template<typename type>
type htoi(string hex)
{
    type output = 0;
    int64_t multiplier = 1;
    string rHex = reverse(hex);
    for (int32_t i=0;i<hex.length();i++)
    {
        if (rHex[i] >= 0 && rHex[i] <= 9)
            output += multiplier*(rHex[i]-48);
        else if (rHex[i] >= 'A' && rHex[i] <= 'F')
            output += multiplier*(rHex[i]-'A'+10);
        multiplier *= 16;
    }

    return output;
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

    for (int i=0;i<instructions.size();i++)
    {
        cout << htoi<uint64_t>(instructions[i]) << endl;
    }

    return 0;
}