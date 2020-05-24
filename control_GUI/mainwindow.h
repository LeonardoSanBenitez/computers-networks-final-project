#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:

    void on_buttonAdvance_clicked();
    void on_buttonStop_clicked();
    void on_buttonLeft_clicked();
    void on_buttonRight_clicked();
    void on_buttonSend_clicked();
    void on_buttonReceive_clicked();

    void on_actionAboutUs_triggered();
    void on_actionAboutQt_triggered();
    void on_actionHowTo_triggered();

    void sendFinished(QNetworkReply *reply);
    void receiveFinished(QNetworkReply *reply);


    void on_sliderThreshold_sliderMoved(int position);

private:
    Ui::MainWindow *ui;
    QNetworkAccessManager *managerSend;
    QNetworkRequest requestSend;
    QNetworkAccessManager *managerReceive;
    QNetworkRequest requestReceive;
    int dir=0;
    int mov=0;
    int threshold=0;
};
#endif // MAINWINDOW_H
