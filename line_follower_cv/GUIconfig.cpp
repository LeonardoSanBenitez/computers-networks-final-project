/**
 * @brief GUI for adjust the parameters
 * @author Beonardo Benitez
 * g++ GUIconfig.cpp -o main `pkg-config --cflags --libs opencv`
 * ./main
 */

#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

/// Global variables
Mat src, srcGray, filtered, edges, houghLines;

const char *nameFilter = "Unsharpen Mask";
int valueFilterSigma = 10;
int valueFilterWeight = 50;
void _filter(int, void *);

const char *nameCanny = "Canny Lines";
int valueCannyThresh1 = 100;
int valueCannyThresh2 = 150;
void _canny(int, void *);

const char *nameHough = "Hough Lines";
int valueHoughThresh = 150;
void _hough(int, void *);

int main()
{
    src = imread("images/lines_0.jpeg", IMREAD_COLOR);

    if (src.empty()) return -1;

    /// Pass the image to gray
    cvtColor(src, srcGray, COLOR_RGB2GRAY);

    /// Create Trackbars for Unharpen Mask
    namedWindow(nameFilter);
    _filter(0, 0);
    createTrackbar("Adjust sigma (std)", nameFilter, &valueFilterSigma, 255, _filter);
    createTrackbar("Adjust sum weight", nameFilter, &valueFilterWeight, 100, _filter);
    waitKey(0);
    destroyWindow(nameFilter);
    cout << "Choosen sigma: " << valueFilterSigma << "\n";
    cout << "Choosen weight: " << valueFilterWeight << "\n\n";

    /// Create Trackbars for Canny
    namedWindow(nameCanny);
    _canny(0, 0);
    createTrackbar("Adjust theshold 1", nameCanny, &valueCannyThresh1, 255, _canny);
    createTrackbar("Adjust theshold 2", nameCanny, &valueCannyThresh2, 255, _canny);
    waitKey(0);
    destroyWindow(nameCanny);
    cout << "Choosen canny thresh1: " << valueCannyThresh1 << "\n";
    cout << "Choosen canny thresh2: " << valueCannyThresh2 << "\n\n";

    /// Create Trackbars for Hough
    namedWindow(nameHough);
    _hough(0, 0);
    createTrackbar("Adjust theshold", nameHough, &valueHoughThresh, 255, _hough);
    waitKey(0);
    destroyWindow(nameHough);
    cout << "Choosen hough threshold: " << valueHoughThresh << "\n";

    return 0;
}

/**
 * @function
 * @brief Apply Unsharpen Mask
 * @return Nothing, but show the image
 */
void _filter(int, void *)
{
    GaussianBlur(srcGray, filtered, Size(9, 9), (double)valueFilterSigma);
    addWeighted(srcGray, 1 + (valueFilterWeight / 100.0), filtered, -(valueFilterWeight / 100.0), 0, filtered);
    imshow(nameFilter, filtered);
}

/**
 * @function
 * @brief Apply Canny edge detector
 * @return Nothing, but show the image
 */
void _canny(int, void *)
{
    Canny(filtered, edges, valueCannyThresh1, valueCannyThresh2, 3);
    imshow(nameCanny, edges);
}

/**
 * @function 
 * @brief Apply Hough Lines with the given threshold
 * @return Nothing, but show the image
 */
void _hough(int, void *)
{
    vector<Vec2f> s_lines;
    cvtColor(edges, houghLines, COLOR_GRAY2BGR);

    HoughLines(edges, s_lines, 1, CV_PI / 180, valueHoughThresh, 0, 0);

    /// Show the result
    for (size_t i = 0; i < s_lines.size(); i++)
    {
        float r = s_lines[i][0], t = s_lines[i][1];
        double cos_t = cos(t), sin_t = sin(t);
        double x0 = r * cos_t, y0 = r * sin_t;
        double alpha = 1000;

        Point pt1(cvRound(x0 + alpha * (-sin_t)), cvRound(y0 + alpha * cos_t));
        Point pt2(cvRound(x0 - alpha * (-sin_t)), cvRound(y0 - alpha * cos_t));
        line(houghLines, pt1, pt2, Scalar(255, 0, 0), 3, LINE_AA);
    }

    imshow(nameHough, houghLines);
}