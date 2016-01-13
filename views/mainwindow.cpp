#include "mainwindow.h"
#include<QDebug>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    qDebug() << "MainWindow init";
}

MainWindow::~MainWindow()
{

}
