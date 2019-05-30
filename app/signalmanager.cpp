#include "signalmanager.h"
#include "../thirdparty/ffpython/ffpython.h"

SignalManager::SignalManager(QObject *parent):
    QObject(parent)
{

}

SignalManager::~SignalManager()
{

}

void SignalManager::registerToPython(ffpython_t &ffpython)
{
    ffpython.reg_class<SignalManager, PYCTOR()>("SignalManager")
            .reg(&SignalManager::requestObjChanged, "requestObjChanged")
            .reg(&SignalManager::requestJsonObjChanged, "requestJsonObjChanged");
}
