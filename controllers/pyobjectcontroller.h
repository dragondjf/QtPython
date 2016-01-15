#ifndef PYOBJECTCONTROLLER_H
#define PYOBJECTCONTROLLER_H

#include <QObject>

class ffpython_t;

class PyObjectController : public QObject
{
    Q_OBJECT
public:
    explicit PyObjectController(const int obj, QObject *parent = 0);
    ~PyObjectController();

    inline static PyObjectController* instance(int v){
        static PyObjectController instance(v);
        return &instance;
    }

    static void registerToPython(ffpython_t& ffpython);

    int getObj();
    void testStl(int v);
    PyObjectController* getInstance(int v);

signals:

public slots:
    void setObj(int obj);

private:
    int m_obj;
};

#endif // PYOBJECTCONTROLLER_H
