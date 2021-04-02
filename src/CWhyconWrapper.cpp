#include "CWhyconWrapper.h"

// @TODO Add parametrs of CWhycon::updateConfiguration to the constructor
CWhyconWrapper::CWhyconWrapper(
    std::string clib_camera_path,
    std::string clib_space_transform_path,
    float circle_diam,  
    int num_markers,
    whycon::ETransformType trans_type,
    int id_bits,
    int id_samples,
    int hamming_dist,
    bool identify,
    bool draw_coords,
    bool draw_segments,
    bool debug
) :
    detector(debug),
    clib_camera_path(clib_camera_path), clib_space_transform_path(clib_space_transform_path), circle_diam(circle_diam),
    num_markers(num_markers), trans_type(trans_type), id_bits(id_bits), id_samples(id_samples), 
    hamming_dist(hamming_dist), identify(identify), draw_coords(draw_coords), draw_segments(draw_segments), debug(debug),     
    intrinsic_mat(cv::Mat::eye(3,3, CV_32FC1)),
    distortion_coeffs(cv::Mat::zeros(1,5, CV_32FC1)),
    autocali_has_started(false)
    {
        read_camera_calib_params();
    }



CWhyconWrapper::~CWhyconWrapper() {}

void CWhyconWrapper::read_camera_calib_params() {
    if (debug) std::cout << "CWhyconWrapper::read_camera_calib_params filename:" << clib_camera_path << std::endl;
   
    cv::FileStorage fs(clib_camera_path, cv::FileStorage::READ);
    if (!fs.isOpened()) {
        std::cerr << "failed to open " << clib_camera_path << std::endl;
        exit(1);
    }
    std::string camera_id;
    
    fs["camera_id"] >> camera_id;
    fs["intrinsic"] >> intrinsic_mat;
    fs["distortion"] >> distortion_coeffs;

    if (debug) {
        std::cout << "reading intrinsic and distortion" << std::endl;
        std::cout << "camera_id = " << camera_id << "\n";
        std::cout << "intrinsic = " << intrinsic_mat << "\n";
        std::cout << "distortion = " << distortion_coeffs << std::endl;
    }
}

// initialize if you know size of image 
void CWhyconWrapper::init_lean(whycon::CRawImage* image) {
    if (initialized) return;
    initialized = true;
    // init(float circle_diam, bool use_gui, int id_b, int id_s, int ham_dist, int markers, bool identify, int img_w, int img_h);
    detector.init(circle_diam, false, id_bits, id_samples, hamming_dist, num_markers, identify,  image->width_, image->height_);
    // @TODO: detector.loadCalibration(clib_space_transform_path);
    detector.updateCameraInfo(intrinsic_mat, distortion_coeffs);
    detector.setDrawing(draw_coords, draw_segments);
    detector.setCoordinates(trans_type);
    detector.loadCalibration(clib_space_transform_path);
    if (debug) {    
        printf("\nDBG: clib_camera_path: %s\n", clib_camera_path.c_str());
        printf("DBG: clib_space_transform_path: %s\n", clib_space_transform_path.c_str());
        printf("DBG: circle_diam: %f\n", circle_diam);
        printf("DBG: num_markers: %d\n", num_markers);
        printf("DBG: trans_type: %d\n", (int) trans_type);
        printf("DBG: id_bits: %d\n", id_bits);
        printf("DBG: id_samples: %d\n", id_samples);
        printf("DBG: hamming_dist: %d\n", hamming_dist);
        printf("DBG: identify: %s\n", identify ? "true" : "false");
        printf("DBG: draw_coords: %s\n", draw_coords ? "true" : "false");
        printf("DBG: draw_segments: %s\n", draw_segments ? "true" : "false");
        printf("DBG: initialized: %s\n", initialized ? "true" : "false");
        //std::cout << "detector" << detector << std::endl;
    }
}

std::vector<whycon::SMarker> CWhyconWrapper::detects(whycon::CRawImage* image)
{   
    init_lean(image);
    std::vector<whycon::SMarker> markers;
    detector.processImage(image, markers);
    return markers;
}

// Entry point for autocalibration
CAutocalibrationResult CWhyconWrapper::detect_and_calibrate(
    whycon::CRawImage* image, std::string autocalib_space_out_path, float field_length, float field_width, bool idebug
) { 
    CAutocalibrationResult autocalibration_result;

    init_lean(image);
    detector.debug = idebug;
    detector.field_length_ = field_length;
    detector.field_width_ = field_width;
    if (not autocali_has_started) {
        try {
            detector.autocalibration();  // Sets autocalibration_result.saved = True (until autocalibration is not done).
            autocalibration_result.saved = false;
            autocali_has_started = true;
        } catch(const std::exception& e) {
            // wait to find 4 markers
            autocali_has_started = false;
        }
    }
    detector.processImage(image, autocalibration_result.markers);
    if (autocali_has_started and (not detector.autocalibrate_)) {
            std::cout << "Write calibration result to " << autocalib_space_out_path <<  std::endl;
            detector.saveCalibration(autocalib_space_out_path);
            autocalibration_result.saved = true;
    }
    return autocalibration_result;
}
