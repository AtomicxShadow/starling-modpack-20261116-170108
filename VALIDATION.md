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

## İlk gerçek derleme günlüğünden sonra

Kullanıcının GitHub Actions günlüğündeki `E_INVALID_HELPER`, ViaHorizon'un
`legacy_boat_ride` enjeksiyonunda görüldü. Starling 0.8.0'daki `remote_ride`
fonksiyonu `bool` döndürürken yardımcı `ControlFlow<Result<bool>>` döndürüyordu.
Yardımcı `ControlFlow<bool>` ve `Break(true)` kullanacak şekilde düzeltildi.
Eski protokol ve tekne kontrolü korundu; bu özellik kapatılmadı.

Bu incelemede Rust/Cargo kuruldu; aynı horizon-mixins sürümü
`ddd9700b21997c95d95ac6ee5ecafe3830cf622a` derlendi. Starling'in
`native_build.sh` içindeki hazırlama adımları geçici kaynak kopyasında
uygulandı: aynı kaynak commit'i, plan-stub, cfg özniteliğinin çıkarılması,
symlink'lerin çıkarılması, geçici mod pinleri ve resmi native_mod_adapt.py.
Beş modun tamamıyla `horizon-mixins plan` başarılı: **83 enjeksiyon,
106 modül, 2 paket crate'i**. Kaynak dosya özetleri tekrar kontrol edildi.
Ardından `horizon-mixins apply` da aynı beş modla başarılı oldu; kaynak
enjeksiyonları geçici aşama dizinine uygulanabildi.

## Yapılmayan kontroller

Android SDK/NDK bu ortamda yok. Android/Rust oyun derlemesi, APK imzası
doğrulaması ve gerçek cihaz testi yapılmadı. Hazır APK veya Android `.so`
üretilmedi. Başarılı AST planı tam derleme veya Android uyumluluğu iddiası
değildir; sonraki derlemede Rust/API hataları görülebilir.
