"""Image quality analysis for barcode detection."""

import cv2
import numpy as np
from typing import Dict, List, Tuple
from .logger import get_logger

logger = get_logger(__name__)


class ImageQualityAnalyzer:
    """Analyze image quality for barcode detection."""
    
    # Quality thresholds
    MIN_RESOLUTION = (300, 300)  # Minimum recommended resolution
    MIN_CONTRAST = 0.3  # Minimum contrast score
    MIN_SHARPNESS = 0.4  # Minimum sharpness score
    MAX_NOISE = 0.6  # Maximum acceptable noise level
    
    def __init__(self, image: np.ndarray):
        """
        Initialize analyzer with image.
        
        Args:
            image: Input image as numpy array
        """
        self.image = image
        self.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        self.height, self.width = self.gray.shape[:2]
    
    def analyze(self) -> Dict:
        """
        Perform comprehensive quality analysis.
        
        Returns:
            Dictionary with analysis results and recommendations
        """
        logger.debug("Starting image quality analysis")
        
        results = {
            'resolution': self._check_resolution(),
            'contrast': self._check_contrast(),
            'sharpness': self._check_sharpness(),
            'noise': self._check_noise(),
            'brightness': self._check_brightness()
        }
        
        # Calculate overall quality score (0-1)
        scores = [
            results['resolution']['score'],
            results['contrast']['score'],
            results['sharpness']['score'],
            1.0 - results['noise']['score'],  # Invert noise (lower is better)
            results['brightness']['score']
        ]
        results['overall_score'] = sum(scores) / len(scores)
        results['overall_quality'] = self._get_quality_rating(results['overall_score'])
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        results['issues'] = self._get_issues(results)
        
        logger.info(f"Quality analysis complete: {results['overall_quality']} ({results['overall_score']:.2f})")
        
        return results
    
    def _check_resolution(self) -> Dict:
        """Check image resolution."""
        score = 1.0
        status = "good"
        message = f"Resolution: {self.width}x{self.height}"
        
        if self.width < self.MIN_RESOLUTION[0] or self.height < self.MIN_RESOLUTION[1]:
            score = 0.5
            status = "low"
            message += f" (recommended: {self.MIN_RESOLUTION[0]}x{self.MIN_RESOLUTION[1]} or higher)"
        
        return {
            'score': score,
            'status': status,
            'message': message,
            'width': self.width,
            'height': self.height
        }
    
    def _check_contrast(self) -> Dict:
        """Check image contrast using standard deviation."""
        std_dev = np.std(self.gray)
        # Normalize to 0-1 range (assuming 8-bit image)
        contrast_score = min(std_dev / 64.0, 1.0)
        
        if contrast_score >= 0.6:
            status = "good"
        elif contrast_score >= self.MIN_CONTRAST:
            status = "moderate"
        else:
            status = "low"
        
        return {
            'score': contrast_score,
            'status': status,
            'message': f"Contrast: {status} ({contrast_score:.2f})",
            'std_dev': float(std_dev)
        }
    
    def _check_sharpness(self) -> Dict:
        """Check image sharpness using Laplacian variance."""
        laplacian = cv2.Laplacian(self.gray, cv2.CV_64F)
        variance = laplacian.var()
        
        # Normalize to 0-1 range
        sharpness_score = min(variance / 500.0, 1.0)
        
        if sharpness_score >= 0.7:
            status = "sharp"
        elif sharpness_score >= self.MIN_SHARPNESS:
            status = "moderate"
        else:
            status = "blurry"
        
        return {
            'score': sharpness_score,
            'status': status,
            'message': f"Sharpness: {status} ({sharpness_score:.2f})",
            'variance': float(variance)
        }
    
    def _check_noise(self) -> Dict:
        """Check image noise level."""
        # Use median filter to estimate noise
        median = cv2.medianBlur(self.gray, 5)
        noise = np.abs(self.gray.astype(float) - median.astype(float))
        noise_level = np.mean(noise) / 255.0
        
        if noise_level <= 0.1:
            status = "low"
        elif noise_level <= self.MAX_NOISE:
            status = "moderate"
        else:
            status = "high"
        
        return {
            'score': noise_level,
            'status': status,
            'message': f"Noise: {status} ({noise_level:.2f})",
            'level': float(noise_level)
        }
    
    def _check_brightness(self) -> Dict:
        """Check image brightness."""
        mean_brightness = np.mean(self.gray) / 255.0
        
        # Optimal brightness is around 0.4-0.6
        if 0.4 <= mean_brightness <= 0.6:
            score = 1.0
            status = "optimal"
        elif 0.3 <= mean_brightness <= 0.7:
            score = 0.8
            status = "acceptable"
        elif mean_brightness < 0.3:
            score = 0.5
            status = "too_dark"
        else:
            score = 0.5
            status = "too_bright"
        
        return {
            'score': score,
            'status': status,
            'message': f"Brightness: {status} ({mean_brightness:.2f})",
            'mean': float(mean_brightness)
        }
    
    def _get_quality_rating(self, score: float) -> str:
        """Convert score to quality rating."""
        if score >= 0.8:
            return "excellent"
        elif score >= 0.6:
            return "good"
        elif score >= 0.4:
            return "fair"
        else:
            return "poor"
    
    def _get_issues(self, results: Dict) -> List[str]:
        """Get list of quality issues."""
        issues = []
        
        if results['resolution']['status'] == "low":
            issues.append("Low resolution")
        
        if results['contrast']['status'] == "low":
            issues.append("Low contrast")
        
        if results['sharpness']['status'] == "blurry":
            issues.append("Image is blurry")
        
        if results['noise']['status'] == "high":
            issues.append("High noise level")
        
        if results['brightness']['status'] == "too_dark":
            issues.append("Image is too dark")
        elif results['brightness']['status'] == "too_bright":
            issues.append("Image is too bright")
        
        return issues
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if results['resolution']['status'] == "low":
            recommendations.append(
                f"Increase image resolution to at least {self.MIN_RESOLUTION[0]}x{self.MIN_RESOLUTION[1]} pixels"
            )
        
        if results['contrast']['status'] == "low":
            recommendations.append(
                "Improve lighting conditions or adjust camera settings to increase contrast"
            )
        
        if results['sharpness']['status'] == "blurry":
            recommendations.append(
                "Ensure camera is focused properly and image is not motion-blurred"
            )
        
        if results['noise']['status'] == "high":
            recommendations.append(
                "Reduce ISO/gain settings or improve lighting to reduce noise"
            )
        
        if results['brightness']['status'] == "too_dark":
            recommendations.append(
                "Increase exposure or add more lighting"
            )
        elif results['brightness']['status'] == "too_bright":
            recommendations.append(
                "Reduce exposure or lighting intensity"
            )
        
        if not recommendations:
            recommendations.append("Image quality is good for barcode detection")
        
        return recommendations


def analyze_image_quality(image_path: str) -> Dict:
    """
    Analyze image quality for barcode detection.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Dictionary with analysis results
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    analyzer = ImageQualityAnalyzer(image)
    return analyzer.analyze()
