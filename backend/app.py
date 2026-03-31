from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import uuid
import hashlib
from werkzeug.utils import secure_filename
from PIL import Image
import io

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Konfiguratsiyalar
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "hackathons.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Rasm yuklash sozlamalari
UPLOAD_FOLDER = os.path.join(basedir, 'hackathon')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

# Upload papkasini yaratish
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

def allowed_file(filename):
    """Fayl kengaytmasini tekshirish"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def optimize_image(file_path, max_size=(800, 600)):
    """Rasmni optimallashtirish"""
    try:
        img = Image.open(file_path)
        
        # Rasm formatini aniqlash
        if img.mode in ('RGBA', 'LA', 'P'):
            # Transparent rasmlar uchun RGB ga o'tkazish
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Rasm hajmini o'zgartirish
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Rasmni saqlash
        img.save(file_path, 'JPEG', quality=85, optimize=True)
        return True
    except Exception as e:
        print(f"Rasm optimallashtirish xatoligi: {e}")
        return False

# Hackathon modeli
class Hackathon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default='online')
    link = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(200), default='hackathon/default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'description': self.description,
            'status': self.status,
            'link': self.link,
            'image': self.image
        }

# API endpoints
@app.route('/api/hackathons', methods=['GET'])
def get_hackathons():
    """Barcha hackathonlarni olish"""
    try:
        hackathons = Hackathon.query.order_by(Hackathon.created_at.desc()).all()
        return jsonify([h.to_dict() for h in hackathons])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hackathons/<int:id>', methods=['GET'])
def get_hackathon(id):
    """Bitta hackathonni olish"""
    try:
        hackathon = Hackathon.query.get_or_404(id)
        return jsonify(hackathon.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/hackathons', methods=['POST'])
def create_hackathon():
    """Yangi hackathon qo'shish"""
    try:
        data = request.json
        print(f"Yangi hackathon: {data}")
        
        hackathon = Hackathon(
            title=data['title'].strip(),
            date=data['date'].strip(),
            description=data['description'].strip(),
            status=data.get('status', 'online'),
            link=data['link'].strip(),
            image=data.get('image', 'hackathon/default.jpg')
        )
        db.session.add(hackathon)
        db.session.commit()
        
        return jsonify(hackathon.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Xatolik: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/hackathons/<int:id>', methods=['PUT'])
def update_hackathon(id):
    """Hackathonni tahrirlash"""
    try:
        hackathon = Hackathon.query.get_or_404(id)
        data = request.json
        
        hackathon.title = data.get('title', hackathon.title).strip()
        hackathon.date = data.get('date', hackathon.date).strip()
        hackathon.description = data.get('description', hackathon.description).strip()
        hackathon.status = data.get('status', hackathon.status)
        hackathon.link = data.get('link', hackathon.link).strip()
        hackathon.image = data.get('image', hackathon.image)
        hackathon.updated_at = datetime.utcnow()
        
        db.session.commit()
        return jsonify(hackathon.to_dict())
    except Exception as e:
        db.session.rollback()
        print(f"Xatolik: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/hackathons/<int:id>', methods=['DELETE'])
def delete_hackathon(id):
    """Hackathonni o'chirish"""
    try:
        hackathon = Hackathon.query.get_or_404(id)
        db.session.delete(hackathon)
        db.session.commit()
        return jsonify({'message': 'Hackathon deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Xatolik: {e}")
        return jsonify({'error': str(e)}), 400

# Rasm yuklash endpointi
@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """Rasm faylini yuklash"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Rasm fayli topilmadi'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Fayl tanlanmagan'}), 400
        
        if file and allowed_file(file.filename):
            # Xavfsiz fayl nomi yaratish
            original_filename = secure_filename(file.filename)
            extension = original_filename.rsplit('.', 1)[1].lower()
            
            # Unikal fayl nomi (vaqt + random + hash)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            random_str = uuid.uuid4().hex[:8]
            filename = f"hackathon_{timestamp}_{random_str}.{extension}"
            
            # Faylni vaqtinchalik saqlash
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
            file.save(temp_path)
            
            # Rasmni optimallashtirish
            final_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if optimize_image(temp_path):
                os.rename(temp_path, final_path)
            else:
                # Optimallashtirish muvaffaqiyatsiz bo'lsa, aslini saqlash
                os.rename(temp_path, final_path)
            
            image_path = f'hackathon/{filename}'
            print(f"Rasm yuklandi: {image_path}")
            
            return jsonify({
                'success': True,
                'image_path': image_path,
                'message': 'Rasm muvaffaqiyatli yuklandi'
            }), 200
        else:
            return jsonify({'error': f'Faqat {", ".join(app.config["ALLOWED_EXTENSIONS"])} formatidagi rasmlar ruxsat etilgan'}), 400
            
    except Exception as e:
        print(f"Rasm yuklash xatoligi: {e}")
        return jsonify({'error': str(e)}), 500

# Admin panel
@app.route('/admin')
def admin_panel():
    """Admin panel sahifasi"""
    return render_template('admin.html')

# Statik fayllarni serve qilish
@app.route('/hackathon/<path:filename>')
def serve_hackathon_image(filename):
    """Rasm fayllarini serve qilish"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'default.jpg')

@app.route('/')
def index():
    """Asosiy sahifa"""
    return send_from_directory(os.path.dirname(basedir), 'hackathons.html')

# Xatoliklarni qayta ishlash
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        # Ma'lumotlar bazasini yaratish
        db.create_all()
        
        # Agar ma'lumotlar bo'sh bo'lsa, test ma'lumotlarini qo'shish
        if Hackathon.query.count() == 0:
            print("Test ma'lumotlari qo'shilmoqda...")
            test_hackathons = [
                Hackathon(
                    title='Startupers ATT school ariza',
                    date='15 Aprel 2026',
                    description='Loyihalarni qo\'llab quvvatlash',
                    status='online',
                    link='https://forms.gle/JFuJ1aykF9N1hriWA',
                    image='hackathon/hack1.png'
                ),
                Hackathon(
                    title='Oliygoh kubogi',
                    date='14 Mart 2026',
                    description='Loyihalarni qo\'llab quvvatlash',
                    status='online',
                    link='https://t.me/fstu_uz/19636',
                    image='hackathon/hack2.jpg'
                ),
                Hackathon(
                    title='The Iris Prize 2026',
                    date='14 Mart 2026',
                    description='Ekologik loyihalar uchun 15 000 dollargacha grantlar',
                    status='online',
                    link='https://t.me/startup_center_fstu/2810',
                    image='hackathon/hack3.jpg'
                )
            ]
            for h in test_hackathons:
                db.session.add(h)
            db.session.commit()
            print(f"{len(test_hackathons)} ta test ma'lumotlari qo'shildi!")
    
    print("\n" + "="*60)
    print("🚀 SATTS Hackathon Management System")
    print("="*60)
    print(f"📍 Admin panel: http://localhost:5000/admin")
    print(f"📍 API: http://localhost:5000/api/hackathons")
    print(f"📍 Asosiy sahifa: http://localhost:5000")
    print(f"📍 Rasm papkasi: {app.config['UPLOAD_FOLDER']}")
    print("="*60)
    print("⚠️  Muhim: Rasm yuklash uchun Pillow kutubxonasi o'rnatilgan bo'lishi kerak")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000)