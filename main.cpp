#include "views/mainwindow.h"
#include "logmanager.h"
#include "controllers/pythonmanager.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    LogManager::instance()->debug_log_console_on();
    MainWindow w;
    w.show();
    PythonManager pythonManager;
    return a.exec();
}
