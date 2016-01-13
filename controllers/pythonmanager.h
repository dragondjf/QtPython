#ifndef PYTHONMANAGER_H
#define PYTHONMANAGER_H

#include <QObject>
#include "../thirdparty/ffpython/ffpython.h"

class PythonManager : public QObject
{
    Q_OBJECT
public:
    explicit PythonManager(QObject *parent = 0);
    ~PythonManager();

signals:

public slots:

private:
    ffpython_t* m_ffpython=NULL;
};

#endif // PYTHONMANAGER_H
