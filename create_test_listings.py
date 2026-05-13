"""
Create test listings for UniEv platform
- 5 listings per landlord (25 total)
- Real Istanbul addresses with coordinates
- Photos from placeholder services
"""

import sys
from sqlalchemy.orm import Session
from database import SessionLocal, User, Listing, ListingPhoto
from datetime import datetime
import uuid
import random

def create_test_listings():
    db = SessionLocal()
    
    try:
        print("🏠 Creating test listings for UniEv...")
        print("=" * 80)
        
        # Get all landlords
        landlords = db.query(User).filter(User.role == "LANDLORD").all()
        
        if not landlords:
            print("❌ No landlords found! Please create landlord accounts first.")
            return
        
        print(f"✅ Found {len(landlords)} landlords")
        print()
        
        # Real Istanbul locations with coordinates
        istanbul_locations = [
            # Kadıköy
            {"city": "İstanbul", "district": "Kadıköy", "address": "Caferağa Mahallesi, Moda Caddesi No:45", "lat": 40.9872, "lng": 29.0261},
            {"city": "İstanbul", "district": "Kadıköy", "address": "Rasimpaşa Mahallesi, Söğütlüçeşme Caddesi No:23", "lat": 40.9923, "lng": 29.0289},
            {"city": "İstanbul", "district": "Kadıköy", "address": "Fenerbahçe Mahallesi, Bağdat Caddesi No:156", "lat": 40.9645, "lng": 29.0347},
            {"city": "İstanbul", "district": "Kadıköy", "address": "Göztepe Mahallesi, Fahrettin Kerim Gökay Caddesi No:78", "lat": 40.9734, "lng": 29.0512},
            {"city": "İstanbul", "district": "Kadıköy", "address": "Kozyatağı Mahallesi, Değirmen Sokak No:12", "lat": 40.9789, "lng": 29.0678},
            
            # Beşiktaş
            {"city": "İstanbul", "district": "Beşiktaş", "address": "Ortaköy Mahallesi, Mecidiye Köprüsü Sokak No:34", "lat": 41.0553, "lng": 29.0276},
            {"city": "İstanbul", "district": "Beşiktaş", "address": "Etiler Mahallesi, Nispetiye Caddesi No:67", "lat": 41.0789, "lng": 29.0234},
            {"city": "İstanbul", "district": "Beşiktaş", "address": "Levent Mahallesi, Büyükdere Caddesi No:89", "lat": 41.0812, "lng": 29.0123},
            {"city": "İstanbul", "district": "Beşiktaş", "address": "Bebek Mahallesi, Cevdetpaşa Caddesi No:45", "lat": 41.0789, "lng": 29.0456},
            {"city": "İstanbul", "district": "Beşiktaş", "address": "Arnavutköy Mahallesi, Bebek Yolu No:23", "lat": 41.0678, "lng": 29.0389},
            
            # Şişli
            {"city": "İstanbul", "district": "Şişli", "address": "Mecidiyeköy Mahallesi, Büyükdere Caddesi No:123", "lat": 41.0634, "lng": 28.9945},
            {"city": "İstanbul", "district": "Şişli", "address": "Osmanbey Mahallesi, Halaskargazi Caddesi No:234", "lat": 41.0512, "lng": 28.9889},
            {"city": "İstanbul", "district": "Şişli", "address": "Nişantaşı Mahallesi, Teşvikiye Caddesi No:56", "lat": 41.0489, "lng": 28.9934},
            {"city": "İstanbul", "district": "Şişli", "address": "Gayrettepe Mahallesi, Yıldız Posta Caddesi No:78", "lat": 41.0723, "lng": 29.0089},
            {"city": "İstanbul", "district": "Şişli", "address": "Esentepe Mahallesi, Büyükdere Caddesi No:145", "lat": 41.0756, "lng": 29.0034},
            
            # Üsküdar
            {"city": "İstanbul", "district": "Üsküdar", "address": "Kuzguncuk Mahallesi, İcadiye Caddesi No:34", "lat": 41.0234, "lng": 29.0456},
            {"city": "İstanbul", "district": "Üsküdar", "address": "Çengelköy Mahallesi, Kuleli Caddesi No:67", "lat": 41.0456, "lng": 29.0789},
            {"city": "İstanbul", "district": "Üsküdar", "address": "Beylerbeyi Mahallesi, Abdullahağa Caddesi No:23", "lat": 41.0412, "lng": 29.0423},
            {"city": "İstanbul", "district": "Üsküdar", "address": "Altunizade Mahallesi, Kısıklı Caddesi No:89", "lat": 41.0123, "lng": 29.0567},
            {"city": "İstanbul", "district": "Üsküdar", "address": "Acıbadem Mahallesi, Çeçen Sokak No:45", "lat": 40.9889, "lng": 29.0634},
            
            # Sarıyer
            {"city": "İstanbul", "district": "Sarıyer", "address": "Maslak Mahallesi, Büyükdere Caddesi No:234", "lat": 41.1089, "lng": 29.0234},
            {"city": "İstanbul", "district": "Sarıyer", "address": "İstinye Mahallesi, İstinye Bayırı Caddesi No:56", "lat": 41.1123, "lng": 29.0456},
            {"city": "İstanbul", "district": "Sarıyer", "address": "Emirgan Mahallesi, Sakıp Sabancı Caddesi No:78", "lat": 41.1067, "lng": 29.0534},
            {"city": "İstanbul", "district": "Sarıyer", "address": "Rumeli Hisarı Mahallesi, Yahya Kemal Caddesi No:34", "lat": 41.0845, "lng": 29.0567},
            {"city": "İstanbul", "district": "Sarıyer", "address": "Tarabya Mahallesi, Haydar Aliyev Caddesi No:12", "lat": 41.1234, "lng": 29.0678}
        ]
        
        # Listing templates with realistic Turkish descriptions
        listing_templates = [
            {
                "title": "Üniversiteye Yakın Ferah 2+1 Daire",
                "description": "Üniversiteye yürüme mesafesinde, güneşli ve ferah 2+1 daire. Eşyalı, beyaz eşya mevcut. Temiz ve bakımlı. Öğrencilere özel fiyat. Toplu taşımaya çok yakın, market ve eczane 2 dakika mesafede.",
                "price_range": (4000, 6000),
                "rules": "Sigara içilmez. Evcil hayvan kabul edilmez. Gürültü yapılmaması rica olunur."
            },
            {
                "title": "Merkezi Konumda Öğrenci Evi",
                "description": "Şehir merkezinde, ulaşımı çok kolay konumda öğrenci evi. 3+1 daire, geniş ve aydınlık. Tüm eşyalar yeni. Güvenli bina, 7/24 güvenlik. Otopark mevcut. Yakınında AVM, kafe ve restoranlar.",
                "price_range": (5000, 7000),
                "rules": "Ev kurallarına uyulması beklenir. Misafir kabul edilebilir ancak önceden haber verilmesi gerekir."
            },
            {
                "title": "Deniz Manzaralı Lüks Daire",
                "description": "Muhteşem deniz manzaralı, lüks rezidansta 2+1 daire. Tam eşyalı, modern mobilyalar. Havuz, spor salonu, güvenlik mevcut. Sessiz ve huzurlu ortam. Çalışkan öğrenciler için ideal.",
                "price_range": (7000, 9000),
                "rules": "Temizlik ve düzen önemlidir. Parti yapılmaz. Sigara balkonlarda içilebilir."
            },
            {
                "title": "Ekonomik ve Temiz Stüdyo Daire",
                "description": "Bütçe dostu, temiz ve bakımlı stüdyo daire. Tek kişilik veya çift için uygun. Eşyalı, mutfak malzemeleri mevcut. Faturalar dahil. Sessiz mahalle, güvenli bina. Market ve durak 1 dakika.",
                "price_range": (3500, 5000),
                "rules": "Temizliğe özen gösterilmesi beklenir. Gece geç saatlerde gürültü yapılmamalı."
            },
            {
                "title": "Geniş Bahçeli Müstakil Ev",
                "description": "Bahçeli, müstakil ev. 4+1, çok geniş ve ferah. Barbekü alanı, otopark mevcut. Doğayla iç içe, sakin bir ortam. Grup öğrenciler için ideal. Evcil hayvan kabul edilir.",
                "price_range": (8000, 12000),
                "rules": "Bahçe bakımına özen gösterilmesi rica olunur. Komşulara saygılı olunmalı."
            },
            {
                "title": "Yeni Yapılı Modern Daire",
                "description": "Sıfır binada, yeni yapılı 2+1 daire. Tüm eşyalar yeni ve modern. Akıllı ev sistemi, merkezi ısıtma. Asansör, kapalı otopark. Güvenlik kamerası mevcut. Öğrencilere özel indirimli.",
                "price_range": (5500, 7500),
                "rules": "Bina kurallarına uyulması zorunludur. Ortak alanlarda sessiz olunmalı."
            },
            {
                "title": "Kampüse 5 Dakika Öğrenci Evi",
                "description": "Kampüse çok yakın, yürüyerek 5 dakika. 3+1 geniş daire. Eşyalı, internet dahil. Çalışma odası mevcut. Sessiz ve huzurlu ortam. Kütüphane ve kafeler yakında.",
                "price_range": (4500, 6500),
                "rules": "Ders çalışma saatlerine saygı gösterilmesi önemlidir. Temizlik ortak sorumluluk."
            },
            {
                "title": "Balkonlu ve Aydınlık Daire",
                "description": "Geniş balkonlu, çok aydınlık 2+1 daire. Güneş tüm gün giriyor. Eşyalı, klima mevcut. Asansörlü bina, temiz ve bakımlı. Market, eczane, durak çok yakın. Öğrencilere uygun.",
                "price_range": (4800, 6800),
                "rules": "Balkon düzenli temizlenmeli. Komşu rahatsız edilmemeli."
            }
        ]
        
        # Photo URLs - using placeholder images
        photo_sets = [
            # Modern apartments
            [
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800",
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800",
                "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800"
            ],
            # Cozy rooms
            [
                "https://images.unsplash.com/photo-1556020685-ae41abfc9365?w=800",
                "https://images.unsplash.com/photo-1556912173-46c336c7fd55?w=800",
                "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800",
                "https://images.unsplash.com/photo-1556912167-f556f1f39faa?w=800"
            ],
            # Bright living spaces
            [
                "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800",
                "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800",
                "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800",
                "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800"
            ],
            # Kitchen and dining
            [
                "https://images.unsplash.com/photo-1556909114-44e3e70034e2?w=800",
                "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800",
                "https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=800",
                "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800"
            ],
            # Bedrooms
            [
                "https://images.unsplash.com/photo-1505693314120-0d443867891c?w=800",
                "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800",
                "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800",
                "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800"
            ]
        ]
        
        listing_count = 0
        
        for landlord in landlords:
            print(f"\n🏠 Creating listings for {landlord.first_name} {landlord.last_name} ({landlord.email})")
            print("-" * 80)
            
            # Create 5 listings per landlord
            for i in range(5):
                # Select random location and template
                location = random.choice(istanbul_locations)
                template = random.choice(listing_templates)
                photos = random.choice(photo_sets)
                
                # Generate price within range
                price = random.randint(template["price_range"][0], template["price_range"][1])
                
                # Create listing
                listing = Listing(
                    id=str(uuid.uuid4()),
                    owner_id=landlord.id,
                    title=template["title"],
                    description=template["description"],
                    price=price,
                    city=location["city"],
                    district=location["district"],
                    address=location["address"],
                    latitude=location["lat"],
                    longitude=location["lng"],
                    rules=template["rules"],
                    status="ACTIVE",
                    fraud_score=random.randint(5, 25),  # Low fraud scores for test data
                    safety_index=random.randint(75, 95),  # High safety for test data
                    created_at=datetime.utcnow()
                )
                db.add(listing)
                db.flush()
                
                # Add photos
                for idx, photo_url in enumerate(photos):
                    photo = ListingPhoto(
                        listing_id=listing.id,
                        url=photo_url,
                        order=idx
                    )
                    db.add(photo)
                
                listing_count += 1
                print(f"  ✅ Listing {i+1}: {template['title']}")
                print(f"     📍 {location['district']}, {location['address']}")
                print(f"     💰 ₺{price:,}/ay")
                print(f"     📊 Fraud Score: {listing.fraud_score}, Safety: {listing.safety_index}")
                print(f"     📸 {len(photos)} photos")
                print()
        
        db.commit()
        
        print("=" * 80)
        print(f"✅ Successfully created {listing_count} listings!")
        print(f"   • {len(landlords)} landlords")
        print(f"   • ~5 listings per landlord")
        print(f"   • All with real Istanbul addresses and coordinates")
        print(f"   • All with photos from Unsplash")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error creating test listings: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_listings()
