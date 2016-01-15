#ifndef SIGNALMANAGER_H
#define SIGNALMANAGER_H

#include <QObject>
class ffpython_t;

class SignalManager : public QObject
{
    Q_OBJECT

public:
    SignalManager();
    ~SignalManager();

    inline static SignalManager* instance(){
        static SignalManager instance;
        return &instance;
    }

    static void registerToPython(ffpython_t& ffpython);
signals:

public slots:
};

#endif // SIGNALMANAGER_H
