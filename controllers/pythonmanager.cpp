#include "pythonmanager.h"
#include <QDir>
#include <QDebug>
#include <QJsonObject>
#include <QJsonArray>
#include <QJsonValue>
#include <QJsonParseError>
#include "logmanager.h"
#include "Logger.h"
#include "pyobjectcontroller.h"
#include "app/signalmanager.h"
#include "../ffpython/ffpython.h"


PythonManager::PythonManager(QObject *parent) :
    QObject(parent)
{
    initPython();
    m_ffpython = new ffpython_t;
    registerLogger();
    testGetGlobalVar();
    testSetGlobalVar();
    testCallModuleMethodNoArgs();
    testCallModuleMethodWidthArgs();
    testCallRetunJson();
    testRegisterClass();
}

PythonManager::~PythonManager()
{
    qDebug() << "Python virtual machine quit started";
    ffpython_t::final_py();
    qDebug() << "Python virtual machine quit finished";
}

void PythonManager::initPython()
{
    qDebug() << "PythonManager init started";
    ffpython_t::init_py();
    ffpython_t::add_path("../QtPython/python");
    ffpython_t::add_path("./python");
    ffpython_t::add_path("./");
    qDebug() << "PythonManager init finished";
}

void PythonManager::registerLogger()
{
    m_ffpython->reg(&PythonManager::debug, "debug");
    m_ffpython->reg(&PythonManager::info, "info");
    m_ffpython->reg(&PythonManager::warning, "warning");
    m_ffpython->reg(&PythonManager::error, "error");
    m_ffpython->reg(&PythonManager::fatal, "fatal");
    m_ffpython->init("qtlogger", "use qDebug in python");
}

int PythonManager::debug(const string &val_1)
{
    LOG_CDEBUG("python") << val_1.c_str();
    return 0;
}

int PythonManager::info(const string &val_1)
{
    LOG_CINFO("python") << val_1.c_str();
    return 0;
}

int PythonManager::warning(const string &val_1)
{
    LOG_CWARNING("python") << val_1.c_str();
    return 0;
}

int PythonManager::error(const string &val_1)
{
    LOG_CERROR("python") << val_1.c_str();
    return 0;
}

int PythonManager::fatal(const string &val_1)
{
    LOG_CFATAL("python") << val_1.c_str();
    return 0;
}

QJsonObject PythonManager::callPythonApi(const string module, const string method, const string jsonArgs)
{
    QJsonObject messageObj{};
    string ret = m_ffpython->call<string>(module, method, jsonArgs);
    qDebug() << ret.c_str();
    QJsonParseError* error = new QJsonParseError();
    messageObj = QJsonDocument::fromJson(QByteArray(ret.c_str()), error).object();
    if (error->error != QJsonParseError::NoError){
        qDebug() << error->errorString();
    }
    return messageObj;
}

QJsonObject PythonManager::callPythonApi(const char* module, const char* method, const char* jsonArgs)
{
    return callPythonApi(string(module), string(method), string(jsonArgs));
}

QJsonObject PythonManager::callPythonApi(const QString &module, const QString &method, const QString &jsonArgs)
{
    return callPythonApi(module.toStdString(), method.toStdString(), jsonArgs.toStdString());
}

void PythonManager::testGetGlobalVar()
{
    qDebug() << m_ffpython->get_global_var<string>("sys", "version").c_str();
}

void PythonManager::testSetGlobalVar()
{
    m_ffpython->set_global_var("main", "global_var", "OhNice");
    qDebug() << m_ffpython->get_global_var<string>("main", "global_var").c_str();
}

void PythonManager::testCallModuleMethodNoArgs()
{
    qDebug() << m_ffpython->call<string>("time", "asctime").c_str();
}

void PythonManager::testCallModuleMethodWidthArgs()
{
//    int a1 = 100;
//    float a2 = 3.14f;
//    string a3 = "OhWell";

    vector<int> a1;
    a1.push_back(100);
    a1.push_back(200);
    list<string> a2;
    a2.push_back("Oh");
    a2.push_back("Nice");
    vector<list<string> > a3;
    a3.push_back(a2);

    m_ffpython->call<void>("main", "test_base", a1, a2, a3);
}

void PythonManager::testCallRetunJson()
{
    QJsonObject args;
    args.insert("a1", "1111");
    QVariantList a2{1, 2, 3 ,4};
    args.insert("a2", QJsonValue(QJsonArray::fromVariantList(a2)));
    QMap<QString, QVariant> a3;
    a3.insert("a", "ddasdsds");
    a3.insert("b", a2);
    args.insert("a3", QJsonValue::fromVariant(a3));
    args.insert("a4", QJsonValue::fromVariant(a3));
    QString jsonArgs = QString(QJsonDocument(args).toJson());
//    qDebug() << jsonArgs;
    callPythonApi("main", "returnJson", jsonArgs);
}

void PythonManager::testRegisterClass()
{
    PyObjectController::registerToPython(*m_ffpython);
    SignalManager::registerToPython(*m_ffpython);
    m_ffpython->init("QtCore");
    m_ffpython->set_global_var("QtCore", "pyobjInstance", PyObjectController::instance(100));
    m_ffpython->set_global_var("QtCore", "signalManager", SignalManager::instance());
    m_ffpython->call<void>("main", "testClass");
}
