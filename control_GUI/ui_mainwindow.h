/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.9.7
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QCommandLinkButton>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionAboutUs;
    QAction *actionAboutQt;
    QAction *actionHowTo;
    QAction *actionSet_root_IP;
    QAction *actionSet_robot_exploration_radius;
    QAction *actionSet_robot_whatever;
    QAction *actionChange_interface_color;
    QAction *actionChange_interface_language;
    QWidget *centralwidget;
    QPushButton *buttonStop;
    QPushButton *buttonAdvance;
    QPushButton *buttonRight;
    QPushButton *buttonLeft;
    QSlider *sliderThreshold;
    QFrame *line;
    QCommandLinkButton *buttonSend;
    QCommandLinkButton *buttonReceive;
    QLabel *image;
    QLabel *label;
    QStatusBar *statusbar;
    QMenuBar *menubar;
    QMenu *menuAbout;
    QMenu *menuconfiguration;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(382, 281);
        actionAboutUs = new QAction(MainWindow);
        actionAboutUs->setObjectName(QStringLiteral("actionAboutUs"));
        actionAboutQt = new QAction(MainWindow);
        actionAboutQt->setObjectName(QStringLiteral("actionAboutQt"));
        actionHowTo = new QAction(MainWindow);
        actionHowTo->setObjectName(QStringLiteral("actionHowTo"));
        actionSet_root_IP = new QAction(MainWindow);
        actionSet_root_IP->setObjectName(QStringLiteral("actionSet_root_IP"));
        actionSet_robot_exploration_radius = new QAction(MainWindow);
        actionSet_robot_exploration_radius->setObjectName(QStringLiteral("actionSet_robot_exploration_radius"));
        actionSet_robot_whatever = new QAction(MainWindow);
        actionSet_robot_whatever->setObjectName(QStringLiteral("actionSet_robot_whatever"));
        actionChange_interface_color = new QAction(MainWindow);
        actionChange_interface_color->setObjectName(QStringLiteral("actionChange_interface_color"));
        actionChange_interface_language = new QAction(MainWindow);
        actionChange_interface_language->setObjectName(QStringLiteral("actionChange_interface_language"));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QStringLiteral("centralwidget"));
        buttonStop = new QPushButton(centralwidget);
        buttonStop->setObjectName(QStringLiteral("buttonStop"));
        buttonStop->setGeometry(QRect(150, 190, 75, 23));
        buttonAdvance = new QPushButton(centralwidget);
        buttonAdvance->setObjectName(QStringLiteral("buttonAdvance"));
        buttonAdvance->setGeometry(QRect(150, 150, 75, 23));
        buttonRight = new QPushButton(centralwidget);
        buttonRight->setObjectName(QStringLiteral("buttonRight"));
        buttonRight->setGeometry(QRect(230, 170, 75, 23));
        buttonLeft = new QPushButton(centralwidget);
        buttonLeft->setObjectName(QStringLiteral("buttonLeft"));
        buttonLeft->setGeometry(QRect(70, 170, 75, 23));
        sliderThreshold = new QSlider(centralwidget);
        sliderThreshold->setObjectName(QStringLiteral("sliderThreshold"));
        sliderThreshold->setGeometry(QRect(20, 160, 22, 61));
        sliderThreshold->setOrientation(Qt::Vertical);
        line = new QFrame(centralwidget);
        line->setObjectName(QStringLiteral("line"));
        line->setGeometry(QRect(0, 120, 411, 20));
        line->setFrameShape(QFrame::HLine);
        line->setFrameShadow(QFrame::Sunken);
        buttonSend = new QCommandLinkButton(centralwidget);
        buttonSend->setObjectName(QStringLiteral("buttonSend"));
        buttonSend->setGeometry(QRect(300, 200, 81, 41));
        buttonReceive = new QCommandLinkButton(centralwidget);
        buttonReceive->setObjectName(QStringLiteral("buttonReceive"));
        buttonReceive->setGeometry(QRect(0, 80, 91, 41));
        image = new QLabel(centralwidget);
        image->setObjectName(QStringLiteral("image"));
        image->setGeometry(QRect(26, 2, 331, 81));
        label = new QLabel(centralwidget);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(10, 140, 47, 13));
        MainWindow->setCentralWidget(centralwidget);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QStringLiteral("statusbar"));
        MainWindow->setStatusBar(statusbar);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QStringLiteral("menubar"));
        menubar->setGeometry(QRect(0, 0, 382, 21));
        menuAbout = new QMenu(menubar);
        menuAbout->setObjectName(QStringLiteral("menuAbout"));
        menuconfiguration = new QMenu(menubar);
        menuconfiguration->setObjectName(QStringLiteral("menuconfiguration"));
        MainWindow->setMenuBar(menubar);

        menubar->addAction(menuAbout->menuAction());
        menubar->addAction(menuconfiguration->menuAction());
        menuAbout->addAction(actionHowTo);
        menuAbout->addAction(actionAboutQt);
        menuAbout->addAction(actionAboutUs);
        menuconfiguration->addAction(actionSet_root_IP);
        menuconfiguration->addAction(actionSet_robot_exploration_radius);
        menuconfiguration->addAction(actionSet_robot_whatever);
        menuconfiguration->addSeparator();
        menuconfiguration->addAction(actionChange_interface_color);
        menuconfiguration->addAction(actionChange_interface_language);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", Q_NULLPTR));
        actionAboutUs->setText(QApplication::translate("MainWindow", "About us", Q_NULLPTR));
        actionAboutQt->setText(QApplication::translate("MainWindow", "About Qt", Q_NULLPTR));
        actionHowTo->setText(QApplication::translate("MainWindow", "How to", Q_NULLPTR));
        actionSet_root_IP->setText(QApplication::translate("MainWindow", "Set robot IP", Q_NULLPTR));
        actionSet_robot_exploration_radius->setText(QApplication::translate("MainWindow", "Set robot exploration radius", Q_NULLPTR));
        actionSet_robot_whatever->setText(QApplication::translate("MainWindow", "Set robot whatever", Q_NULLPTR));
        actionChange_interface_color->setText(QApplication::translate("MainWindow", "Change interface color", Q_NULLPTR));
        actionChange_interface_language->setText(QApplication::translate("MainWindow", "Change interface language", Q_NULLPTR));
        buttonStop->setText(QApplication::translate("MainWindow", "Stop", Q_NULLPTR));
        buttonAdvance->setText(QApplication::translate("MainWindow", "Advance", Q_NULLPTR));
        buttonRight->setText(QApplication::translate("MainWindow", "Turn Right", Q_NULLPTR));
        buttonLeft->setText(QApplication::translate("MainWindow", "Turn Left", Q_NULLPTR));
        buttonSend->setText(QApplication::translate("MainWindow", "Send", Q_NULLPTR));
        buttonReceive->setText(QApplication::translate("MainWindow", "Receive", Q_NULLPTR));
        image->setText(QString());
        label->setText(QApplication::translate("MainWindow", "Theshold", Q_NULLPTR));
        menuAbout->setTitle(QApplication::translate("MainWindow", "Help", Q_NULLPTR));
        menuconfiguration->setTitle(QApplication::translate("MainWindow", "Configurations", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
