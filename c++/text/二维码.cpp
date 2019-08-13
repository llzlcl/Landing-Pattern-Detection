#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
using namespace cv;
using namespace std;
void find(Mat &src);
int map_w, map_h, qr_x, qr_y, qr_w, qr_h, angle;
int main()
{
	VideoCapture cap = VideoCapture(0);
	double rate = cap.get(CV_CAP_PROP_FPS);
	int delay = cvRound(1000.000 / rate);
	if (!cap.isOpened())
	{
		return -1;
	}
	else
	{
		while (true)
		{
			Mat frame;
			cap >> frame;
			find(frame);
			imshow("video", frame);
			if (waitKey(20) == 27)//esc¹Ø±Õ
			{
				break;
			}
		}
	}
	return 0;
}
void find(Mat &src)
{
	Mat src_gray;
	Mat src_all = src.clone();
	Mat threshold_output;
	vector<vector<Point>> contours, contours1;
	vector<Point> contours2;
	vector<Vec4i> hierarchy;
	cvtColor(src, src_gray, CV_BGR2GRAY);
	blur(src_gray, src_gray, Size(3, 3));
	imshow("blur", src_gray);
	threshold(src_gray, threshold_output, 100, 255, THRESH_OTSU);
	Mat element = getStructuringElement(MORPH_RECT, Size(2, 2));
	erode(threshold_output, threshold_output, element);
	imshow("bw", threshold_output);
	findContours(threshold_output, contours, hierarchy, CV_RETR_TREE, CHAIN_APPROX_NONE, Point(0, 0));
	for (int i = 0; i < hierarchy.size(); i++)
	{
		int count = 0, k = i;
		while (hierarchy[k][2] != -1)
		{
			count++;
			k = hierarchy[k][2];
		}
		if (count >= 2)
		{
			contours1.push_back(contours[i]);
		}
	}
	if (contours1.size() >= 3)
	{
		for (int i = 0; i < contours1.size(); i++)
		{
			drawContours(src_all, contours1, i, Scalar(0, 255, 0), 3);
			contours2.insert(contours2.end(), contours1[i].begin(), contours1[i].end());
		}
		RotatedRect rect = minAreaRect(contours2);
		Point2f P[4];
		rect.points(P);
		for (int j = 0; j <= 3; j++)
		{
			line(src_all, P[j], P[(j + 1) % 4], Scalar(255), 2);
		}
		Size map;
		//Î»ÖÃ¸³Öµ
		map_h = src.rows, map_w = src.cols, qr_x = rect.center.x, qr_y = rect.center.y,
			qr_w = rect.size.width, qr_h = rect.size.height, angle = rect.angle;
	}
	else
	{
		src_all = src_gray;
	}
	src = src_all;
}
