#include "pythonmanager.h"
#include <QDebug>

PythonManager::PythonManager(QObject *parent) :
    QObject(parent),
    m_ffpython(new ffpython_t)
{
    m_ffpython->add_path("./");
    qDebug() << "PythonManager init";
    qDebug() << m_ffpython->get_global_var<string>("sys", "version").c_str();
}

PythonManager::~PythonManager()
{
    m_ffpython->final_py();
}

