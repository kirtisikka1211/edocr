import cv2
import numpy as np
from utils.log_config import setup_logger

# initialise loger object
logger = setup_logger(__name__)

class ImagePreprocessor:
    """
    each image from pdf are preprocessed
    """
    def __init__(self, length_threshold: float = 0.7):
        """
        Initializes the image preprocessor with a line length threshold.
        """
        self.length_threshold = length_threshold
    
    def remove_long_lines(self, img: np.ndarray) -> np.ndarray:
        """
        Remove horizontal and vertical lines from the input image.
        :param img: Input image as a NumPy array.
        :return: Preprocessed image with long lines removed.
        """
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Edge detection
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)

            # Detect alll lines using the Hough Line Transform
            lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
            
            # Image dimensions
            img_height, img_width = gray.shape
            mask = np.ones_like(gray) * 255  # Start with a white mask

            if lines is not None:
                for line in lines:
                    for x1, y1, x2, y2 in line:
                        # Check if the line is vertical
                        if abs(x1 - x2) < 5:  # Small tolerance for vertical lines
                            line_length = abs(y2 - y1)
                            if line_length > self.length_threshold * img_height:
                                # Draw the vertical line on the mask (in black)
                                cv2.line(mask, (x1, y1), (x2, y2), 0, thickness=2)
                        elif abs(y1 - y2) < 5:  # Check for horizontal lines (y-coordinates nearly the same)
                                line_length = abs(x2 - x1)
                                if line_length > self.length_threshold * img_width:
                                    # Draw the horizontal line on the mask (in black)
                                    cv2.line(mask, (x1, y1), (x2, y2), 0, thickness=2)

            # Remove the vertical lines from the original image
            result = cv2.inpaint(img, cv2.bitwise_not(mask), inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        except Exception as e:
            raise Exception(str(e))
        return result
    
    def preprocess_images(self, image_list: list[np.ndarray]) -> list[np.ndarray]:
        """
        Apply preprocessing to a list of images.
        :param image_list: List of images as NumPy arrays.
        :return: List of preprocessed images.
        """
        try:
            preprocessed_imgs = [self.remove_long_lines(img) for img in image_list]
        except Exception as e:
            logger.error(f"Error preprocessing images: {str(e)}")
        logger.info("All Images preprocesseed sucessfully")
        return preprocessed_imgs