#include <Ice/Ice.h>
#include <VS.h>
#include <stdexcept>
//#include <unistd.h>

 
using namespace std;
using namespace VideoStreaming;
 
int run(const shared_ptr<Ice::Communicator>&);

int main(int argc, char* argv[])
{
#ifdef ICE_STATIC_LIBS
    Ice::registerIceSSL();
    Ice::registerIceUDP();
    Ice::registerIceWS();
#endif
    int status = 0;
    /*system("python3 /home/harsha/Desktop/Videostreaming_v1/nativeUI_vs/native_ui.py &");
    cout.flush();
    sleep(1); */
    try
    {
        // CommunicatorHolder's ctor initializes an Ice communicator,
        // and its dtor destroys this communicator.
        Ice::CommunicatorHolder ich(argc, argv, "config.client");
        //string s1(argv[1]);
        //string s2(argv[2]);
        status = run(ich.communicator());
    }
    catch(const std::exception& ex)
    {
        cerr << argv[0] << ": " << ex.what() << endl;
        status = 1;
    }

    return status;
}


int run(const shared_ptr<Ice::Communicator>& communicator)
{
    auto x = Ice::checkedCast<VSPrx>(communicator->propertyToProxy("VS.Proxy"));
    x->initVideoStreamingApp();
    return 0;
}
