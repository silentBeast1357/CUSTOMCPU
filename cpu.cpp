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

instructionInfo getInfo(string instruction)
{
    instructionInfo dIns;
    dIns.instruction = instruction;
    dIns.opcode = instruction[0];
    dIns.opperand = instruction.substr(1,15);
    dIns.opcodeI = htoi<uint8_t>(dIns.opcode);
    dIns.opperandI = htoi<uint64_t>(dIns.opperand);
    return dIns;
}

template<typename type>
string itoh(type num,uint8_t is64)
{
    string output = "";
    vector<uint8_t> stack;
    type n = num;
    while(num > 0)
    {
        stack.push_back(num%16);
        num /= 16;
    }

    while (stack.size() != 0)
    {
        uint32_t bit = stack.back();
        stack.pop_back();

        if (bit >= 0 && bit <= 9)
        {
            output += bit + 48;
        } else if (bit >= 10 && bit <= 15)
        {
            output += 'A' + bit - 10;
        }
    }
    
    if (is64)
    {
        string zeros = "";
        for (int i=0;i<16-output.length();i++)
        {
            zeros += "0";
        }
        output = zeros + output;
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
        dInstructions.push_back(getInfo(instructions[i]));
    }

    uint64_t registers[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

    for (uint64_t i=0;i<dInstructions.size();i++)
    {
        instructionInfo current = dInstructions[i];
        if (current.opcode=="0")
        {
            registers[0] = current.opperandI; 
        }
        if (current.opcode=="1") // mov
        {
            uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
            uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(12,1));
            uint8_t r1p = htoi<uint8_t>(current.opperand.substr(13,1));
            uint8_t r2p = htoi<uint8_t>(current.opperand.substr(11,1));

            if (r1p==0   &&   r2p==0)
            {
                *r2 = *r1;
            }
            else if (r1p!=0   &&    r2p==0)
            {
                *r2 = htoi<uint64_t>(dInstructions[*r1].instruction);
            }
            else if (r1p==0    &&     r2p!=0)
            {
                string r2h = itoh(*r1,true);
                instructionInfo r2s = getInfo(r2h);
                dInstructions[*r2] = r2s;
            }
            else if (r1p!=0   &&    r2p!=0)
            {
                dInstructions[*r2] = dInstructions[*r1];
            }
        }

        /*
        for (int i=0;i<16;i++)
        {
            cout << registers[i] << ", ";
        }
        cout << endl;

        for (int i=0;i<dInstructions.size();i++)
        {
            cout << dInstructions[i].instruction << ",";
        }
        cout << endl;
        */

        if (current.opcode=="F") // int
        {
            if (current.opperandI == 60)
            {
                return 0;
            }
            else if (current.opperandI = 1)
            {
                printf("%c",registers[1]);
            }
            else if (current.opperandI = 2)
            {
                printf("%ld",registers[1]);
            }
        }
    }

    cout << "Segmentation fault: Core dumped or whatever its called" << endl;
    return 1;
}