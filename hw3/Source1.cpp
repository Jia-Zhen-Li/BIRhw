#include<stdio.h>

int main() {
	file_name = "img1.jpg"
	Mat img = imread(file_name)
	Vec3b intensity = img.at<Vec3b>(y, x);
	uchar blue = intensity.val[0];
	uchar green = intensity.val[1];
	uchar red = intensity.val[2];

	return 0;
}