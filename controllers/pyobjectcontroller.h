#ifndef PYOBJECTCONTROLLER_H
#define PYOBJECTCONTROLLER_H

#include <QObject>

class ffpython_t;

class PyObjectController : public QObject
{
    Q_OBJECT
public:
    explicit PyObjectController(const int& v, QObject *parent = 0);
    ~PyObjectController();

    inline static PyObjectController* instance(int v){
        static PyObjectController instance(v);
        return &instance;
    }

    static void registerToPython(ffpython_t& ffpython);

    Q_INVOKABLE int getObj();
    Q_INVOKABLE void testStl(int v);
    Q_INVOKABLE PyObjectController* getInstance(int v);

signals:

public slots:
    void setObj(int obj);

private:
    int m_obj;
};

#endif // PYOBJECTCONTROLLER_H
