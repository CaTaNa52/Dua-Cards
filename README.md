# 1000 – Dua Kartları Uygulaması

Günlük dualar için hazırlanmış, tamamen çevrimdışı çalışan bir flashcard uygulaması.
Tek bir HTML dosyası — kurulum veya hesap gerektirmez.

---

## Özellikler

* **1.000 dua** — Türkce ve Arapça, 40 bölüm hâlinde düzenlenmiş
* **Flashcard gezinmesi** — Önceki / Sonraki / Rastgele
* **Kaydırma hareketleri** — sola kaydır: sonraki, sağa kaydır: önceki
* **Arama** — İngilizce metin, Arapça metin veya bölüm adına göre arama
* **Bölüm filtresi** — duaları konuya göre görüntüleme
* **Favoriler** — ♡ ile dua kaydetme, yalnızca favorileri filtreleme
* **Benim Dualarım** — kendi kişisel dualarınızı çevrimdışı ekleyip saklayın
* **Yazı boyutu kontrolü** — A− ve A+ düğmeleriyle dua metnini büyütüp küçültün
* **Karanlık mod** — telefon temasını takip eder veya manuel olarak değiştirilebilir
* **İlerleme kaydedilir** — dosyayı tekrar açtığınızda kaldığınız yerden devam eder

---

## Dosyalar

| Dosya                            | Açıklama                                                                  |
| -------------------------------- | ------------------------------------------------------------------------- |
| `index.html`                     | Uygulamanın kendisi — ihtiyacınız olan tek dosya                          |
| `build_standalone_flashcards.py` | Kaynak verilerden HTML dosyasını yeniden oluşturmak için kullanılan betik |

---

## HTML Dosyasını Yeniden Oluşturma (isteğe bağlı)

Kaynak JSON verilerinden dosyayı yeniden oluşturmak isterseniz:

```bash
python build_standalone_flashcards.py
```

Python 3 ve bir üst dizindeki `duas_repo/data/` klasörü gereklidir.
