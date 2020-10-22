/*
To compile: g++ main.cpp -o main `pkg-config --cflags --libs opencv`
To execute: ./main
TODO: OS ANGULOS PODEM SER NEGATIVOS... X&&X || Y&&Y
*/
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
using namespace cv;
using namespace std;

string decideMovement(Mat dst, Mat cdst, string filename,  int verbose=1);

int main(int argc, char **argv){
    // Declare the output variables
    Mat dst, cdst;
    string result;

    
    // filename list
    for (int i=0; i<=7; i++){
        cout << "Image " + to_string(i) << "\n";
        result = decideMovement(dst, cdst, "assets/lines_" + to_string(i) + ".jpeg", 0);

        cout << result << "\n";
        cout << "-----------------" << "\n\n";
    }

    

    return 0;
}

string decideMovement(Mat dst, Mat cdst, string filename, int verbose){
    int left = 0, right = 0, center = 0;

    Mat src = imread(filename, IMREAD_GRAYSCALE);
    if (src.empty()) return(" Error opening image\n");

    Canny(src, dst, 100, 150, 3); // Edge detection
    cvtColor(dst, cdst, COLOR_GRAY2BGR); // Copy edges to the images that will display the results in BGR
    vector<Vec2f> lines;                              // will hold the results of the detection
    HoughLines(dst, lines, 1, CV_PI / 180, 50, 1, 1); // runs the actual detection
    
    /// Draw the lines
    for (size_t i = 0; i < lines.size(); i++)
    {
        float rho = lines[i][0];
        float theta = lines[i][1];
        if ((theta > -0.261799 && theta < 0.261799) || (theta > 2.87979 && theta < 3.40339))
        {
            //0+-15º or 180+-15º
            center++;
        }
        else if ((theta > 0.523599 && theta < 1.0472) || (theta < -2.0944 && theta > -2.61799))
        {
            //45+-15º or -135+-15º
            right++;
        }
        else if ((theta > 2.0944 && theta < 2.61799) || (theta < -0.523599 && theta > -1.0472))
        {
            //135+-15º or -45+-15º
            left++;
        }

        if (verbose>=1){
            cout << "rho = " << rho << ", theta = " << theta << "\n";
            Point pt1, pt2;
            double a = cos(theta), b = sin(theta);
            double x0 = a * rho, y0 = b * rho;
            pt1.x = cvRound(x0 + 1000 * (-b));
            pt1.y = cvRound(y0 + 1000 * (a));
            pt2.x = cvRound(x0 - 1000 * (-b));
            pt2.y = cvRound(y0 - 1000 * (a));
            line(cdst, pt1, pt2, Scalar(0, 0, 255), 3, LINE_AA);
        }
    }

    if (verbose>=1){
        // Show results
        imshow("Detected Lines (in red)", cdst);
        cout << left << " - " << center << " - " << right << "\n";
        waitKey();
    }
    
    if (left > right && left > center)
    {
        return ("turn left");
    }
    else if (right > left && right > center)
    {
        return ("turn right");
    }
    else
    {
        return ("keep straight");
    }
}
