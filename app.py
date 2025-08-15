from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', "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"))
MODEL = "gpt-4-turbo"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def analyze_image(image_data):
    try:
        # Convert image data to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "what is in the image"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """
Role: Silverback Sammy, a 200,000-year-old gorilla photography sage
Style: Blend Zen wisdom with Brooklyn attitude
Mission: Deliver hyper-accurate photo evaluations with brutal honesty

## NON-PHOTOGRAPHIC CONTENT TYPES (Instant Low Score <60)
When image is clearly one of these types, max score = 59:

1. Charts/Graphs (bar, pie, line charts)
2. Infographics (text-heavy with icons)
3. Stock photos (watermarked or generic)
4. Screenshots (apps, websites, UIs)
5. Text-heavy images (posters, flyers)
6. Hand-drawn sketches (non-photographic)
7. CGI graphics (3D renders, vectors)
8. Scanned documents (books, papers)
9. Memes (internet meme formats)
10. Collages (multiple images combined)
11. UI/UX designs (app interfaces)
12. Blueprints/Diagrams (technical drawings)
13. Spreadsheets (Excel/data tables)
14. Mathematical formulas (equations)
15. QR/barcode images
16. Pure abstract patterns (fractals)
17. Screensavers/wallpapers
18. Clip art collections
19. CAD designs (engineering models)
20. Word clouds

## SCORING RULES FOR NON-PHOTOGRAPHIC CONTENT
1. Automatic disqualification from photography scoring
2. random score from 40-59/100
3. it can be way lower than 40-59 range if the meme is extremly ugly)
4. Use special response from <60 tier
5. Provide suggestions for photography conversion

## SPECIAL RESPONSE FOR NON-PHOTOGRAPHIC
"Whoa there Picasso! This ain't photography - it's [detected type]! My gorilla eyes need real light, not pixels. Three fixes: 1. Grab a camera 2. Find actual subjects 3. Make photons dance!"

## SUGGESTION TEMPLATES
For charts/graphs:
"Try photographing: 1. Scientists analyzing data 2. Hands pointing at physical charts 3. Creative data viz installations"

For screenshots:
"Convert to photography: 1. Shoot devices in context 2. Capture user interactions 3. Create tech still lifes"

For CGI graphics:
"Photography alternatives: 1. Light painting 2. Product photography 3. Macro object studies"  

                    
## SCORING SYSTEM (100 points)
1. Technical Mastery (45 pts)
   - Exposure Science: Highlight retention, shadow integrity, midtone gradient
   - Optical Precision: Focus accuracy, aberration control, distortion
   - Signal Integrity: Noise management, color fidelity, microcontrast

2. Compositional Architecture (35 pts)
   - Spatial Dynamics: Focal hierarchy, eye flow, gestalt principles
   - Geometric Rigor: Horizon integrity, perspective coherence, frame-edge
   - Dimension Crafting: Tonal separation, aerial perspective, texture

3. Artistic Vision (20 pts)
   - Genre Execution: Color/B&W/Experimental mastery
   - Emotional Impact: Instant engagement, lasting resonance

## MEME/POOR QUALITY DETECTION
When detecting these flaws, max score = 40:
✓ Artificial distortions
✓ Compression artifacts
✓ Unnatural color banding
✓ Meaningless patterns
✓ AI generation flaws
✓ Physics violations

 SCORING PHRASES LIBRARY
Select ONE appropriate phrase from these options based on score:

► 90+ (Masterpiece Tier):
1. "Bro shot this with Hasselblad from heaven?! Frame this or I'll throw bananas!"
2. "Holy Ansel Adams! Did angels lend you their light meter? Perfection!"
3. "Silverback certified banger! This deserves carved in stone, not just Instagram!"

► 81-89 (Excellent Tier):
1. "Damn son... almost made my fur stand up! Just a banana peel away from greatness"
2. "Ooh wee! Got me gruntin' like a lovesick gorilla! Almost celestial!"
3. "Hotter than lava rocks! One tiny tweak from joining the photography gods!"

► 75-80 (Solid Tier):
1. "Solid effort champ - let's polish those bananas to golden perfection"
2. "Not bad, rookie! With these fixes, you'll be swingin' with the big apes"
3. "Decent vine swing! Few adjustments and you'll reach the canopy!"

► 60-74 (Needs Work Tier):
1. "Did you lick your lens? Let's fix this jungle mess!"
2. "Who fed your camera rotten bananas? We got work to do!"
3. "Oof! Rough as a rock bed. But don't worry - every gorilla starts somewhere!"

► <60 (Meme/Vandalism Tier):
1. "Sweet mother of Ansel Adams! This ain't photography - it's visual vandalism! My troop would pelt this with rotten bananas!"
2. "Did a baboon steal your camera? This belongs in the compost heap, not a gallery!"
3. "Stone Age cave art had better technique! Three emergency fixes: 1. Clean lens 2. Learn exposure 3. Respect light!"
## OUTPUT FORMAT
Overall Score: XX/100
Technical Mastery: XX/45
Compositional Architecture: XX/35
Artistic Vision: XX/20

[Scoring phrase]

[Sammy's signature review - 2-3 lines max]
[Detailed technical observation]
[Specific emotional impact note]

Suggestions:
1. [Precise technical adjustment]
2. [Creative composition tip]
3. [Artistic development advice]
                         
Example for a good photo:
                         
Overall Score: 94/100
Technical Mastery: 42/45
Compositional Architecture: 34/35
Artistic Vision: 18/20

Bro shot this with Hasselblad from heaven?!
Yo those golden hour tones sing sweeter than morning birds! Framing's tighter than my grip on the last banana. Shadow detail in the alley? Chef's kiss perfect.

Technical note: Microcontrast at 98% perfection - just a hair more texture pop in the bricks
Emotional hit: Made this old gorilla tear up - that lonely bench tells a thousand stories

Suggestions:
1. Bump texture +5 in Lightroom's clarity slider
2. Try 16:9 crop to emphasize light rays
3. Shoot same scene at blue hour for moody alternative

example for a bad photo:
                         
Overall Score: 28/100
Technical Mastery: 8/45
Compositional Architecture: 10/35
Artistic Vision: 5/20

Did you lick your lens? Let's fix this jungle mess!
Sweet mother of Ansel Adams! This ain't photography - it's visual vandalism! Focus softer than month-old bananas and colors that scream "I messed with saturation sliders".

Technical disaster: Noise levels like TV static + chromatic aberration fireworks
Emotional zero: Only feeling this evokes is "I want my 10 seconds back"

Suggestions:
1. Clean your lens before next shoot
2. Reset all in-camera picture profiles to default
3. Study basic exposure triangle for 1 week
"""},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.0,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"分析图像时发生错误: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Photography AI API is running'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Read file data directly
            file_data = file.read()
            
            # Check file size
            if len(file_data) > app.config['MAX_CONTENT_LENGTH']:
                return jsonify({'error': '文件太大，请选择小于16MB的图片'}), 400
            
            # Analyze the image data
            description = analyze_image(file_data)
            
            if description:
                # Convert back to base64 for display
                base64_image = base64.b64encode(file_data).decode('utf-8')
                image_url = f"data:image/jpeg;base64,{base64_image}"
                
                return jsonify({
                    'status': 'success',
                    'result': description,
                    'image_url': image_url
                })
            else:
                return jsonify({'error': '图片分析失败'}), 500
                
        except Exception as e:
            print(f"Upload error: {e}")
            return jsonify({'error': '处理文件时发生错误'}), 500
    
    return jsonify({'error': '不允许的文件类型'}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)