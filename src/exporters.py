"""Export decoded barcode data in multiple formats."""

import json
import csv
import xml.etree.ElementTree as ET
from typing import List, Dict
from datetime import datetime
from pathlib import Path


class BaseExporter:
    """Base class for exporters."""
    
    def export(self, results: List[Dict], output_path: str, metadata: Dict = None) -> None:
        """Export results to file."""
        raise NotImplementedError


class TextExporter(BaseExporter):
    """Export results as plain text."""
    
    def export(self, results: List[Dict], output_path: str, metadata: Dict = None) -> None:
        """Export results to text file."""
        lines = []
        
        if metadata:
            lines.append(f"# Decoded at: {metadata.get('timestamp', 'N/A')}")
            lines.append(f"# Source: {metadata.get('source', 'N/A')}")
            lines.append("")
        
        for i, result in enumerate(results, 1):
            lines.append(f"--- Barcode {i} ---")
            lines.append(f"Data: {result['data']}")
            if metadata and metadata.get('verbose'):
                lines.append(f"Type: {result['type']}")
                lines.append(f"Position: {result['rect']}")
                lines.append(f"Quality: {result['quality']}")
                lines.append(f"Method: {result['preprocess_method']}")
            lines.append("")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))


class JSONExporter(BaseExporter):
    """Export results as JSON."""
    
    def export(self, results: List[Dict], output_path: str, metadata: Dict = None) -> None:
        """Export results to JSON file."""
        # Convert non-serializable objects to strings
        serializable_results = []
        for result in results:
            serializable = {
                'data': result['data'],
                'type': str(result['type']),
                'quality': result['quality'],
                'preprocess_method': result['preprocess_method'],
                'rect': {
                    'left': result['rect'].left,
                    'top': result['rect'].top,
                    'width': result['rect'].width,
                    'height': result['rect'].height
                },
                'polygon': [{'x': p.x, 'y': p.y} for p in result['polygon']]
            }
            serializable_results.append(serializable)
        
        output = {
            'metadata': metadata or {},
            'results': serializable_results,
            'count': len(serializable_results)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)


class CSVExporter(BaseExporter):
    """Export results as CSV."""
    
    def export(self, results: List[Dict], output_path: str, metadata: Dict = None) -> None:
        """Export results to CSV file."""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'barcode_id', 'data', 'type', 'quality', 
                'preprocess_method', 'rect_left', 'rect_top', 
                'rect_width', 'rect_height', 'data_length'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, result in enumerate(results, 1):
                writer.writerow({
                    'barcode_id': i,
                    'data': result['data'],
                    'type': str(result['type']),
                    'quality': result['quality'],
                    'preprocess_method': result['preprocess_method'],
                    'rect_left': result['rect'].left,
                    'rect_top': result['rect'].top,
                    'rect_width': result['rect'].width,
                    'rect_height': result['rect'].height,
                    'data_length': len(result['data'])
                })


class XMLExporter(BaseExporter):
    """Export results as XML."""
    
    def export(self, results: List[Dict], output_path: str, metadata: Dict = None) -> None:
        """Export results to XML file."""
        root = ET.Element('pdf417_results')
        
        # Add metadata
        if metadata:
            meta_elem = ET.SubElement(root, 'metadata')
            for key, value in metadata.items():
                elem = ET.SubElement(meta_elem, key)
                elem.text = str(value)
        
        # Add results
        barcodes_elem = ET.SubElement(root, 'barcodes', count=str(len(results)))
        
        for i, result in enumerate(results, 1):
            barcode_elem = ET.SubElement(barcodes_elem, 'barcode', id=str(i))
            
            data_elem = ET.SubElement(barcode_elem, 'data')
            data_elem.text = result['data']
            
            type_elem = ET.SubElement(barcode_elem, 'type')
            type_elem.text = str(result['type'])
            
            quality_elem = ET.SubElement(barcode_elem, 'quality')
            quality_elem.text = str(result['quality'])
            
            method_elem = ET.SubElement(barcode_elem, 'preprocess_method')
            method_elem.text = result['preprocess_method']
            
            rect_elem = ET.SubElement(barcode_elem, 'rectangle')
            rect_elem.set('left', str(result['rect'].left))
            rect_elem.set('top', str(result['rect'].top))
            rect_elem.set('width', str(result['rect'].width))
            rect_elem.set('height', str(result['rect'].height))
        
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(output_path, encoding='utf-8', xml_declaration=True)


def get_exporter(format_type: str) -> BaseExporter:
    """
    Get exporter instance for specified format.
    
    Args:
        format_type: Output format (txt, json, csv, xml)
        
    Returns:
        Exporter instance
        
    Raises:
        ValueError: If format is not supported
    """
    exporters = {
        'txt': TextExporter,
        'json': JSONExporter,
        'csv': CSVExporter,
        'xml': XMLExporter
    }
    
    format_lower = format_type.lower()
    if format_lower not in exporters:
        raise ValueError(
            f"Unsupported format: {format_type}. "
            f"Supported formats: {', '.join(exporters.keys())}"
        )
    
    return exporters[format_lower]()


def export_results(
    results: List[Dict], 
    output_path: str, 
    format_type: str = 'txt',
    metadata: Dict = None
) -> None:
    """
    Export barcode results to file in specified format.
    
    Args:
        results: List of decoded barcode results
        output_path: Path to output file
        format_type: Output format (txt, json, csv, xml)
        metadata: Optional metadata to include in export
    """
    # Add default metadata
    if metadata is None:
        metadata = {}
    
    metadata.setdefault('timestamp', datetime.now().isoformat())
    metadata.setdefault('count', len(results))
    
    # Get appropriate exporter and export
    exporter = get_exporter(format_type)
    exporter.export(results, output_path, metadata)
