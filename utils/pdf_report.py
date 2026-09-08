"""
PDF Report Generator for ByteBreaker
"""
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
import json


class PDFReportGenerator:
    """Generate PDF reports"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    def generate(self, results: Dict[str, Any], output_path: str) -> str:
        """Generate PDF report"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors
            
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#00ff88'),
                spaceAfter=30
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#16213e'),
                spaceAfter=12
            )
            
            # Title
            story.append(Paragraph("ByteBreaker Framework", title_style))
            story.append(Paragraph(f"Security Assessment Report", styles['Heading2']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 24))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", heading_style))
            story.append(Paragraph(
                f"This report contains the results of automated security assessment "
                f"performed by ByteBreaker Framework.",
                styles['Normal']
            ))
            story.append(Spacer(1, 24))
            
            # Results section
            story.append(Paragraph("Scan Results", heading_style))
            
            # Extract vulnerability data
            scan_data = results.get("results", {}).get("scan", {}).get("data", {})
            vulnerabilities = scan_data.get("vulnerabilities", [])
            total_vulns = scan_data.get("total_found", 0)
            
            if vulnerabilities:
                # Create vulnerability table
                table_data = [["Severity", "Type", "Title"]]
                
                for vuln in vulnerabilities:
                    severity = vuln.get("severity", "unknown")
                    vuln_type = vuln.get("type", "unknown")
                    title = vuln.get("title", "No title")
                    
                    table_data.append([severity.upper(), vuln_type, title])
                
                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f3460')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(table)
                story.append(Spacer(1, 12))
                story.append(Paragraph(f"Total vulnerabilities found: {total_vulns}", styles['Normal']))
            else:
                story.append(Paragraph("No vulnerabilities detected.", styles['Normal']))
            
            story.append(Spacer(1, 24))
            
            # Recommendations
            story.append(Paragraph("Recommendations", heading_style))
            
            recommendations = [
                "Implement security headers (X-Frame-Options, CSP, HSTS)",
                "Update all software and dependencies",
                "Implement input validation and sanitization",
                "Use parameterized queries for database access",
                "Implement proper authentication and authorization",
                "Regular security assessments",
                "Employee security training",
                "Implement monitoring and alerting"
            ]
            
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", styles['Normal']))
                story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 24))
            
            # Footer
            story.append(Paragraph(
                "This report was generated automatically by ByteBreaker Framework. "
                "For authorized testing purposes only.",
                styles['Normal']
            ))
            
            doc.build(story)
            self.logger.info(f"PDF report generated: {output_path}")
            return output_path
            
        except ImportError:
            self.logger.warning("reportlab not installed, falling back to HTML")
            return self._generate_html_fallback(results, output_path)
        except Exception as e:
            self.logger.error(f"PDF generation failed: {e}")
            return self._generate_html_fallback(results, output_path)
    
    def _generate_html_fallback(self, results: Dict[str, Any], output_path: str) -> str:
        """Fallback to HTML if PDF generation fails"""
        html_path = output_path.replace('.pdf', '.html')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ByteBreaker Report</title>
            <style>
                body {{ font-family: Arial; margin: 40px; }}
                h1 {{ color: #00ff88; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #0f3460; color: white; }}
            </style>
        </head>
        <body>
            <h1>ByteBreaker Report</h1>
            <p>Generated: {datetime.now().isoformat()}</p>
            <pre>{json.dumps(results, indent=4)}</pre>
        </body>
        </html>
        """
        
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        return html_path
