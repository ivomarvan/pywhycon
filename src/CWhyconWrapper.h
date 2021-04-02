/*
 * Author:   ivo@marvan.cz
 */

#ifndef __CPOSITIONDETECTOR_H__
#define __CPOSITIONDETECTOR_H__

#include <stdlib.h>
#include <list>
#include <iostream>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>
#include <whycon/CRawImage.h>
#include <whycon/SStructDefs.h>
#include <whycon/CWhycon.h>

class CAutocalibrationResult {
    public:
        std::vector<whycon::SMarker> markers;
        bool saved = false;        
};

class CWhyconWrapper
{
public:

    CWhyconWrapper(
        std::string clib_camera_path,               // path to existing camera calibration file
        std::string clib_space_transform_path,      // path to existing space calibration file
        float circle_diam,                          // default black circle diameter [m];
        int num_markers=3,                          // num of markers to track
        whycon::ETransformType trans_type=whycon::TRANSFORM_NONE,   // calibation transform type
        int id_bits = 3,                            // num of ID id_bits
        int id_samples = 360,                       // num of id_samples to identify ID
        int hamming_dist = 1,                       // hamming distance of ID code
        bool identify = true,                       // whether to identify ID
        bool draw_coords = true,
        bool draw_segments = true,
        bool debug = false                          // whether write debug info
    );
    ~CWhyconWrapper();
    std::vector<whycon::SMarker> detects(whycon::CRawImage* image);
    CAutocalibrationResult detect_and_calibrate(
        whycon::CRawImage* image, std::string autocalib_space_out_path, float field_length, float field_width, bool debug = false
    );

private:
    whycon::CWhycon detector;
    std::string clib_camera_path;
    std::string clib_space_transform_path;
    float circle_diam;
    int num_markers = 0;		//num of robots to track
    whycon::ETransformType trans_type;
    int id_bits;
    int id_samples;
    int hamming_dist;
    bool identify;          // whether to identify ID
    bool draw_coords;
    bool draw_segments;
    bool debug;
    // --- camera params ---
    cv::Mat intrinsic_mat;         // camera intrinsic matrix
    cv::Mat distortion_coeffs;     // camera distortion parameters

    bool autocali_has_started = false;

    bool initialized = false; // is whole object (with all object which it owns) initialized?

    void init_lean(whycon::CRawImage* image); // initialize if you know size of image
    void read_camera_calib_params();
};


#endif
/* end of CWhyconWrapper.h */

