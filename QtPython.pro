#-------------------------------------------------
#
# Project created by QtCreator 2016-01-13T10:24:01
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets


win32 {
    INCLUDEPATH += C:/Python27/include
    LIBS += "C:/Python27/libs/libpython27.a"

    DEFINES += MS_WIN64
}
unix {
    PKGCONFIG += python-2.7
    CONFIG += link_pkgconfig
}

CONFIG += c++11

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





