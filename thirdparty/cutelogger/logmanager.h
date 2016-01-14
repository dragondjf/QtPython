#ifndef LOGMANAGER_H
#define LOGMANAGER_H

#include <QtCore>

class ConsoleAppender;
class RollingFileAppender;

class LogManager
{
public:
    void initConsoleAppender();
    void initPythonCategoryAppender();
    void initRollingFileAppender();

    inline static LogManager* instance(){
        static LogManager instance;
        return &instance;
    }

    void debug_log_console_on();
    QString joinPath(const QString& path, const QString& fileName);
    QString getlogFilePath();

signals:

public slots:

private:
    QString m_format;
    QString m_logPath;
    ConsoleAppender* m_consoleAppender;
    ConsoleAppender* m_pythonCategoryAppender;
    RollingFileAppender* m_rollingFileAppender;
    RollingFileAppender* m_pythonCategoryRollingFileAppender;


    explicit LogManager();
    ~LogManager();
    LogManager(const LogManager &);
    LogManager & operator = (const LogManager &);
};

#endif // LOGMANAGER_H
