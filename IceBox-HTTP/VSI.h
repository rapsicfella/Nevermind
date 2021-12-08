//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#ifndef HELLO_I_H
#define HELLO_I_H

#include <VS.h>

class VSI : public VideoStreaming::VS
{
public:

    virtual void initVideoStreamingApp(const Ice::Current&) override;
};

#endif
