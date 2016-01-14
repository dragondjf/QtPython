#include "mainwindow.h"
#include <QDebug>
#include <QApplication>
#include <QDesktopWidget>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    qDebug() << "MainWindow init";
    resize(800, 600);
    moveCenter();
    setWindowIcon(QIcon(":/images/skin/images/qtpython.png"));
}

void MainWindow::moveCenter(){
    QRect qr = frameGeometry();
    QPoint cp;
    if (parent()){
        cp = static_cast<QWidget*>(parent())->geometry().center();
    }else{
        cp = qApp->desktop()->availableGeometry().center();
    }
    qr.moveCenter(cp);
    move(qr.topLeft());
}

MainWindow::~MainWindow()
{

}
