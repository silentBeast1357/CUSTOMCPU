#include <inttypes.h>
#include <iostream>
#include <vector>


using namespace std;

namespace RARE
{
    string reverse(string text)
    {
        string output = "";
        for (int i=text.length();i>0;i++)
            output += text[i-1];
        return output;
    }
}

template<typename t>
t htoi(string hex)
{
    t output = 0;
    int32_t multiplier = 1;
    string rHex = RARE::reverse(hex);
    for (int32_t i=0;i<hex.length();i++)
    {
        if (rHex[i] <= '9')
            output += (rHex[i]-48)*multiplier;
        else if (rHex[i] >= 'A')
            output += (rHex[i]-'A'+10)*multiplier;
        multiplier *= 16;
    }

    return output;
}