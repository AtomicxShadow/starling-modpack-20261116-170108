# Starling 0.8.0: beş mod için Android derleme kiti

**Durum: kaynak paketi hazırlandı ve statik kontroller yapıldı. Android/Rust
derlemesi ve telefonda çalışma testi yapılmadı. Bu ZIP hazır APK değildir.**

Kullanıcının Horizonmatica telefon derleme kitinin çok modlu sürümü. Aynı
Starling Dev APK'sına şunları eklemeyi dener:

| Mod kimliği | Sürüm |
| --- | --- |
| horizonmatica | 0.3.2-starling.1 |
| mod_menu | 0.3.5 |
| viahorizon | 0.8.8-dev |
| toggle_sprint | 1.0.0 |
| motion_blur | 0.1.0 |

Starling kaynağı 0.8.0 etiketinin tam commit'ine sabittir:
`ac874422ed8f892505ff73d67ae486ecfee7a516`.
Horizonmatica, kullanıcının `horizonmatica-phone-build.zip` paketinden alındı;
`play_mouse` ve `pauses_game` hedefleri için önceki değişiklikler korundu.
ViaHorizon'un `legacy_boat_ride` yardımcısı Starling 0.8.0'daki `bool` dönüş
türüne uyarlandı (`Result<bool>` kaldırıldı). Diğer modların Rust kodu
değiştirilmedi. Starling'in kendi adaptörü ve
horizon-mixins aracı derleme sırasında çalışır. Bunlar tüm API farklarını
çözme garantisi vermez; ilk gerçek derlemede ek uyarlama gerekebilir.

Toggle Sprint ve Motion Blur, gönderilen katalog ZIP'leri yerine mod
yazarlarının ilgili sürümlerinin `.hnmod` paketlerinden alındı. SHA-256
değerleri katalog kayıtlarıyla karşılaştırıldı:

- Toggle Sprint: `b2a4190f9c19adbceae4a639342b7630bfc3047339eabf57673b7807db5edc6a`
- Motion Blur: `4cdaa6369fffea8116b013edfc618358ca989f48ed65c83306d2102f0e506c47`

Kaynaklar ve lisanslar paketin içinde. `sources.lock.json` her mod dosyasının
özetini tutar. Kaynak değiştirildiyse bu kayıt bilinçli olarak güncellenmelidir;
derleme betiği değişiklikleri kendiliğinden onaylamaz.

## Telefondan GitHub Actions ile derle

1. ZIP'i aç. GitHub'da yeni bir depo oluştur ve `starling-modpack-phone-build`
   klasörünün **içeriğini** depo köküne yükle. `.github/workflows/android.yml`
   dosyası da yüklenmeli. GitHub hesabının Actions kullanım kotası geçerlidir.
2. Deponun **Actions > Build mods for Starling 0.8.0 > Run workflow** sayfasını aç.
3. Mod alanını `all` bırakıp başlat. Tek bir modu denemek için örneğin
   `horizonmatica`; bir alt küme için `horizonmatica,mod_menu,toggle_sprint` yaz.
4. Başarılı çalıştırmanın **Artifacts** bölümünden
   `starling-080-modpack-arm64` dosyasını indir.
5. İçindeki Dev APK'yı telefona kur. Resmi Starling'in yanında ayrı uygulama
   olarak kurulur ve kendi oyun klasörünü/kaynak hazırlığını kullanır.

Derleme GitHub'da yapılır. APK'ya eklenmiş modlar için oyun içinden Compile'a
basılmaz. Mod listesini değiştirmek için yeni APK derlenir. Bu kit Android
ARM64 içindir. Üretilen APK deneysel anahtarla imzalanır; sonraki derlemenin
üzerine güncelleme kurulabilmesi garanti değildir. Kaldırma gerekecekse önce
Dev uygulamasındaki dünyalarını dışarı aktar.

Derleme başarısız olursa `build.log` dosyasını veya başarısız adımın Actions
günlüğünü indir. Kaynak/AST/derleyici hatalarının çözümü için bu gerçek günlük
gerekir. Bir mod hatası bütün kombinasyonun derlenmesini durdurabilir; mod
alanından daha küçük bir kombinasyon seçerek ayırabilirsin.

## Bilgisayarda kontrol ve derleme

Python 3.11+ ile yalnızca kaynak bütünlüğü ve paket referansları:

```sh
python3 tools/check.py
```

Starling 0.8.0 kaynağı ile adaptör sonrası hedef dosyaların varlığı:

```sh
python3 tools/check.py --source /path/to/starling-0.8.0
```

Rust, cargo-ndk, Android SDK/NDK ve JDK 25 hazır bir Linux ortamında:

```sh
bash build.sh /path/to/starling-0.8.0 out all
```

Statik kontrol; AST enjeksiyonlarının geçerliliğini, Rust tür uyumluluğunu,
modlar arası davranışı veya telefondaki render/dokunma işleyişini doğrulamaz.
Gerçek derleme ve cihaz testi ayrı aşamalardır.

## ZIP → hazır Android mod çıktısı fikri

`.hnmod` kaynak paketidir. Mevcut native sistem bağımsız mod `.so` dosyalarını
dinamik eklenti olarak bağlamaz; seçilen modları oyun kütüphanesine birlikte
derler. Bu kit APK, `libhorizon_android.so` ve `build.json` üretmeyi hedefler.

Ayrı bir uygulama ZIP seçimini, sürüm/ABI kontrolünü, sunucuda derlemeyi ve
çıktı indirmeyi yönetebilir. Resmi Starling'e hazır çıktının doğrudan aktarımı
için mevcut hazır derleme dağıtım akışına entegrasyon veya yeni bir içe
aktarma özelliği gerekir. `.so` dosyasını `.hnmod` içine koymak tek başına
bunu sağlamaz. Evrensel otomatik uyarlama yerine desteklenen modlar ve
kombinasyonlar üzerinden ilerlemek uygulanabilir.

## Kaynak ve lisanslar

Her modun `mixins/<kimlik>/LICENSE` dosyası korunmuştur. ViaHorizon'un
`THIRD_PARTY_NOTICES.md` dosyası da kendi klasöründedir. Bu paket tüm kaynakları
tek bir lisans altında yeniden lisanslamaz.

- Horizonmatica: https://github.com/keksi2k/horizonmatica (MIT)
- Mod Menu: kullanıcının ModMenuHorizon-main.zip arşivi (MIT)
- ViaHorizon: https://github.com/hhhhsffd/viahorizon (GPL-3.0-or-later)
- Toggle Sprint: https://github.com/CayMac97/toggle-sprint/tree/v1.0.0 (MIT)
- Motion Blur: https://github.com/levzzz5154/horizon-motion-blur/tree/v0.1.0 (MIT)
- Starling: https://github.com/starling-client/starling/tree/v0.8.0
