#-------------------------------------------------
#
# Project created by QtCreator 2016-01-13T10:24:01
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

PKGCONFIG += python-2.7
CONFIG += c++11 link_pkgconfig

TARGET = QtPython
TEMPLATE = app

DEFINES += QT_MESSAGELOGCONTEXT

include(./thirdparty/cutelogger/cutelogger.pri)
include(./thirdparty/ffpython/ffpython.pri)
include(./thirdparty/utils/utils.pri)

HEADERS += \
    views/mainwindow.h \
    controllers/pythonmanager.h \
    controllers/pyobjectcontroller.h \
    app/global.h \
    app/signalmanager.h

SOURCES += \
    views/mainwindow.cpp \
    main.cpp \
    controllers/pythonmanager.cpp \
    controllers/pyobjectcontroller.cpp \
    app/signalmanager.cpp

DISTFILES += \
    main.py

RESOURCES += \
    skin.qrc





