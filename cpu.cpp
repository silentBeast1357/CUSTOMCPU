#include <iostream>
#include <vector>
#include <inttypes.h>
#include <fstream>
#include <string>

using namespace std;

template<typename t>
void printVector(vector<t> a)
{
    for (uint32_t i=0;i<a.size();i++)
        cout << a[i] << ", ";
    cout << "\n";
}

string reverse(string text)
{
    string output = "";
    for (uint32_t i=text.length();i>0;i--)
        output += text[i-1];
    return output;
}


template<typename type>
type htoi(string hex)
{
    type output = 0;
    int64_t multiplier = 1;
    string rHex = reverse(hex);
    for (uint32_t i=0;i<hex.length();i++)
    {
        if (rHex[i] >= '0' && rHex[i] <= '9')
            output += multiplier*(rHex[i]-48);
        else if (rHex[i] >= 'A' && rHex[i] <= 'F')
            output += multiplier*(rHex[i]-'A'+10);
        multiplier *= 16;
    }

    return output;
}

struct instructionInfo 
{
    string opcode;
    string opperand;
    string instruction;
    uint8_t opcodeI;
    uint64_t opperandI;
};

void printInsDat(instructionInfo ins)
{
    cout << "Instruction: " << ins.instruction << endl
    << "Opcode: " << ins.opcode << ", " << (uint32_t)ins.opcodeI << endl
    << "Opperand: " << ins.opperand << ", " << ins.opperandI << endl;
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

    uint64_t filelength = fileContents.length();
    if (filelength % 16 != 0)
    {
        cout << "Error: File is of incorrect length" << endl;
        return 1;
    }

    vector<string> instructions;
    string tmpStr;
    for (uint64_t i=0;i<filelength;i++)
    {
        tmpStr += fileContents[i];
        if ((i+1)%16 == 0)
        {
            instructions.push_back(tmpStr);
            tmpStr = "";
        }
    }

    vector<instructionInfo> dInstructions;
    for (uint64_t i=0;i<instructions.size();i++)
    {
        instructionInfo dIns;
        dIns.instruction = instructions[i];
        dIns.opcode = instructions[i][0];
        dIns.opperand = instructions[i].substr(1,15);
        dIns.opcodeI = htoi<uint8_t>(dIns.opcode);
        dIns.opperandI = htoi<uint64_t>(dIns.opperand);
        dInstructions.push_back(dIns);
    }

    for (uint64_t i=0;i<dInstructions.size();i++)
    {
        instructionInfo current = dInstructions[i];

        if (current.opcode=="F")
        {
            if (current.opperand == "FFFFFFFFFFFFFFF")
            {
                return 0;
            }
        }
    }

    cout << "Segmentation fault: Core dumped or whatever its called" << endl;
    return 1;
}