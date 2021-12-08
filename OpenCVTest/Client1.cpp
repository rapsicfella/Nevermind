#include <Ice/Ice.h>
#include <Printer1.h>
#include <stdexcept>
 
using namespace std;
using namespace Demo;
 
int
main(int argc, char* argv[])
{
    try
    {
        Ice::CommunicatorHolder ich(argc, argv);
        auto base = ich->stringToProxy("SimplePrinter:default -p 10000");
        auto printer = Ice::checkedCast<Printer1Prx>(base);
        if(!printer)
        {
            throw std::runtime_error("Invalid proxy");
        }
 
        printer->printString("Hello World!");
    }
    catch(const std::exception& e)
    {
        cerr << e.what() << endl;
        return 1;
    }
    return 0;
}
