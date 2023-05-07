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

    string fileContents, l;
    while(getline(File,l))
        fileContents += l;
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

    uint64_t line=0;
    while (line<dInstructions.size())
    {
        instructionInfo current = dInstructions[line];

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
        if (current.opcode=="2") // Math instructions
        {
            if (current.opperand[0] == '0') // add
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                *r2 = *r1 + *r2;
            }
            if (current.opperand[0] == '1') // sub 
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                *r2 = *r2 - *r1;
            }
            if (current.opperand[0] == '2') // mul
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                registers[1] *= *r1;
            }
            if (current.opperand[0] == '3') // div
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                registers[2] = registers[1] % *r1;
                registers[1] /= *r1;
            }
            if (current.opperand[0] == '4') // << 
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                *r2 = *r2 << *r1;
            }
            if (current.opperand[0] == '5') // >> 
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                *r2 = *r2 >> *r1;
            }
            if (current.opperand[0] == '6') // not
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                *r1 = ~*r1;
                registers[13] = *r1;
            }
            if (current.opperand[0] == '7') // and
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                *r2 = *r1 & *r2;
                registers[13] = *r2;
            }
            if (current.opperand[0] == '8') // nand
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                *r2 = ~(*r1 & *r2);
                registers[13] = *r2;
            }
            if (current.opperand[0] == '9') // or
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                *r2 = *r1 | *r2;
                registers[13] = *r2;
            }
            if (current.opperand[0] == 'A') // nor
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                *r2 = ~(*r1 | *r2);
                registers[13] = *r2;
            }
            if (current.opperand[0] == 'B') // xor
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                *r2 = *r1 ^ *r2;
                registers[13] = *r2;
            }
        }
        if (current.opcode=="3") // jmp
        {
            if (current.opperandI == 0)
                line = registers[14];
            else if (current.opperand[0] == '1') // je
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));

                if (*r1 == *r2)
                {
                    line = registers[14];
                }
                else
                {
                    line++;
                }
            }
            else if (current.opperand[0] == '2') // jne
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                if (*r1 != *r2)
                {
                    line = registers[14];
                }
                else
                {
                    line++;
                }
            }
            else if (current.opperand[0] == '3') // jl
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                if (*r2 < *r1)
                {
                    line = registers[14];
                }
                else
                {
                    line++;
                }
            }
            else if (current.opperand[0] == '4') // jle
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                if (*r2 <= *r1)
                {
                    line = registers[14];
                }
                else
                {
                    line++;
                }
            }
            else if (current.opperand[0] == '5') // jg
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                if (*r2 > *r1)
                {
                    line = registers[14];
                }
                else
                {
                    line++;
                }
            }
            else if (current.opperand[0] == '6') // jge
            {
                uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
                uint64_t* r2 = registers + htoi<uint8_t>(current.opperand.substr(13,1));
                if (*r2 >= *r1)
                {
                    line = registers[14];
                }
                else
                {
                    line++;
                }
            }
            else if (current.opperand[0] == '7') // jz
            {
                if (registers[13] == 0)
                {
                    line = registers[14];
                }
                else
                {
                    line++;
                }
            }
            else if (current.opperand[0] == '8') // jnz
            {
                if (registers[13] != 0)
                {
                    line = registers[14];
                }
                else
                {
                    line++;
                }
            }
            continue;
        }
        if (current.opcode=="4")//push
        {
            uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
            string r2h = itoh(*r1,true);
            instructionInfo r2s = getInfo(r2h);
            dInstructions[registers[15]] = r2s;
            registers[15]--;
        }
        if (current.opcode=="5")//pop
        {
            registers[15]++;
            uint64_t* r1 = registers + htoi<uint8_t>(current.opperand.substr(14,1));
            *r1 = htoi<uint64_t>(dInstructions[registers[15]].instruction);
            instructionInfo zero = getInfo(itoh<uint64_t>(0,true));
            dInstructions[registers[15]] = zero;
        }
        if (current.opcode=="6")
        {
            if (current.opperandI == 1) // call
            {
                string currentLoc = itoh(line,true);
                instructionInfo cli = getInfo(currentLoc);
                dInstructions[registers[15]] = cli;
                registers[15]--;

                line = registers[14];
                continue;
            }
            if (current.opperandI == 2) //ret
            {
                registers[15]++;
                line = htoi<uint64_t>(dInstructions[registers[15]].instruction);
                line++;
                instructionInfo zero = getInfo(itoh<uint64_t>(0,true));
                dInstructions[registers[15]] = zero;
                continue;
            }
        }

        if (current.opcode=="F") // int
        {
            if (current.opperandI == 60)
            {
                return 0;
            }
            else if (current.opperandI == 1)
            {
                printf("%c",registers[1]);
            }
            else if (current.opperandI == 2)
            {
                printf("%lu",registers[1]);
            }
            else if (current.opperandI == 3)
            {
                uint32_t length = registers[2];
                char* input = new char[length];
                for (uint32_t i=0;i<length;i++)
                    input[i] = 0;
                fgets(input, length, stdin);

                for (uint32_t i=registers[1];i-registers[1]<length;i++)
                {
                    dInstructions[i] = getInfo(itoh<uint64_t>(input[i-registers[1]],1));
                }
                delete[] input;
            }
            else if (current.opperandI == 4)
            {
                uint64_t input;
                cin >> input;
                registers[1] = input;
            }
        }
        line++;
    }

    cout << "Segmentation fault: Core dumped or whatever its called" << endl;
    return 1;
}