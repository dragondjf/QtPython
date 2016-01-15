#include "pyobjectcontroller.h"
#include "../thirdparty/ffpython/ffpython.h"
#include "app/global.h"
#include <QDebug>


PyObjectController::PyObjectController(const int& v, QObject *parent) :
    QObject(parent),
    m_obj(v)
{
    connect(signalManager, SIGNAL(requestObjChanged(int)), this, SLOT(setObj(int)));
}

PyObjectController::~PyObjectController()
{

}

void PyObjectController::registerToPython(ffpython_t& ffpython)
{
    ffpython.reg_class<PyObjectController, PYCTOR(int)>("PyObjectController")
                .reg(&PyObjectController::getObj, "getObj")
                .reg(&PyObjectController::setObj, "setObj")
                .reg(&PyObjectController::testStl, "testStl")
                .reg(&PyObjectController::getInstance, "getInstance")
                .reg_property(&PyObjectController::m_obj, "m_obj");
}

int PyObjectController::getObj()
{
    return m_obj;
}

void PyObjectController::testStl(int v)
{
    qDebug() << v << __FUNCTION__;
}

PyObjectController *PyObjectController::getInstance(int v)
{
    return PyObjectController::instance(v);
}

void PyObjectController::setObj(int obj)
{
    m_obj = obj;
}

