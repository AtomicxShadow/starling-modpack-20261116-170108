# Yapılan kontroller

- Beş modun kaynak dosyaları ve manifest referansları doğrulandı.
- Paket kaynakları `sources.lock.json` ile eşleşiyor.
- Starling checkout'u `ac874422ed8f892505ff73d67ae486ecfee7a516` ile eşleşiyor.
- Starling'in adaptöründen sonra modül ekleme hedeflerinin dosyaları mevcut.
- Tek mod, bir alt küme ve tüm modlar için seçim kontrolü geçti.
- Geçersiz mod seçiminin ve değiştirilmiş kaynak dosyasının reddedildiği denendi.
- `build.sh` Bash sözdizimi kontrolünden geçti.
- İş akışı YAML yapısı, salt okunur varsayılan yetkisi ve Starling commit'i kontrol edildi.
- İndirilen Toggle Sprint ve Motion Blur paketlerinin SHA-256 değerleri katalogla eşleşti.

## Yapılmayan kontroller

Rust/Cargo ve Android SDK/NDK bu çalışma ortamında kurulu değil; kullanılabilir
disk yaklaşık 7 GB. Bu nedenle horizon-mixins AST plan/apply, Android derlemesi,
APK imzası doğrulaması ve gerçek cihaz testi yapılmadı. Hazır APK veya `.so`
üretilmedi. Bu doğrulama raporu Android uyumluluğu iddiası değildir.

İlk GitHub Actions çalıştırmasının `build.log` çıktısı, gerekli ek API
uyarlamalarını ve kombinasyonun gerçek derlenme durumunu belirleyecek.
