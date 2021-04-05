#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>
#include <whycon/CRawImage.h>
#include "CWhyconWrapper.h"

namespace py = pybind11;

typedef unsigned char uint8_t;


class CWhyconMarker {
    public:
        whycon::SSegment segment_in_image;
        whycon::STrackedObject coords;
        CWhyconMarker(const whycon::SMarker marker) {
           segment_in_image = marker.seg;
           coords = marker.obj;
        }
};

typedef std::list<CWhyconMarker> WhyconMarkersList;

class WhycodeAutocalibResult {
    public:
        WhyconMarkersList markers;
        bool saved = false;        
};

class WhyCodeCppPython
{

  public:

    enum trans_type {
        T_NONE  = whycon::TRANSFORM_NONE,  //camera-centric
        T_2D    = whycon::TRANSFORM_2D,      //3D->2D homography
        T_3D    = whycon::TRANSFORM_3D,      //3D user-defined - linear combination of four translation/rotation transforms
        T_4D    = whycon::TRANSFORM_4D,      //3D user-defined - full 4x3 matrix
        T_INV   = whycon::TRANSFORM_INV,    //for testing purposes
        T_NUMBER = whycon::TRANSFORM_NUMBER
    };

    // contructor
    WhyCodeCppPython(
      std::string clib_camera_path,
      std::string clib_space_transform_path,
      float circle_diam,
      int num_markers,
      WhyCodeCppPython::trans_type trans_type = WhyCodeCppPython::trans_type::T_NONE,
      int id_bits = 3,
      int id_samples = 360,
      int hamming_dist = 1,
      bool identify = true,
      bool draw_coords = true,
      bool draw_segments = true,
      bool debug = false  
    ):  detector(
          clib_camera_path, clib_space_transform_path, circle_diam, num_markers, 
          whycon::ETransformType(trans_type), id_bits, id_samples, hamming_dist, identify, draw_coords, draw_segments, debug
        ) {}        

    // desstructor
    ~WhyCodeCppPython() {}

    // wraper python/c++ interface
    WhyconMarkersList detect(py::array_t<uint8_t, py::array::c_style | py::array::forcecast> array) {
      std::vector<whycon::SMarker> markers_list;
      whycon::CRawImage* img = prepare_image(array);
      // --- detect ----
      markers_list = detector.detects(img);
      img->swapRGB();
      return return_results(markers_list);
    }

  
    // wraper python/c++ interface
    WhycodeAutocalibResult detect_and_calibrate(
      py::array_t<uint8_t, py::array::c_style | py::array::forcecast> array, 
      std::string outCalibPath, float fieldLength = 1, float fieldWidth = 1, bool debug = false
    ) {
      WhycodeAutocalibResult py_autocalib_result;
      CAutocalibrationResult autocalib_result;
      whycon::CRawImage* img = prepare_image(array);
      // --- detect and calibrate ----
      autocalib_result = detector.detect_and_calibrate(img, outCalibPath, fieldLength, fieldWidth, debug);
      img->swapRGB();
      py_autocalib_result.saved = autocalib_result.saved;
      py_autocalib_result.markers = return_results(autocalib_result.markers);
      return py_autocalib_result;
    }
    

    private:
      CWhyconWrapper detector;

      whycon::CRawImage* prepare_image(py::array_t<uint8_t, py::array::c_style | py::array::forcecast> array) {
        // --- convert np.ndarray (image with shape NxMx3) to CRawImage ---------------------------------------------------------
        // check input dimensions
        if ( array.ndim()     != 3 )
          throw std::runtime_error("Input should be 3-D NumPy array");
        if ( array.shape()[2] != 3 )
          throw std::runtime_error("Input should have size [N,M,3]");


        // ssize_t ndim = array.ndim();
        auto rows = array.shape()[0];
        auto cols = array.shape()[1];
        auto colors = array.shape()[2];
        auto byte_size = (long int)  sizeof(uint8_t);      

        // allocate std::vector (to pass to the C++ function)
        std::vector<uint8_t> vect(array.size());
        // copy py::array -> std::vector
        std::memcpy(vect.data(),array.data(),array.size()*byte_size);


        std::vector<ssize_t> shape   = { rows , cols, colors };

        // creatw wraper which share data of original vector vect
        whycon::CRawImage* img = new whycon::CRawImage( (unsigned char*) array.data(), cols, rows, colors);
        /*
        whycon::CRawImage* img = img_orig->copy();
        delete img_orig;
        */
        img->swapRGB();
        //show_and_wait(img, false, "C++ Before detect, after swap"); 
        return img;
      }

