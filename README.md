# VEX IQ Object Scanner

A VEX IQ robotics project that uses rotational scanning to detect, analyze, and display objects within its scanning field. The system automatically identifies object shape, orientation, and color, then renders the results on the IQ Brain's screen.

## Overview

This project creates an automated object detection system using a VEX IQ Brain Gen 2 with a rotating scanner arm. The scanner performs a 360-degree sweep around objects, collecting distance and color data to reconstruct and display the object's characteristics.

## Hardware Requirements

### VEX IQ Components
- **VEX IQ Brain Gen 2** - Main controller and display unit
- **Motor** (Port 5) - Drives the rotating scanner arm
- **Distance Sensor** (Port 6) - Measures object distances during scan
- **Optical Sensor** (Port 1) - Detects object colors during scan
- **Inertial Sensor** - Used for random seed generation
- **254mm 2x20 Beam** - Forms the diameter of the scanner arm assembly

### Physical Setup
- Scanner arm radius: 127mm (half of the 254mm beam diameter)
- Angular resolution: 18 degrees per measurement (20 data points per full rotation)
- Scanning range: 360 degrees around the object

## Features

### Object Detection
- **Shape Recognition**: Converts polar coordinate measurements to rectangular coordinates to determine object outline
- **Color Detection**: Analyzes hue values to identify primary object colors (Red, Yellow, Green, Cyan, Blue)
- **Size Scaling**: Automatically scales detected objects to fit the Brain's 160x108 pixel display
- **Orientation Mapping**: Maintains spatial relationships and object orientation during display

### Display Capabilities
- Real-time shape rendering with filled polygons
- Color-coded object display matching detected hue
- Automatic centering and scaling for optimal viewing
- Clean wireframe outline with color fill using scanline polygon fill algorithm

### User Interface
- **Left Button**: Return scanner arm to initial position
- **Right Button**: Start new scanning sequence
- **Visual Feedback**: Shows scanning progress and countdown timers
- **Menu System**: Simple navigation between scanning and positioning modes

## How It Works

### Scanning Process
1. **Initialization**: Scanner arm moves to starting position
2. **Data Collection**: Performs 20-step rotation (18° increments) collecting:
   - Distance measurements from Distance Sensor
   - Color hue values from Optical Sensor
   - Angular position data from Motor encoder
3. **Processing**: Converts polar coordinates to rectangular coordinates
4. **Rendering**: Displays reconstructed object with detected color

### Coordinate Transformation
- Subtracts distance measurements from arm radius to get object coordinates
- Converts polar coordinates (distance, angle) to Cartesian coordinates (x, y)
- Calculates object centroid and centers it on screen
- Applies uniform scaling to fit display dimensions while maintaining aspect ratio

### Color Analysis
- Averages hue values across all measurement points
- Maps hue ranges to primary colors:
  - Red: 300°-360° and 0°-30°
  - Yellow: 30°-75°
  - Green: 75°-140°
  - Cyan: 140°-210°
  - Blue: 210°-300°

## Software Architecture

### Main Functions
- `test()`: Main program loop handling user input and scanning sequence
- `polar_rect_coord_conv()`: Coordinate transformation and scaling
- `scanline_poly_fill()`: Advanced polygon fill algorithm for object rendering
- `convert_hue_to_color()`: Color classification from hue analysis
- `print_shape()`: Display rendering and visualization

### Data Structures
- `distance_vals[20]`: Distance measurements for each scan point
- `color_vals[20]`: Hue values for each scan point  
- `angle_dist_record[20]`: Angular positions in radians
- `scaled_coords[]`: Final screen coordinates for display

## Usage Instructions

1. **Setup**: Position object within scanner arm reach (< 127mm from center)
2. **Power On**: Start VEX IQ Brain with program loaded
3. **Menu Navigation**:
   - Press **Left Button** to return arm to home position
   - Press **Right Button** to begin scanning sequence
4. **Scanning**: Wait for automatic scan completion (approximately 10-15 seconds)
5. **Results**: View detected object shape, size, and color on screen
6. **Repeat**: Return to menu for additional scans

## Technical Specifications

- **Scanning Resolution**: 20 data points per 360° rotation
- **Angular Precision**: 18° increments
- **Color Detection**: HSV hue-based classification
- **Display Resolution**: 160x108 pixels
- **Coordinate System**: Polar to Cartesian conversion with centroid alignment
- **Rendering**: Scanline polygon fill with anti-aliasing

## File Structure

```
VexObjectScanner/
├── ObjectScanner.py          # Main program file
├── README.md                 # Project documentation
└── VEXcode Spinn Project-1.iqpython  # VEXcode project file
```

## Development Environment

- **Platform**: VEXcode IQ (Python)
- **Language**: Python 3.x with VEX IQ libraries
- **Dependencies**: 
  - `vex` - VEX IQ hardware interface library
  - `math` - Mathematical functions for coordinate conversion
  - `urandom` - Random number generation for sensor calibration

## Future Enhancements

- Multiple object detection and tracking
- Enhanced color palette recognition
- 3D visualization capabilities
- Object classification and identification
- Data logging and analysis features

## License

This project is developed for educational and competition use with VEX IQ robotics systems.

## Contributors

Created for VEX IQ robotics competitions and educational demonstrations.