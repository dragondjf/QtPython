#include "signalmanager.h"
#include "../thirdparty/ffpython/ffpython.h"

SignalManager::SignalManager()
{

}

SignalManager::~SignalManager()
{

}

void SignalManager::registerToPython(ffpython_t &ffpython)
{
    ffpython.reg_class<SignalManager, PYCTOR()>("SignalManager");
    ffpython.init("SignalManager");
    ffpython.set_global_var("SignalManager", "signalManager", SignalManager::instance());
}
