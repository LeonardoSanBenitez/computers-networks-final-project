#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QPixmap>
#include <QDebug>
#include <QMessageBox>


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    //Image
    QPixmap pix(":/assets/last_image.jpg");
    int w = ui->image->width();
    int h = ui->image->height();
    ui->image->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));

    //Network manager
    managerSend = new QNetworkAccessManager();
    QObject::connect(managerSend, SIGNAL(finished(QNetworkReply*)),
                     this, SLOT(sendFinished(QNetworkReply*)));
    managerReceive = new QNetworkAccessManager();
    QObject::connect(managerReceive, SIGNAL(finished(QNetworkReply*)),
                     this, SLOT(receiveFinished(QNetworkReply*)));
}

MainWindow::~MainWindow()
{
    delete ui;
    delete managerSend;
}

/************************/
/* Robot control over network*/
void MainWindow::on_buttonSend_clicked()
{
    QString url = "http://google.com";//raspberry server
    url += "?dir=" + QString::number(dir);
    url += "&mov=" + QString::number(mov);
    url += "&thresh=" + QString::number(threshold);
    qDebug() << "Requesting to " << url;
    requestSend.setUrl(QUrl(url));
    managerSend->get(requestSend);
}

void MainWindow::sendFinished (QNetworkReply *reply) {
            if (reply->error()) {
                qDebug() << "Error: " << reply->errorString();
                return;
            }
            QString answer = reply->readAll();
            qDebug() << "Response: " << answer << "\n";
            dir=0;
            mov=0;
            threshold=0;
}

void MainWindow::on_buttonReceive_clicked()
{
    QString url = "http://google.com";//raspberry server
    url += "/update_image";
    qDebug() << "Requesting to " << url;
    requestReceive.setUrl(QUrl(url));
    managerReceive->get(requestReceive);
}

void MainWindow::receiveFinished (QNetworkReply *reply) {
            if (reply->error()) {
                qDebug() << "Error: " << reply->errorString();
                return;
            }
            QString answer = reply->readAll();
            qDebug() << "Response: " << answer << "\n";
            //TODO: save image response to disk
            ui->image->update();
}

/************************/
/* Menus and interface */
void MainWindow::on_buttonAdvance_clicked(){
    mov=1;
}
void MainWindow::on_buttonStop_clicked(){
    mov=-1;
}

void MainWindow::on_buttonRight_clicked(){
    dir=1;
}

void MainWindow::on_buttonLeft_clicked(){
    dir=-1;
}
void MainWindow::on_sliderThreshold_sliderMoved(int position)
{
    threshold = position;
}
void MainWindow::on_actionAboutUs_triggered()
{
    QMessageBox::about(this, "About us", "We are students at IFSC. \nThat all.");
}

void MainWindow::on_actionAboutQt_triggered()
{
    QMessageBox::aboutQt(this);
}

void MainWindow::on_actionHowTo_triggered()
{
    QMessageBox::StandardButton reply = QMessageBox::information(this,
                                                           "About this software",
                                                           "I could help... but it would be better if you learn by yourself!\nWas this dialog useful?",
                                                           QMessageBox::Yes | QMessageBox::No);
    if (reply==QMessageBox::Yes){
        qDebug() << "User liked the information :)";
    } else {
        qDebug() << "User didnt liked :(";
    }
}
