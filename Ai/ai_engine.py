# النهائي

import os
import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from tensorflow.keras.models import load_model


class AdvancedDentalAnalysis:
    def __init__(self, detection_model_path, classification_model_path):
        """
        Initialize the dental analysis system with both detection and classification models
        """
        # Load YOLOv8 detection model
        self.det_model = YOLO(detection_model_path)

        # Load CNN classification model
        self.cls_model = load_model(classification_model_path)
        # self.class_names = ['Implant', 'Impacted Tooth', 'Fillings', 'Cavity']
        self.class_names = ['Fillings', 'Cavity', 'Implant', 'Impacted Tooth']

        # Visualization settings
        self.colors = {
            'Cavity': (255, 50, 50),        # Red
            'Fillings': (50, 255, 50),      # Green
            'Implant': (50, 50, 255),       # Blue
            'Impacted Tooth': (255, 255, 50)  # Yellow
        }
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.6
        self.font_thickness = 1

    def preprocess_for_classification(self, img, bbox):
        """
        Prepare cropped tooth image for classification
        """
        x1, y1, x2, y2 = bbox
        cropped = img[y1:y2, x1:x2]

        # Convert to grayscale and resize
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (200, 200))
        normalized = resized / 255.0
        # Add batch and channel dims
        return np.expand_dims(normalized, axis=(0, -1))

    def detect_and_classify(self, image_path):
        """
        Perform detection and classification with enhanced visualization
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Failed to load image: {image_path}")

        # Run detection
        detections = self.det_model(img)

        # Prepare results structure
        results = {
            'original': img.copy(),
            'annotated': img.copy(),
            'teeth_data': [],
            'classification_results': []
        }

        # Process each detection
        for i, det in enumerate(detections[0].boxes, start=1):
            # Extract detection info
            cls_id = int(det.cls)
            conf = float(det.conf)
            bbox = [int(x) for x in det.xyxy[0].tolist()]
            det_class = detections[0].names[cls_id]

            # Classify the detected region
            cls_input = self.preprocess_for_classification(img, bbox)
            cls_pred = self.cls_model.predict(cls_input, verbose=0)[0]
            cls_conf = np.max(cls_pred)
            cls_label = self.class_names[np.argmax(cls_pred)]

            # Store results
            tooth_data = {
                'id': i,
                'detection_class': det_class,
                'detection_confidence': conf,
                'classification_class': cls_label,
                'classification_confidence': cls_conf,
                'classification_details': {self.class_names[i]: float(cls_pred[i]) for i in range(4)},
                'bbox': bbox
            }
            results['teeth_data'].append(tooth_data)

            # Visualization
            self._visualize_tooth(results['annotated'], tooth_data)

        return results

    def _visualize_tooth(self, img, tooth_data):
        """Helper method to annotate image with tooth information"""
        x1, y1, x2, y2 = tooth_data['bbox']
        color = self.colors.get(
            tooth_data['classification_class'], (255, 255, 255))

        # Draw bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # Prepare classification info text
        text = f"{tooth_data['id']}: {tooth_data['classification_class']} ({tooth_data['classification_confidence']:.2f})"
        (text_w, text_h), _ = cv2.getTextSize(
            text, self.font, self.font_scale, self.font_thickness)

        # Draw text background
        cv2.rectangle(img,
                      (x1, y1 - text_h - 10),
                      (x1 + text_w + 10, y1),
                      color, -1)

        # Draw text
        cv2.putText(img, text,
                    (x1 + 5, y1 - 5),
                    self.font, self.font_scale,
                    (0, 0, 0), self.font_thickness)

    def generate_report(self, analysis_results):
        """Generate comprehensive dental report"""
        report = {
            'visualization': analysis_results['annotated'],
            'summary': self._generate_summary(analysis_results['teeth_data']),
            'detailed_findings': analysis_results['teeth_data']
        }
        return report

    def _generate_summary(self, teeth_data):
        """Generate diagnostic summary"""
        counts = {
            'Cavity': 0,
            'Fillings': 0,
            'Implant': 0,
            'Impacted Tooth': 0
        }

        for tooth in teeth_data:
            counts[tooth['classification_class']] += 1

        # Generate diagnosis based on counts
        if counts['Cavity'] >= 3:
            severity = "high" if counts['Cavity'] > 5 else "medium"
            return f"Multiple cavities detected ({counts['Cavity']}) - Severity: {severity}"
        elif counts['Cavity'] > 0:
            return f"Dental cavities detected ({counts['Cavity']}) - Requires treatment"
        elif counts['Impacted Tooth'] > 0:
            return f"Impacted teeth detected ({counts['Impacted Tooth']}) - Surgical evaluation needed"
        elif counts['Fillings'] > 2:
            return f"Multiple dental fillings ({counts['Fillings']}) - Previously treated teeth"
        elif counts['Implant'] > 0:
            return f"Dental implants present ({counts['Implant']}) - Good condition"
        else:
            return "No significant dental issues detected"

    def visualize_report(self, report):
        """Display professional report visualization"""
        plt.figure(figsize=(18, 12))
        plt.suptitle('Comprehensive Dental Analysis Report',
                     fontsize=16, y=0.98)

        # 1. Show annotated image
        plt.subplot(2, 2, (1, 2))
        plt.imshow(cv2.cvtColor(report['visualization'], cv2.COLOR_BGR2RGB))
        plt.title('Dental Anomaly Detection Results', fontsize=12)
        plt.axis('off')

        # 2. Show diagnostic summary
        plt.subplot(2, 2, 3)
        plt.text(0.1, 0.5, report['summary'],
                 fontsize=12,
                 bbox=dict(facecolor='lightyellow', alpha=0.5),
                 verticalalignment='center')
        plt.axis('off')
        plt.title('Clinical Diagnosis Summary', fontsize=12)

        # 3. Show detailed findings table
        plt.subplot(2, 2, 4)
        plt.axis('off')
        plt.title('Detailed Tooth-by-Tooth Analysis', fontsize=12)

        # Prepare table data
        table_data = []
        for tooth in report['detailed_findings']:
            table_data.append([
                tooth['id'],
                tooth['classification_class'],
                f"{tooth['classification_confidence']:.2f}",
                tooth['bbox']
            ])

        # Create table
        table = plt.table(cellText=table_data,
                          colLabels=['ID', 'Classification',
                                     'Confidence', 'Bounding Box'],
                          loc='center',
                          cellLoc='center',
                          colColours=['#f0f0f0']*4)

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.2)

        plt.tight_layout()
        plt.show()

        # Print detailed classification probabilities
        print("\n🔍 Detailed Classification Probabilities:")
        print("-" * 85)
        print(
            f"{'Tooth':<6} | {'Class':<15} | {'Confidence':<10} | {'Probabilities':<45}")
        print("-" * 85)
        for tooth in report['detailed_findings']:
            probs = ", ".join(
                [f"{k}: {v:.2f}" for k, v in tooth['classification_details'].items()])
            print(f"{tooth['id']:<6} | {tooth['classification_class']:<15} | "
                  f"{tooth['classification_confidence']:<10.2f} | {probs:<45}")
        print("-" * 85)