    // store results to one object
    WhyconMarkersList return_results(std::vector<whycon::SMarker> markers_list) {
      WhyconMarkersList ret_markers_list;
      
      for(auto const& marker: markers_list) {
        CWhyconMarker ret_marker = CWhyconMarker(marker);
        ret_markers_list.push_back(ret_marker);
      }

      /*
        // --- store modified img back to result -------------------------------------------------------------------------------------

        std::vector<ssize_t> strides = { cols * colors * byte_size, colors * byte_size, byte_size };  

        // add 3-D NumPy array to result
        result.img = py::array(py::buffer_info(
          vect.data(),                              // data as contiguous array  
          byte_size,                                // size of one scalar        
          py::format_descriptor<uint8_t>::format(), // data type                 
          ndim,                                     // number of dimensions      
          shape,                                    // shape of the matrix       
          strides                                   // strides for each axis     
        ));

        return result.markers_list.size();
        // return result;
      */

      return ret_markers_list;
    }
};

PYBIND11_MODULE(whycon, m) {
  using namespace pybind11::literals; // for _a literal to define arguments
  m.doc() = "WhyCon is a version of a vision-based localization system that can be used with low-cost web cameras, and achieves millimiter\n"
  "precision with very high performance.\n"
  "It also searches for marker IDs with the \"whycode\" extension.\n\n"
  "See https://github.com/LCAS/whycon, https://github.com/lrse/whycon, https://github.com/jiriUlr/whycon-ros for details and credits.\n\n";

  pybind11::class_<WhyCodeCppPython> whycon_detector ( m,  "WhyCodeDetector", 
    "The detector implements the algorithm of searching markers and ist numeric ID's."
  );
  whycon_detector
    .def(pybind11::init<
        std::string, 
        std::string, 
        float, 
        int, 
        WhyCodeCppPython::trans_type, 
        int, 
        int, 
        int, 
        bool,
        bool,
        bool,
        bool
      >(), "The constructor.",
      py::arg("\n\tcalib_camera_path"), // "path to existing camera calibration file"
      py::arg("\n\tcalib_space_transform_path"), // "path to existing space calibration file"
      py::arg("\n\tcircle_diam"), // default black circle diameter [m];
      py::arg("\n\tnum_markers"), // num of markers to track
      py::arg("\n\ttrans_type"),  // transform type
      py::arg("\n\tid_bits"),     // num of ID id_bits
      py::arg("\n\tid_samples"),  // num of id_samples to identify ID
      py::arg("\n\thamming_dist"),// hamming distance of ID code
      py::arg("\n\tidentify"),    // whether to identify ID
      py::arg("\n\tdraw_coords"), 
      py::arg("\n\tdraw_segments"),
      py::arg("\n\tdebug")       // whether write debug info
    )

    .def(
          "detect", 
          &WhyCodeCppPython::detect,
          "Detect whycon markers in the image (np.ndarray, shape=(W,H,3)) and returns list of found markers (as WhyconMarker object).\n"
          "Tags found markers or highlights they in the image (according to the boolean parameters fill_found and fill_found_highlight)",
          py::arg("\n\timg_array, shape=(width, height,3)")
        //  py::arg("\n\tfill_found - show found markers in the image"),
        //  py::arg("\n\tfill_found_highlight - highlight markers in the image"),
        //  py::arg("\n\tdebug - do you like to write debug info?")         
     )

    .def(
        "detect_and_calibrate",
        &WhyCodeCppPython::detect_and_calibrate,
        "Autocalibration. Searches for 4 outermost circular patterns and uses them to establisht the coordinate system.\n"
        "In the field markers returns last found markes. The fild saved is true after results is saved to file.",
        py::arg("\n\timg_array, shape=(width, height,3)"),
        py::arg("\n\tout_autocalibration_path - path to store result of alibration"),
        py::arg("\n\tfield_height - X dimension of the coordinate system"),
        py::arg("\n\tfield_width - Y dimension of the coordinate system"),
        py::arg("\n\tdebug - do you like to write debug info?")           
    )
    ;

  pybind11::class_<CWhyconMarker> marker (
    m, 
    "WhyconMarker",
    "Object with info about found WhyconMarker"
  );
  marker
    .def_readwrite("segment_in_image", &CWhyconMarker::segment_in_image, "found segment in the image")
    .def_readwrite("coords", &CWhyconMarker::coords, "logical coordinates of found marker")
    ;
    
  
  pybind11::class_<WhycodeAutocalibResult> autocalibration_results (
    m, 
    "WhyconAutocalibResult",
    "Object with list of markers and info about saved result"
  );
  autocalibration_results
    .def_readwrite("markers", &WhycodeAutocalibResult::markers, "found markers in the image")
    .def_readwrite("saved", &WhycodeAutocalibResult::saved, "is result of aotocalibration saved?")
    ;
  
  pybind11::class_<whycon::SSegment> segment (
    m, 
    "WhyconSegment",
    "Object with info about found segment in the image."
  );
  segment
    .def_readwrite("x", &whycon::SSegment::x, "float, center in image coordinates")
    .def_readwrite("y", &whycon::SSegment::y, "float, center in image coordinates")
    // .def_readwrite("angle", &whycon::SSegment::angle, "float, orientation (not really used in this case, see the SwarmCon version of this software)")
    // .def_readwrite("horizontal", &whycon::SSegment::horizontal, "float, orientation (not really used in this case, see the SwarmCon version of this software)")
    .def_readwrite("size", &whycon::SSegment::size, "int, number of pixels")
    .def_readwrite("maxy", &whycon::SSegment::maxy, "int, bounding box dimensions")
    .def_readwrite("miny", &whycon::SSegment::miny, "int, bounding box dimensions")
    .def_readwrite("maxx", &whycon::SSegment::maxx, "int, bounding box dimensions")
    .def_readwrite("minx", &whycon::SSegment::minx, "int, bounding box dimensions")
    .def_readwrite("mean", &whycon::SSegment::mean, "int, mean brightness")
    .def_readwrite("type", &whycon::SSegment::type, "int, black or white ?")
    .def_readwrite("roundness", &whycon::SSegment::roundness, "float roundness, result of the first roundness test, see Eq. 2 of paper [1]")
    .def_readwrite("bwRatio", &whycon::SSegment::bwRatio, "float, ratio of white to black pixels, see Algorithm 2 of paper [1]")
    .def_readwrite("round", &whycon::SSegment::round, "bool, segment passed the initial roundness test")
    .def_readwrite("valid", &whycon::SSegment::valid, "bool, marker passed all tests and will be passed to the transformation phase")
    .def_readwrite("m0", &whycon::SSegment::m0, "float, eigenvalues of the pattern's covariance matrix, see Section 3.3 of [1]")
    .def_readwrite("m1", &whycon::SSegment::m1, "float, eigenvalues of the pattern's covariance matrix, see Section 3.3 of [1]")
    .def_readwrite("v0", &whycon::SSegment::v0, "float, eigenvectors of the pattern's covariance matrix, see Section 3.3 of [1]")
    .def_readwrite("v1", &whycon::SSegment::v1, "float, eigenvectors of the pattern's covariance matrix, see Section 3.3 of [1]")
    .def_readwrite("r0", &whycon::SSegment::r0, "ratio of inner vs outer ellipse dimensions (used to establish ID, see the SwarmCon version of this class)")
    .def_readwrite("r1", &whycon::SSegment::r1, "ratio of inner vs outer ellipse dimensions (used to establish ID, see the SwarmCon version of this class)")
    .def_readwrite("ID", &whycon::SSegment::ID, "pattern ID (experimental, see the SwarmCon version of this class)")
    ;

  pybind11::class_<whycon::STrackedObject> coords (
    m, 
    "WhyconCoords",
    "Object with logical coordinates of found marker."
  );

  coords
    .def_readwrite("u", &whycon::STrackedObject::u, "float, x center in the image coords")
    .def_readwrite("v", &whycon::STrackedObject::v, "float, y center in the image coords")
    .def_readwrite("x", &whycon::STrackedObject::x, "float, x position in the camera coords")
    .def_readwrite("y", &whycon::STrackedObject::y, "float, y position in the camera coords")
    .def_readwrite("z", &whycon::STrackedObject::z, "float, z position in the camera coords")
    .def_readwrite("d", &whycon::STrackedObject::d, "float, position and distance in the camera coords")
    .def_readwrite("pitch", &whycon::STrackedObject::pitch, "float, fixed axis angles")
    .def_readwrite("roll", &whycon::STrackedObject::roll, "float, fixed axis angles")
    .def_readwrite("yaw", &whycon::STrackedObject::yaw, "float, fixed axis angles")
    .def_readwrite("angle", &whycon::STrackedObject::angle, "float, axis angle around marker's surface normal")
    .def_readwrite("n0", &whycon::STrackedObject::n0, "float, marker surface normal pointing from the camera")
    .def_readwrite("n1", &whycon::STrackedObject::n1, "float, marker surface normal pointing from the camera")
    .def_readwrite("n2", &whycon::STrackedObject::n2, "float, marker surface normal pointing from the camera")
    .def_readwrite("qx", &whycon::STrackedObject::qx, "quaternion")
    .def_readwrite("qy", &whycon::STrackedObject::qy, "quaternion")
    .def_readwrite("qz", &whycon::STrackedObject::qz, "quaternion")
    .def_readwrite("qw", &whycon::STrackedObject::qw, "quaternion")
    ;


  py::enum_< WhyCodeCppPython::trans_type>(m, "SpaceTransofmType")
    .value("T_NONE", WhyCodeCppPython::trans_type::T_NONE)
    .value("T_2D", WhyCodeCppPython::trans_type::T_2D)
    .value("T_3D", WhyCodeCppPython::trans_type::T_3D)
    .value("T_4D", WhyCodeCppPython::trans_type::T_4D)
    .value("T_INV", WhyCodeCppPython::trans_type::T_INV)
    .value("T_NUMBER", WhyCodeCppPython::trans_type::T_NUMBER)  
    .export_values();
}

