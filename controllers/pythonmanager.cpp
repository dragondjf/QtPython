#include "pythonmanager.h"
#include <QDir>
#include <QDebug>
#include <QJsonObject>
#include <QJsonParseError>

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
    m_ffpython->init("logger", "use qDebug in python");
}

int PythonManager::debug(const string &val_1)
{
    qDebug() << val_1.c_str();
    return 0;
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
    vector<int> a1;
    a1.push_back(100);
    a1.push_back(200);
    list<string> a2;
    a2.push_back("Oh");
    a2.push_back("Nice");
    vector<list<string> > a3;
    a3.push_back(a2);
    const char* ret = m_ffpython->call<string>("main", "returnJson", a1, a2, a3, a3).c_str();
    qDebug() << ret;
    QJsonParseError* error = new QJsonParseError();
    QJsonObject messageObj = QJsonDocument::fromJson(QByteArray(ret), error).object();
    qDebug() << messageObj << error->errorString();
}
