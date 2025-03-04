import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from datetime import datetime
import base64
import requests
import json
from transformers import pipeline
import re

class ModernUI:
    COLORS = {
        'primary': '#2D3250',  # Koyu lacivert
        'secondary': '#424769', # Orta lacivert
        'accent': '#7077A1',   # Açık lacivert
        'light': '#F6B17A',    # Turuncu accent
        'text': '#FFFFFF',     # Beyaz metin
        'text_dark': '#2D3250', # Koyu metin
        'bg': '#1E1E2E',       # Arka plan
        'success': '#4CAF50',  # Yeşil
        'warning': '#FFC107',  # Sarı
        'error': '#F44336'     # Kırmızı
    }
    
    FONTS = {
        'heading': ('Helvetica', 24, 'bold'),
        'subheading': ('Helvetica', 18),
        'body': ('Helvetica', 12),
        'small': ('Helvetica', 10)
    }

class StilAnalizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Stil Analiz")
        self.geometry("1280x800")
        self.configure(bg=ModernUI.COLORS['bg'])
        
        # API ve model ayarları
        self.api_key = self.ayarlari_yukle()
        self.sonuclar_dizini = "analizler"
        if not os.path.exists(self.sonuclar_dizini):
            os.makedirs(self.sonuclar_dizini)
            
        # Model yükleme
        try:
            self.image_analyzer = pipeline("image-to-text", 
                                         model="Salesforce/blip-image-captioning-large",
                                         max_new_tokens=50)  # Daha kısa analiz için
        except Exception as e:
            messagebox.showerror("Hata", f"Model yüklenemedi: {str(e)}")
        
        self.create_widgets()
        self.setup_styles()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button styles
        style.configure('Primary.TButton',
                       background=ModernUI.COLORS['primary'],
                       foreground=ModernUI.COLORS['text'],
                       padding=10,
                       font=ModernUI.FONTS['body'])
        
        # Frame styles
        style.configure('Card.TFrame',
                       background=ModernUI.COLORS['secondary'],
                       relief='raised',
                       borderwidth=1)
        
        # Label styles
        style.configure('Title.TLabel',
                       background=ModernUI.COLORS['bg'],
                       foreground=ModernUI.COLORS['text'],
                       font=ModernUI.FONTS['heading'])
        
        style.configure('Body.TLabel',
                       background=ModernUI.COLORS['secondary'],
                       foreground=ModernUI.COLORS['text'],
                       font=ModernUI.FONTS['body'])
    
    def create_widgets(self):
        # Ana container
        self.main_container = ttk.Frame(self, style='Card.TFrame')
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Sol Panel (Görsel ve Kontroller)
        self.left_panel = ttk.Frame(self.main_container, style='Card.TFrame')
        self.left_panel.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Görsel seçme butonu
        self.select_btn = ttk.Button(self.left_panel, 
                                   text="Fotoğraf Seç",
                                   style='Primary.TButton',
                                   command=self.select_image)
        self.select_btn.pack(pady=10)
        
        # Görsel gösterme alanı
        self.image_frame = ttk.Frame(self.left_panel, style='Card.TFrame')
        self.image_frame.pack(fill='both', expand=True, pady=10)
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(padx=10, pady=10)
        
        # Sağ Panel (Analiz ve Puanlama)
        self.right_panel = ttk.Frame(self.main_container, style='Card.TFrame')
        self.right_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Kontrol butonları
        self.control_frame = ttk.Frame(self.right_panel, style='Card.TFrame')
        self.control_frame.pack(fill='x', pady=10)
        
        self.analyze_btn = ttk.Button(self.control_frame,
                                    text="Analiz Et",
                                    style='Primary.TButton',
                                    command=self.analyze_image)
        self.analyze_btn.pack(side='left', padx=5)
        
        self.save_btn = ttk.Button(self.control_frame,
                                 text="Sonucu Kaydet",
                                 style='Primary.TButton',
                                 command=self.sonuc_kaydet)
        self.save_btn.pack(side='left', padx=5)
        
        # Puanlama sistemi
        self.score_frame = ttk.LabelFrame(self.right_panel,
                                        text="Stil Puanlaması",
                                        style='Card.TFrame')
        self.score_frame.pack(fill='x', pady=10, padx=5)
        
        self.scores = {
            'Tarz': {'value': tk.IntVar(value=0), 'stars': []},
            'Renk': {'value': tk.IntVar(value=0), 'stars': []},
            'Uyum': {'value': tk.IntVar(value=0), 'stars': []},
            'Etki': {'value': tk.IntVar(value=0), 'stars': []}
        }
        
        for category, data in self.scores.items():
            category_frame = ttk.Frame(self.score_frame, style='Card.TFrame')
            category_frame.pack(fill='x', pady=5)
            
            ttk.Label(category_frame,
                     text=f"{category}:",
                     style='Body.TLabel').pack(side='left')
            
            star_frame = ttk.Frame(category_frame, style='Card.TFrame')
            star_frame.pack(side='right')
            
            for i in range(5):
                star = ttk.Label(star_frame,
                               text='☆',
                               style='Body.TLabel',
                               cursor='hand2')
                star.pack(side='left', padx=2)
                star.bind('<Button-1>',
                         lambda e, c=category, v=i+1: self.update_score(c, v))
                data['stars'].append(star)
        
        # Analiz sonuçları için scrollable text area
        self.result_frame = ttk.Frame(self.right_panel, style='Card.TFrame')
        self.result_frame.pack(fill='both', expand=True, pady=10)
        
        self.result_text = tk.Text(self.result_frame,
                                 wrap=tk.WORD,
                                 font=ModernUI.FONTS['body'],
                                 bg=ModernUI.COLORS['secondary'],
                                 fg=ModernUI.COLORS['text'],
                                 padx=10,
                                 pady=10)
        self.result_text.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.result_frame,
                                orient='vertical',
                                command=self.result_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # Değişkenler
        self.current_image_path = None
        self.photo = None
        
    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Görsel Dosyaları", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.current_image_path = file_path
            self.show_image(file_path)
            self.clear_analysis()
            
    def show_image(self, path):
        image = Image.open(path)
        width, height = image.size
        max_size = 400
        ratio = min(max_size/width, max_size/height)
        new_size = (int(width*ratio), int(height*ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.photo)
        
    def clear_analysis(self):
        self.result_text.delete(1.0, tk.END)
        for category in self.scores.values():
            category['value'].set(0)
            for star in category['stars']:
                star.configure(text='☆')
                
    def update_score(self, category, value):
        self.scores[category]['value'].set(value)
        stars = self.scores[category]['stars']
        for i, star in enumerate(stars):
            star.configure(text='★' if i < value else '☆')
            
    def analyze_image(self):
        if not self.current_image_path:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görsel seçin!")
            return
            
        if not self.api_key:
            messagebox.showwarning("Uyarı", "API anahtarı gerekli!")
            return
            
        try:
            # Görsel analizi
            image = Image.open(self.current_image_path)
            initial_analysis = self.image_analyzer(image)[0]['generated_text']
            
            # GPT-3.5 ile stil analizi
            prompt = f"""Aşağıdaki kıyafet analizini değerlendir ve detaylı bir stil analizi yap:

{initial_analysis}

Lütfen şu başlıklarda analiz yap ve her kategori için 1-5 arası puan ver (parantez içinde belirt):

1. Tarz Değerlendirmesi (Puan: X/5)
- Stil uyumu ve genel görünüm analizi
- Giyim tarzının uygunluğu

2. Renk Analizi (Puan: X/5)
- Renk kombinasyonları
- Renklerin kişiye uygunluğu

3. Uyum Değerlendirmesi (Puan: X/5)
- Parçaların birbiriyle uyumu
- Proporsiyon dengesi

4. Genel Etki (Puan: X/5)
- Görünümün genel etkisi
- Tarzın yansıttığı mesaj

Ardından şunları ekle:
1. Güçlü Yönler (madde madde)
2. Geliştirme Önerileri (madde madde)"""

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "Sen profesyonel bir moda danışmanısın. Her kategori için detaylı değerlendirme yap ve 1-5 arası puanla. Puanları mutlaka (Puan: X/5) formatında belirt."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 800,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if 'error' in response.json():
                raise Exception(response.json()['error']['message'])
                
            analysis = response.json()['choices'][0]['message']['content']
            
            # Puanları analiz metninden çıkar ve güncelle
            score_patterns = {
                'Tarz': r'Tarz Değerlendirmesi \(Puan: (\d)/5\)',
                'Renk': r'Renk Analizi \(Puan: (\d)/5\)',
                'Uyum': r'Uyum Değerlendirmesi \(Puan: (\d)/5\)',
                'Etki': r'Genel Etki \(Puan: (\d)/5\)'
            }
            
            # Puanları güncelle
            for category, pattern in score_patterns.items():
                match = re.search(pattern, analysis)
                if match:
                    score = int(match.group(1))
                    self.update_score(category, score)
            
            # Sonuçları göster
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, analysis)
            
        except Exception as e:
            messagebox.showerror("Hata", str(e))
            
    def ayarlari_yukle(self):
        try:
            if os.path.exists('ayarlar.json'):
                with open('ayarlar.json', 'r') as f:
                    return json.load(f).get('api_key')
        except:
            return None
        return None

    def sonuc_kaydet(self):
        if not self.result_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Uyarı", "Kaydedilecek analiz sonucu bulunamadı!")
            return

        try:
            # Dosya adı için tarih-saat formatı
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dosya_adi = f"stil_analiz_{timestamp}.txt"
            dosya_yolu = os.path.join(self.sonuclar_dizini, dosya_adi)

            # Puanları ve analiz sonucunu birleştir
            sonuc_metni = "STİL ANALİZ RAPORU\n"
            sonuc_metni += "=" * 20 + "\n\n"
            
            # Puanları ekle
            sonuc_metni += "PUANLAMA:\n"
            for kategori, data in self.scores.items():
                puan = data['value'].get()
                yildizlar = "★" * puan + "☆" * (5 - puan)
                sonuc_metni += f"{kategori}: {yildizlar} ({puan}/5)\n"
            
            sonuc_metni += "\nANALİZ SONUCU:\n"
            sonuc_metni += "=" * 20 + "\n"
            sonuc_metni += self.result_text.get(1.0, tk.END)

            # Dosyaya kaydet
            with open(dosya_yolu, 'w', encoding='utf-8') as f:
                f.write(sonuc_metni)

            messagebox.showinfo("Başarılı", f"Analiz sonucu kaydedildi:\n{dosya_yolu}")

        except Exception as e:
            messagebox.showerror("Hata", f"Sonuç kaydedilirken hata oluştu: {str(e)}")

if __name__ == "__main__":
    app = StilAnalizApp()
    app.mainloop() 