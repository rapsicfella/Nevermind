//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#ifndef HELLO_I_H
#define HELLO_I_H

#include <Hello.h>

class HelloI : public Demo::Hello
{
public:

    virtual void sayHello(const Ice::Current&) override;
};

#endif
