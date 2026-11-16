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

## İkinci gerçek derleme günlüğünden sonra

GitHub Actions bu kez `horizon-client-lib` derlemesine ulaştı. Mod Menu'nin
`title_buttons.rs` yardımcısındaki `Button` oluşturucusunda `action: None`
bulunuyordu; Starling 0.8.0'ın `title::Button` yapısında böyle bir alan yok.
Yalnızca bu alan çıkarıldı. Düğme kimliği, konumu ve tıklama enjeksiyonu
korundu. Beş modla `horizon-mixins apply` tekrar başarılı oldu.

Linux'ta ses/kontrolcü özellikleri kapalı `cargo check` de çalıştırıldı.
İlk çalıştırma, oyun crate'inde iki ek ViaHorizon uyumsuzluğu gösterdi:
`remote.predictions` bir HashMap değil, Starling'in `BlockPredictions` yapısı.
Doğrudan `remove` ve harita biçimindeki `retain` çağrıları değiştirildi.
Yeni `block_predictions.rs` modülü horizon-mixins ile bu yapının bulunduğu
modüle eklenir; sadece ilgili bloğu veya `sequence` eşiğine kadar tahminleri
unutur. İşlem sayacı ve teleport kaydı değiştirilmez. İlgisiz/yeni tahminler
korunur. Son AST uygulaması **83 enjeksiyon, 107 modül, 2 crate** ile geçti.

Gerçekte dönüştürülmüş `block_predictions.rs` dosyasını ve gerçek
`horizon-core` bağımlılığını kullanan küçük, geçici Cargo test paketiyle
Starling'in 4 mevcut testi ve yeni köprünün 3 davranış testi çalıştırıldı:
**7 geçti, 0 başarısız**. Kaynak veya oyun durumu taklit edilmedi.

Düzeltmelerden sonra beş modun hepsini içeren dönüştürülmüş ağaçta:

```sh
cargo check --locked --lib --no-default-features -p horizon-client
```

**Başarılı** (Rust 1.100.0, Linux x86_64). Bu kontrol `horizon-client-lib`,
render, protokol ve Horizonmatica'nın iki crate'i dahil ortak kodun türlerini
kontrol etti. Linux sistem ses/kontrolcü bağımlılıkları olmadan çalıştırıldı;
Android APK iş akışındaki özellikler kapatılmadı. Android'e özel kod, bağlama,
APK hazırlama ve gerçek cihaz davranışı bu kontrolle doğrulanmaz.

## Yapılmayan kontroller

Android SDK/NDK bu ortamda yok. Android/Rust oyun derlemesi, APK imzası
doğrulaması ve gerçek cihaz testi yapılmadı. Hazır APK veya Android `.so`
üretilmedi. Başarılı AST planı tam derleme veya Android uyumluluğu iddiası
değildir; sonraki derlemede Rust/API hataları görülebilir.
