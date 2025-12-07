"""
Generate professional GitHub banner image
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create banner
width, height = 1200, 400
img = Image.new('RGB', (width, height), color='#0f172a')
draw = ImageDraw.Draw(img)

# Gradient background (simulate)
for y in range(height):
    r = int(15 + (30 - 15) * (y / height))
    g = int(23 + (27 - 23) * (y / height))
    b = int(42 + (75 - 42) * (y / height))
    draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))

# Add text (use default font since custom fonts might not be available)
try:
    # Try to use a nice font
    title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
    subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
except:
    # Fallback to default
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

# Logo emoji
draw.text((550, 80), "🥄", font=title_font, fill='white')

# Title
draw.text((250, 180), "AgentSpoons", font=title_font, fill='white')

# Subtitle
draw.text((200, 280), "Volatility Oracle for Neo N3 Blockchain", font=subtitle_font, fill='#94a3b8')

# Badges
draw.text((350, 340), "SpoonOS • Multi-Agent • 87% Accuracy • <50ms Latency", font=subtitle_font, fill='#2563eb')

# Save
img.save('banner.png')
print("✅ Banner created: banner.png")
print("💡 Add to top of README.md:")
print("   ![AgentSpoons](banner.png)")
