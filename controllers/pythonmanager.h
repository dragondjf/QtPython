#ifndef PYTHONMANAGER_H
#define PYTHONMANAGER_H

#include <QObject>
#include <QJsonObject>

using namespace std;

class ffpython_t;

class PythonManager : public QObject
{
    Q_OBJECT
public:
    explicit PythonManager(QObject *parent = 0);
    ~PythonManager();
    static void initPython();
    void registerLogger();
    static int debug(const string& val_1);
    static int info(const string& val_1);
    static int warning(const string& val_1);
    static int error(const string& val_1);
    static int fatal(const string& val_1);
    QJsonObject callPythonApi(const string module, const string method, const string jsonArgs="");
    QJsonObject callPythonApi(const char* module, const char* method, const char* jsonArgs="");
    QJsonObject callPythonApi(const QString& module, const QString& method, const QString& jsonArgs="");
    QJsonObject callPythonApi(const QString& module, const QString& method, const QJsonObject& obj = {});
    void testGetGlobalVar();
    void testSetGlobalVar();
    void testCallModuleMethodNoArgs();
    void testCallModuleMethodWidthArgs();
    void testCallRetunJson();
    void testRegisterClass();
signals:

public slots:

private:
    ffpython_t* m_ffpython=NULL;
};

#endif // PYTHONMANAGER_H
