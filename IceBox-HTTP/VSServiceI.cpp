//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#include <Ice/Ice.h>
#include <VSServiceI.h>
#include <VSI.h>
#include <memory>
using namespace std;

extern "C"
{

//
// Factory function
//
ICE_DECLSPEC_EXPORT IceBox::Service* create(const shared_ptr<Ice::Communicator>&)
{
    return new VSServiceI;
}

}
//string VS_CONTAINER_NAME=vs_application;
void VSServiceI::start(const string& name, const shared_ptr<Ice::Communicator>& communicator, const Ice::StringSeq& /*args*/)
{ 
    system("docker run -d --rm --net=host --name vs_app ggs &");
    _adapter = communicator->createObjectAdapter(name);
    auto vs = make_shared<VSI>();
    _adapter->add(vs, Ice::stringToIdentity("vs"));
    _adapter->activate();
}

void VSServiceI::stop()
{
    system("pkill -f -9 native_ui.py &");
    system("docker stop vs_app");
    _adapter->destroy();
}
int main(){return 0;}
