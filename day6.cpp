#include <iostream>

long ways(long t, long d)
{
    long count = 0;
    for (long i = 1; i < t; i++)
    {
        // std::cout << (i * (t - i)) << std::endl;
        if ((i * (t - i)) > d)
        {
            count++;
        }
    }
    return count;
};

int main()
{
    long t = 35696887;
    long d = 213116810861248;

    std::cout << ways(t, d) << std::endl;
    return 0;
}