from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

class PDFService:
    def generate_itinerary_pdf(self, itinerary_data):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom styles for better formatting
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        ))
        
        styles.add(ParagraphStyle(
            name='DayHeader',
            parent=styles['Heading2'],
            fontSize=18,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#2E7D32')
        ))
        
        styles.add(ParagraphStyle(
            name='TimeBlock',
            parent=styles['Normal'],
            fontSize=12,
            spaceBefore=12,
            spaceAfter=8,
            leftIndent=20,
            textColor=colors.HexColor('#333333')
        ))
        
        styles.add(ParagraphStyle(
            name='RegularText',
            parent=styles['Normal'],
            fontSize=11,
            spaceBefore=6,
            spaceAfter=6,
            leading=14
        ))
        
        story = []
        
        # Add title
        story.append(Paragraph(itinerary_data['title'], styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Format description with proper spacing and styling
        description_lines = itinerary_data['description'].split('\n')
        for line in description_lines:
            if line.strip().startswith('📅 Day'):
                story.append(Paragraph(line, styles['DayHeader']))
            elif any(time in line for time in ['Morning:', 'Afternoon:', 'Evening:']):
                story.append(Paragraph(line, styles['TimeBlock']))
            elif line.strip().startswith(('🍽️', '🏨')):
                story.append(Paragraph(line, styles['TimeBlock']))
            elif line.strip():
                story.append(Paragraph(line, styles['RegularText']))
                story.append(Spacer(1, 6))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
