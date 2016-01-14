#include "logmanager.h"
#include <Logger.h>
#include <ConsoleAppender.h>
#include <RollingFileAppender.h>

LogManager::LogManager()
{
    m_format = "%{time}{yyyy-MM-dd HH:mm:ss.zzz} [%{Type:7}] [%{file:-25} %{line}] %{message}\n";
}

void LogManager::initConsoleAppender(){
    m_consoleAppender = new ConsoleAppender;
    m_consoleAppender->setFormat(m_format);
    logger->registerAppender(m_consoleAppender);
}

void LogManager::initPythonCategoryAppender()
{
    m_pythonCategoryAppender = new ConsoleAppender();
    m_pythonCategoryAppender->setFormat("%{message}\n");
    logger->registerCategoryAppender("python", m_pythonCategoryAppender);
}

void LogManager::initRollingFileAppender(){
    QString cachePath = QStandardPaths::standardLocations(QStandardPaths::CacheLocation).at(0);
    if (!QDir(cachePath).exists()){
        QDir(cachePath).mkpath(cachePath);
    }
    m_logPath = joinPath(cachePath, QString("%1.log").arg(qApp->applicationName()));
    m_rollingFileAppender = new RollingFileAppender(m_logPath);
    m_rollingFileAppender->setFormat(m_format);
    m_rollingFileAppender->setLogFilesLimit(5);
    m_rollingFileAppender->setDatePattern(RollingFileAppender::DailyRollover);
    logger->registerAppender(m_rollingFileAppender);

    m_pythonCategoryRollingFileAppender = new RollingFileAppender(m_logPath);
    m_pythonCategoryRollingFileAppender->setFormat("%{message}\n");
    m_pythonCategoryRollingFileAppender->setLogFilesLimit(5);
    m_pythonCategoryRollingFileAppender->setDatePattern(RollingFileAppender::DailyRollover);
    logger->registerCategoryAppender("python", m_pythonCategoryRollingFileAppender);
}

void LogManager::debug_log_console_on(){
    #if !defined(QT_NO_DEBUG)
    LogManager::instance()->initConsoleAppender();
    LogManager::instance()->initPythonCategoryAppender();
    #endif
    LogManager::instance()->initRollingFileAppender();
}


QString LogManager::joinPath(const QString &path, const QString &fileName){
    QString separator(QDir::separator());
    return QString("%1%2%3").arg(path, separator, fileName);
}


QString LogManager::getlogFilePath(){
    return m_logPath;
}

LogManager::~LogManager()
{

}
