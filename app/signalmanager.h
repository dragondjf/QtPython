#ifndef SIGNALMANAGER_H
#define SIGNALMANAGER_H

#include <QtCore>

using namespace std;

class ffpython_t;

class SignalManager : public QObject
{
    Q_OBJECT
public:
    explicit SignalManager(QObject *parent = 0);
    ~SignalManager();

    inline static SignalManager* instance(){
        static SignalManager instance;
        return &instance;
    }

    static void registerToPython(ffpython_t& ffpython);

signals:
    void requestObjChanged(const int& v);
    void requestJsonObjChanged(const string& v);
};

#endif // SIGNALMANAGER_H
