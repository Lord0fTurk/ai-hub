

````markdown
# AI Hub - Unified Desktop AI Chat Client

## Proje Özeti

AI Hub, Google Gemini, OpenAI ChatGPT ve Microsoft Copilot servislerini tek bir Flet tabanlı Windows masaüstü uygulamasında birleştiren modern, modüler ve kullanıcı dostu bir chat arayüzüdür.

- Üç ayrı sekme ile farklı AI servislerine bağlanma  
- API anahtarları şifreli olarak yerel depolamada saklanır  
- Işık/Karanlık tema desteği  
- Chat geçmişi, token kullanımı ve gecikme bilgisi gösterimi  
- API istekleri için otomatik rate limiting ve yeniden deneme  
- Async API çağrıları ile responsive kullanıcı deneyimi  
- İleri seviye hata yönetimi ve logging  

## Kurulum

1. **Python 3.10+ yüklü olduğundan emin olun.**  
2. Projeyi klonlayın veya indirin:  
   ```bash  
   git clone https://github.com/kullanici/ai-hub.git  
   cd ai-hub/src  
````

3. Sanal ortam oluşturun ve aktif edin:

   ```bash
   python -m venv venv  
   source venv/bin/activate  # Windows: venv\\Scripts\\activate  
   ```
4. Gereksinimleri yükleyin:

   ```bash
   pip install -r ../requirements.txt  
   ```
5. İlk çalıştırmada API anahtarlarınızı uygulama ayarlarından girin.

## Kullanım

```bash
python main.py
```

* Ana pencerede üç sekme bulunur: Gemini, ChatGPT, Copilot
* Üst sağ köşeden tema değiştirme ve ayarları açabilirsiniz
* Chat penceresinden mesajlarınızı yazıp gönderin
* Ayarlardan API anahtarlarını yönetebilirsiniz

## Paketleme

PyInstaller ile tek çalıştırılabilir dosya oluşturmak için:

```bash
pyinstaller --onefile --windowed src/main.py
```

## Testler

```bash
pytest tests/
```

## Katkıda Bulunma

Katkılarınız ve önerileriniz için pull request veya issue açabilirsiniz.

## Lisans

MIT License

```
