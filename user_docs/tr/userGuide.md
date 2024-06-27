# NVDA NVDA_VERSION Kullanıcı Rehberi

[TOC]

<!-- KC:title: NVDA NVDA_VERSION Komutlar Hızlı Rehber -->



## Giriş {#Introduction}

NVDA'ya hoş geldiniz!

İngilizce dilinde Görsel olmayan Masaüstü Erişimi anlamına gelen ifadenin kısaltması olan (NVDA) Microsoft Windows işletim sistemi için ücretsiz ve açık kaynak bir ekran okuma programıdır.
NVDA bir konuşma sentezleyici ya da braille ile geri bildirim sağlayarak, kör ya da az görenlerin ek bir ücret ödemeden Windows işletim sistemi kurulu bilgisayarları kullanabilmesini mümkün kılar.
NVDA [NV Access tarafından](https://www.nvaccess.org/), camiadan ilgili birçok insanın katkısıyla geliştirilmektedir.

### Genel Özellikler {#GeneralFeatures}

NVDA, kör ve az görenlerin Windows işletim sistemi ve sistemde kurulu birçok farklı uygulamaya erişimine ve bunlarla etkileşimine imkan vermektedir.

NVDA'nın kısaca tanıtıldığı şu [videoya (ingilizce)](https://www.youtube.com/watch?v=tCFyyqy9mqo) NV Access YouTube kanalı üzerinden ULAŞILABİLİR.

Öne çıkan özellikler:

* internet web tarayıcıları, e-posta programları, sohbet programları ve ofis gibi popüler uygulamalara destek
* 80'den fazla dili destekleyen ve programla birlikte kurulan konuşma sentezleyicisi
* Mevcut olduğunda, yazıtipi adı ve boyutu, sitili, ve imla hataları gibi metin biçimlendirmelerinin bildirimi
* Fare altındaki metnin otomatik bildirimi ve fare hareketlerinin isteğe bağlı olarak ses yoluyla ifade edilmesi
* Braille klavyesi bulunanlardan bilgisayar braille girişi yapılmasını ve bir çoğunun bilgisayara bağlandığında otomatik olarak tanınmasını da kapsayan Birçok Braille (kabartma) ekran için destek
* Kuruluma ihtiyaç duyulmaksızın bütün olarak USB bellek veya başka bir taşınabilir aygıttan çalışabilme özelliği
* Kullanımı kolay konuşan kurulum uygulaması
* 54 dile çevrilmiş oluşu
* 32 ve 64 bit dahil modern Windows işletim sistemlerinin desteklenmesi
* Windows Logon ve diğer [güvenli ekranlarda](#SecureScreens) çalışabilme özelliği
* Dokunmatik hareketlerle metin ve kontrollerin bildirimi
* Microsoft Active Accessibility, Java Access Bridge, IAccessible2 ve UI Automation gibi yaygın erişilebilirlik arayüzlerinin desteklenmesi
* Windows Komut İstemi ve Console uygulamalarının desteklenmesi
* Sistem odağını görsel olarak vurgulama özelliği

### sistem gereksinimleri {#SystemRequirements}

* İşletim Sistemleri: Windows 8.1, Windows 10, Windows 11'in tüm 32 bit ve 64 bit sürümleri ve Windows Server 2012 R2'den başlayarak tüm server İşletim Sistemleri. 
  * .Windows'un AMD64 ve ARM64 olmak üzere iki sürümü de desteklenir.
* en az 150 MB depolama alanı.

### Yerel Dil Desteği {#Internationalization}

Dünyada nerede yaşıyor olurlarsa olsunlar ve hangi dili konuşurlarsa konuşsunlar, İnsanların teknolojiye eşit biçimde erişebilmeleri önemlidir.
İngilizcenin yanı sıra, NVDA aşağıda belirtilen 54 dile de çevrilmiştir. Afrikaca, Almanca (Almanya ve İsviçre), Amharca, Aragonca, Arapça, Arnavutça, Bulgarca, Birmanya dili, Çekce, Danimarka dili, Dutch, Farsça, Fince, Fransızca, Galiçyaca, Geleneksel ve basitleştirilmiş Çince, Gürcüce, Hırvatça, Hint dili, İbranice, İspanyolca, İsveç dili, İrlanda Dili, İtalyanca, İzlanda dili, Japonca, Kannada, Katalanca, Kırgızca, Korece, Kolombiya İspanyolcası, Lehçe, Litfanca, Macarca, Makedonca, Moğolca, Nepal dili, Norveççe, Pencap dili, Portekizce (Brazilya ve Portekiz), Rumence, Rusca, Slovence, Sırpça, Slovakca, Tamil dili, Tayca, Türkçe, Ukraynaca, Yunanca, ve Viyetnamca.

### Konuşma Sentezleyici Desteği {#SpeechSynthesizerSupport}

Kendi mesajları ve arayüzünü birçok dilde sağlamanın yanında, NVDA Kullanıcıların bir içeriği konuşma sentezleyiciler aracılığıyla istedikleri dilde okuyabilmelerine olanak tanır.

NVDA ücretsiz, açık kaynak kodlu ve çok dilli bir sentezleyici olan [eSpeak NG](https://github.com/espeak-ng/espeak-ng), sentezleyicisiyle birlikte dağıtılmaktadır.

NVDA tarafından desteklenen diğer sentezleyicilerle ilgili bilgi [Desteklenen Konuşma Sentezleyicileri](#SupportedSpeechSynths) bölümünden alınabilir.

### Braille Desteği {#BrailleSupport}

NVDA birçok braille ekranla çalışabilir.
NVDA metni braille dönüştürmek için açık kaynak  kodlu[LibLouis](https://liblouis.io/)  kullanır.
Braille klavyeyle yapılan kısaltmasız ve kısaltmalı braille girişi de desteklenir.
Ayrıca NVDA varsayılan durumda birçok braille ekranı otomatik olarak algılayacaktır.
Lütfen desteklenen braille ekranlarla ilgili bilgi için [Desteklenen Braille Ekranlar](#SupportedBrailleDisplays) bölümüne bakın.

NVDA birçok dilde kısaltmalı, kısaltmasız ve bilgisayar braille kodlarını desteklemektedir.

### Lisans ve Kopya Hakkı {#LicenseAndCopyright}

NVDA kopya hakkı NVDA_COPYRIGHT_YEARS NVDA katkı sağlayanlarına aittir.

NVDA GNU General Public License (Version 2) (Yeni Genel Kamu Lisansı Sürüm2) ile iki özel istisna dışında kullanılabilir.
İstisnalar, lisans belgesinde "Eklentiler ve Sürücülerdeki GPL Olmayan Bileşenler" ve "Microsoft Dağıtılabilir Kodu" bölümlerinde özetlenmiştir.
NVDA ayrıca farklı ücretsiz ve açık kaynak lisansları altında kullanıma sunulan bileşenleri içerir ve kullanır.
Programı, lisans şartlarına uyduğunuz ve kodlarını isteyen kişilerle de paylaştığınız müddetçe, kullanmakta, dağatmakta ve istediğiniz biçimde değiştirmekte özgürsünüz.
Bu, Özgün ve değiştirilmiş yazılım kopyaları ile, bu kodları kullanan diğer yazılımlar için geçerlidir. 

Daha fazla detay için [Tam lisansı açıp okuyabilirsiniz.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
İstisnalarla ilgili ayrıntılar için "yardım" bölümünün altındaki NVDA menüsünden lisans belgesine erişin.

## NVDA Hızlı Başlangıç Rehberi {#NVDAQuickStartGuide}

Bu rehber,  NVDA'yı indirme, kurma ve ilk çalıştırma olmak üzere üç ana bölümden oluşmaktadır.
Ayrıca yukarıdaki belirtilen konulara ek olarak, NVDA'yı özelleştirme, eklentileri kullanma, NVDA topluluğuna katılma ve yardım alma hakkında da bilgiler içermektedir. 
Bu rehberdeki bilgiler, NVDA Kullanıcı Rehberinin diğer BÖLÜMLERİNİ ÖZETLER NİTELİKTEDİR.
Bahsi geçen konular ve pek çok diğer fazlası hakkında daha ayrıntılı bilgi için lütfen Kullanıcı Rehberine bakın.

### NVDA'yı indirme {#GettingAndSettingUpNVDA}

NVDA herkesin kullanımı için tamamen ücretsizdir.
Lisans anahtarları ya da ödenmesi gereken pahalı abonelikleri yoktur.
NVDA yılda ortalama dört kez güncellenir.
NVDA'nın en son sürümüne [NV Access web sitesi](NVDA_URL)'nin "download" sayfasından ulaşabilirsiniz.

NVDA, Microsoft Windows'un tüm yeni sürümleriyle çalışır.
Sistem gereksinimleri hakkında daha fazla bilgi için[sistem gereksinimleri](#SystemRequirements) bölümünü inceleyebilirsiniz.

#### NVDA'yı İndirme Adımları {#StepsForDownloadingNVDA}

Listelenen bu adımlar, web sayfalarında gezinme konusunda biraz bilgi sahibi olduğunuzu varsaymaktadır.

* Web tarayıcınızı açın (`Windows` tuşuna basın, aşağıdaki adresi yazın ve `enter` tuşuna basın.)
* NV Access indirme sayfasına gitmek için (`alt+d` tuşlarına basın, aşağıdaki adresi yazın veya kopyalayın ve `enter` tuşuna basın): 
https://www.nvaccess.org/download 
* "Download" düğmesine basın
* Kullandığınız tarayıcıya ve ayarlarınıza göre dosyayı indirmek için ekstra bir işlem gerekebilir
* Tarayıcıya bağlı olarak, dosya indirildikten sonra otomatik olarak çalıştırılabilir.
* Dosyanın manuel olarak çalıştırılması gerekiyorsa, bildirim alanına gitmek için `alt+n` tuşlarına, ardından dosyayı çalıştırmak için `alt+r` tuşlarına basın. (Listelenen adımlar farklı tarayıcılarda değişiklik gösterebilmektedir)

### NVDA'yı Kurma {#SettingUpNVDA}

İndirdiğiniz dosyayı çalıştırdığınızda, NVDA'nın geçici bir kopyası açılacaktır.
Daha sonra sizden, NVDA kurulumunu yapmak, taşınabilir bir kopya oluşturmak ve geçici kopyayı kullanmaya devam etmek seçenekleri arasında seçim yapmanız istenecektir.

Kurulum dosyası indirildikten sonra NVDA'nın çalışması veya kurulması için İnternet erişimi gerekmez.
İnternete erişiminiz varsa NVDA otomatik olarak belli aralıklarda güncellemeleri kontrol eder.

#### İndirilen kurulum dosyasını çalıştırma {#StepsForRunningTheDownloadLauncher}

Kurulum dosyasını "nvda_2022.1.exe" veya benzeri bir ad ile bulabilirsiniz.
Güncel sürümü belirtmek için her güncellemede yıl ve sürüm numarası değişir.

1. İndirilen dosyayı çalıştırın.
NVDA'nın geçici kopyası yüklenirken bir melodi çalar.
Yüklendikten sonra, NVDA kurulum süreci boyunca konuşacaktır.
1. NVDA Kurulumu penceresinde ilk odaklı öğe lisans koşullarıdır.
Dilerseniz `Aşağı OK` tuşuna basarak lisans koşullarını okuyabilirsiniz.
1. "Kabul ediyorum" onay kutusuna gitmek için `tab` tuşuna basın, ardından işaretlemek için `boşluk çubuğu`na basın.
1. Seçenekler arasında gezinmek için `tab` tuşuna basın, ardından istediğiniz seçeneğin üzerinde `enter` tuşuna basın.

Seçenekler şunlardır:

* "NVDA'yı bu bilgisayara kur": bu seçenek NVDA'yı bilgisayarlarına kurmak isteyen kullanıcılar içindir.
* "Taşınabilir kopya oluştur": Bu seçenek, NVDA'nın kurulum yapmadan herhangi bir klasöre kurulmasını ve çalıştırılmasını sağlar.
Taşınabilir kopya, yönetici hakları olmayan bilgisayarlarda veya bir USB bellekte NVDA'yı yanınızda taşımanıza yarar. 
Seçildiğinde, NVDA sizi taşınabilir kopya oluşturma sırasında gerekli adımlar ile yönlendirecektir.
Taşınabilir kopya için bilinmesi gereken en önemli bilgi, taşınabilir kopyanın kurulacağı klasördür. 
* "Geçici kopyayla devam et": Bu, NVDA'nın geçici kopyasını çalışır durumda tutar.
Geçici kopya yeni bir sürümdeki özellikleri NVDA'yı yüklemeden test etmeye yarar. 
Seçildiğinde, başlatıcı penceresi kapanır ve NVDA'nın geçici kopyası, çıkılana veya bilgisayar kapatılana kadar çalışmaya devam eder.
Ayarlarda yapılan değişikliklerin kaydedilmediğini unutmayın. 
* "Çıkış": Bu, NVDA'yı herhangi bir işlem yapmadan kapatır.

NVDA'yı her zaman bu bilgisayarda kullanmayı düşünüyorsanız, NVDA'yı kur seçeneğini seçmeniz önerilir.
NVDA'yı kurmak, oturum açtıktan sonra NVDA'nın otomatik olarak başlatılması, Windows oturum açma ve [güvenli ekranlarda](#SecureScreens) NVDA'nın kullanılabilmesi gibi çeşitli özellikler sağlamaktadır.
Bu özellikler taşınabilir ve geçici kopyalarda bulunmaz.
NVDA'nın taşınabilir veya geçici kopyasını çalıştırırken karşılaşabileceğiniz tüm kısıtlamaların ayrıntıları için lütfen [Taşınabilir ve Geçici Kopyaların Kısıtlamaları](#PortableAndTemporaryCopyRestrictions) bölümüne bakın.

NVDA'yı bilgisayarınıza kurmak ayrıca Başlat Menüsü ve masa üstü kısayolları oluşturmayı ve NVDA'nın `kontrol+alt+n` ile başlatılmasını sağlar.

#### Kurulum dosyasından NVDA'nın kurulma adımları {#StepsForInstallingNVDAFromTheLauncher}

Bu adımlarda en çok kullanılan seçenekler açıklanmaktadır.
Daha fazla ayrıntı için lütfen [NVDA'yı Kurma](#InstallingNVDA) bölümüne bakın.

1. Kurulum ekranında lisans sözleşmesini kabul etmek için onay kutusunun işaretli olduğundan emin olun.
1. `Tab` tuşuna, ardından "NVDA'yı bu bilgisayara kur" düğmesine basın.
1. Sonrasında, Windows oturum açma sırasında NVDA'yı kullanma ve bir masa üstü kısayolu oluşturma seçenekleri sizi karşılayacaktır.
Bu seçeneklerin onay kutuları varsayılan olarak işaretlidir.
İsterseniz, bu seçeneklerden herhangi birini değiştirmek için `tab` ve `boşluk çubuğu` tuşlarını kullanabilir veya seçenekleri varsayılan ayarlarında bırakabilirsiniz.
1. Sonra devam etmek için `enter` tuşuna basın.
1. "Bu uygulamanın PC'nizde değişiklik yapmasına izin vermek istiyor musunuz?" diye soran bir Windows "Kullanıcı Hesabı Denetimi (UAC)" iletişim kutusu görüntülenir.
1. UAC istemini kabul etmek için `alt+y` tuşlarına basın.
1. NVDA yüklenirken bir aşama çubuğu görüntülenir.
Bu işlem sırasında NVDA giderek daha yüksek perdeli bir bip sesi çıkarır.
Bu süreç genellikle hızlıca tamamlanır.
1. NVDA kurulumunun başarılı olduğunu bildiren bir iletişim kutusu görüntülenir.
Mesaj, "Kurulu kopyayı başlatmak için Tamam düğmesine basın" şeklinde olacaktır.
Kurulmuş kopyayı başlatmak için `enter` tuşuna basın. 
1. "NVDA'ya Hoş Geldiniz" iletişim kutusu açılır ve NVDA bir karşılama mesajı okur.
Odak noktası "Klavye Düzeni" seçim kutusu üzerindedir.
Varsayılan olarak "Masa üstü" klavye düzeni, bazı işlevler için numaratör tuş takımını kullanır.
İsterseniz, diğer tuşlara numaratör işlevlerini atamak için "Dizüstü" klavye düzenini kullanabilirsiniz. Dizüstü klavye düzenini seçmek için `AşağıOk` tuşuna basın.
1. "Büyük harf kilidini `NVDA` tuşu olarak kullan" seçeneğine gitmek için `tab` tuşuna basın.
`Insert` tuşu varsayılan olarak NVDA tuşu olarak ayarlanmıştır.
`Büyük Harf Kilidi`'ni NVDA tuşu olarak ayarlamak için `Boşluk Çubuğu`'na basın.
Klavye düzeninin NVDA Tuşundan ayrı olarak ayarlandığını unutmayın.
NVDA tuşu ve klavye düzenini daha sonra Klavye Ayarları'ndan değiştirebilirsiniz.
1. Bu ekranda dolaşmak ve diğer seçenekleri ayarlamak için `tab` ve `Boşluk Çubuğu`' tuşlarını kullanın.
Bu seçenekler NVDA'nın otomatik olarak başlayıp başlamayacağını belirler.
1. Sonrasında bu iletişim kutusunu kapatmak için `enter` tuşuna basın.

### NVDA'yı Çalıştırma {#RunningNVDA}

NVDA'nın tüm komutları kullanıcı rehberinde farklı başlıklara ayrılmış şekilde bulunmaktadır.
Komutlar ayrıca "komutlar için çabuk rehber" bölümünde de bulunmaktadır.
"NVDA için Temel Eğitim" modülü, her komutu derinlemesine anlatmaktadır.
"NVDA Temel Eğitimi" (İngilizce), [NV Access Shop](http://www.nvaccess.org/shop) adresinden bulabilirsiniz.

İşte sık kullanılan bazı temel komutlar: 
Tüm komutlara farklı kısayol tuşları atanabilir. Bu listedeki kısayol tuşları varsayılan kısayollardır.

#### NVDA Tuşu {#NVDAModifierKey}

Varsayılan NVDA tuşu, `NumaratörSıfır` (`numLock tuşu` veya `delete`, `home` ve `end` tuşlarının yanındaki `insert` tuşudur. 
NVDA tuşu ayrıca `capsLock` tuşuna da atanabilir.

#### Girdi yardımı {#InputHelp}

Tuşların yerini öğrenmek ve alıştırma yapmak için `NVDA+1` tuşlarına basarak girdi yardımı'nı kullanabilirsiniz.
Girdi yardımı'ndayken, herhangi bir tuşa bastığınızda veya dokunma hareketi yaptığınızda, NVDA bastığınız tuşu bildirecek ve ne işe yaradığını (eğer varsa) açıklayacaktır.
Girdi yardımı açıkken komutlar farklı uygulamalara gönderilmez. 

#### NVDA'yı açıp kapama {#StartingAndStoppingNVDA}

| işlev |Masa üstü kısayolu |Dizüstü Kısayolu |Açıklama|
|---|---|---|---|
|NVDA'yı başlatma |`kontrol+alt+n` |`kontrol+alt+n` |NVDA'yı başlatır veya yeniden başlatır|
|NVDA'dan çıkma |`NVDA+q`, sonra `enter` |`NVDA+q`, sonra `enter` |NVDA'dan çıkar|
|Konuşmayı duraklat veya devam ettir |`şift` |`şift` |Konuşmayı duraklatır. Tuşa tekrar basılması konuşmayı kaldığı yerden devam ettirir|
|Konuşmayı durdur |`kontrol` |`kontrol` |Konuşmayı durdurur|

#### Metin okuma {#ReadingText}

| işlev |Masa üstü kısayolu |Dizüstü Kısayolu |Açıklama|
|---|---|---|---|
|Tümünü oku |`NVDA+AşağıOk` |`NVDA+a` |Mevcut konumdan okumaya başlar ve imleci de taşıyarak metnin sonuna kadar okur|
|Mevcut satırı oku |`NVDA+YukarıOk` |`NVDA+l` |Sistem imlecinin o an üzerinde bulunduğu satırı okur. İki kez basıldığında satır harf harf kodlanır. Üç kez basılırsa, harfler "adana", "bolu", "ceyhan" gibi karakter tanımlarıyla seslendirilir|
|Seçimi oku |`NVDA+şift+YukarıOk` |`NVDA+şift+s` |Seçilen metni okur|
|Panodaki metni oku |`NVDA+c` |`NVDA+c` |Panodaki metni okur|

#### Konum ve diğer bilgileri öğrenme {#ReportingLocation}

| işlev |Masa üstü kısayolu |Dizüstü Kısayolu |Açıklama|
|---|---|---|---|
|Pencere başlığı |`NVDA+t` |`NVDA+t` |Mevcut uygulama ya da aktif pencerenin başlığını okur. İki kez basılırsa, başlığı adana, bolu, ceyhan şeklinde kodlar. Üç kez basılırsa, başlığı panoya kopyalar|
|Odağı bildir |`NVDA+tab` |`NVDA+tab` |Odaklanan mevcut kontrolü bildirir. İki kez basılırsa bilgiler hecelenerek okunur|
|Pencereyi oku |`NVDA+b` |`NVDA+b` |Etkin penceredeki tüm kontrolleri okur (iletişim kutularında kullanışlı olabilir)|
|Durum çubuğunu oku |`NVDA+end` |`NVDA+şift+end` |Eğer saptanırsa, NVDA durum çubuğu bilgisini bildirir. İki kez basıldığında, bilgi hecelenerek okunur. Üç kere basıldığında metin panoya kopyalanır|
|Saati oku |`NVDA+f12` |`NVDA+f12` |Bir kez basmak geçerli saati, iki kez basmak tarihi bildirir. Saat ve tarih bilgisi, sistem ayarlarında sistem tepsisi ayar formatlarına göre bildirilir.|
|Metin biçimini oku |`NVDA+f` |`NVDA+f` |Metin biçimlendirmesini bildirir. İki kez basıldığında bilgileri bir pencerede gösterir|
|Link hedefini bildir |`NVDA+k` |`NVDA+k` |NESNE Sunucusu üzerinde bulunduğu linkin yönlendirdiği web adresini okur. İki kez basıldığında daha kolay incelenebilmesi için web adresini bir pencerede gösterir|

#### NVDA'nın hangi bilgileri okumasınıAyarlama {#ToggleWhichInformationNVDAReads}

| işlev |Masa üstü kısayolu |Dizüstü Kısayolu |Açıklama|
|---|---|---|---|
|Yazılan karakterleri seslendir |`NVDA+2` |`NVDA+2` |Etkinleştirildiğinde, NVDA klavyede yazdığınız tüm karakterleri seslendirir|
|Yazılan sözcükleri seslendir |`NVDA+3` |`NVDA+3` |Etkinleştirildiğinde, NVDA klavyede yazdığınız kelimeyi duyurur.|
|Komut tuşlarını seslendir |`NVDA+4` |`NVDA+4` |Etkinleştirildiğinde, NVDA klavyede bastığınız tüm kısayol tuşlarını seslendirir (örneğin windows+m).|
|Fare izlemeyi aç |`NVDA+m` |`NVDA+m` |Etkinleştirildiğinde, fare ile ekranda dolaşırken, NVDA, fare işaretinin altında bulunan metni söyleyecektir. Bu, ekrandaki bir şeyi nesne dolaşımı yerine, fiziksel olarak fareyi hareket ettirerek bulmanızı sağlar.|

#### Sentezleyici ayar zinciri {#TheSynthSettingsRing}

| işlev |Masa üstü kısayolu |Dizüstü Kısayolu |Açıklama|
|---|---|---|---|
|Sonraki sentezleyici ayarına git |`NVDA+kontrol+SağOk` |`NVDA+şift+kontrol+SağOk` |Sentezleyici ayar zincirinde bir sonraki ayara gider, eğer gidilen ayar sonuncusuysa başa döner.|
|Önceki sentezleyici ayarına git |`NVDA+kontrol+SolOk` |`NVDA+şift+kontrol+SolOk` |Sentezleyici ayar zincirinde bir önceki ayara gider, eğer gidilen ayar sonuncusuysa başa döner.|
|Seçili  sentezleyici ayarını arttır |`NVDA+kontrol+YukarıOk` |`NVDA+şift+kontrol+YukarıOk` |üzerinde bulunduğunuz geçerli sentezleyici ayarını artırır. Örneğin. hızı artırır, bir sonraki sesi seçer, ses seviyesini artırır|
|Seçili sentezleyici ayarını geniş ölçekte arttır |`NVDA+kontrol+pageUp` |`NVDA+şift+kontrol+pageUp` |üzerinde bulunduğunuz geçerli sentezleyici ayarını  daha geniş bir ölçekte artırır. Örneğin. konuşma ayarındayken 20 ses ileri gider veya ses seviyesi veya ses perdesi gibi sürgülü alanlarda değeri 20 arttırır|
|Seçili sentezleyici ayarını azalt |`NVDA+kontrol+AşağıOk` |``NVDA+şift+kontrol+`AşağıOk` |üzerinde bulunduğunuz geçerli sentezleyici ayarını azaltır. Örneğin. hızı azaltır, bir önceki sesi seçer, ses seviyesini azaltır|
|Seçili sentezleyici ayarını geniş ölçekte azalt |`NVDA+kontrol+pageDown` |`NVDA+şift+kontrol+pageDown` |üzerinde bulunduğunuz geçerli sentezleyici ayarını  daha geniş bir ölçekte azaltır Örneğin. konuşma ayarındayken 20 ses geri gider veya ses seviyesi veya ses perdesi gibi sürgülü alanlarda değeri 20 azaltır|

Ayrıca, [Girdi hareketleri iletişim kutusu](#InputGestures)'nda bulunan konuşma kategorisinden özel girdiler atayarak Seçili sentezleyici ayarının ilk veya son değerini ayarlayabilirsiniz.
Örneğin hız ayarında olduğunuzda hızı 0 veya 100a ayarlamanıza yarar.
Konuşma ayarındayken ilk ve son konuşucuyu ayarlar.

#### Web Dolaşımı {#WebNavigation}

Tek Tuşla Dolaşım komut listesine kullanıcı rehberinin [Tarama kipi](#BrowseMode) bölümünden ulaşılabilir.

| işlev |kısayol |Açıklama|
|---|---|---|
|Başlık |`h` |Sonraki başlığa git|
|Başlık seviyesi 1, 2 veya 3 |`1`, `2`, `3` |Belirtilen düzeyde bir sonraki başlığa git|
|Form alanı |`f` |Sonraki form alanına gider (yazma kutuları, düğmeler vb.)|
|Link |`k` |Sonraki linke git|
|Sınır imi |`d` |Sonraki sınır imine git|
|Liste |`l` |Sonraki listeye git|
|Tablo |`t` |Sonraki tabloya git|
|Geri git |`şift+Harf` |basılan türde önceki öğeye gitmek için `şift` tuşuna ve yukarıdaki harflerden herhangi birine basın|
|Öğe listesi |`NVDA+f7` |Linkler ve başlıklar gibi çeşitli öğe türlerini listeler|

### tercihler {#Preferences}

NVDA'nın birçok işlevi, NVDA ayarları iletişim kutusundan değiştirilebilmektedir.
Ayarlara ve diğer seçeneklere NVDA menüsüne giderek ulaşılmaktadır.
NVDA menüsünü açmak için `NVDA+n` tuşlarına basın.
Direkt NVDA genel ayarlar iletişim kutusunu açmak için `NVDA+kontrol+g` tuşlarına basın.
Çoğu ayar ekranına hızlıca gitmek için atanmış kısayol tuşları bulunmaktadır. Örneğin, sentezleyici iletişim kutusunu açmak için `kontrol+NVDA+S` tuşlarına, diğer konuşma ayarlarına gitmek için `kontrol+NVDA+V` tuşları kullanılabilir.

### Eklentiler {#Addons}
Eklentiler, NVDA için yeni veya değiştirilmiş işlevsellik sağlayan programlardır.
Eklentiler NVDA topluluğu veya harici şirketler tarafından geliştirilir ve NV Access'e bağlı değildir.
Her yazılımda olduğu gibi, bir eklentiyi kullanmadan önce geliştiricisine güvenmek önemlidir
Kurulumdan önce eklentileri doğrulamanın yolları için lütfen [Eklentileri Yükleme](#AddonStoreInstalling) bölümüne bakın.

Eklenti Mağazası ilk açıldığında, NVDA eklentiler hakkında bir uyarı görüntüler.Eklentiler NV Access tarafından incelenmez ve sınırsız işlevselliğe ve bilgiye erişime sahip olabilir.
Eklentiler NV Access tarafından denetlenmez ve kısıtlanmamış işlevselliğe ve bilgiye erişime sahip olabilir.
Uyarıyı okuduysanız ve bir daha görmek istemiyorsanız `boşluk" tuş`'na basın.
"Tamam" düğmesine ulaşmak için `sekme` tuşuna, ardından uyarıyı kapatmak ve mağazaya dönmek için `enter` tuşuna basın.
Kullanıcı Rehberinin  "[Eklentiler ve Eklenti Mağazası](#AddonsManager)" Eklenti Mağazasının her özelliği hakkında bilgi bulunmaktadır.

Eklenti Mağazasına Araçlar alt menüsünden erişilebilir.
NVDA menüsünü açmak için `NVDA+n`ye sonra araçlar için `r`ye, ardından Eklenti Mağazası için `m`ye basın.
Eklenti Mağazası açıldığında, herhangi bir eklenti kurulu değilse "Kullanılabilir eklentiler" penceresi  gösterilir.
Eklentiler kurulduğunda Eklenti Mağazası "Kurulu eklentiler" sekmesini açar.

#### Kullanılabilir eklentiler {#AvailableAddons}
Pencere ilk açıldığında eklentilerin yüklenmesi birkaç saniye sürebilir.
Eklentiler listesi yüklendikten sonra NVDA ilk eklentinin adını okuyacaktır.
Kullanılabilir eklentiler bir listede alfabetik olarak listelenir.
Listeye göz atmak ve belirli bir eklenti hakkında bilgi edinmek için:

1. Listede gezinmek için ok tuşlarını kullanın veya bir eklenti adının ilk harfine basın.
1. Seçili eklentinin açıklamasına gitmek için `tab` tuşuna bir kez basın.
1. Açıklamanın tamamını okumak için [okuma tuşlarını](#ReadingText) veya ok tuşlarını kullanın.
1. Diğer eylemlerin yanı sıra eklentiyi kurma için kullanılabilecek "İşlemler" düğmesine gitmek için `sekme` tuşuna basın.
1. Yayıncı, sürüm ve ana sayfa gibi ayrıntıları listeleyen "Diğer Ayrıntılar"a gitmek için `sekmeye` basın.
1. Eklentiler listesine dönmek için alt+k veya `şift` `+sekme tuşlarına` listeye ulaşana kadar basın.

#### Eklentileri Arama {#SearchingForAddons}
Mevcut tüm eklentilere göz atmanın yanı sıra, gösterilen eklentileri filtrelemek de mümkündür.
Arama yapmak için `alt+a tuşlarına` basarak "ara" alanına gidin ve aranacak metni yazın.
Arama eklenti kimliği, görünen ad, yayıncı, yazar veya açıklama gibi bilgileri arar.
Arama terimleri yazılırken liste otomatik olarak güncellenir.
İşiniz bittiğinde, filtrelenmiş eklenti listesine gitmek ve sonuçları görüntülemek için `sekme` tuşuna basın.

#### Eklentileri kurma {#InstallingAddons}

Bir eklentiyi kurmak için:

1. Kurmak istediğiniz bir eklentiye odaklanarak entertuşuna `basın`.
1. Eylemler menüsü, kullanılabilecek eylemlerin bir listesini içeren bir açılır menüdür. Bu menüdeki ilk eylem "kur"dur.
1. Eklentiyi kurmak için `K` veya `aşağıOk`  tuşlarına basarak  "kur" ardından `enter` tuşuna basın.
1. Odak, listedeki eklentiye geri döner ve NVDA eklenti hakkındaki ayrıntıları okuyacaktır.
1. NVDA tarafından bildirilen "Durum" bilgisi "Kullanılabilir"den "İndiriliyor"a değişir.
1. Eklentinin indirilmesi tamamlandıktan sonra durum bilgisi "İndirildi" olarak değişecektir. Kurulum bekleniyor ".
1. Aynı anda yüklemek istediğiniz diğer eklentilerle işlemleri tekrarlayın.
1. Bitirdikten sonra, odak "Kapat" düğmesine gelene kadar `sekmeye` basın, ardından entertuşuna `basın`.
1. İndirilen eklentiler, Eklenti Mağazası kapatıldıktan sonra kurulacaktır.
kurulum sırasında eklentiler yanıtlamanız gereken iletişim kutuları görüntüleyebilir.
1. Eklentiler kurulduğunda , değişikliklerin tamamlandığını bildiren bir iletişim kutusu görüntülenir ve eklenti kurulumun tamamlanması için NVDA'yı yeniden başlatmanız istenir.
1. NVDA'yı yeniden başlatmak için `Enter` tuşuna basın.

#### Kurulu eklentileri yönetme {#ManagingInstalledAddons}
Eklenti Mağazasının sekmelerinde gezinmek için `control+tab` tuşlarına basın.
Sekmeler şunları içerir: "Kurulu eklentiler "," Güncellenebilen eklentiler ", "Mağazadaki eklentiler" ve "Kurulu uyumsuz eklentiler ".
+Sekmelerin her biri, bir eklenti listesi, seçilen eklenti hakkında daha fazla ayrıntı için bir panel ve seçilen eklenti için eylemler gerçekleştirmek için bir düğme olacak şekilde birbirine benzer tasarlanmıştır.
Kurulu eklentilerin eylemler menüsü, "Kur" yerine "Devre Dışı Bırak" ve "Kaldır" ı içerir.
Bir eklentinin devre dışı bırakılması, NVDA'nın onu başlatmasını  durdurur, ancak eklenti kurulu kalmaya devam eder.
Devre dışı bırakılmış bir eklentiyi yeniden etkinleştirmek için, eylemler menüsünden "Etkinleştir"  düğmesine basın.
Eklentileri etkinleştirdikten, devre dışı bıraktıktan veya kaldırdıktan sonra, Eklenti Mağazasını kapatırken NVDA'yı yeniden başlatmanız istenecektir.
Bu değişiklikler yalnızca NVDA yeniden başlatıldığında geçerli olacaktır.
Eklenti mağazasında `escape` tuşunun Kapat düğmesiyle aynı şekilde çalıştığını unutmayın.+

#### Eklentileri Güncelleme {#UpdatingAddons}
Kurduğunuz bir eklentide güncelleme olduğunda, "Güncellenebilir eklentiler" sekmesinde listelenecektir.
Eklenti Mağazası'ndaki herhangi bir yerden bu sekmeye ulaşmak için `control+sekme` tuşlarına basın.
Eklentinin durumu "Güncelleme mevcut" olarak listelenecektir.
Listede  mevcut kurulu sürüm ve yüklenebilir güncel sürüm görüntülenecektir.
Eylem listesini açmak için eklentide `enter` tuşuna basın ve "Güncelle" yi seçin.

### Topluluk {#Community}

NVDA'nın dinamik bir kullanıcı topluluğu bulunmaktadır. 
Örneğin, [İngilizce e-posta listesi](https://nvda.groups.io/g/nvda) veya yerel dil gruplarını bulabileceğiniz ve farklı NVDA topluluklarını listeleyen [https://github.com/nvaccess/nvda-community/wiki/Connect] gibi birçok topluluk bulunmaktadır.
NVDA'nın üreticileri olan NV Access, [Twitter](https://twitter.com/nvaccess) ve [Facebook](https://www.facebook.com/NVAccess) sayfalarında aktif olarak yer almaktadır.
NV Access'in ayrıca düzenli periyotlarla güncellenen bir [İnprocess blogu](https://www.nvaccess.org/category/in-process/) vardır.

Ayrıca bir [NVDA Certified Expert](https://certification.nvaccess.org/) programı da mevcuttur.
Bu program, NVDA'daki becerilerinizi göstermek için tamamlayabileceğiniz çevrimiçi bir testten oluşmaktadır.
[NVDA Sertifikalı Uzman websitesi](https://certification.nvaccess.org/) üzerinden iletişim bilgilerini ve ilgili iş ayrıntılarını görüntüleyebilirsiniz.

### Yardım Alma {#GettingHelp}

NVDA ile ilgili yardım almak için `nvda+n` tuşlarına basın, ardından yardım altmenüsüne gitmek için `a` tuşuna basın. 
Bu alt menüden Kullanıcı Rehberine, Komutlar İçin Çabuk Rehbere, ne yeni dosyasına ve daha fazlasına ulaşılabilir.
Bu ilk üç seçenek, varsayılan web tarayıcınızda açılacaktır.
Ayrıca [NV Access Shop](https://www.nvaccess.org/shop) adresinde daha kapsamlı Eğitim Materyalleri bulunmaktadır.

Başlangıç için "NVDA temel eğitimi" (İngilizce) modülü önerilmektedir.
Bu modül, başlangıçtan itibaren web'de gezinmeden nesne sunucusunu kullanmaya kadar birçok konuyu kapsamaktadır.
Modüle aşağıdaki formatlarda ulaşabilirsiniz:

* [elektronik metin, Word DOCX, Web sayfası HTML, eBook ePub ve Kindle KFX Formatlarında](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/).
* [İnsan-sesi MP3 formatında](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* Dünyanın her yerine teslim edilecek şekilde [Basılı kopya UEB Braille formatında](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) .

Diğer modüller ve indirimli [NVDA Üretkenlik Paketi](https://www.nvaccess.org/product/nvda-productivity-bundle/) gibi modüllere [NV Access Shop](https://www.nvaccess.org/shop/) adresinden ulaşılabilir.

NV Access ayrıca bloklar halinde veya [NVDA Verimlilik Paketi](https://www.nvaccess.org/)'nin bir parçası olarak [telefon desteği](https://www.nvaccess.org/product/nvda-telephone-support/) vermektedir.
Telefon desteği, Avustralya ve ABD'deki yerel numaraları içermektedir.

Yukarıda belirtilen yollar dışında [NVDA Topluluğu e-posta listesi](https://github.com/nvaccess/nvda-community/wiki/Connect) ve [sertifikalı NVDA uzmanları](https://certification.nvaccess.org/) kaynaklarından da destek alınabilir.

[GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md) üzerinden hata bildirimi veya önerilerde bulunabilirsiniz.
Ayrıca, NVDA'ya katkıda bulunmak için aşağıdaki [katkıda bulunma yönergeleri](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) önemli bilgiler içermektedir.

## Daha Fazla Kurulum Seçeneği {#MoreSetupOptions}
### NVDA'yı Kurma {#InstallingNVDA}

NVDA'yı doğrudan indirdiğiniz dosya üzerinden kuruyorsanız, NVDA'yı kur düğmesine basın.
Bu iletişim kutusunu kapattıysanız ya da kurulumu taşınabilir kopya üzerinden yapmak istiyorsanız, lütfen NVDA Araçlar menüsü altında bulunan NVDA'yı Kur menü ögesini bulup çalıştırın.

Karşınıza çıkan kurulum iletişim kutusu, sizi yeni bir kurulum yapılacağı ya da mevcut kurulumun güncelleneceği yönünde bilgilendirecek ve onayınızı isteyecektir.
Devam düğmesine basarak kurulumu başlatabilirsiniz.
Bu iletişim kutusunda, aşağıda açıklanan birkaç seçenek daha bulunmaktadır.
Kurulum bittiğinde, sürecin başarıyla tamamlandığını belirten bir mesajla karşılaşacaksınız.
Bu noktada Tamam'a basmanız NVDA'nın kurulmuş olan kopyasını başlatacaktır.

#### Uyumsuz eklentiler uyarısı {#InstallWithIncompatibleAddons}

Zaten yüklü olan eklentileriniz varsa, uyumsuz eklentilerin devre dışı bırakılacağı konusunda da bir uyarı olabilir.
Devam düğmesine basmadan önce, bu eklentilerin devre dışı bırakılacağını anladığınızı doğrulamak için onay kutusunu kullanmanız gerekir.
Devre dışı bırakılacak eklentileri incelemek için bir düğme de bulunacaktır.
Bu düğme hakkında daha fazla yardım için [uyumsuz eklentiler iletişim kutusu bölümüne](#incompatibleAddonsManager) bakın.
Kurulum sonrası, [Eklenti Mağazası](#AddonsManager) bölümünden uyumsuz eklentileri kendi sorumluluğunuzda etkinleştirebilirsiniz.

#### Windows Giriş Ekranında NVDA'yı Kullan {#StartAtWindowsLogon}

Bu seçenek NVDA'nın Windows giriş ekranında, parolanızı girmeden önce otomatik olarak başlayıp başlamayacağını belirlemenizi sağlar.
Bu, kullanıcı hesabı denetimi (UAC) ekranı ve diğer [güvenli ekranlar](#SecureScreens) için de geçerlidir.
Bu seçenek yeni kurulumlar için varsayılan olarak etkindir.

#### Masaüstünde Kısayol Oluştur (kontrol+alt+n) {#CreateDesktopShortcut}

Bu seçenek NVDA'nın başlatılması için bir masaüstü kısayolu oluşturmanızı sağlar. 
Kısayol oluşturulduğu taktirde, NVDA'nın başlatılması için bir kısayol tuşu da `kontrol+alt+n` atanır.

#### Taşınabilir Konfigürasyonu Mevcut Kullanıcı Hesabına Kopyala {#CopyPortableConfigurationToCurrentUserAccount}

Bu seçenek, çalışmakta olan NVDA için kullanılan konfigürasyonun, kurulacak NVDA için de geçerli olmasını belirlemenize olanak tanır. 
Bu, konfigürasyonu yalnızca mevcut kullanıcı için kopyalar, başka kullanıcıların ayarları ya da [güvenli ekranlarda](#SecureScreens) için kullanılan konfigürasyon değiştirilmez.
Bu seçenek yalnızca kurulumu NVDA taşınabilir kopyası üzerinden yaparken sunulur, doğrudan ana kurulum paketini kullanarak yapacağınız kurulumlarda gösterilmez.

### Taşınabilir Bir Kopya Oluşturma {#CreatingAPortableCopy}

Doğrudan indirdiğiniz dosyayı çalıştırarak NVDA taşınabilir kopyasını oluşturmak istiyorsanız, Taşınabilir Kopya Oluştur düğmesine basmanız yeterli.
Bu iletişim kutusunu kapattıysanız ya da bilgisayarınızda NVDA kurulu durumdaysa, lütfen NVDA Araçlar menüsü altında bulunan Taşınabilir Kopya Oluştur menü ögesini bulup çalıştırın.

Karşınıza çıkacak iletişim kutusu, taşınabilir kopyanın oluşturulacağı yeri belirlemenize olanak tanır.
Bu, yerel diskinizde bulunan bir klasör ya da USB bellek benzeri taşınabilir ortamda bulunan bir konum olabilir.
Burada, aktif kullanıcının NVDA konfigürasyonunu, yeni oluşturulacak taşınabilir kopya için de geçerli kılmanızı sağlayacak bir seçenek de bulunmaktadır.
Seçenek yalnızca, taşınabilir kopya oluşturma işlemini kurulu bir NVDA üzerinden yapıyorsanız geçerlidir, ana kurulum paketi üzerinden yapılan oluşturma işlemlerinde gösterilmez.
Devam düğmesine basmanız taşınabilir kopyayı oluşturacaktır.
Oluşturma işlemi bittiğinde, sürecin başarıyla tamamlandığını bildiren bir mesajla karşılaşırsınız.
Bu iletişim kutusunu kapatmak için Tamam'a basabilirsiniz.

### Taşınabilir Kopya Kısıtlamaları {#PortableAndTemporaryCopyRestrictions}

NVDA'yı bir USB sürücüde veya başka bir ortamda yanınızda taşımak istiyorsanız, taşınabilir bir kopya oluşturmanız önerilir. 
Bir taşınabilir kopyayı istediğiniz zaman NVDA'yı kurmak için kullanabilirsiniz. 
Bilgisayarınıza kurulu NVDA kopyası üzerinden de taşınabilir kopya oluşturabilirsiniz. 
Ancak, NVDA'yı CD gibi salt okunur bir ortama kopyalamak isterseniz, sadece indirdiğiniz kurulum dosyasını kopyalamanız yeterlidir. 
Taşınabilir Kopyanın doğrudan salt okunur ortamdan çalıştırılması şu anda desteklenmemektedir.

[NVDA Kurulum dosyası](#StepsForRunningTheDownloadLauncher), NVDA'nın geçici bir kopyası olarak kullanılabilir.
Geçici kopyalar, NVDA ayarlarının kaydedilmesini engeller.
Bu, [Eklenti Mağazası](#AddonsManager) kullanımının devre dışı bırakılmasını da içerir.

NVDA'nın taşınabilir ve geçici kopyaları aşağıdaki kısıtlamalara tabidir:

* Oturum açma sırasında ve/veya sonrasında otomatik olarak başlayamaması.
* Eğer taşınabilir kopya yönetici haklarıyla çalıştırılmadıysa (önerilmez<) Yönetici haklarıyla çalıştırılmış uygulamalarda taşınabilir kopyanın çalışmaması 
* Yönetici izni isteyen bir uygulamayı başlatmaya çalışırken Kullanıcı Hesabı Denetimi (UAC) ekranlarını okuyamaması<
* Dokunmatik ekran desteğinin olmaması
* Windows Mağazası uygulamalarında tarama kipi ve yazılan karakterlerin söylenmesi gibi özelliklerin kullanılamaması
* Ses zayıflamasının kullanılamaması gibi kısıtlamalar bulunmaktadır. 

## NVDA'ya Başlarken {#GettingStartedWithNVDA}
### NVDA'yı açma {#LaunchingNVDA}

NVDA'yı yükleyiciyle bilgisayarınıza kurduysanız, programı kontrol+alt+n tuşlarına basarak veya başlat menüsündeki programlar altındaki NVDA menüsünden kolayca başlatabilirsiniz.
Ayrıca Çalıştır bölümüne NVDA yazıp entır tuşuna basarak da programı başlatabilirsiniz.
NVDA zaten çalışıyorsa, yeniden başlatılır.
Ek olarak, NVDA'yı kapatmak için (-q), eklentileri devre dışı bırakmak için (--disable-addons), gibi bazı [komut satırı seçeneklerini](#CommandLineOptions) de kullanabilirsiniz.

Kurulu kopyalar için, NVDA, varsayılan olarak konfigürasyonu mevcut kullanıcının roaming application data klasörüne kaydeder (örneğin, "`C:\\Users\\<user>\\AppData\\Roaming`").
Bunu, NVDA'nın konfigürasyonunu local application data klasörüne kaydedecek şekilde değiştirmek mümkündür.
Daha fazla detay için [sistem çapında geçerli parametreler](#SystemWideParameters) hakkındaki bölüme bakın.

Taşınabilir sürümü başlatmak için, NVDA taşınabilir kopyasını oluşturduğunuz dizine gidin ve NVDA'.exe dosyası üzerinde girişe basın veya çift tıklatın.
NVDA zaten çalışıyorsa, taşınabilir sürüme başlamadan önce otomatik olarak kapanacaktır.

NVDA başlarken, kalından inceye doğru yükselen bir dizi ses duyacaksınız. bu NVDA'nın açıldığını anlatmak içindir.
Bilgisayarınızın hızına bağlı olarak, ya da NVDA'yı USB bellek gibi daha yavaş bir yerden çalıştırıyorsanız, programın başlaması biraz zaman alabilir.
Programın başlaması daha fazla zaman alıyorsa, NVDA "NVDA başlıyor, Lütfen bekleyiniz..." şeklinde bir Uyarı vermelidir.

Bunlardan hiçbirini duymuyorsanız, ya da Windows'un hata sesini veya kalınlaşan bir dizi ses duyuyorsanız, NVDA'nın bir hatası var demektir ve programı geliştirenlere bu olası sorunu bildirmeniz gerekebilir.
Bunu nasıl yapacağınızı öğrenmek için lütfen NVDA web sayfasını ziyaret edin.

#### Hoş Geldiniz İletişim Kutusu {#WelcomeDialog}

NVDA ilk kez başladığında, NVDA değişken tuşu ve NVDA menüsü hakkında temel bilgiler veren bir iletişim kutusuyla karşılanacaksınız.
Lütfen bu konularla ilgili sonraki bölümlere bakın.
Bu iletişim kutusunda ayrıca bir seçim kutusu ve üç onay kutusu bulunmaktadır.
Seçim kutusu klavye düzenini belirlemenizi sağlar.
Birinci onay kutusu büyük harf kilidi tuşunun NVDA değişken tuşu olarak kullanılıp kullanılmayacağını kontrol ederken;
ikincisi, NVDA'nın Windows başladıktan sonra otomatik olarak devreye girmesiyle ilgilidir ve yalnızca kurulu NVDA kopyaları için geçerlidir.
Üçüncüsü de, karşılaştığınız hoşgeldin iletişim kutusunun NVDA her açıldığında gösterilip gösterilmeyeceğini kontrol eder.

#### Veri kullanım istatistikleri iletişim kutusu {#UsageStatsDialog}

2018.3 sürümünden itibaren, kullanıcılara NVDA'yı iyileştirmek için kullanım verilerinin NV Access'e gönderilmesine izin vermek isteyip istemedikleri sorulur. 
NVDA'yı ilk kez başlatırken, NVDA'yı kullanırken NV Access'e veri göndermeyi kabul etmek isteyip istemediğinizi soran bir iletişim kutusu açılacaktır.
NV Access tarafından toplanan veriler hakkında daha fazla bilgiyi genel ayarlar bölümünde, [NV Access'in NVDA kullanım istatistiklerini toplamasına izin verin](#GeneralSettingsGatherUsageStats) diyerek okuyabilirsiniz.
Not: "evet" veya "hayır" a basmak bu ayarı kaydeder ve NVDA'yı yeniden yüklemediğiniz sürece iletişim kutusu bir daha asla gösterilmez.
Ancak NVDA'nın genel ayarlar panelinde veri toplama işlemini manuel olarak etkinleştirip devre dışı bırakabilirsiniz. Bu ayarı manuel olarak değiştirmek için, [NVDA kullanım verilerini toplaması için NVDA projesine izin ver](#GeneralSettingsGatherUsageStats) adlı onay kutusunu işaretleyebilir veya işaretini kaldırabilirsiniz.

### NVDA Klavye Komutları Hakkında {#AboutNVDAKeyboardCommands}
#### NVDA Tuşu {#TheNVDAModifierKey}

NVDA'ya özel birçok klavye komutu NVDA değişken tuşu adı verilen özel bir tuş ile klavyedeki başka tuşlara basılarak meydana gelen kombinasyonlardan oluşmaktadır.
Masaüstü klavye düzeninde sadece numaratördeki tuşları kullanan metin inceleme komutları istisnai durumlardandır ve elbette başka istisnalar da olabilir.

Numaratördeki insert, diğer insert, veya büyük harf kilidi tuşlarından birisi NVDA değişken tuşu olarak ayarlanabilir.
Varsayılan olarak, numaratördeki insert ve diğer insert tuşlarının her ikisi NVDA değişken tuşu olarak atanmıştır.

NVDA değişken tuşu olarak atadığınız bir tuşun, kendi özgün görevini yapmasını istiyorsanız, (Örneğin NVDA tuşu olarak büyük harfkilidi tuşunu ayarladıysanız, büyük harf kilidini açabilmek için), bu tuşa peşpeşe 2 kez basmanız gerekir.

#### Klavye Düzenleri {#KeyboardLayouts}

NVDA halihazırda 2 klavye düzeniyle gelmektedir.
NVDA ilk kurulduğunda masaüstü klavye düzeni etkindir ancak dizüstü bilgisayar kullanıyorsanız bunu  [NVDA Ayarları](#NVDASettings) altındaki klavye kategorisinden değiştirebilirsiniz.

Masaüstü düzeni numara kilidi kapalıyken çoğunlukla numaratörü kullanır.
Birçok dizüstü bilgisayarın fiziki bir numaratörü olmamasına karşın, Bazı dizüstü bilgisayarlar FN tuşuyla birlikte sağ elin kullandığı 7 8 9 u ı o j k l gibi tuşlara basarak bu işlevi yapabilirler.
Dizüstü bilgisayarınız bunu yapamıyorsa veya numaratörü kapamanıza izin vermiyorsa, dizüstü klavye düzenine geçmek isteyebilirsiniz.

### NVDA Dokunma Hareketleri {#NVDATouchGestures}

NVDA'yı dokunmatik ekranı olan bir cihaz üzerinde kullanıyorsanız, NVDA'yı dokunmatik hareketlerle de kontrol edebilirsiniz.
NVDA çalışırken, dokunma etkileşimi desteği devre dışı bırakılmadıkça, tüm dokunma girdileri doğrudan NVDA'ya gönderilir.
Dolayısıyla, NVDA çalışmıyorken normal olarak gerçekleştirilen işlemler NVDA açıkken yapılmaz.
<!-- KC:beginInclude -->
Dokunma etkileşimi desteğini açıp  kapatmak için, NVDA+kontrol+alt+t tuşlarına basın.
<!-- KC:endInclude -->
[dokunma etkileşimi desteği](#TouchSupportEnable) NVDA ayarlarının Dokunma Etkileşimi kategorisinden de etkinleştirilip devre dışı bırakılabilir.

#### Ekranı İnceleme {#ExploringTheScreen}

Dokunmatik ekranla Gerçekleştirebileceğiniz en temel işlem ekranda herhangi bir noktada bulunan metin ya da kontrolü seslendirmektir.
Bunu yapmak için, ekranda herhangi bir yere bir parmağınızla dokunun.
Parmağınızı ekranda gezdirerek diğer metin ya da kontrollerin seslendirilmesini de sağlayabilirsiniz.

#### Dokunma Hareketleri {#TouchGestures}

Kullanıcı rehberinin geri kalanında NVDA komutları açıklanırken , bir işlemin gerçekleşmesi için yapılması gereken dokunma hareketi de listelenebilir.
Aşağıda, dokunmatik ekranda çalışan NVDA ile ilgili komutların gerçekleşmesi için yapılabilecek dokunma hareketleri açıklanmaktadır.

##### Dokunmalar {#Taps}

Ekrana, bir ya da birkaç parmakla dokunun.

Bir parmakla bir kez dokunmak anlamında "bir dokunma" ifadesi kullanılır.
Aynı zamanda iki parmakla dokunmak anlamında da "iki parmakla dokunma" ifadesi kullanılır.

Aynı dokunma hareketi arka arkaya yapılırsa,, NVDA bunu çoklu-dokunma hareketi olarak algılar.
İki kez dokunmak çift dokunma olarak algılanır.
Üç kez dokunmak da benzer şekilde üçlü dokunma olarak algılanır.
Tabii bu çoklu-dokunma hareketleri de birden fazla parmakla yapılabilir. Dolayısıyla, iki parmakla çift dokunma, üç parmakla üçlü dokunma vb hareketler de kullanılabilir.

##### Fiskeler {#Flicks}

Parmağınızı ekranda hızlı bir şekilde kaydırın.

Kaydırdığınız yöne göre dört olası fiske hareketi vardır: sola fiske, sağa fiske, yukarı fiske ve aşağı fiske.

Dokunmalarda olduğu gibi, fiske hareketleri için birden fazla parmak kullanılabilir.
Dolayısıyla iki parmakla sağa fiske, dört parmakla yukarı fiske gibi hareketler mümkündür.

#### Dokunma Kipleri {#TouchModes}

Mümkün olan dokunma hareketlerinden daha fazla NVDA komutu bulunduğu için, NVDA, arasında geçiş yapabileceğiniz birden fazla dokunma kipine sahiptir.
Şİmdilik, varolan iki kip, metin kipi ve nesne kipidir.
Bu belgede listelenen bazı NVDA komutları, komut sonrasında parantez içinde belirtilecek kipler için geçerli olabilir.
Örneğin, yukarı fiske (metin kipi) ifadesi bu komutun gerçekleştireceği işlemin metin kipi için geçerli olduğu anlamına gelir.
Komutla ilgili herhangi bir kip verilmemişse, tüm kipler için geçerli olduğu anlamına gelir.

<!-- KC:beginInclude -->
Dokunma kipleri arasında geçiş yapmak için, üç parmakla bir kez dokunun.
<!-- KC:endInclude -->

#### Dokunmatik klavye {#TouchKeyboard}

Dokunmatik klavye, dokunmatik ekrandan metin ve komut girmek için kullanılır.
Odak bir düzenleme alanındayken, ekranın altındaki dokunmatik klavye simgesine iki kez dokunarak dokunmatik klavyeyi etkinleştirebilirsiniz.
Microsoft Surface Pro gibi tabletler için, klavye uzatıldığında dokunmatik klavye her zaman mevcuttur.
Dokunmatik klavyeyi kapatmak için, dokunmatik klavye simgesine çift dokunun ya da düzenleme alanından uzaklaşın.

Dokunmatik klavye etkinken, tuşları bulmak için genellikle ekranın alt kısmında bulunan dokunmatik klavyenin üzerinde parmağınızı hareket ettirin, sonra klavye üzerinde bir parmağınızla dolaşın.
Basmak istediğiniz tuşu bulduğunuzda, [dokunmatik etkileşim ayarları kategorisinde](#TouchInteraction) yapılan ayara bağlı olarak, ekrana çift dokunun ya da parmağınızı ekrandan kaldırın.

### Girdi Yardım Kipi {#InputHelpMode}

Bu rehberin geri kalanında birçok dokunma hareketi ve tuş kombinasyonundan bahsedilecektir. ancak farklı tuş kombinasyonlarını keşfetmenizin en kolay yollarından birisi, girdi yardım kipini açmaktır.

Girdi yardım kipini açmak için NVDA+1 tuşlarına basın.
Girdi yardım kipini kapamak için de yine NVDA+1 tuşlarına basabilirsiniz.
Girdi yardım kipi açıkken, bir tuş ya da tuş kombinasyonuna bastığınızda veya bir dokunma hareketi yaptığınızda, tuşların ya da dokunma hareketinin NVDA tarafından ne amaçla kullanıldığı söylenecektir.
Girdi Yardım kipindeyken, tuşlar gerçek işlevlerini yerine getirmeyeceği için, istediğiniz tuş veya tuşlara basabilirsiniz.

### NVDA Menüsü {#TheNVDAMenu}

NVDA menüsü altında, çeşitli ayarları değiştirmenizi, Yardıma erişimi, ayarlarınızı kalıcı olarak kaydetmenizi veya geri almanızı, konuşma sözlüğünü değiştirmenizi, NVDA'yla ilgili diğer ek araçlara erişiminizi ve NVDA'yı kapatmanızı sağlayacak menü ögelerine ulaşabilirsiniz.

NVDA çalışırken Windows'ta herhangi bir yerden NVDA menüsüne gitmek için aşağıdakilerden birini yapabilirsiniz:

* klavyede `NVDA+n` tuşlarına basmak.
* Dokunmatik ekrana 2 parmakla çift dokunmak.
* `Windows+b` tuşlarına basarak sistem tepsisine gitmek, ardından `AşağıOk` tuşuyla NVDA simgesini bulmak ve `enter` tuşuna basmak.
* Ayrıca `Windows+b` tuşlarına basarak sistem tepsisine gidip `AşağıOk` tuşuyla NVDA simgesini bulduktan sonra, çoğu klavyede sağ kontrol tuşunun yanındaki `uygulama` tuşuna basarak içerik menüsüne ulaşabilirsiniz.
`Uygulama` tuşu olmayan bir klavyede `şift+F10` tuşlarına  da basabilirsiniz.
* Windows sistem tepsisinde bulunan NVDA simgesine sağ tıklamak

Menü açıldığında, menüde gezinmek için ok tuşlarını, bir öğeyi etkinleştirmek için `enter` tuşunu kullanabilirsiniz.

### Temel NVDA Komutları {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Ad |Masaüstü Kısayol tuşu |Dizüstü kısayol tuşu |Dokunma hareketi |Tarif|
|---|---|---|---|---|
|NVDA'yı başlatır veya yeniden başlatır |Kontrol+alt+n |Kontrol+alt+n |yok |Bu Windows kısayolu NVDA'nın yükleme işlemi sırasında etkinleştirilirse, NVDA'yı Masaüstünden başlatır veya yeniden başlatır. Bu, Windows'a özgü bir kısayoldur ve bu nedenle girdi hareketleri iletişim kutusunda yeniden atanamaz.|
|Konuşmayı Durdur |Kontrol |Kontrol |iki parmakla bir kez dokunma |Ekran okuyucunun konuşmasını o an için durdurur|
|Konuşmayı Duraklat |Şift |Şift |yok |Konuşmayı O an için Duraklatır. Duraklama işlevi, geçerli sentezleyici tarafından destekleniyorsa, Şifte tekrar bastığınızda konuşma kaldığı yerden devam eder|
|NVDA Menüsü |NVDA+n |NVDA+n |iki parmakla çift dokunma |Tercihler, Araçlar ve yardım gibi bölümlere ulaşabileceğiniz NVDA menüsünü açar|
|Girdi yardım kipini açıp kapama |NVDA+1 |NVDA+1 |yok |Kip açıkken, bir tuşa basıldığında, önce tuşların adı söylenir ve sonra kısayol NVDA ile ilişkiliyse, işlevi açıklanır|
|NVDA'dan çıkış |NVDA+q |NVDA+q |yok |NVDA'yı kapatır|
|Sonraki komutun NVDA işlevini yoksay |NVDA+f2 |NVDA+f2 |yok |Basılacak klavye kısayol tuşunun bir NVDA komutu olsa bile, bu komutu bir kereliğine yoksayarak geçerli uygulamanın tuşa atadığı işlevin gerçekleşmesini sağlar|
|Uygulamaya özel uyku kipini açıp kapama |NVDA+şift+s |NVDA+şift+z |yok |Uyku kipinde geçerli uygulamada Tüm NVDA komutları, konuşma ve braille geribildirimleri devre dışı kalır. Bu, kendi konuşması veya ekran okuma özelliği olan uygulamalarda çok yararlıdır. Uyku kipini kapamak için bu tuşlara tekrar basın.|

<!-- KC:endInclude -->

### Sistem Bilgisini Raporlama {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Ad |Kısayol tuşu |Tarif|
|---|---|---|
|Tarih ve Saati Söyle |NVDA+f12 |Bir kez basıldığında saat, 2 kez peşpeşe basıldığında tarih belirtilir|
|Pil durumunu bildir |NVDA+şift+b |O anki pil durumunu yüzde olarak verir veya şarjın takılı olup olmadığını söyler.|
|Panodaki metni oku |NVDA+c |Varsa, panoya kopyalanmış olan metni okur.|

<!-- KC:endInclude -->

### konuşma modları {#SpeechModes}

Konuşma modu, NVDA'nın ekran içeriğinin, bildirimlerin, komutlara verilen yanıtların ve diğer bildirimlerin nasıl seslendirileceğini belirler.
Varsayılan olarak "konuşma" modu etkindir; bu, çıktıların ve bildirimlerin her zaman sesli olarak duyurulacağı anlamına gelir.
Ancak bazı durumlarda veya belirli programları kullanırken diğer konuşma modlarını kullanmak daha faydalı olabilir.

Kullanılabilir dört konuşma modu şunlardır:

* Konuş (Varsayılan): NVDA, ekran değişikliklerine, bildirimlere ve odağın taşınması veya komut verilmesi gibi eylemlere tepki olarak normal şekilde konuşacaktır.
* İsteğe bağlı: NVDA yalnızca bildirme işlevi olan komutları kullandığınızda konuşacaktır (örn. pencerenin başlığını bildirme); ancak odağın veya imlecin taşınması gibi eylemlerde konuşmayacaktır.
* Kapalı: NVDA konuşmaz, ancak uyku modundan farklı olarak komutları işlemeye devam eder.
* bipleme: NVDA konuşmak yerine bip sesi çıkarır.

Bipleme modu, terminel gibi uygulamalarda büyük miktarda çıktı verdiği ve içeriğin değil, bir işlemin devam edip etmediğini bilmek istediğiniz gibi durumlarda kullanışlı olabilir.

İsteğe bağlı konuşma modu, ekranda olup biten hakkında süreçli bir geribildirime gerek olmadığı durumlarda kullanılabilir.
Kullanım örnekleri olarak, ses kaydetmek, büyüteç kullanmak, toplantı veya bir çağrı sırasında, veya bipleme moduna bir alternatif olarak kullanılması verilebilir.

Farklı konuşma modları arasında geçiş yapabilmek için bir kısayol tuşu bulunmaktadır:
<!-- KC:beginInclude -->

| Ad |Kısayol Tuşu |Tarif|
|---|---|---|
|konuşma modları arasında geçiş yap |`NVDA+s` |Konuşma modları arası geçiş yapar.|

<!-- KC:endInclude -->

Sadece belirli modları kullanmak istiyorsanız, [konuşma modları arasında geçiş yap](#SpeechModesDisabling) bölümüne bakarak istemediğiniz modları listeden kaldırabilirsiniz.

## NVDA ile Dolaşım {#NavigatingWithNVDA}

NVDA, bilinen yöntemlere ek olarak, inceleme imleci gibi sistemi incelemenize ve dolaşmanıza yarayan olanaklar sağlar.

### Nesneler {#Objects}

Her bir uygulama ve işletim sisteminin kendisi birçok nesneden oluşur.
Bu, bir metin bloğu, düğme, onay kutusu ya da düzenlenebilir bir yazı alanı olabilir.

### Sistem odağıyla Dolaşım {#SystemFocus}

Sistem odağı, sadece "odak" olarak da anılır, klavyede basılacak tuşlardan etkilenecek olan [nesnedir](#Objects).
Örneğin bir yazı alanına giriş yapıyorsanız bu yazı alanı sistem odağında demektir.

NVDA ile windows içinde dolaşmanın en yaygın ve kolay yolu, Tab ve şift tab ile kontroller arasında ileri geri gidiş, Alt ile bir uygulamanın menü çubuğuna ulaşım ve yön tuşları kullanılarak menü ögeleri arasında dolaşım, veya alt+tab ile pencereler arasında dolaşım gibi temel windows komutlarını kullanmaktır. Bu, sistem odağını hareket ettirir; Örneğin, Bazı nesneler klavyede basılan tuşlara göre hareket eder.
Siz yukarıda bahsedilen tuşlara bastıkça, NVDA Üzerine gelinen nesnenin adı, Türü, değeri, durumu, tanımı, klavye kısayolu ve pozisyonuyla ilgili bilgileri seslendirecektir.
[görsel vurgu](#VisionFocusHighlight) etkinleştirildiğinde, geçerli sistem odağının konumu  görsel olarak da gösterilir.

Sistem odağıyla dolaşırken, bazı yararlı tuş kombinasyonları bulunmaktadır:
<!-- KC:beginInclude -->

| Ad |Masaüstü kısayol tuşu |Dizüstü kısayol tuşu |Tarif|
|---|---|---|---|
|Üzerinde bulunulan Odağın bildirimi |NVDA+tab |NVDA+tab |Sistem odağının üzerinde bulunduğu geçerli nesne veya kontrolü belirtir. İki kez basıldığında Bilgi harf harf okunur|
|Başlığın Bildirimi |NVDA+t |NVDA+t |Üzerinde bulunulan geçerli pencerenin başlığını seslendirir. İki kez basıldığında Bilgi harf harf söylenecektir. Üç kez basıldığında bilgi panoya kopyalanır|
|Etkin Pencerenin okunması |NVDA+b |NVDA+b |etkin penceredeki tüm kontroller okunur (iletişim kutuları için yararlıdır)|
|Durum çubuğunun bildirimi |NVDA+end |NVDA+şift+end |NVDA bulabilirse, durum çubuğunu bildirir. İki kez basılırsa bilgi kodlanır. Üç kez basılırsa bilgi panoya kopyalanır.|
|Kısayol tuşunun bildirimi |`şift+numpad2` |`NVDA+kontrol+şift+.` |O anda odaklanılan nesnenin kısayol (hızlandırıcı) tuşunu bildirir.|

<!-- KC:endInclude -->

### Sistem Düzenleme İmleciyle Dolaşım {#SystemCaret}

[Sistem odağı](#SystemFocus), sizin üzerinde dolaşmanızı ve/veya giriş yapmanızı mümkün kılan, yani düzenleme imleci bulunan bir [nesnenin](#Objects) üzerindeyse, normalde yaptığınız gibi yön tuşlarını kullanarak metin için dolaşabilir ve metni düzenleyebilirsiniz.

Odak sistem düzeltme imleci olan bir nesnedeyken, metin üzerinde önceki sayfa (page up), sonraki sayfa (page down), baş (home), son (end) ve yön tuşlarını kullanarak dolaşabilirsiniz.
Salt-okunur bir alan değilse, metin üzerinde değişiklik de yapabilirsiniz.
Siz karakter karakter, sözcük sözcük ve satır satır dolaştıkça NVDA bunu size söyleyecek, ayrıca bir şeyi seçip seçmediğinizi de belirtecektir.

Sistem düzenleme imleciyle ilişkili olarak NVDA aşağıdaki tuş komutlarını sağlamaktadır:
<!-- KC:beginInclude -->

| Ad |Masaüstü kısayol tuşu |Dizüstü kısayol tuşu |Tarif|
|---|---|---|---|
|Tümünü Oku |NVDA+AşağıOk |NVDA+a |Sistem imlecinin bulunduğu yerden okumaya başlar, ve metnin sonuna kadar okumaya devam eder|
|Bulunulan satırı okuma |NVDA+yukarıOk |NVDA+l |Sistem imlecinin o an üzerinde bulunduğu satırı okur. İki kez basıldığında satır harf harf kodlanır. Üç kez basılırsa, harfler karakter tanımlarıyla seslendirilir.|
|Seçili metnin okunması |NVDA+şift+YukarıOk| NVDA+Şift+s |o an seçili olan metni okur|
|Metin biçimlendirmesini bildir |NVDA+f |NVDA+f |İmlecin o anda bulunduğu metnin biçim bilgisini bildirir. İki kez basılırsa bilgileri tarama modunda gösterir|
|Link hedefini bildir |`NVDA+k` |`NVDA+k` |Bir kez basıldığında, imleç veya odağın konumundaki linkin hedef URL'si okunur. İki kez basıldığında daha detaylı bir inceleme için bilgi farklı bir pencerede gösterilir|
|İmleç konumunu bildir |NVDA+numaratörSil |NVDA+sil |Sistem imleci bulunduğu pozisyondaki metin veya nesnenin konumuyla ilgili bilgileri raporlar. Örneğin, bu, belgede yüzdelik cinsinden konumu, sayfanın kenarından olan mesafeyi veya tam ekran konumunu içerebilir. İki kez basmak daha fazla ayrıntı sunabilir.|
|sonrakiCümle |alt+aşağıOk |alt+aşağıOk |sonraki cümleye gider ve okur. (Yalnızca Microsoft Word ve Outlook için desteklenmektedir)|
|öncekiCümle |alt+yukarıOk |alt+yukarıOk |Önceki cümleye gider ve okur. (Yalnızca Microsoft Word ve outlook için desteklenmektedir)|

Tablolarda aşağıdaki tuşlar da kullanılabilir:

| Ad |Kısayol tuşu |Tarif|
|---|---|---|
|Bir önceki sütuna gitme |kontrol+alt+Sol yön tuşu |Sistem imlecini aynı satırdaki bir önceki sütuna götürür|
|Bir sonraki sütuna gitme |kontrol+alt+Sağ yön tuşu |Sistem imlecini aynı satırdaki bir sonraki sütuna götürür|
|Bir önceki satıra gitme |kontrol+alt+YukarıOk| Sistem imlecini aynı sütunda kalarak bir önceki satıra götürür|
|Bir sonraki satıra gitme |kontrol+alt+AşağıOk| Sistem imlecini aynı sütunda kalarak bir sonraki satıra götürür|
|İlk sütuna gitme |kontrol+alt+Home |Sistem imlecini aynı satırda kalarak ilk sütuna götürür|
|Son sütuna gitme |kontrol+alt+End |Sistem imlecini aynı satırda kalarak son sütuna götürür|
|İlk satıra gitme |kontrol+alt+sayfaYukarı |Sistem imlecini aynı sütunda kalarak ilk satıra götürür|
|Son satıra gitme |kontrol+alt+sayfaAşağı |Sistem imlecini aynı sütunda kalarak ilk satıra götürür|
|Sütunu bulunulan hücreden aşağıya doğru oku |`NVDA+kontrol+alt+AşağıOk` |Sütunu, üzerinde bulunulan hücreden başlayarak aşağıya, son hücreye kadar dikey olarak okur.|
|Satırı bulunulan hücreden sağa doğru oku |`NVDA+kontrol+alt+Sağ Ok` |Satırı, üzerinde bulunulan hücreden başlayarak sağa doğru son hücreye kadar yatay olarak okur.|
|Tüm sütunu oku |`NVDA+kontrol+alt+YukarıOK` |Sistem imlecinin konumunu değiştirmeden mevcut sütunu yukarıdan aşağıya dikey olarak okur.|
|Tüm satırı oku |`NVDA+kontrol+alt+SolOK` |Sistem imlecinin konumunu değiştirmeden mevcut satırı soldan sağa yatay olarak okur.|

<!-- KC:endInclude -->

### Nesne Dolaşımı {#ObjectNavigation}

Çoğu zaman, [sistem odağını](#SystemFocus) ve [sistem düzenleme imlecini](#SystemCaret)hareket ettiren uygulamalarla çalışırsınız.
Öte yandan, Bazen aktif uygulamayı veya işletim sistemini sistem odağını ya da düzenleme imlecinin konumunu değiştirmeden dolaşmak isteyebilirsiniz. 
Aynı zamanda, normal şartlarda klavye ile ulaşamayacağınız [nesnelerle](#Objects) çalışmak isteyebilirsiniz.
İşte bu tür durumlar için, NVDA'nın nesne dolaşım özelliğini kullanabilirsiniz.

Nesne dolaşımı tek tek [nesneler](#Objects) arasında geçiş yapmanızı ve bilgi almanızı sağlar.
Nesne dolaşım komutlarını kullanarak bir nesnenin üzerine geldiğinizde, NVDA sistem imlecini hareket ettirdiğinizdekine benzer biçimde sizi bilgilendirecektir.
Metni ekranda göründüğü şekliyle incelemek isterseniz, nesne sunucusunu kullanmak yerine [ekran inceleme kipine](#ScreenReview) geçebilirsiniz.

Nesne dolaşım özelliğiyle, ekrandaki tüm nesneler arasında tek tek dolaşmak yerine, hiyerarşik olarak gruplanmış nesneler arasında dolaşım olanağı sunulmaktadır.
Yani, bir nesnenin içinde bulunan diğer nesnelere ulaşmak için o nesne içine girip dolaşmanız gerekmektedir.
Örneğin, not defteri uygulamasında menü çubuğu nesnesinin üzerine geldikten sonra nesnenin içine girip, dosya, düzen, görünüm, yardım gibi alt nesneler arasında dolaşabilirsiniz. Bir listeyle karşılaşıldığında, tüm liste ögeleri arasında dolaşmak yerine, bir liste ögesinin altındaki diğer ögeleri görmek için, bu liste ögesinin alt nesnesi ya da nesnelerine giderek bu liste ögesi içinde dolaşmanız gerekecektir.
Bir liste ögesi ile aynı liste içinde bulunan diğer liste ögeleri arasında önceki nesne ve sonraki nesne komutlarıyla dolaşabilirsiniz.
Önceki nesne komutuyla da bu ögeleri kapsayan liste nesnesine gidebilirsiniz.
Bu şekilde, incelemekte olduğunuz uygulamanın liste ögeleri dışındaki kısmında bulunan nesnelere de kolayca ulaşabilirsiniz.
Benzer biçimde, bir araç çubuğu da çeşitli kontrolleri kapsar ve bu kontrollere erişebilmek için, araç çubuğu nesnesinin içine girmelisiniz.

Sistemdeki nesneler arasında ileri geri hareket etmek istiyorsanız, düzleştirilmiş bir görünümde önceki/sonraki nesneye gitmek için komutları kullanabilirsiniz.
Örneğin, düzleştirilmiş görünümde bir sonraki nesneye geçerseniz ve geçerli nesne başka nesneler içeriyorsa, NVDA otomatik olarak onu içeren ilk nesneye gider.
Diğer bir seçenek olarak, mevcut nesne herhangi bir içerik içermiyorsa, NVDA ilgili hiyerarşinin düzeyindeki bir sonraki nesneye geçer.
Eğer içerik içeren bir sonraki nesne yoksa, hiyerarşideki bir sonraki nesneye geçer. Bu işlem, taşınabilecek nesne kalmayana kadar devam eder.
Hiyerarşide geri gitmek için de aynı kurallar geçerlidir.

İncelenmekte olan nesneye dolaşım nesnesi denir. 
Nesne dolaşım komutlarıyla bir nesne üzerine geldikten sonra, nesneyi [metin inceleme komutlarını](#ReviewingText) kullanarak [Nesne inceleme kipinde](#ObjectReview) inceleyebilirsiniz.
[görsel vurgu](#VisionFocusHighlight) etkinse, geçerli nesne sunucusunun konumu  görsel olarak da gösterilir.
Varsayılan olarak, nesne sunucusu sistem odağıyla birlikte hareket eder; ancak bu özellik kapatılıp açılabilir.

Not: Braille'in nesne sunucusunu takibi  [Braille taşınsın](#BrailleTether) altından ayarlanabilir.

Nesneler arasında dolaşmak için aşağıdaki komutları kullanın:

<!-- KC:beginInclude -->

| Ad |Masaüstü Kısayol tuşu |Dizüstü Kısayol tuşu |Dokunma hareketi |Tarif|
|---|---|---|---|---|
|Geçerli nesnenin bildir |NVDA+numaratör5 |NVDA+şift+o |yok |Nesne sunucusunun üzerinde bulunduğu nesneyi okur. İki kez basıldığında bilgi kodlanır, ve 3 kez basıldığında nesnenin adı ve değeri panoya kopyalanır.|
|Ana nesneye git |NVDA+numaratör8 |NVDA+şift+YukarıOk| yukarı fiske |nesne sunucusunun Üzerinde bulunduğu nesnenin bir üst düzeyindeki ana nesneye gider|
|önceki nesneye git |NVDA+numaratör4 |NVDA+şift+sol yön tuşu |sola fiske |nesne sunucusunu, üzerinde bulunulan nesneyle aynı seviyede bulunan bir önceki nesneye taşır|
|Düzleştirilmiş görünümde önceki nesneye git |NVDA+numaratör9 |NVDA+şift+Ğ |sola fiske (object mode) |Düzleştirilmiş nesne sunum hiyerarşisinde önceki nesneye gider|
|bir sonraki nesneye git |NVDA+numaratör6 |NVDA+şift+sağ yön tuşu |sağa fiske |nesne sunucusunu, üzerinde bulunulan nesneyle aynı seviyede bulunan bir sonraki nesneye taşır|
|Düzleştirilmiş görünümde sonraki nesneye git |NVDA+numaratör3 |NVDA+şift+Ü |sağa fiske (object mode) |Düzleştirilmiş nesne sunum hiyerarşisinde sonraki nesneye gider|
|İlk Yavru nesneye git |NVDA+numaratör2 |NVDA+şift+AşağıOk| aşağı fiske |Nesne sunucusunu, Üzerinde bulunulan nesnenin ilk alt nesnesine taşır ve okur.|
|Odaktaki nesneye git |NVDA+numaratörMinus |NVDA+GeriSil |yok |Nesne sunucusunu, sistem odağının üzerinde bulunduğu nesneye taşır ve varsa, inceleme imlecini de sistem düzenleme imlecinin bulunduğu noktaya taşır|
|Üzerinde bulunulan nesneyi etkinleştir |NVDA+numaratörEnter |NVDA+enter |çift dokunma |Sistem odağı bir şeyin üzerindeyken oraya fare ile tıklamak veya boşluk çubuğuna basılmasına benzer biçimde, nesne sunucusunun üzerinde bulunduğu nesneyi etkinleştirir|
|Sistem odağını nesne sunucusuna taşı |NVDA+şift+numaratörEksi |NVDA+şift+GeriSil |yok |Eğer mümkünse, bir kez basıldığında sistem odağını nesne sunucusunun konumuna; iki kez basıldığında, sistem düzenleme imlecini inceleme imlecinin konumuna taşır|
|İnceleme imleci konumunu bildir |NVDA+şift+numaratörSil |NVDA+şift+Sil |yok |İnceleme imlecinin konumundaki nesnenin belgenin neresinde ya da sayfanın solundan ya da üstünden ne kadar uzakta olduğuyla ilgili bilgi verir. İki kez basılırsa daha ayrıntılı bilgi sunulabilir|
|İnceleme imlecini durum çubuğuna taşı |Yok |Yok |Yok |NVDA  bulabilirse Durum Çubuğunu bildirir. Ayrıca nesne sunucusunu bu konuma taşır.|

<!-- KC:endInclude -->

Not: Numaratördeki tuşların düzgün çalışabilmesi için, numara kilidi kapalı olmalıdır.

### Metin inceleme {#ReviewingText}

NVDA üzerinde bulunduğunuz [ekranı](#ScreenReview), aktif [belgeyi](#DocumentReview) ya da üzerinde bulunduğunuz [nesneyi](#ObjectReview) karakter karakter, sözcük sözcük, ya da satır satır incelemenize imkan vermektedir.
Bu, [sistem imlecinin](#SystemCaret) çok kısıtlı olduğu veya hiç bulunmadığı Windows komut konsolu gibi yerler için oldukça yararlıdır.
Örneğin, bir iletişim kutusundaki uzun bir bilgi metnini incelemek için kullanabilirsiniz.

İnceleme imlecini hareket ettirirken, sistem imleci bunu takip etmeyeceğinden, klavye odağını değiştirmeden ekranda gösterilen metni inceleyebilirsiniz.
Ancak varsayılan olarak, sistem odağı hareket ettikçe inceleme imleci de onu takip etmektedir.
Bu özellik açılıp kapatılabilir.

Not: Braille'in inceleme imlecini  takibini [Braille taşınsın](#BrailleTether) altından ayarlayabilirsiniz.

Metni incelerken, aşağıdaki komutlar kullanılabilir:
<!-- KC:beginInclude -->

| Ad |Masaüstü Kısayol tuşu |Dizüstü Kısayol tuşu |Dokunma hareketi |Tarif|
|---|---|---|---|---|
|inceleme imlecinde en üst satıra gitme |şift+numaratör7 |NVDA+kontrol+home |yok |İnceleme imlecini en üst satıra taşır|
|inceleme imlecinde bir önceki satıra gitme |numaratör7 |NVDA+YukarıOk| yukarı fiske (metin kipi) |İnceleme imlecini bir önceki satıra taşır|
|Mevcut satırı okuma |numaratör8 |NVDA+şift+nokta |yok |İnceleme imlecinin üzerinde bulunduğu satırı okur. İki kez basıldığında satır harf harf kodlanır. Üç kez basıldığında ise satır Adana, Bolu, Ceyhan gibi karakter tanımlarıyla kodlanır.|
|inceleme imlecinde bir sonraki satıra gitme |numaratör9 |NVDA+AşağıOk| aşağı fiske (metin kipi) |İnceleme imlecini bir sonraki satıra taşır|
|inceleme imlecinde son satıra gitme |şift+numaratör9 |NVDA+kontrol+end |yok |İnceleme imlecini son satıra taşır|
|inceleme imlecinde bir önceki sözcüğe gitme |numaratör4 |NVDA+kontrol+sol yön tuşu |iki parmakla sola fiske (metin kipi) |İnceleme imlecini bir önceki sözcüğe taşır|
|Mevcut sözcüğü okuma |numaratör5 |NVDA+kontrol+nokta |yok |İnceleme imlecinin üzerinde bulunduğu sözcüğü okur. İki kez basıldığında sözcük harf harf kodlanır. Üç kez basıldığında sözcük, Adana, Bolu, Ceyhan gibi karakter tanımlarıyla kodlanır.|
|inceleme imlecinde bir sonraki sözcüğe gitme |numaratör6 |NVDA+kontrol+sağ yön tuşu |iki parmakla sağa fiske (metin kipi) |İnceleme imlecini bir sonraki sözcüğe taşır|
|inceleme imlecinde satır başına gitme |şift+numaratör1 |NVDA+home |yok |İnceleme imlecini metinde üzerinde bulunduğunuz satırın başına taşır|
|inceleme imlecinde bir önceki karaktere gitme |numaratör1 |NVDA+sol yön tuşu |sola fiske (metin kipi) |İnceleme imlecini üzerinde bulunulan satırdaki bir önceki karaktere taşır|
|Mevcut karakteri okuma |numaratör2 |NVDA+nokta |yok |İnceleme imlecinin üzerinde bulunduğu karakteri okur. İki kez basıldığında, karakter tanımıyla söylenir. Üç kez basıldığında karakterin değerini numerik olarak ondalık ve onaltılık sistemlerde belirtir.|
|inceleme imlecinde bir sonraki karaktere gitme |numaratör3 |NVDA+sağ yön tuşu |sağa fiske (metin kipi) |İnceleme imlecini üzerinde bulunulan satırdaki bir sonraki karaktere taşır|
|inceleme imlecinde satır sonuna gitme |şift+numaratör3 |NVDA+end |yok |İnceleme imlecini üzerinde bulunulan satırın sonuna taşır|
|İnceleme imlecinde önceki sayfaya gitme |`NVDA+pageUp` |`NVDA+şift+pageUp` |yok |Uygulama tarafından destekleniyorsa inceleme imlecini metnin önceki sayfasına taşır|
|inceleme imlecinde sonraki sayfaya gitme |`NVDA+pageDown` |`NVDA+şift+pageDown` |yok |Uygulama tarafından destekleniyorsa inceleme imlecini metnin sonraki sayfasına taşır|
|İnceleme imlecinde tümünü okuma |numaratörArtı |NVDA+şift+a |üç parmakla aşağı fiske (metin kipi) |İnceleme imlecinde bulunulan noktadan başlayarak metnin sonuna kadar okur|
|İnceleme imlecinin bulunduğu yerden kopyalama ve seçme işlemini başlatma |NVDA+f9 |NVDA+f9 |yok |inceleme imlecinin pozisyonundan itibaren metni seçmeye ya da kopyalamaya başlar. NVDA'ya metnin sonunu belirtmeden işlem gerçekleşmez|
|İnceleme imlecinin bulunduğu yere kadar seçme ve kopyalama |NVDA+f10 |NVDA+f10 |yok |metnin başladığı yer olarak ayarlanan noktadan, inceleme imlecinin mevcut konumuna kadar olan metni seçer. İki kez basılırsa, metin panoya kopyalanır|
|Kopyalanmak üzere işaretlenmiş kısmın başına taşı |NVDA+şift+f9 |NVDA+şift+f9 |none |inceleme imlecini, kopya için önceden belirlenmiş kısmın başlangıç konumuna taşır|
|Metin biçimini söyle |NVDA+şift+f |NVDA+şift+f |yok |İnceleme imlecinin pozisyonundaki metnin biçimi hakkında bilgi verir. İki kez basılırsa, biçim bilgisi tarama kipinde gösterilir|
|Mevcut sembol için belirlenmiş okunuşu seslendir |None |None |none |inceleme imlecinin bulunduğu konumdaki sembolü söyler. Pressed twice, shows the symbol and the text used to speak it in browse mode.|

<!-- KC:endInclude -->

Not: Numaratördeki tuşların düzgün çalışabilmesi için, numara kilidi kapalı olmalıdır.

Eğer masaüstü klavye düzenini kullanıyorsanız, tuş komutlarını hatırlamanıza yardımcı olması için, temel metin inceleme komutlarının üçlü bir parmaklık biçiminde organize edildiğini lütfen not edin. yukarıdan aşağıya üçlü satır, sözcük ve karakter anlamına gelirken, soldan sağa üçlü önceki, üzerinde bulunulan ve sonraki anlamına gelmektedir.
Düzen aşağıdaki biçimde gösterilmiştir:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|Önceki satır |Üzerinde bulunulan satır |Sonraki satır|
|Önceki sözcük |üzerinde bulunulan sözcük |Sonraki sözcük|
|Önceki karakter |Üzerinde bulunulan karakter |Sonraki karakter|

### İnceleme Kipleri {#ReviewModes}

NVDA'nın [inceleme komutları](#ReviewingText), seçilen kipe bağlı olarak, mevcut gezgin nesnesindeki, aktif belgede ya da ekrandaki içeriği incelemenizi sağlar.

Aşağıdaki komutlarla, inceleme kipleri arasında geçiş yapılabilir:
<!-- KC:beginInclude -->

| Ad |Masaüstü Kısayol tuşu |Dizüstü Kısayol tuşu |Dokunma hareketi |Tarif|
|---|---|---|---|---|
|Sonraki inceleme kipine geç |NVDA+numaratör7 |NVDA+önceki sayfa |iki parmakla yukarı fiske |varsa mevcut kipten sonraki inceleme kipine geçer.|
|Önceki inceleme kipine geç |NVDA+numaratör1 |NVDA+sonraki sayfa |iki parmakla aşağı kadırma |varsa mevcut kipten önceki inceleme kipine geçer.|

<!-- KC:endInclude -->

#### Nesne İnceleme {#ObjectReview}

Nesne inceleme kipindeyken, yalnızca [mevcut nesne](#ObjectNavigation) içindeki metni inceleyebilirsiniz.
Yazı alanları ya da temel belge kontrolleri gibi nesneler için, bu genellikle metinsel bir içeriktir.
Başka nesneler için bu, nesne adı ya da değeri olabilir.

#### Belge İncelemesi {#DocumentReview}

[mevcut nesne](#ObjectNavigation) tarama kipindeki bir belge içindeyse (örneğin, web sayfası) ya da birçok nesne içeren başka bir karmaşık belge (örneğin Lotus Symphony belgeleri), belge inceleme kipine geçmek mümkündür.
Belge inceleme kipiyle açık dokümandaki tüm metni inceleyebilirsiniz.

Nesne inceleme kipinden belge incelemeye geçtiğinizde , inceleme imleci nesne sunucusunun konumundaki metin üzerinde bulunur.
Belge içinde inceleme imleciyle ilgili komutlarla hareket ederken, nesne sunucusunun konumu da otomatik olarak güncellenir.

Tarama kipindeki belgeler incelenirken, NVDA'nın otomatik olarak nesne inceleme kipinden belge incelemeye geçeceğini not edin.

#### Ekran İncelemesi {#ScreenReview}

Ekran inceleme kipi, aktif uygulama ekranında gösterilen metni incelemenizi sağlar.
Bu, başka ekran okuyucularda bulunan, inceleme imleci ya da fare imleci gibi işlevlere benzer bir özelliktir.

Ekran inceleme kipine geçildiğinde, inceleme imleci [nesne sunucusunun](#ObjectNavigation) konumundaki nesne üzerinde bulunur.
İnceleme komutlarıyla ekranda hareket edilirken, nesne sunucusunun konumu da otomatik olarak güncellenir.

Bazı uygulamalar için, henüz desteklenmeyen ekran çizim teknolojileri kullanılmasından dolayı, ekrandaki metnin tamamının gösterilemeyebileceğini not edin.

### Fare ile Dolaşım {#NavigatingWithTheMouse}

Fare ile hareket ederken, varsayılan olarak NVDA, fare ile üzerine gelinen kontrolleri okur.
Destekleniyorsa, NVDA metni paragraf bazında okur. ancak bazı kontroller sadece satır satır okunmasına izin vermektedir.

NVDA ayrıca, fare hareket ettikçe üzerinde bulunduğu [nesnenin](#Objects) liste, düğme gibi türünü de okuyacak biçimde ayarlanabilmektedir.
Bu, özellikle tamamen kör olanlar için sadece metnin okunmasının yeterli olmadığı durumlarda çok yararlıdır.

NVDA, kullanıcıların ekran boyutlarına göre farenin tam olarak nerede olduğunu anlayabilmelerini sağlamak için, farenin o anki koordinatlarını bip sesleriyle raporlayabilir.
Fare ekranda yukarı doğru çıktıkça biplerin sesi incelir.
Fare ekranın sağ veya sol tarafına doğru hareket ettikçe, kullanıcıların steryo hoparlör kullandıkları varsayılarak ses de daha sağdan veya daha soldan gelir.

Bu ekstra fare seçenekleri varsayılan olarak kapalıdır.
Ancak bunların avantajlarından faydalanmak isterseniz, tercihler menüsü içinde bulunan [NVDA ayarlar](#NVDASettings) iletişim kutusundaki [Fare ayarları](#MouseSettings) kategorisinden    bu özellikleri konfigüre edebilirsiniz.

NVDA, fareyi hareket ettirmek için, ek bir işleve sahip değildir. Fiziksel fare veya dizüstü bilgisayarlarda fare pedlerini kullanabilirsiniz. Ancak farenin nesne sunucusunun konumuna ya da nesne sunucusunun fare konumuna taşınması, sol tık, sağ tık gibi çeşitli işlevler için kullanılan  bazı  komutlar bulunmaktadır:
<!-- KC:beginInclude -->

| Ad |Masaüstü Kısayol tuşu |Dizüstü Kısayol tuşu |Dokunma |Tarif|
|---|---|---|---|---|
|Sol fare tıklaması |numaratörBölü |NVDA+ğ |yok |Sol fare düğmesine bir kez tıklar çift tıklamak için tuşlara peşpeşe 2 kez basılabilir|
|Sol fare kilidi |şift+numaratörbölü |NVDA+kontrol+ğ |yok |Sol fareyi kilitler. kilidi açmak için tuşa tekrar basılmalıdır. bulunulan yeri taşımak için, bu tuşla fareyi kilitleyin ve fareyi fiziksel olarak veya diğer fare komutlarıyla hareket ettirin|
|Sağ fare tıklaması |numaratörÇarpı |NVDA+ü |dokun ve tut |sağ fare düğmesine bir kez tıklar.|
|sağ fare kilidi |şift+numaratörÇarpı |NVDA+kontrol+ü |yok |sağ fareyi kilitler. kilidi açmak için tuşa tekrar basılmalıdır. fareyi taşımak için, bu tuşla fareyi kilitleyin ve fareyi fiziksel olarak veya diğer fare komutlarıyla hareket ettirin|
|Fareyi nesne sunucusunun üzerinde bulunduğu nesneye taşıma |NVDA+numaratörbölü |NVDA+şift+m |yok |Fareyi nesne sunucusunun konumundaki nesnenin üzerine taşır|
|farenin altındaki nesneye gitme |NVDA+numaratörÇarpı |NVDA+şift+n |yok |nesne sunucusunu farenin konumundaki nesneye taşır.|

<!-- KC:endInclude -->

## Tarama Kipi {#BrowseMode}

Web sayfaları gibi karmaşık salt okunur belgeler, NVDA'da tarama kipinde gösterilir.
Bu, aşağıdaki uygulamalardaki belgeleri içerir:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* Microsoft Outlook'da HTML mesajları
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* Amazon Kindle for PC içinde desteklenen kitaplar

Tarama kipi aynı zamanda Microsoft Word için karmaşık belgelerde dolaşılırken kullanılmak üzere opsiyonel olarak mevcuttur.

Tarama kipi, web sayfası gibi bir içeriğin bir metin dosyası gibi sunulduğu bir inceleme alanıdır ve içerik içinde yön tuşlarıyla dolaşılabilir.
NVDA'nın [sistem düzenleme imleci](#SystemCaret) için geçerli olan hepsini okuma, tablo inceleme, yazı biçimini raporlama gibi komutları bu kip için de geçerlidir.
[Görsel vurgu](#VisionFocusHighlight) etkinleştirildiğinde, tarama kipi imlecinin konumu  görsel olarak da gösterilir.
Metin içinde hareket ettikçe, okunan metnin bir link veya başlık olup olmadığı gibi bilgiler de belirtilir.

Bazen, belge içindeki kontrollerle doğrudan etkileşim içinde olmanız gerekebilir.
Örneğin, yazılabilir alanlar ve liste kutularında giriş yapabilmeniz ya da imleci hareket ettirerek liste ögeleri arasında seçim yapabilmeniz için kontrolle etkileşim içinde olmanız gerekir.
Bunu hemen hemen tüm tuşların doğrudan ilgili kontrollere aktarıldığı odak kipine geçerek yapabilirsiniz.
Tarama kipindeyken, tab ile veya tıklayarak odak kipinin gerektirdiği bir kontrole gelindiğinde, NVDA otomatik olarak odak kipini açabilir.
Odak kipine geçmenin gerektiği durumlarda, kontrol üzerinde giriş veya boşluk çubuğuna basılarak da odak kipine geçilebildiğini lütfen not edin.
NVDA otomatik olarak odak kipine geçtiyse, sonrasında tab ile veya başka bir yolla odak kipine ihtiyaç olmayan bir noktaya geçildiğinde, NVDA otomatik olarak tarama kipine geri döner.
Odak kipine otomatik olarak geçildiyse, eskeyp tuşuyla da tarama kipine geri dönülebilir.
Tarama ve odak kipleri arasında manuel olarak da geçiş yapabilirsiniz ve Odak kipine manuel olarak geçildikten sonra, NVDA bu kipte kalır ve siz tekrar ilgili tuşlara basarak odak kipinden çıkmadıkça tarama kipine geçilmez.

<!-- KC:beginInclude -->

| Ad |Kısayol tuşu |Tarif|
|---|---|---|
|Tarama ve odak kipleri arasında geçiş |NVDA+aralık çubuğu |Odak ve tarama kipleri arasında geçiş yapar|
|Odak kipinden çıkış |eskeyp |Odak kipine otomatik olarak geçildiyse, tarama kipine geri döner|
|Tarama kipinde gösterilen belgeyi güncelleme |NVDA+f5 |Geçerli belgeyi yeniden yükler. (İçeriğin bir kısmı eksik gibi görünüyorsa ya da ziyaret ettiğiniz sayfa sık aralıklarla güncelleniyorsa bu tuşları kullanmak yararlı olabilir.)|
|Metin ara |NVDA+kontrol+f |Geçerli belgede yazıp bir metin arayabileceğiniz bir iletişim kutusu açar Daha fazla bilgi için [metin arama](#SearchingForText) bölümüne bakın.|
|Sonrakini bul |NVDA+f3 |metni belgenin sonraki kısmında arar|
|Öncekini bul |NVDA+şift+f3 |metni belgenin önceki kısmında arar|

<!-- KC:endInclude -->

### Tek Tuşla Dolaşım {#SingleLetterNavigation}

Tarama kipindeyken, NVDA, mevcut belgedeki belirli ögeler arasında daha seri bir dolaşım için, tek tuşla dolaşım olanağı sunar.
Bu komutların her belge için geçerli olmayabileceğini unutmadan aşağıdaki listeyi inceleyebilirsiniz.

<!-- KC:beginInclude -->
Aşağıdaki tuşlara kendi başlarına basıldığında bir sonraki ögeye gidilirken, bu tuşlara şift ile basıldığında bir önceki ögeye gidilmektedir:

* h: Başlık
* l: liste
* i: liste ögesi
* t: tablo
* k: link
* n: link dışı metin
* f: form alanı
* u: ziyaret edilmemiş link
* v: ziyaret edilmiş link
* e: yazı alanı
* b: düğme
* x: onay kutusu
* c: seçim kutusu
* r: seçim düğmesi
* q: alıntı bloğu
* s: ayraç
* m: çerçeve
* g: grafik
* d: ARIA sınır imi
* o: gömülü nesne (ses ve video oynatıcı, uygulama, iletişim kutusu, vb.)
* 1'den 6'ya kadar: sırayla başlık birden altıya
* a: açıklama (yorum, editör düzenlemeleri, dipnot vs.)
* `p`: metin paragraf
* w: yazım hatası

Tablolar, listeler vb öge bloklarının başına ve sonuna gitmek için:

| Ad |Kısayol tuşu |Tarif|
|---|---|---|
|Öge bloğunun başına git |şift+, |İçinde bulunulan öge bloğunun başına, ilk ögesinin üzerine gider (liste, tablo vb)|
|Öge bloğunun sonuna git |, |İçinde bulunulan öge bloğunun sonuna gider ve bloğun dışına çıkar (liste, tablo vb)|

<!-- KC:endInclude -->

Bazı web uygulamaları mesela Gmail, Twitter and Facebook bazı tuşları kısayol olarak kullanmaktadır.
Tarama kipinde kalarak tuşları o anda kullandığınız web uygulamasının kısayolları olarak kullanmak istiyorsanız tek tuşla dolaşımı geçici olarak kapatabilirsiniz.
<!-- KC:beginInclude -->
Mevcut belge için tek tuşla dolaşımı açıp kapatmak için, NVDA+şift+aralık tuşlarını kullanın.
<!-- KC:endInclude -->

#### Metin paragraf gezinme komutu {#TextNavigationCommand}

`p` veya `şift+p` tuşlarına basarak sonraki veya önceki metin paragrafına atlayabilirsiniz.
Metin paragrafları, tam cümleler halinde yazılmış gibi görünen bir metin grubuyla tanımlanır.
Bu komut, çeşitli web sayfalarındaki okunabilir içeriğin başlangıcını bulmak için yararlı olabilir, örneğin:

* Haber siteleri
* Forumlar
* Blog yazıları

Bu komutlar ayrıca aşağıdaki gibi karmaşık içeriği geçmenizede yardımcı olabillir:

* Reklamlar
* Menüler
* Başlıklar

NVDA metin paragraflarını tanımak için mümkün olan en iyi performansı göstermeye çalışsa da, kullanılan algoritma kusursuz değildir ve zaman zaman hatalar olabilir.
Ayrıca bu komut `kontrol+AşağıOk/YukarıOk` paragraf gezinme komutlarından farklıdır.
Metin paragraf gezinme yalnızca metin paragrafları arasında geçiş yaparken, paragraf gezinme komutları ise metin içerip içermediğine bakılmaksızın imleci önceki/sonraki paragrafa taşır.

#### Diğer gezinme komutları {#OtherNavigationCommands}

Yukarıda listelenen hızlı gezinme komutlarına ek olarak, NVDA'da varsayılan olarak atanmayan komutlar bulunmaktadır.
Bu komutları kullanmak için öncelikle [girdi hareketleri iletişim kutusu](#InputGestures) üzerinden girdi ataması yapmanız gerekmektedir.
Komut listesi

* Makale
* Şekil
* Gruplama
* Sekme
* Menü Öğesi
* Geçiş düğmesi
* İlerleme çubuğu
* Matematik formülü
* Dikey olarak hizalanmış paragraf
* Aynı stilde metin
* Farklı stilde metin

Hızlıca ileri geri gidebilmek için her komut için iki komut bulunduğunu ve her iki yönde de hızlıca gezinebilmek için her iki komuta da girdi hareketi atamanız gerektiğini unutmayın.
Örneğin, sekmeler arasında hızlı bir şekilde gezinmek için `y` / `şift+y` tuşlarını kullanmak istiyorsanız aşağıdakileri yapmanız gerekir:

1. Tarama kipinden girdi hareketleri iletişim kutusunu açın.
1. Tarama kipi bölümünden "sonraki sekmeye geçer" öğesini bulun.
1. Bulunan hareket için `y` tuşunu atayın.
1. Tarama kipi bölümünden "Önceki sekmeye geçer" öğesini bulun.
1. Bulunan hareket için `şift+y` tuşunu atayın.

### Öğe Listesi {#ElementsList}

Öğe listesi, uygulamaya bağlı olarak değişen, belgedeki çeşitli ögelerin listesine erişminizi sağlamaktadır.
Örneğin, web tarayıcıları için bunlar, link, başlık, form alanı, düğme ya da sınır imi olabilir.
Seçim düğmeleri, bu öge türlerinden hangilerinin gösterileceğini belirlemenizi sağlar.
İletişim kutusuna, bir de sayfada aradığınız şeye göre listeyi daraltabileceğiniz bir yazı alanı eklenmiştir.
İlgilendiğiniz ögeyi belirledikten sonra, iletişim kutusundaki düğmeleri kullanarak imleci ögenin üzerine taşıyabilir veya ögeyi etkinleştirebilirsiniz.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu |Tarif|
|---|---|---|
|Tarama kipi öge listesi |NVDA+f7 |tarama kipinde gösterilen belgedeki çeşitli ögelerin listesini gösterir|

<!-- KC:endInclude -->

### Metin arama {#SearchingForText}

Bu iletişim kutusu, geçerli belgedeki terimleri aramanızı sağlar.
"Aramak istediğiniz metni yazın" alanına, bulunacak metin girilebilir.
"Büyük / küçük harfe duyarlı" onay kutusu, aramanın büyük ve küçük harfleri farklı düşünmesini sağlar.
Örneğin, "Büyük / küçük harfe duyarlı" seçiliyken "NV Access" ifadesini bulabilirken, "nv access" ifadesini bulamazsınız.
Arama yapmak için aşağıdaki tuşları kullanın:
<!-- KC:beginInclude -->

| Ad |Kısayol |Açıklama|
|---|---|---|
|Metin ara |NVDA+kontrol+f |Arama iletişim kutusunu açar|
|Sonrakini ara |NVDA+ff3 |Mevcut arama teriminin bir sonraki tekrarını arar|
|Öncekini ara |NVDA+şift+f3 |geçerli arama teriminin önceki tekrarını arar|

<!-- KC:endInclude -->

### Gömülü Nesneler {#ImbeddedObjects}

Sayfalar, Oracle Java ve HTML 5 gibi teknolojilerle üretilmiş öğelerin yanında uygulamalar ve iletişim kutuları gibi zengin içerikler barındırabilir.
Bunlarla tarama kipinde karşılaşıldığında, NVDA "gömülü nesne", "uygulama" ya da "iletişim kutusu" olduklarını bildirecektir.
Bu öğelere o ve şift+o gömülü nesne tek tuşla dolaşım kısayollarını kullanarak hızlı bir şekilde ulaşabilirsiniz.
Enter tuşuna basarak onlarla etkileşime geçebilirsiniz.
Eğer erişilebilir olarak düzenlenmişse, tab tuşuyla içinde dolaşabilir ve diğer uygulamalar gibi etkileşimde bulunabilirsiniz.
Gömülü nesneyi barındıran sayfaya geri dönmek için bir kısayol tuşu tanımlanmıştır:
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu |Tarif|
|---|---|---|
|Gömülü nesneyi kapsayan belgeye geri dön |NVDA+kontrol+ara çubuğu |odağı geçerli gömülü nesnenin dışına çıkararak bu nesneyi barındıran sayfaya geri döner|

<!-- KC:endInclude -->

### yerel girdi modu {#NativeSelectionMode}

Varsayılan olarak, Tarama kipinde `şift+ok` tuşlarıyla metin seçerken, seçim sadece nvda bazında yapılır, uygulamayı etkilemez.
Bu, seçimin ekranda görünmediği ve metnin `control+c` ile kopyalanmasının yalnızca NVDA'nın içeriğin düz metin temsilini kopyalayacağı anlamına gelir. yani tabloların biçimlendirilmesi veya seçili metnin  bağlantı olup olmadığı gibi biçimsel özellikleri kopyalanmayacaktır.
Ancak NVDA'nın belirli tarama kipi belgelerinde (şimdilik sadece Firefox'ta) kullanılabilen bir Yerel Girdi Modu  bulunmaktadır. Bu mod açıkken yaptığınız seçimlerin belge bazında da yapılmasını sağlayabilirsiniz.

<!-- KC:beginInclude -->

| Ad |Kısayol tuşu |tarif|
|---|---|---|
|Yerel Girdi Modunu aç/kapat |`NVDA+şift+f10` |Yerel Girdi modunu açar ve kapatır|

<!-- KC:endInclude -->

Yerel Girdi Modu açıldığında, seçimin `control+c` ile kopyalanması uygulamanın kopyalama içeriğini de tetikler. Bu, düz metin yerine zengin içeriğin panoya kopyalanacağı anlamına gelir.
Böylece Microsoft Word veya Excele yapıştıracağınız metnin bağlantı veya tablo gibi biçimsel özellikleri korunacaktır.
Ancak yerel girdi modunda, NVDA'nın Tarama  kipinde oluşturduğu bazı erişilebilir etiketlerin veya diğer bilgilerin dahil edilmeyeceğini lütfen unutmayın.
Ayrıca, uygulama yerel girdi NVDA'nın Tarama Modu s denk bir seçim yapabilmek için çalışsa da için elinden geleni yapsa da ,bu her zaman tam olarak doğru olmayabilir.
Ancak zengin içerikli bir tablonun veya paragrafın tamamını kopyalamak istediğiniz durumlar için bu özellik faydalı olacaktır.

## Matematiksel İçerik Okuma {#ReadingMath}

NVDA desteklenen maatematiksel içerik üzerinde dolaşıp okumanızı sağlar.
Ancak NVDA'nın matematiksel içeriği okuyabilmesi ve etkileşime girebilmesi için öncelikle NvDA'ya bir Matematik bileşeni yüklemeniz gerekir.
NVDA Eklenti Mağazasında matematik desteği sağlayan [MathCAT NVDA eklentisi](https://nsoiffer.github.io/MathCAT/) ve [Access8Math](https://github.com/tsengwoody/Access8Math) gibi çeşitli NVDA eklentileri bulunmaktadır. . 
NVDA'da eklentilerin bulunmasını ve kurulmasını öğrenmek için lütfen [Eklenti Mağazası bölümü](#AddonsManager)'ne bakın.
NVDA, sisteminizde bulunması halinde Wiris'in eski [MathPlayer](https://info.wiris.com/mathplayer-info) yazılımını da kullanabilir, ancak bu yazılım artık geliştirlmemektedir.

### Desteklenen matematiksel içerik {#SupportedMathContent}

Uygun bir matematik bileşeni kurulduğunda, NVDA aşağıdaki matematiksel içerik türlerini destekler:

* Mozilla Firefox, Microsoft Internet Explorer ve Google Chrome MathML.
* UI otomasyonu aracılığıyla Microsoft Word 365 Modern Matematik Denklemleri:
NVDA, Microsoft Word 365/2016 build 14326 ve üzeri sürümlerde matematik denklemlerini okuyabilir ve bunlarla etkileşim kurabilir.
Ancak, önceden oluşturulmuş MathType denklemlerinin önce Office Math'a dönüştürülmesi gerektiğini unutmayın.
Denklemleri dönüştürmek için, her birini seçip "Denklem Seçenekleri"ni ve ardından bağlam menüsünde "Office Math'a Dönüştür"ü seçin.
Bunu yapmadan önce MathType sürümünüzün en son sürüm olduğundan emin olun.
Microsoft Word ayrıca denklemlerin kendisinde doğrusal sembol tabanlı gezinme sağlar ve LateX dahil olmak üzere çeşitli sözdizimlerini kullanarak matematik girişini destekler. 
Daha fazla ayrıntı için lütfen [Word'de UnicodeMath ve LaTeX kullanan doğrusal biçimli denklemler](https://support.microsoft.com/en-us/office/linear-format-equations-using-unicodemath-and-latex-in-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8) makalesine bakın
* Microsoft Powerpoint ve Microsoft Word'ün eski sürümleri:
NVDA, MathType denklemlerini hem Microsoft Powerpoint hem de Microsoft word'de okuyabilir ve içlerinde dolaşılmasını sağlayabilir.
Bunun çalışabilmesi için MathType'ın kurulu olması gerekir.
Deneme sürümü yeterlidir.
Şuradan https://www.wiris.com/en/mathtype/ indirilebilir.
* Adobe Reader:
Bunun henüz resmi bir standart olmadığını not edin, dolayısıyla şu anda bu içeriği üretebilen hiçbir kamuya açık yazılım bulunmamaktadır.
* Kindle Reader for PC:
NVDA, erişilebilir matematik içeren kitaplar için Kindle for PC'de Math'ı okuyabilir ve bu kitaplarda dolaşılmasını sağlayabilir.

Bir belgeyi okurken, NVDA desteklenen herhangi bir matematiksel içeriği seslendirecektir.
Braille ekran kullanıyorsanız, ayrıca braille olarak da gösterilir.

### Etkileşimli Navigasyon {#InteractiveNavigation}

Öncelikli olarak konuşma ile çalışıyorsanız, çoğu durumda, muhtemelen tüm ifadeyi bir kerede dinlemek yerine, daha küçük segmentlerde incelemek isteyebilirsiniz.

Tarama kipindeyseniz, matematiksel içerik üzerine gelip enter tuşuna basarak bunu yapabilirsiniz.

Tarama kipinde değilseniz:

1. İnceleme imlecini matematiksel içerik üzerine getirin.
Varsayılan olarak, inceleme imleci sistem imlecini izler, yani genellikle istenilen içerik üzerine gitmek için sistem düzeltme imlecini kullanabilirsiniz.
1. Sonra, aşağıdaki komutu gerçekleştirin:

<!-- KC:beginInclude -->

| Ad |Tuş |Tarif|
|---|---|---|
|Matematik içeriği ile etkileşim |NVDA+alt+m |Matematik içeriği ile etkileşim başlar.|

<!-- KC:endInclude -->

Bu noktada, NVDA Matematiksel etkileşim moduna girecektir. İfadeyi incelemek için yön tuşları gibi komutları kullanabilirsiniz.
Örneğin, ifade üzerinde sol ve sağ Ok tuşları ile hareket edebilirsiniz ve kesir vb ifadenin bir bölümünü daha yakından incelemek için aşağı ok tuşuna basabilirsiniz.

Matematiksel içeriğe sahip olan belgeye geri dönmek istediğinizde, escape tuşuna basmanız yeterli.

Matematiksel içeriği okumak ve gezinmek için mevcut komutlar ve tercihler hakkında daha fazla bilgi için lütfen yüklediğiniz matematik bileşeninin belgelerine bakın.

* [MathCAT kullanıcı rehberi](https://nsoiffer.github.io/MathCAT/users.html)
* [Access8Math kullanıcı rehberi](https://github.com/tsengwoody/Access8Math)
* [MathPlayer kullanıcı rehberi](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Bazen matematiksel içerik, etkinleştirildiğinde formülle ilgili bir iletişim kutusu veya daha fazla bilgi gösterebilen bir düğme veya başka bir öğe türü olarak gösterilebilir.
Düğmeyi veya formülü içeren öğeyi etkinleştirmek için kontrol + enter tuşlarına basın.

### MathPlayer'ı Yükleme {#InstallingMathPlayer}

NVDA'da matematiksel içerik desteği için genellikle daha yeni NVDA eklentilerinden birinin kullanılması önerilse de, bazı durumlarda MathPlayer'ın kullanılması daha uygun bir seçenek olabilir.
Örneğin MathPlayer, yeni eklentilerde desteklenmeyen belirli bir dili veya Braille kodunu desteklediği durumlarda.
MathPlayer, Wiris web sitesinden ücretsiz olarak edinilebilir
[MathPlayer'ı indirin](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
MathPlayer'ı yükledikten sonra NVDA'yı yeniden başlatmanız gerekir.
MathPlayer'ın sadece Internet Explorer 8 gibi daha eski tarayıcılar için olduğu bilgilerle karşılaşabilirsiniz.
Bu yalnızca MathPlayer'ın matematiksel içeriği görsel olarak görüntülemek için kullanılmasıyla ilgilidir ve NVDA ile matematik okumak veya matematikte gezinmek için kullananlar tarafından yoksayılabilir.

## Braille {#Braille}

Eğer braille ekrana sahipseniz, NVDA bilgileri braille olarak gösterebilir.
Braille ekranınızın perkins tarzı bir klavyesi varsa, kısaltmalı ya da kısaltmasız braille girişi de yapabilirsiniz.
Braille ayrıca fiziksel bir braille ekran yerine veya onunla aynı anda [Braille Görüntüleyicisi](#BrailleViewer) kullanılarak ekranda görüntülenebilir.

Lütfen desteklenen braille ekranlar hakkında bilgi için [desteklenen braille ekranlar](#SupportedBrailleDisplays) bölümünü inceleyin.
Bu bölümde ayrıca, NVDA'nın otomatik arka plan braille ekran algılama işlevinin hangi braille ekranlar için geçerli olduğuna dair bilgi de verilmektedir.
Braille ayarlarını [NVDA ayarları](#NVDASettings) iletişim kutusundaki [Braille kategorisinden](#BrailleSettings) yapabilirsiniz.

### Braille Kontrol türü, Durumu ve Sınırimi kısaltmaları {#BrailleAbbreviations}

Braille ekranaa mümkün olduğunca fazla bilgi sığdırmak amacıyla, kontrol türünü ve durumunu göstermenin yanı sıra sınırimlerinin bildirimi için aşağıdaki kısaltmalar tanımlanmıştır.

| Kısaltma |Kontrol türü|
|---|---|
|uyg |uygulama|
|mkl |makale|
|lnt |alıntı bloku|
|dğm |düğme|
|drdğm |açılır düğme|
|döndğm |dönen düğme|
|blmdğm |bölünmüş düğme|
|gçşdğm |geçiş düğmesi|
|alty |altyazı|
|sk |seçim kutusu|
|ok |onay kutusu|
|ik |iletişim kutusu|
|bel |belge|
|Yza |yazı alanı|
|prlyza |şifre yazı alanı|
|gömülü |gömülü nesne|
|snot |sonnot|
|fig |figür|
|dnot |dipnot|
|grf |grafik|
|grp |gruplandırma|
|bN |başlık seviyesi n, Örneğin, b1, b2.|
|yrd |yardım balonu|
|snrimi |sınırimi|
|lnk |link|
|zlnk |ziyaret edilmiş link|
|lst |liste|
|mnu |menu|
|mçb |menü çubuğu|
|mnüdğm |menü düğmesi|
|mnüöğe |menü öğesi|
|pnl |panel|
|aşmçb |aşama çubuğu|
|mşkl |meşgul göstergesi|
|sd |seçim düğmesi|
|kydrçb |kaydırma çubuğu|
|blm |bölüm|
|drmçb |durum çubuğu|
|skmdntm |sekme denetimi|
|tbl |tablo|
|sütN |tablo sütun numarası n, örneğin süt1, süt2.|
|satN |tablo satır numarası n, örneğin sat1, sat2.|
|term |terminal|
|arçb |araç çubuğu|
|ipu |araç ipucu|
|ag |ağaç görünümü|
|ağçdğm |ağaç görünümü düğmesi|
|ağçg |ağaç görünümü öğesi|
|sv N |ağaç görünüm öğesinin hiyerarşik seviyesi N|
|pnc |pencere|
|⠤⠤⠤⠤⠤ |ayraç|
|sçli |işaretli içerik|

Aşağıdaki durum belirtenleri de tanımlanmıştır:

| Kısaltma |Kontrol durumu|
|---|---|
|... |bir nesne otomatik tamamlamayı destekliyorsa gösterilir|
|⢎⣿⡱ |bir nesneye, örneğin bir geçiş düğmesine basılmışsa gösterilir|
|⢎⣀⡱ |bir nesneye, örneğin bir geçiş düğmesine basılı değilse gösterilir|
|⣏⣿⣹ |bir nesne (örneğin bir onay kutusu) işaretli olduğunda gösterilir|
|⣏⣸⣹ |bir nesne (örneğin bir onay kutusu) yarı işaretli olduğunda gösterilir|
|⣏⣀⣹ |onay kutusu vb nesneler işaretli değilse gösterilir|
|- |Bir nesne örneğin bir ağaç görünüm öğesi daraltılabilir olduğunda gösterilir|
|+ |Bir nesne örneğin, bir ağaç görünüm öğesi genişletilebilir olduğunda gösterilir|
|*** |korunmuş bir kontrol ya da belge açıldığında gösterilir|
|tkl |bir nesne tıklanabilirse gösterilir|
|açk |bir çalışma sayfası ya da bir belge içinde açıklamayla karşılaşıldığında gösterilir|
|frml |çalışma sayfasındaki hücrede formül varsa gösterilir|
|geçersiz |geçersiz bir giriş olduğunda gösterilir|
|uzntrf |bir nesneyle, genellikle bir grafikle ilgili uzun tarif varsa gösterilir|
|çkstryza |çok satırlı bir yazı alanıyla karşılaşıldığında gösterilir, örneğin bazı web sayfalarındaki açıklama alanları|
|grkl |zorunlu giriş gerektiren form alanlarıyla karşılaşıldığında gösterilir|
|so |bir nesne örneğin bir yazı alanı salt okunursa gösterilir|
|seç |Bir nesne seçildiğinde gösterilir|
|sçldğl |nesne seçili değilse gösterilir|
|A'dan Z'ye |a'dan z'ye sıralı bir nesneyle karşılaşıldığında gösterilir|
|Z'den A'ya |z'den a'ya sıralı bir nesneyle karşılaşıldığında gösterilir|
|altmnu |Bir nesne açılan (genellikle bir alt-menü) olduğunda gösterilir|

Son olarak, sınırimleri için aşağıdaki kısaltmalar tanımlanmıştır:

| Kısaltma |sınırimi|
|---|---|
|bnnr |benır|
|içrkblg |içerik bilgisi|
|tmmlyc |tamamlayıcı|
|form |form|
|ana |ana|
|navi |navigasyon|
|ara |arama|
|blg |bölge|

### Braille Girişi {#BrailleInput}

NVDA braille klavye ile kısaltmasız ve kısaltmalı braille girişini destekler.
Braille'i metne çevirmek için kullanılacak çeviri tablosunu [NVDA ayarları](#NVDASettings) iletişim kutusundaki Braille kategorisi altından [Giriş tablosu](#BrailleSettingsInputTable) ayarını kullanarak seçebilirsiniz.

Kısaltmasız braille kullanıldığında, metin doğrudan girilir.
Kısaltmalı braille kullanılıyorken, metin aralık ya da enter tuşuna bastığınızda eklenir.
Çevirinin yalnızca girdiğiniz braille ifadeyi yansıtacağını ve daha önceki metinle ilgili olmadığını aklınızda tutun.
Mesela, rakam işaretiyle başlayıp girdiğiniz bazı rakamlardan sonra geri sil tuşuna basarsanız, rakam girişine devam etmek için tekrar rakam işareti kullanmanız gerekir.

<!-- KC:beginInclude -->
7. nokta basarak son braille hücreyi ya da girilen karakteri silersiniz.
8. nokta braille girişi çevirir ve enter tuşuna basar.
7. ve 8. noktalara birlikte basarsanız aralık ya da enter tuşuna basılmaksızın braille girişi metne çevrilir.
<!-- KC:endInclude -->

#### Klavye kısayolları girişi {#BrailleKeyboardShortcuts}

NVDA, klavye kısayollarının girilmesini ve braille ekranını kullanarak tuşlaran taklit edilmesini destekler.
Taklit iki şekilde gelir: bir tuşa doğrudan bir Braille girdisi atamak ve sanal değiştirici tuşları kullanmak.

Ok tuşları veya menülere ulaşmak için Alt tuşuna basmak gibi yaygın olarak kullanılan tuşlar, doğrudan Braille girişlerine eşlenebilir.
Her bir Braille ekranının sürücüsü, bu görevlerden bazılarıyla önceden donatılmış olarak gelir.
[Girdi Hareketleri iletişim kutusu](#InputGestures) altından bu atamaları değiştirebilir veya yeni taklit  tuşlar ekleyebilirsiniz.

Bu yaklaşım, yaygın olarak basılan veya biricik tuşlar (Tab gibi) için kullanışlı olsa da, her klavye kısayoluna biricik bir tuş takımı atamak istemeyebilirsiniz.
NVDA, değiştirici tuşların basılı tutulduğu durumlarda tuş basmalarının taklit edilmesini sağlamak için kontrol, alt, şift, windows ve NVDA tuşlarının  ayrı ayrı , bu tuşların bazı kombinasyonlarının birlikte kullanılması için çeşitli komutlar sunar.
Bu geçişleri kullanmak için önce basılmasını istediğiniz değiştirici tuşlar için komuta (veya komut dizisine) basın. 
Ardından girmek istediğiniz klavye kısayolunun parçası olan karakteri girin.
Örneğin, kontrol+f kısayol tuşunu kullanmak için "Kontrol tuşunu aç" komutunu kullanın ve ardından f yazın,
ve kontrol+alt+t'yi girmek için, sırası fark etmez, "Kontrol tuşunu aç" ve "Alt tuşunu aç" komutlarını veya "Kontrol+alt tuşlarını aç" komutunu kullanın ve ardından t yazın.

Değiştirici tuşları yanlışlıkla açarsanız, geçiş komutunu tekrar çalıştırmak değiştiriciyi kaldıracaktır.

Kısaltmalı Braille'de yazarken, değiştirici tuşlarını açıp kapatmak, girişinizin tıpkı 7+8 noktalarına basmışsınız gibi çevrilmesine neden olur.
Ayrıca, taklit edilen tuş girişi, değiştirici tuşa basılmadan önce girilen Braille kodu yansıtamaz.
Bu, rakam işareti kullanan bir Braille koduyla alt+2 basmak için önce Alt'ı açmanız ve ardından bir rakam işareti girmeniz gerektiği anlamına gelir.

## Görsellik {#Vision}

NVDA öncelikli olarak kör ve az gören kişilere bir bilgisayarı çalıştırmak için öncelikle konuşma ve / veya braille kullanma olanağı  sunarken, ekranın içeriğini değiştirmek için yerleşik olanaklar da sağlar.
NVDA içinde böyle bir görsel yardım, görsel geliştirme sağlayıcısı olarak adlandırılır.

NVDA, aşağıda açıklanan çeşitli yerleşik görsel geliştirme sağlayıcıları sunmaktadır.
[NVDA eklentileri](#AddonsManager) ile ek görsel geliştirme sağlayıcıları sunulabilir.

NVDA'nın görsellikle ilgili  ayarları [NVDA Ayarları](#NVDASettings) iletişim kutusu  altında [görsellik kategorisinden](#VisionSettings) değiştirilebilir.

### Görsel Vurgu {#VisionFocusHighlight}

Görsel vurgu [sistem odağı](#SystemFocus), [nesne sunucusu](#ObjectNavigation) ve [tarama kipi](#BrowseMode) konumlarının anlaşılmasına görsel olarak yardımcı olur.
Bu konumlar renkli bir dikdörtgen çizgiyle vurgulanır.

* Düz mavi, sistem odağı ve nesne sunucusu aynı konumdaysa vurgulama için kullanılır. (e.g. Çünkü [nesne sunucusu sistem odağını takip ediyordur](#ReviewCursorFollowFocus)).
* Kesik mavi sistem imleci konumunu vurgular.
* Düz pembe, sadece nesne sunucusunu vurgular.
* Düz sarı (web tarayıcılarındaki gibi fiziksel bir imlecin bulunmadığı yerlerde ) tarama kipinde kullanılan sanal imleci vurgular.

[NVDA Ayarları](#NVDASettings) iletişim kutusunda [görsellik kategorisi](#VisionSettings) altındaki Görsel vurgu etkinse, [odağın, nesne sunucusunun ya da tarama kipi imleci konumunun  vurgulanıp vurgulanmayacağını değiştirebilirsiniz](#VisionSettingsFocusHighlight)

### Ekran perdesi {#VisionScreenCurtain}

Kör ya da az gören bir kullanıcı iseniz, ekranda ne olduğunu algılamanız yüksek olasılıkla mümkün ya da gerekli değildir.
Dahası omzunuzun üzerinden biri ekranınızı dikizliyor olabilir.
Bu tür durumlar için  NVDA, ekranı karartmak için etkinleştirilebilen "ekran perdesi" adı verilen bir özelliğe sahiptir.

[NVDA Ayarları](#NVDASettings) iletişim kutusunda [görsellik  kategorisi](#VisionSettings) altından ekran perdesini etkinleştirebilirsiniz.

<!-- KC:beginInclude -->

| Ad |Kısayol tuşu |Tarif|
|---|---|---|
|Ekran perdesini ayarla |`NVDA+control+escape` |Ekranı karartmak için etkinleştirin veya karartmayı kaldırmak için devre dışı bırakın. Bir kez basıldığında, NVDA yeniden başlatılıncaya kadar ekran perdesi etkin kalır. İki kez basıldığında ekran perdesi siz devre dışı bırakana kadar etkin kalır.|

<!-- KC:endInclude -->

Ekran perdesi etkinse, [OCR](#Win10Ocr) veya  ekran görüntüsü almak gibi doğrudan ekranda görünenle ilgili işlemler gerçekleştirilemez.

Windows Büyüteç API'sindeki bir değişiklik nedeniyle, Ekran Perdesi, Windows'un en yeni sürümlerini destekleyecek şekilde güncellenmek zorunda kaldı.
Windows 10 21H2 (10.0.19044) veya sonraki sürümlerde Ekran Perdesini etkinleştirmek için NVDA 2021.2'yi kullanın.
Güvenliği gözeterek, Windows'un yeni bir sürümünü kullanırken Ekran Perdesinin ekranı tamamen kararttığına dair görsel onay alın.

Windows Büyüteç ve renkleri terse çevir özellikleri açıkken ekran perdesinin etkinleştirilemeyeceğini lütfen unutmayın.

## Görsel İçerik Tanıma {#ContentRecognition}

Yazarlar bir şeyin içeriğiyle ilgili ekran okuyucuların algılayabileceği tarzda yeterli bilgi sunmadıklarında, bir görüntünün içeriğinin tanınması için çeşitli araçlar kullanılabilir.
NVDA görsellerin içerisindeki metnin tanınması için Windows 10 ve sonraki  windows sürümleriyle sunulan (OCR) işlevini optik karakter tanımayı destekler.
Başka içerik tanıma araçları NVDA eklentisi olarak sunulmaktadır.

İçerik tanıma (OCR) komutu kullandığınızda, NVDA [nesne sunucusu](#ObjectNavigation) tarafından odaklanan nesne içeriğini tanımaya çalışır.
Varsayılan olarak, nesne sunucusu sistem odağı ya da tarama kipi imlecini takip eder, dolayısıyla yalnızca odağı ya da tarama kipi imlecini istediğiniz noktaya getirip tanıma işlemini başlatabilirsiniz.
Mesela, tarama kipi imlecini bir grafiğe taşıdıktan sonra, tanıma işlemi bu grafikle sunulan içerik için yapılır.
Bununla birlikte, nesne sunucusunu doğrudan tanıma işlemi yapılacak nesne üzerine de götürüp tanıma işlemini başlatabilirsiniz.

Tanıma işlemi tamamlandıktan sonra, sonuç tarama kipinde gösterilir ve yön tuşlarını kullanarak içerik üzerinde dolaşabilirsiniz.
Enter ya da aralığa basarsanız, mümkünse üzerinde bulunduğunuz metnin işaret ettiği kontrolü etkinleştirebilirsiniz.
Escape tuşuyla tanıma sonucunu kapatabilirsiniz.

### Windows OCR {#Win10Ocr}

Windows 10 ve sonrası birçok dil için OCR içerir.
NVDA bu aracı görsellerdeki metni ya da erişilebilir olmayan uygulamalardaki kontrolleri tanımak için kullanabilir.

[NVDA ayarları](#NVDASettings) iletişim kutusundaki [Windows OCR kategorisi](#Win10OcrSettings) altından metin tanıma için kullanılacak dili seçebilirsiniz.
başlat menüsü, ayarlar, zaman ve dil, bölge ve dil altında dil ekle düğmesi kullanılarak ek diller yüklenebilir.

Altyazılı bir video gibi sürekli değişen bir içeriği takip etmek istediğinizde, isteğe bağlı olarak tanınan içeriğin otomatik olarak yenilenmesini etkinleştirebilirsiniz.
Bu aynı zamanda [NVDA Ayarları](#NVDASettings) iletişim kutusunun [Windows OCR kategorisi](#Win10OcrSettings) bölümünde de yapılabilir.

Windows OCR, [NVDA görsel geliştirmeleri](#Vision) ya da  diğer harici görsel yardımcılarla  kısmen veya tamamen uyumsuz olabilir. Tanıma işlemine geçmeden önce bu araçları devre dışı bırakmanız gerekecektir.

<!-- KC:beginInclude -->
Windows OCR kullanarak geçerli nesne içindeki metni tanımak için, NVDA+r tuşlarına basın.
<!-- KC:endInclude -->

## Uygulamaya Özgü Özellikler {#ApplicationSpecificFeatures}

NVDA çeşitli işlemlerin yapılmasını kolaylaştırmak ya da ekran okuyucu kullanıcıları için erişilebilir olmayan işlevleri onlar için de ulaşılabilir kılmak için bazı uygulamalara özgü ek olanaklar sağlamaktadır.

### Microsoft Word {#MicrosoftWord}
#### Otomatik Sütun ve Satır Başlığı Okuma {#WordAutomaticColumnAndRowHeaderReading}

NVDA Microsoft Word'de, tablolarda dolaşılırken otomatik olarak satır ve sütun başlıklarını seslendirebilir.
Bu öncelikle, [NVDA ayarları](#NVDASettings) iletişim kutusunda, Belge formatları kategorisindeki Tablo Satır ve sütun başlıklarını bildir onay kutusunun işaretli olmasını gerektirir.

Word ve Windows'un son sürümlerinde varsayılan olarak [Word belgelerine erişmek için UIA](#MSWordUIA) seçeneğini kullanıyorsanız, ilk satırın hücreleri otomatik olarak sütun başlıkları olarak, ilk sütunun hücreleri de otomatik olarak satır başlıkları olarak tanınacaktır.

Ancak, [Word belgelerine erişmek için UIA](#MSWordUIA) kullanmıyorsanız, bir tablodaki başlıkların hangi satır veya sütunda bulunduğunu NVDA'ya belirtmeniz gerekecektir.
Tabloda satır ya da sütun başlık bilgisini içeren hücreye geldikten sonra, aşağıdaki tuşlardan birini kullanın:
<!-- KC:beginInclude -->

| Ad |Kısayol |Açıklama|
|---|---|---|
|Sütun başlıklarını ayarla |NVDA+şift+c |Bir kez basıldığında mevcut satır sütun başlığı olarak ayarlanır ve bu satırın altındaki sütunlar arasında dolaşılırken ayarlanan satırdaki bilgi otomatik olarak seslendirilir. İki kez basıldığında ayar sıfırlanır.|
|Satır başlıklarını ayarla |NVDA+şift+r |Bir kez basıldığında mevcut sütun satır başlığı olarak ayarlanır ve sütunun sağındaki satırlar arasında dolaşılırken ayarlanan sütundaki bilgi otomatik olarak seslendirilir. İki kez basıldığında ayar sıfırlanır.|

<!-- KC:endInclude -->
Bu ayarlar, belge içinde yer imi olarak kaydedilir ve JAWS gibi başka ekran okuyucu yazılımlarla uyumludur.
Dolayısıyla, belge daha sonra başka ekran okuyucular aktifken açıldığında da başlık bilgilerine ulaşılabilir. 

#### Microsoft Word'de Tarama Kipi {#BrowseModeInMicrosoftWord}

Webde olduğu gibi, Microsoft Word için de tek tuşla dolaşım ve Öğe Listesine ulaşmanız için tarama kipi özelliği kullanılabilir.
<!-- KC:beginInclude -->
Microsoft Word'de Tarama kipini açıp kapamak için, NVDA+Aralık tuşunu kullanın.
<!-- KC:endInclude -->
Tarama kipi ve tek tuşla dolaşım hakkında daha fazla bilgi için, [Tarama Kipi bölümüne](#BrowseMode) bakın.

##### Öğe Listesi {#WordElementsList}

<!-- KC:beginInclude -->
Microsoft Word'de tarama kipi etkinken, öğe listesine NVDA+F7 tuşlarına basarak ulaşabilirsiniz.
<!-- KC:endInclude -->
Öğe Listesi başlıkları, linkleri, yazım hatalarını, (bilgi notları ve belgede yapılmış değişiklikleri içeren) açıklamaları listeleyebilir.

#### Açıklamaların Bildirimi {#WordReportingComments}

<!-- KC:beginInclude -->
İmleç konumundaki açıklamayı okumak için, NVDA+alt+c tuşlarına basın.
<!-- KC:endInclude -->
Belgedeki tüm değişiklik ve açıklamalar, tür bölümünden "Açıklama" seçeneği tercih edilerek NVDA+F7 ile açılan Öğe Listesi iletişim kutusunda da listelenebilir.

### Microsoft Excel {#MicrosoftExcel}
#### Otomatik Sütun ve Satır Başlığı Okuma {#ExcelAutomaticColumnAndRowHeaderReading}

NVDA Microsoft Excel çalışma sayfalarında, tablolarda dolaşılırken otomatik olarak satır ve sütun başlıklarını seslendirebilir.
Bu öncelikle, [NVDA ayarları](#NVDASettings) iletişim kutusunda, Belge formatları kategorisindeki Tablo Satır ve sütun başlıklarını bildir onay kutusunun işaretli olmasını gerektirir.
İkinci olarak, NVDA'nın, tabloda hangi satır ya da sütunun başlık bilgisini içerdiğini bilmesi gerekir.
Satır ya da sütun başlık bilgisini içeren hücreye geldikten sonra, aşağıdaki tuşlardan birini kullanın:
<!-- KC:beginInclude -->

| Ad |Kısayol Tuşu |Tarif|
|---|---|---|
|Sütun başlıklarını ayarla |NVDA+şift+c |Bir kez basıldığında mevcut satır sütun başlığı olarak ayarlanır ve satırın altındaki sütunlar arasında dolaşılırken ayarlanan satırdaki bilgi otomatik olarak seslendirilir. İki kez basıldığında ayar sıfırlanır.|
|Satır başlıklarını ayarla |NVDA+şift+r |Bir kez basıldığında mevcut sütun satır başlığı olarak ayarlanır ve sütunun sağındaki satırlar arasında dolaşılırken ayarlanan sütundaki bilgi otomatik olarak seslendirilir. İki kez basıldığında ayar sıfırlanır.|

<!-- KC:endInclude -->
Bu ayarlar, çalışma kitabında tanımlı ad aralıkları olarak saklanacaktır ve Jaws gibi diğer Ekran Okuyucular ile uyumludur.
Dolayısıyla, daha sonraki bir tarihte bu çalışma kitabını açın diğer ekran okuyucu kullanıcıları için otomatik olarak satır ve sütun başlıkları önceden ayarlanmış olacaktır. 

#### Öğe Listesi {#ExcelElementsList}

Web'de olduğu gibi, NVDA'nın Microsoft Excel için de, farklı bilgi tiplerini listeleyip ulaşmanızı sağlayan öğe listesi bulunmaktadır.
<!-- KC:beginInclude -->
Excel'de öğe listesine ulaşmak için, NVDA+f7 tuşlarını kullanın.
<!-- KC:endInclude -->
Öğe listesinde ulaşılabilecek farklı türdeki bilgiler şunlardır:

* Grafikler: Bu çalışma sayfasındaki tüm grafikleri listeler. 
Grafiği seçip üzerinde enter tuşuna ya da Git düğmesine basarsanız yön tuşlarıyla dolaşmanız ve okumanız için grafik üzerine odaklanmış olursunuz.
* Açıklamalar: Bu çalışma sayfasındaki açıklama içeren tüm hücreleri listeler. 
Her hücre için adres bilgisiyle birlikte açıklama metni gösterilir. 
Listedeki açıklama üzerinde enter tuşuna ya da Git düğmesine basarsanız ilgili hücreye gidebilirsiniz.
* Formüller: Bu çalışma sayfasındaki formül içeren tüm hücreleri listeler. 
Her hücre için adres bilgisiyle birlikte formül gösterilir.
Listelenmiş formüllerden birinin üzerinde enter tuşuna ya da Git düğmesine basarsanız ilgili hücreye gidebilirsiniz. 
* Çalışma sayfaları: Bu çalışma kitabındaki tüm sayfaları listeler. 
Listeden seçtiğiniz bir sayfa üzerinde f2 tuşuna basarak sayfanın adını değiştirebilirsiniz. 
Seçili sayfa üzerinde enter tuşuna ya da Git düğmesine basarak ilgili çalışma sayfasına ulaşabilirsiniz.
* Form alanları: Etkin çalışma sayfasındaki tüm form alanlarını listeler.
Her form alanı için, Öğe listesi kapsanan hücre adresleri ile birlikte alanın alternatif metinlerini gösterir.
Bir form alanını seçip entır tuşuna ya da git düğmesine basarak tarama kipinde o form alanına gidilebilir.

#### Notların Bİldirimi {#ExcelReportingComments}

<!-- KC:beginInclude -->
Üzerinde bulunduğunuz hücreyle ilgili notu okumak için NVDA+alt+c tuşlarını kullanın.
Microsoft 2016, 365 ve daha yeni sürümlerde, Microsoft Excel'deki klasik açıklamalar "notlar" olarak yeniden adlandırılmıştır.
<!-- KC:endInclude -->
Çalışma sayfasındaki tüm notlar NVDA+F7 ile açılan öğe listesinde de gösterilebilir.

NVDA ayrıca  bir not eklenmesi  veya düzenlenmesi için bir iletişim kutusu açabilir.
NVDA, erişilebilirlik kısıtlamaları nedeniyle yerel MS Excel bölge düzenleme özelliğini geçersiz kılar, ancak iletişim kutusunu göstermek için kullanılan kısayol tuşu  MS Excel'den devralınır ve bu nedenle NVDA aktif değilken de çalışır.
<!-- KC:beginInclude -->
Bir not eklemek veya düzenlemek için, odaktaki hücrede, şift + f2 tuşlarına basın.
<!-- KC:endInclude -->

Bu kısayol tuşu NVDA girdi hareketleri altında gösterilmez ve dolayısıyla değiştirilemez.

Not: MS Excel'de not düzenleme bölgesini, çalışma sayfasının herhangi bir hücresinin bağlam menüsünden de açmak mümkündür.
Ancak bu, NVDA'ya özgü not düzenleme iletişim kutusunu değil, erişilebilir olmayan not düzenleme bölgesini açar.

Microsoft Office 2016, 365 ve daha yeni sürümlerde, yeni bir stil açıklama iletişim kutusu eklendi.
Bu iletişim kutusu  erişilebilirdir ve açıklamaları yanıtlama vb. Gibi daha fazla işlem sunar.
Ayrıca belirli bir hücrenin içerik menüsünden de açılabilir.
Yeni stil açıklama iletişim kutusu aracılığıyla hücrelere eklenen açıklamalar "notlar" ile ilgili değildir.

#### Korunan Hücreleri Okuma {#ExcelReadingProtectedCells}

Bir çalışma kitabı korunuyorsa, düzenleme için kilitlenmiş hücrelere ulaşmak mümkün olmayabilir.
<!-- KC:beginInclude -->
Kilitli hücrelere ulaşılmasını mümkün kılmak için, NVDA+space ile Tarama Kipi'ne geçin ve sonra Standart Excel hareket komutlarını kullanın. Örneğin yön tuşları.
<!-- KC:endInclude -->

#### Form Alanları {#ExcelFormFields}

Excel çalışma kitapları form alanları içerebilir.
Bunlara öğe listesini kullanarak ya da f ve şift+f form alanı tek tuş dolaşım kısayolları ile ulaşabilirsiniz.
Bir form alanına tarama kipinde ulaştıktan sonra, kontrole bağlı olarak, enter ya da aralık tuşuna basarak etkinleştirebilir veya etkileşimde bulunabilmek için odak kipine geçebilirsiniz.
Tarama kipi ve tek tuş dolaşımı  hakkında daha fazla bilgi için, [tarama kipi bölümüne](#BrowseMode) bakın.

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Ad |Kısayol tuşu |Tarif|
|---|---|---|
|Konuşmacı notları okuma modu |kontrol+şift+s |Aktif bir slayt gösterisi içindeyken, bu komut slayt içeriğinin mi yoksa konuşmacı notlarının mı seslendirileceğini belirler. Bu sadece NVDA'nın neyi seslendireceği ile ilgilidir, ekranda görüntülenen bilgi değişmez.|

<!-- KC:endInclude -->

### foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Ad |Kısayol Tuşu |Tarif|
|---|---|---|
|Kalan süreyi oku |kontrol+şift+r |Mevcutsa, çalmakta olan parçanın bitmesi için kalan süreyi okur.|
|Geçen süreyi oku |Kontrol+şift+e |Varsa, çalan parçanın geçen süre bilgisini seslendirir.|
|Parça süresini oku |Kontrol+şift+t |varsa, çalan parça süresini okur.|

<!-- KC:endInclude -->

Not: yukarıdaki kısayol tuşları, yalnızca Foobar2000 durum çubuğu varsayılan görünümünde geçerlidir.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Ad |Kısayol Tuşu |Tarif|
|---|---|---|
|En son mesajı oku |NVDA+kontrol+1-4 |Basılan numaraya göre, En son mesajlardan birini okur; Örneğin, NVDA+kontrol+2 sondan ikinci mesajı okur.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA, Poedit 3.4 veya daha yeni sürümler için gelişmiş destek sunar.

<!-- KC:beginInclude -->

| Ad |Kısayol Tuşu |Tarif|
|---|---|---|
|Çeviri notlarını oku |`kontrol+şift+a` |Çeviri ile ilgili notları okur. İki kez basıldığında notlar tarama kipinde görüntülenir|
|Açıklama penceresini oku |`kontrol+şift+c` |Açıklama penceresindeki açıklamaları okur. İki kez basıldığında açıklamalar tarama kipinde görüntülenir|
|Eski Kaynak Metni Bildir |`kontrol+şift+o` |Varsa eski kaynak metni bildirir. İki kez basıldığında metin tarama kipinde görüntülenir|
|Çeviri Uyarısını Bildir |`kontrol+şift+w` |Varsa bir çeviri uyarısı bildirir. İki kez basıldığında uyarı tarama kipinde görüntülenir|

<!-- KC:endInclude -->

### Kindle for PC {#Kindle}

NVDA supports reading and navigating books in Amazon Kindle for PC.
This functionality is only available in Kindle books designated with "Screen Reader: Supported" which you can check on the details page for the book.

Browse mode is used to read books.
It is enabled automatically when you open a book or focus the book area.
The page will be turned automatically as appropriate when you move the cursor or use the say all command.
<!-- KC:beginInclude -->
You can manually turn to the next page with the pageDown key and turn to the previous page with the pageUp key.
<!-- KC:endInclude -->

Single letter navigation is supported for links and graphics, but only within the current page.
Navigating by link also includes footnotes.

NVDA provides early support for reading and interactive navigation of mathematical content for books with accessible math.
Please see the [Reading Mathematical Content](#ReadingMath) section for further information.

#### Text Selection {#KindleTextSelection}

Kindle allows you to perform various functions on selected text, including obtaining a dictionary definition, adding notes and highlights, copying the text to the clipboard and searching the web.
To do this, first select text as you normally would in browse mode; e.g. by using şift and the cursor keys.
<!-- KC:beginInclude -->
Once you have selected text, press the applications key or şift+f10 to show the available options for working with the selection.
<!-- KC:endInclude -->
If you do this with no text selected, options will be shown for the word at the cursor.

#### User Notes {#KindleUserNotes}

You can add a note regarding a word or passage of text.
To do this, first select the relevant text and access the selection options as described above.
Then, choose Add Note.

When reading in browse mode, NVDA refers to these notes as comments.

To view, edit or delete a note:

1. Move the cursor to the text containing the note.
1. Access the options for the selection as described above.
1. Choose Edit Note.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
When in the table view of added books:

| Name |Key |Description|
|---|---|---|
|Enter |enter |Opens the selected book.|
|Context menu |applications |Opens the context menu for the selected book.|

<!-- KC:endInclude -->

### Windows Konsolu {#WinConsole}

NVDA, Komut İstemi, PowerShell ve Linux için Windows Subsystem tarafından kullanılan Windows komut konsolu için destek sağlar.
Konsol penceresi sabit bir boyuta sahiptir, genellikle çıktıyı tutan arabellekten çok daha küçüktür.
Yeni metin yazılırken, içerik yukarı kaydırılır ve önceki metin artık görünmez. 
Windows 11 22H2'den önceki Windows sürümlerinde, pencerede görünmeyen bir metne NVDA'nın metin inceleme komutlarıyla erişilemez.
Bu nedenle, önceki metni okumak için konsol penceresini kaydırmanız gerekir.
Yeni konsol sürümlerinde, pencereyi kaydırmaya gerek kalmadan tüm metin arabelleğinnde serbestçe gezinebilirsiniz.
<!-- KC:beginInclude -->
Eski Windows Konsolu sürümlerinde NVDA ile [metin incelemesi](#ReviewingText) için aşağıdaki yerleşik klavye kısayolları  yararlı olabilir:

| Ad |Kısayol |Tarif|
|---|---|---|
|Yukarı kaydır |kontrol + yukarı yön tuşu |Konsol penceresini yukarı kaydırır, böylece daha önceki metinler okunabilir.|
|Aşağı kaydır |kontrol + AşağıYönTuşu |Konsol penceresini aşağı kaydırır, böylece sonra girilen  metin okunabilir.|
|Başa kaydır |kontrol+home |Konsol penceresini ara belleğin başına kaydırır.|
|Sona kaydır |kontrol+end |Konsol penceresini arabellek sonuna kaydırır.|

<!-- KC:endInclude -->

## NVDA'yı Yapılandırma {#ConfiguringNVDA}

Birçok NVDA ayarı NVDA menüsü içindeki tercihler alt menüsünden erişilebilen iletişim kutuları kullanılarak değiştirilebilmektedir.
Bu ayarların çoğu çoklu sekme sayfası olarak gösterilen [NVDA Ayarlar iletişim kutusu](#NVDASettings) içerisinde bulunabilir.
Tüm NVDA iletişim kutularında yaptığınız değişiklikleri onaylamak için tamam tuşuna basın.
herhangi bir değişikliği iptal etmek için, iptal tuşuna ya da eskeyp tuşuna basın.
Bazı iletişim kutuları  için, iletişim kutusunu kapatmadan yapılan değişikliğin etkin olmasını isterseniz Uygula düğmesine basabilirsiniz.
Çoğu iletişim kutusu dinamik yardımı destekler.
<!-- KC:beginInclude -->
Bir iletişim kutusunda `f1`e basıldığında, odaklanılan ayar veya geçerli iletişim kutusuyla ilgili bölüm kullanıcı rehberinde açılır.
<!-- KC:endInclude -->
Bazı ayarlar kısayol tuşlarıyla da değiştirilebilmektedir. bu tuşlar ilgili olan aşağıdaki bölümlerinde listelenmiştir.

### NVDA Ayarları {#NVDASettings}

<!-- KC:settingsSection: || Ad | Masaüstü Kısayol tuşu | Dizüstü Kısayol tuşu | Tarif | -->
NVDA, ayarlar iletişim kutusundan değiştirilebilen birçok yapılandırma seçeneği sunar.
Değiştirmek istediğiniz ayarları bulmayı kolaylaştırmak için, iletişim kutusu değiştirilecek  kategorilerin bir listesini gösterir.
Bir kategori seçtiğinizde, kategori ile ilgili ayarlar bu iletişim kutusunda gösterilecektir.
Kategoriler arasında geçiş yapmak için önce `tab` ve `şift+tab` tuşlarıyla kategori listesini bulun, ardından yukarı ve aşağı okları kullanarak kategoriler arasında gezinin.
Ayrıca ayarlar iletişim kutusunun herhangi bir yerinde kategoriler arasında hızlı bir şekilde geçiş yapmak için `kontrol+tab` ile ileri, `kontrol+şift+tab` tuşlarıyla ise geri gidebilirsiniz.

Ayarlarla ilgili değişiklikleri iletişim kutusunu kapatmadan kaydetmek için uygula düğmesine basın.
Değişiklikleri kaydedip iletişim kutusunu kapatmak içinse tamam düğmesine basabilirsiniz.

Bazı kategorilerle ilgili iletişim kutusunu açmak için daha önce atanmış kısayol tuşlarını kullanabilirsiniz.
Söz konusu kısayol tuşlarına bastığınızda, NVDA ayarlar iletişim kutusu ilgili kategori sekme sayfası etkin şekilde açılacaktır.
Varsayılan olarak tüm kategoriler için kısayol tuşu belirlenmemiştir.
Daha önce atanmış kısayol tuşu bulunmayan kategorilere kısayol tuşu ya da dokunma hareketiyle ulaşmak isterseniz, [Girdi Hareketleri iletişim kutusunu](#InputGestures) kullanın.

NVDA Ayarları iletişim kutusu altındaki ayar kategorileri aşağıda verilmektedir.

#### Genel {#GeneralSettings}

<!-- KC:setting -->

##### Genel ayarları aç {#OpenGeneralSettings}

Kısayol Tuşu: `NVDA+kontrol+g`

NVDA Ayarları iletişim kutusundaki Genel kategorisi, arayüz dili, güncelleme kontrolünün otomatik yapılıp yapılmayacağı gibi NVDA'nın genel davranışını belirleyen ayarlarla ilgilidir.
Bu kategori altında aşağıdaki seçenekler mevcuttur:

##### Dil {#GeneralSettingsLanguage}

NVDA arayüzü ve mesajlarının gösterileceği dilin seçildiği bir seçim kutusudur.
İçinde birçok dil bulunur; ancak varsayılan ayar "Kullanıcı varsayılan Windows" ayarıdır.
Bu seçenek NVDA'ya O an windowsun ayarlandığı dili kullanmasını söylemektedir.

Dili değiştirdiğinizde NVDA'nın yeniden başlatılması gerektiğini lütfen not edin.
NVDA seçimi değiştirip kaydettiğinizde programı yeniden başlatmak isteyip istemediğinizi soaracaktır. Onaylama diyalogu belirdiğinde, yeni dili şimdi veya daha sonra kullanmak istiyorsanız, "şimdi yeniden başlat" veya "daha sonra yeniden başlat" seçeneğini seçin. "Daha sonra yeniden başlat" seçilirse, konfigürasyon kaydedilmelidir (manuel  veya çıkışta kaydet seçeneği kullanılarak).

##### Çıkışta Ayarları (konfigürasyonu) Kaydet {#GeneralSettingsSaveConfig}

Bu bir onay kutusudur ve işaretlendiğinde, NVDA'ya çıkışta yapılan ayarların kaydedilmesini söyler.

##### NVDA'yı kapatırken çıkış seçeneklerini göster {#GeneralSettingsShowExitOptions}

Bu seçenek, NVDA kapatılırken, çeşitli seçeneklerin bulunduğu bir iletişim kutusunun gösterilip gösterilmeyeceğiyle ilgili bir onay kutusudur.
İşaretlenirse, NVDA'yı kapatmaya teşebbüs ettiğinizde, NVDA'yı kapatmak mı, yeniden başlatmak mı, eklentileri devre dışı bırakarak yeniden başlatmak mı yoksa, varsa bekleyen güncellemeyi kurmak mı istediğinizi soran bir iletişim kutusu açılacaktır.
İşaretlenmezse, NVDA hemen kapanır.

##### NVDA Açılırken ve Kapanırken Ses Çal {#GeneralSettingsPlaySounds}

BU seçenek NVDA açılış ve kapanış sesinin çalınıp çalınmamasıyla ilgili bir onay kutusudur.

##### Kayıt Tutma (logging) Seviyesi {#GeneralSettingsLogLevel}

Bu bir seçim kutusudur ve NVDA çalışırken ne kadar kayıt tutacağınızı ayarlamanızı sağlar.
Genellikle kullanıcıların çok fazla kayıt tutulmasını istemeye ihtiyaçları yoktur.
Bununla birlikte, bir hata raporunda bilgi sağlamak veya  günlük kaydını tamamen etkinleştirmek veya devre dışı bırakmak istiyorsanız, yararlı bir seçenek olabilir.

Mevcut günlük tutma seviyeleri:

* Devre dışı: Kısa bir başlangıç mesajı dışında, NVDA çalışırken hiçbir şeyi kaydetmez.
* Bilgi: NVDA, başlangıç mesajları ve geliştiriciler için yararlı bilgiler gibi temel bilgileri kaydeder.
* Hata ayıklama uyarısı: Ciddi hatalardan kaynaklanmayan uyarı mesajları kaydedilir.
* girdi/çıktı: Klavye ve braille ekranlarından girdilerin yanı sıra konuşma ve braille çıktısı kaydedilecektir.
Gizlilik konusunda endişeleriniz varsa, günlük düzeyini bu seçeneğe ayarlamayın.
* Hata ayıklama: Bilgi, uyarı ve girdi/çıktı mesajlarına ek olarak, ek hata ayıklama mesajları kaydedilecektir.
Girdi/çıktı ayarında  olduğu gibi, gizlilikten endişe duyuyorsanız, günlük kaydı seviyesini bu seçeneğe ayarlamamalısınız.

##### NVDA'yı Windowsu açınca Otomatik Olarak Başlat {#GeneralSettingsStartAfterLogOn}

Bu seçenek etkinleştirilirse, Windowsta oturum açar açmaz NVDA otomatik olarak başlayacaktır.
Bu seçenek, yalnızca yüklenebilen NVDA kopyalarında mevcuttur.

##### Windows Giriş Ekranında NVDA'yı Kullan (Yönetici yetkisi gerekirr) {#GeneralSettingsStartOnLogOnScreen}

Windowsa kullanıcı adı ve şifre girerek oturum açıyorsanız, bu seçeneği etkinleştirdiğinizde, oturum açma ekranında NVDA da otomatik olarak başlayacaktır.
Bu seçenek, yalnızca sisteme yüklenmiş olan NVDA kopyalarında mevcuttur.

##### Windows Giriş ve Diğer Güvenli Ekranlarda Mevcut kaydedilmiş Ayarları Kullan (Yönetici yetkisi gerekirr) {#GeneralSettingsCopySettings}

Bu düğmeye basmak Şu anki NVDA ayarlarınızı NVDA system configuration dizinine kopyalar ve böylece oturum açma, kullanıcı hesapları kontrolü (uac) ve diğer [güvenli ekranlarda](#SecureScreens) NVDA bu ayarları kullanır.
Tüm ayarlarınızın transfer edildiğinden emin olmak için, önce kontrol+NVDA+c tuşlarına basarak NVDA ayarlarınızı kaydettiğinizden emin olun veya NVDA menüsünden konfigürasyonu  kaydedin.
Bu seçenek, yalnızca bilgisayara kurulu  NVDA kopyalarında mevcuttur.

##### NVDA Güncellemelerini Otomatik Olarak Kontrol Et {#GeneralSettingsCheckForUpdates}

Bu etkinleştirildiyse, NVDA güncel sürüm olup olmadığını otomatik olarak kontrol edecek ve güncelleme bulunduğunda sizi bilgilendirecektir.
Ek olarak, NVDA Yardım menüsü altında bulunan, güncelleme olup olmadığına bak seçeneğini kullanarak istediğiniz zaman güncelleme kontrolü yapabilirsiniz.
Manuel veya otomatik olarak güncellemeleri kontrol ederken, sisteminiz için doğru güncellemeyi indirmeniz için NVDA'nın güncelleme sunucusuna bazı bilgileri göndermesi gerekir.
Aşağıdaki bilgiler, her zaman gönderilir: 

* Mevcut NVDA sürümü
* İşletim Sistemi sürümü
* İşletim Sisteminin 64 veya 32 bit mi olduğu bilgisi

##### NV Access'in NVDA kullanım istatistiklerini toplamasına izin ver {#GeneralSettingsGatherUsageStats}

Etkinleştirilmişse, NV Access NVDA kullanıcı sayısını takip etmek için güncelleme kontrollerinden topladığı işletim sistemi, ülke gibi bazı demografik bilgileri kullanır.
Ülkenizi belirlemek için IP adresi kullanılıyor olsa da, bu bilginin hiçbir suretle kaydedilmediğini not edin.
Güncellemeleri kontrol etmek için zorunlu olan bilgilerin yanında, aşağıdaki ek bilgiler de gönderilir:

* NVDA arayüz dili
* NVDA kopyasının kurulu mu yoksa taşınabilir mi olduğu
* Kullanılan geçerli konuşma sentezleyici adı (eklentinin adı ve kaynağı dahil)
* Kullanılan geçerli Braille ekranın adı (eklentinin adı ve kaynağı dahil)
* Braille çıktısı için kullanılan tablo (tabii braille kullanılıyorsa)

Bu bilgi, NVAccess'e NVDA gelişim sürecindeki öncelikleri belirlemesinde önemli bir destek sunmaktadır.

##### NVDA başladığında Bekleyen Güncelleme Varsa Bildir {#GeneralSettingsNotifyPendingUpdates}

Etkinleştirilmişse, NVDA başlangıçta bekleyen bir güncelleme olduğu zaman, kurma seçeneği sunarak size bilgi verecektir.
NVDA kapatılırken çıkış seçenekleri gösteriliyorsa, buradan manuel olarak da bekleyen güncellemeyi kurabilirsiniz  ya da yardım menüsü altından güncelleme kontrolü yapabilirsiniz.

#### Konuşma Ayarları {#SpeechSettings}

<!-- KC:setting -->

##### Konuşma ayarlarını aç {#OpenSpeechSettings}

Kısayol Tuşu: `NVDA+lpmtrpş+v`

NVDA Ayarları iletişim kutusundaki konuşma kategorisi, konuşmacı ve  sesle ilgili parametreleri değiştirmenizi sağlayan seçenekler içerir.
Konuşma parametrelerini istenen her yerden değiştirebileceğiniz daha hızlı bir alternatif için, lütfen [Hızlı Sentezleyici Ayarları](#SynthSettingsRing) bölümüne bakın.

Ses ayarları iletişim kutusunda şu seçenekler bulunmaktadır:

##### Sentezleyici Değiştir {#SpeechSettingsChange}

Konuşma Ayarları kategorisinde ilk seçenek Değiştir... düğmesidir. Bu düğme etkin konuşma sentezleyiciyi ve çıkış aygıtını belirlemeniz için  [sentezleyici değiştir](#SelectSynthesizer) iletişim kutusunu etkinleştirir.
Bu iletişim kutusu, NVDA Ayarları iletişim kutusunun üzerinde açılır.
Sentezleyici seçimiyle ilgili değişiklikler kaydedilirse ya da iptal edilirse odak NVDA Ayarları iletişim kutusuna döner.

##### Ses {#SpeechSettingsVoice}

Bu iletişim kutusuna girdiğinizde karşınıza çıkan ilk seçenek, yüklediğiniz sentezleyicinin seslerinin listelendiği bir seçim kutusudur.
Oklara basarak farklı ses seçeneklerini dinleyebilirsiniz.
Sol ve yukarı yön tuşları sizi listenin yukarısına götürürken, sağ ve aşağı yön tuşları listenin aşağısına doğru götürür.

##### Konuşucu {#SpeechSettingsVariant}

NVDA ile gelen Espeak NG sentezleyicisini kullanıyorsanız, burası, sentezleyicinin konuşacağı konuşucuların listelendiği bir seçim kutusudur.
Espeak NG konuşucuları farklı seslere benzer ve bir sese farklı özelliklerin yüklenmesini sağlar.
Bazı sesler kadın, bazıları erkek, hatta bazıları kurbağa sesi gibi çıkabilir.
Bir üçüncü taraf sentezleyici kullanıyorsanız, seçtiğiniz ses destekliyorsa bu değeri değiştirebilirsiniz.

##### Hız {#SpeechSettingsRate}

Bu seçenek konuşma hızını değiştirmenizi sağlar.
Burası 0'dan 100'e giden bir göstergedir, ve 0 en yavaşı gösterirken, 100 en hızlıyı gösterir.

##### Hızlandırıcı {#SpeechSettingsRateBoost}

Bu seçeneğin etkinleştirilmesi, mevcut sentezleyici tarafından destekleniyorsa konuşma hızını önemli ölçüde artıracaktır.

##### Ses Perdesi {#SpeechSettingsPitch}

Bu seçenek konuşmacının  ses perdesini değiştirmenizi sağlar.
Burası 0'dan 100'e giden bir göstergedir, ve 0 en düşük perdeyi yani kalını gösterirken, 100 en yüksek perdeyi yani en inceyi gösterir.

##### Ses Seviyesi {#SpeechSettingsVolume}

Burası 0'dan 100'e giden bir göstergedir, ve 0 en düşük ses seviyesini gösterirken, 100 en yüksek ses seviyesini gösterir.

##### Tonlama {#SpeechSettingsInflection}

Bu seçenek, sentezleyicinin konuşacağı  tonlamayı (iniş çıkış) kullanacağını belirlemenizi sağlayan bir göstergedir.

##### Konuşma Dilinin Otomatik Değişimi {#SpeechSettingsLanguageSwitching}

Bu onay kutusu, okunmakta olan belgedeki metinlerin dili tanımlandıysa,, NVDA'nın konuşma dilini otomatik olarak değiştirip değiştirmemesiyle ilgili ayarı yapmanızı sağlar.
Bu seçenek varsayılan olarak etkinleştirilmiştir.

##### Otomatik Lehçe Değişimi {#SpeechSettingsDialectSwitching}

Otomatik dil değişimiyle ilgili seçenek etkinse, bu onay kutusu da okunan belgedeki lehçe değişikliklerine göre NVDA'nın da konuşma dilini otomatik olarak değiştirip değiştirmemesiyle ilgili ayarı yapmanızı sağlar.
Örneğin, ABD İngilizcesiyle yazılmış bir belge içinde Büyük Krallık İngilizcesiyle yazılmış kısımlar varsa, NVDA konuşma dilini otomatik olarak ABD İngilizcesinden Büyük Krallık İngilizcesine değiştirebilir.
Bu seçenek varsayılan olarak etkin değildir.

<!-- KC:setting -->

##### Noktalama İşaretlerini Söyleme düzeyi {#SpeechSettingsSymbolLevel}

Kısayol tuşu: NVDA+p

Bu, noktalama ya da başka işaretlerin ne kadarının sözcük olarak seslendirileceğiyle ilgili ayarı değiştirmenizi sağlar.
Örneğin, Tümü olarak ayarladığınızda işaretlerin hepsi sözcük olarak seslendirilir.
Bu ayardan sadece halihazırda kullanılan sentezleyici değil; tüm sentezleyiciler etkilenir.

##### Karakter ve sembolleri işlerken sentezleyici ve sesin dilini dikkate al {#SpeechSettingsTrust}

Bu seçenek varsayılan olarak etkindir ve NVDA'ya karakter ve semboller seslendirilirken seçili sesin dilinin dikkate alınıp alınmayacağını söyler.
NVDA'nın noktalama işaretlerini herhangi bir sentezleyici ya da ses için yanlış dilde seslendirdiğini fark ederseniz, bu seçeneği NVDA global ayarlarının kullanılmasını sağlamak için kapatabilirsiniz.

##### Karakter ve sembooleri işlerken (emoji dahil) Unicode Konsorsiyumu verisini dahil et {#SpeechSettingsCLDR}

Bu onay kutusu etkinleştirildiğinde, NVDA karakter ve sembolleri tellaffuz ederken  ek  telaffuz sözlüklerini kullanır.
Bu sözlükler çeşitli sembollerin telaffuzunu içerir  (özellikle emoji) ve [Unicode Consortium](https://www.unicode.org/consortium/) tarafından [Ortak Yerel Veri Deposu](http://cldr.unicode.org/) içinde sağlanırlar.
Emojilerin bu verilere dayanılarak seslendirilmesini istiyorsanız bu onay kutusunu işaretleyin.
Ancak emojilerin kullandığınız sentezleyici tarafından seslendirilmesini istiyorsanız bu onay kutusunu işaretlememelisiniz.

Öte yandan, elle eklediğiniz ya da düzenlediğiniz karakter tanımları kullanıcı ayarlarınızın bir bölümü olarak kaydedilir.
Dolayısıyla, bir emojinin okunuşunu değiştirdiğinizde, bu onay kutusu işaretli olsun olmasın, emoji yaptığınız değişiklik doğrultusunda telaffuz edilecektir.
NVDA'nın [noktalama/imla sözlüğü iletişim kutusundan](#SymbolPronunciation) karakter okunuşlarını ekleyebilir, düzenleyebilir ya da silebilirsiniz.

Unicode Konsorsiyum verisinin dahil edilmesini her yerden değiştirmek için, lütfen [Girdi Hareketleri iletişim kutusu](#InputGestures)nu kullanarak özel bir hareket atayın.

##### Büyük Harflerde Ses Perdesi Değişim Yüzdesi {#SpeechSettingsCapPitchChange}

Bu yazı alanı , büyük harfler seslendirilirken ses perdesinin hangi oranda değiştirileceğini belirlemenizi sağlar.
Bu değer yüzde belirtir ve negatif değer sesi kalınlaştırırken pozitif değer sesi inceltecektir. 
Ses perdesinde değişiklik olmasını istemezseniz buraya 0 yazabilirsiniz.
Genellikle, NVDA herhangi bir büyük harf için ses perdesini hafifçe yükseltir, ancak bazı sentezleyiciler bunu desteklemeyebilir.
Büyük harfler için perde değişiminin desteklenmediği durumlarda, [Büyük harflerden önce "büyük" de](#SpeechSettingsSayCapBefore) ve / veya [Büyük harflerde bip sesi çıkar](#SpeechSettingsBeepForCaps) seçeneklerini kullanabilirsiniz.

##### Büyük Harflerden Önce Büyük De {#SpeechSettingsSayCapBefore}

Bu ayar bir onay kutusudur ve işaretlendiğinde, metin içinde oklarla dolaşırken veya bir karakteri yazarken, karakter büyük yazılmışsa, öncesinde "büyük" sözcüğü söylenecektir.

##### Büyük harflerde Bip sesi çıkar {#SpeechSettingsBeepForCaps}

Bu onay kutusu işaretlenirse, NVDA büyük yazılmış bir karakterle karşılaştığında bip sesi çıkaracaktır.

##### Destekleniyorsa Kodlama İşlevini Kullan {#SpeechSettingsUseSpelling}

Bazı sözcükler sadece bir karakterden oluşabilir, ancak o karakterin bir sözcüğün içerisinde kodlanırkenki telaffuzu farklılık gösterir.
Örneğin, İngilizce'de "a" hem bir harftir hem de tek başına bir sözcük. Sözcükken "a" olarak okunurken kodlama sırasında "ey" olarak seslendirilmelidir.
Bu seçenek, tabii destekliyorsa, mevcut sentezleyicinin bu iki durumu birbirinden ayırt etmesine olanak sağlar.
Birçok sentezleyici bu işlevi destekler.

Bu seçenek genel olarak etkin olmalıdır.
Öte yandan, bazı Microsoft SAPI sentezleyiciler bu işlevi desteklemezler ve bu seçenek etkin olduğunda, yazarken ve okurken karakterlerin seslendirilmemesi gibi tuhaf tepkiler verebilirler.
Eğer karakterlerin seslendirilmemesi gibi bir sorun yaşıyorsanız bu seçeneği etkisizleştirmeniz problemi çözecektir.

##### İmleç hareketi sırasında karakter tanımını bildir {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Varsayılan |Devre dışı|
|Seçenekler |Etkin, Devre Dışı|

Bu ayar Etkinken, imleçle karakterler arasında gezinirken NVDA karakter tanımını otomatik olarak bildirecektir.

Örneğin, bir kelimede karakter karakter dolaşılırken b harfi bildirildikten 1 saniye sonra NVDA harfin tanımını, (Bolu) Bildirecektir.
Bu, telaffuzları benzer olan sembol veya karakterlerin kolayca ayırt edilebilmelerini sağlar ve işitme engelli kullanıcılara yardımcı olabilir.

Tanımların okunması `Kontrol` tuşuna basılması veya yeni bir metin gelmesi durumunda iptal edilir.

##### Konuşma modları arasında geçiş yapma komutuyla geçiş yapılabilecek konuşma modları {#SpeechModesDisabling}

Bu liste, `NVDA+s` ile geçiş yapılabilecek [konuşma modlarını](#SpeechModes) seçmenizi sağlar.
Onay kutusu işaretli olmayan modlar görüntülenmez.
Varsayılan olarak tüm modlar görünür.

Örneğin, "bipleme" ve "kapalı" modunu kullanmanız gerekmiyorsa, mevcut iki seçeneğin işaretini kaldırarak sadece "konuşma" ve "isteğe bağlı" seçeneklerini işaretli bırakabilirsiniz.
En az iki modun işaretli olması gerektiğini unutmayın.

#### sentezleyici seç {#SelectSynthesizer}

<!-- KC:setting -->

##### Sentezleyici Seç İletişim Kutusunu Aç {#OpenSelectSynthesizer}

Kısayol Tuşu: `NVDA+kontrol+s`

NVDA Ayarları iletişim kutusundaki konuşma kategorisinde Değiştir... düğmesini etkinleştirerek  açılan sentezleyici iletişim kutusu, NVDA'nın hangi sentezleyiciyle konuşacağını seçmenizi sağlar.
İstediğiniz sentezleyiciyi seçtikten sonra, Tamam düğmesine basarsanız, NVDA seçilen sentezleyiciyi yükleyecektir.
Sentezleyici yükleme sırasında bir hata oluşursa, NVDA sizi bir mesajla uyarıp önceki sentezleyiciyi kullanmaya devam edecektir.

##### Sentezleyici {#SelectSynthesizerSynthesizer}

Bu seçenek, NVDA'nın konuşma çıktısı için kullanmasını istediğiniz sentezleyiciyi seçmenizi sağlar.

NVDA'nın desteklediği sentezleyicilerin listesi için lütfen [Desteklenen Konuşma Sentezleyicileri](#SupportedSpeechSynths) bölümüne bakın.

Bu listede sunulan seçeneklerden biri de "Sessiz" ögesidir ve NVDA'yı hiç konuşma çıktısı olmadan kullanmanızı sağlar.
BU, NVDA'yı yalnızca braille ekran ile kullanmak isteyenler ve belki de yalnızca konuşma ekranlarını görmek isteyen gören NVDA geliştiricileri için yararlı olabilir.

#### Hızlı Sentezleyici Ayarları {#SynthSettingsRing}

Eğer NVDA ile çalışırken ses ayarları iletişim kutusuna gitmeden herhangi bir yerde seri biçimde konuşma ayarlarını değiştirmek istiyorsanız, en sık kullanılan konuşma ayarlarını değiştirmenizi sağlayan bazı NVDA tuş komutları bulunmaktadır:
<!-- KC:beginInclude -->

| Ad |Masaüstü Kısayol tuşu |Dizüstü Kısayol tuşu |Tarif|
|---|---|---|---|
|Bir sonraki sentezleyici ayarına gitme |NVDA+kontrol+Sağ Yön tuşu |NVDA+kontrol+şift+Sağ Yön tuşu |Geçerli sentezleyici ayarından bir sonrakine geçer. eğer en son sentezleyici ayarındaysanız en baştakine atlar|
|Bir önceki sentezleyici ayarına gitme |NVDA+kontrol+SolYön tuşu |NVDA+kontrol+şift+Sol Yön tuşu |Geçerli sentezleyici ayarından bir öncekine geçer. eğer en baştaki sentezleyici ayarındaysanız en sondakine atlar|
|Seçili sentezleyici ayarını arttırma |NVDA+kontrol+YukarıYön tuşu |NVDA+kontrol+şift+YukarıOk| üzerinde bulunduğunuz sentezleyici ayarını arttırır. (örnek: hızı arttırır, bir sonraki sesi seçer, ses seviyesini arttırır.)|
|Seçili sentezleyici ayarını geniş ölçekte arttır |`NVDA+kontrol+pageUp` |`NVDA+şift+kontrol+pageUp` |üzerinde bulunduğunuz geçerli sentezleyici ayarını  daha geniş bir ölçekte artırır. Örneğin. konuşma ayarındayken 20 ses ileri gider veya ses seviyesi veya ses perdesi gibi sürgülü alanlarda değeri 20 arttırır|
|Seçili sentezleyici ayarını azaltma |NVDA+kontrol+AşağıOk| NVDA+kontrol+şift+AşağıOk| üzerinde bulunduğunuz sentezleyici ayarını azaltır. (örnek: hızı azaltır, bir önceki sesi seçer, ses seviyesini azaltır.)|
|Seçili sentezleyici ayarını geniş ölçekte azalt |`NVDA+kontrol+pageDown` |`NVDA+şift+kontrol+pageDown` |üzerinde bulunduğunuz geçerli sentezleyici ayarını  daha geniş bir ölçekte azaltır Örneğin. konuşma ayarındayken 20 ses geri gider veya ses seviyesi veya ses perdesi gibi sürgülü alanlarda değeri 20 azaltır|

<!-- KC:endInclude -->

#### Braille {#BrailleSettings}

NVDA Ayarları iletişim kutusundaki Braille kategorisi braille girişi ve çıktısıyla ilgili çeşitli parametrelerin ayarlanabileceği seçenekleri içerir.
Bu kategori aşağıdaki seçenekleri içerir:

##### Braille Ekranı Değiştir {#BrailleSettingsChange}

NVDA Ayarları iletişim kutusundaki Braille kategorisindeki Değiştir... düğmesi etkin kabartma ekranı belirlemenizi sağlayan [braille ekran seçimi](#SelectBrailleDisplay) iletişim kutusunu açar.
Bu iletişim kutusu NVDA ayarları iletişim kutusunun üzerinde açılır.
Braille ekran değişikliğini kaydetmeniz ya da iptal etmeniz sonucunda odak NVDA ayarları iletişim kutusuna döner.

##### Çıktı Tablosu {#BrailleSettingsOutputTable}

Bu iletişim kutusundaki bir sonraki seçenek braille çıktı tablosu seçim kutusudur.
Bu seçim kutusunda, farklı diller için braille tabloları bulacaksınız.
Seçilen tablo, kabartma ekranda metnin nasıl gösterileceğini belirler.
Bir braille tablodan diğerine yön tuşlarını kullanarak geçebilirsiniz.

##### Girdi Tablosu {#BrailleSettingsInputTable}

Önceki seçeneği bütünleyen bir özellik olarak, bulacağınız sonraki ayar braille girdi tablosu seçim kutusudur.
Seçilen tablo kabartma ekranınızın klavyesinden braille olarak metin girişi yapmanız için kullanılır.
Bir braille tablodan diğerine yön tuşlarını kullanarak geçebilirsiniz.

Bu işlev yalnızca, üzerinde klavye bulunan ve sürücüsü bu özelliği destekleyen braille ekranlar için geçerlidir.
Üzerinde klavye bulunduğu halde kabartma ekran bu özelliği desteklemiyorsa, bu [Desteklenen Kabartma Ekranlar](#SupportedBrailleDisplays) bölümünde belirtilir.

<!-- KC:setting -->

##### Braille Modu {#BrailleMode}

Kısayol Tuşu: `NVDA+alt+t`

Bu seçenek mevcut braille modları arasında seçim yapmanıza yarar.

Mevcut durumda "imleçleri takip et" ve "konuşma çıkışını takip et" modları bulunmaktadır.

İmleçleri takip et seçildiğinde, braille ekran ==== Braille'in İzleyeceği İmlece göre sistem odağını veya inceleme imlecini takip edecektir.

Konuşma Çıkışını Takip Et seçildiğinde, braille ekranı konuşma modu konuşmaya ayarlandığında NVDA'nın okuyacağı metni gösterecektir.

##### İmleç altındaki sözcüğü bilgisayar braille olarak Genişlet {#BrailleSettingsExpandToComputerBraille}

Bu seçenek, imlecin üzerinde bulunduğu sözcüğün kısaltmasız bilgisayar braille ile gösterilmesini sağlar.

##### İmleci göster {#BrailleSettingsShowCursor}

Bu seçenek, brail imlecini açıp kapatmanızı sağlar.
Sistem imleci ve inceleme imleci için uygulanır; seçimin belirtilmesi için geçerli değildir.

##### İmleç Sinyali {#BrailleSettingsBlinkCursor}

Bu seçenek, braille imlecin yanıp sönmesini sağlar.
Sinyal kapatıldıysa, braille imleç yukarıda sabitlenir.
Seçim göstergesi bu tercihten etkilenmez, her zaman 7 ve 8 nokta yukarıdadır.

##### İmleç inip çıkma hızı {#BrailleSettingsBlinkRate}

Bu seçenek, imleç inip çıkma hızının milisaniyede ne kadar hızlı olacağını değiştirmenizi sağlayan rakamsal bir alandır.

##### odak için imleç Şekli {#BrailleSettingsCursorShapeForFocus}

Bu seçenek, odak tarafından taşındığı durumda braille imlecin şeklini belirlemenizi sağlar.
Seçim belirteci bu tercihten etkilenmez, her zaman 7 ve 8 nokta yukarıdadır.

##### İnceleme imleci için imleç Şekli {#BrailleSettingsCursorShapeForReview}

Bu seçenek, inceleme imleci tarafından taşındığı durumda braille imlecin şeklini belirlemenizi sağlar.
Seçim belirteci bu tercihten etkilenmez, her zaman 7 ve 8 nokta yukarıdadır.

##### Mesajları Göster {#BrailleSettingsShowMessages}

Bu, NVDA'nın braille mesajlarını gösterip göstermeyeceğini ve bunların ne zaman otomatik olarak kaybolacağını seçmenize olanak tanıyan bir seçim kutusudur.

Mesajları Göster ayarını hızlıca değiştirmek için [Girdi Hareketleri iletişim kutusu](#InputGestures) üzerinden bir girdi ataması yapabilirsiniz.

##### Mesaj Zaman Aşımı Saniyesi {#BrailleSettingsMessageTimeout}

Bu seçenek, sistem mesajlarının braille ekranda ne kadar uzun süre gösterileceğini kontrol eden bir rakamsal alandır.
Braille ekranında bir yönlendirme tuşuna basıldığında NVDA mesajı hemen kapatılır, ancak mesajı tetikleyen ilgili tuşa basıldığında tekrar gösterilir.
Bu seçenek yalnızca "Mesajları Göster", "Zaman aşımını kullan" olarak ayarlanmışsa gösterilir.

<!-- KC:setting -->

##### Braille'in İzleyeceği İmleç {#BrailleTether}

Kısayol tuşu: NVDA+kontrol+t

Bu seçenek Braille ekranın sistem imlecini mi, nesne sunucusu/inceleme imlecini mi yoksa her ikisini de mi izleyeceğini belirlemenizi sağlar.
"Otomatik olarak" seçildiğinde, NVDA varsayılan olarak odağı ve düzenleme imlecini takip eder.
Bu durumda, kullanıcı nesne sunucusunun ya da inceleme imlecinin konumunu değiştirirse, NVDA geçici olarak inceleme imlecini takip eder, odak ya da düzenleme imlecinin konumu değişene kadar.
Sadece odağı ve sistem düzenleme imlecini takip etmesini istiyorsanız, braille'in odak tarafından taşınmasını ayarlayabilirsiniz.
Bu durumda, braille nesne navigasyonu sırasında NVDA nesne sunucusunu veya inceleme sırasında inceleme imlecini takip etmez.
Braille'in nesne sunucusu ve metin inceleme imlecini takip etmesini  istiyorsanız, braille'in inceleme imleci tarafından taşınmasını ayarlayabilirsiniz.
Bu durumda braille sistem odağını ve düzenleme imlecini takip etmez.

##### Braille inceleme imlecini taşırken sistem düzenleme imlecini hareket ettir {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|seçenekler |varsayılan (hiçbir zaman), hiçbir zaman, Yalnızca otomatik olarak bağlandığında, herzaman|
|Varsayılan |hiçbir zaman|

Bu seçenek, sistem imlecinin hareket ettirme düğmesine basarak da hareket ettirilip ettirilmeyeceğini belirler.
Bu seçenek, varsayılan olarak Hiçbir zaman olarak seçilidir. Yani inceleme imleci taşındığında imleç hareket etmez.

Bu seçenek Her Zaman olarak ayarlandığında ve [Braille taşınsın](#BrailleTether) "otomatik olarak" veya "inceleme imleci" olarak ayarlandığında, hareket ettirme tuşuna basmak, desteklendiğinde sistem imlecini veya odağını da hareket ettirir.
Mevcut inceleme modu [inceleme imleci](#ScreenReview) olduğunda, görünür bir imleç yoktur.
Bu durumda, NVDA hareket ettirdikçe metnin altındaki nesneyi odaklamaya çalışır.
Aynı durum [nesne incelemesi](#ObjectReview) için de geçerlidir.

Ayrıca, imleci yalnızca otomatik olarak bağlandığında hareket ettirecek şekilde ayarlayabilirsiniz.
Bu durumda, hareket tuşuna basmak yalnızca NVDA inceleme imlecine otomatik olarak taşındığında sistem imlecini veya odak noktasını hareket ettirir. Ancak inceleme imlecinin manuel olarak taşınması durumunda herhangi bir hareket gerçekleşmez.

Bu seçenek yalnızca "[Braille taşınsın](#BrailleTether)", "Otomatik" veya "inceleme imleci" olarak ayarlandığında gösterilir.

Braille inceleme imlecini taşırken sistem düzenleme imlecini hareket ettir'i değiştirmek için lütfen [Girdi Hareketleri iletişim kutusu](#InputGestures) üzerinden özel bir girdi atayın.

##### Paragraf Paragraf Oku {#BrailleSettingsReadByParagraph}

Etkinleştirilirse, braille yazı satır yerine paragraf bazında gösterilir.
Aynı zamanda, önceki satır ve sonraki satır komutları da bu ayar uyarınca önceki ya da sonraki paragrafa gider.
Bu, braille ekranı, daha fazla metin sığması için sürekli kaydırmak zorunda olmayacağınız anlamına gelir.
Sayesinde, uzun metinleri daha akıcı olarak okuyabilirsiniz.
Varsayılan olarak, bu ayar etkinleştirilmemiştir.

##### Mümkün olduğunda sözcükleri bölmemeye çalış {#BrailleSettingsWordWrap}

Bu etkinleştirilirse, braille satıra sığmayan son sözcük bölünmez.
Bunun yerine, satır sonunda boş hücreler gösterilir.
Ekranı kaydırdığınızda sözcüğü okuyabilirsiniz.
Bu bazen "sözcük kaydırma" olarak çağrılır.
Sözcüğün tek başına satıra sığmaması halinde bu kez bölüneceğini not edin.

Bu etkinleştirilmemişse, satıra mümkün olduğunca fazla karakter sığdırılır.
Ekranı kaydırdığınızda bölünmüş sözcüğün kalanını okuyabilirsiniz.

Bunu etkinleştirmek daha akıcı bir okuma olanağı sunmakla birlikte, ekranı kaydırmak için ilgili tuşlara daha fazla basmanızı gerektirecektir.

##### Odak bağlam sunumu {#BrailleSettingsFocusContextPresentation}

Bu seçenek bir nesne üzerine gittiğinizde NVDA'nın braille ekranda hangi bağlamı göstereceğini seçmenizi sağlar.
Bağlam bilgisi odağı içeren nesnelerin hiyerarşisini ifade eder.
Mesela, bir liste öğesine odaklanırsanız, bu liste öğesi bir listede yer alır.
Bu liste, iletişim kutusu, vb tarafından içerilmiş olabilir.
Lütfen NVDA nesneleri için geçerli olan hiyerarşi hakkında daha fazla bilgi için ilgili bölüme başvurun [nesne dolaşımı](#ObjectNavigation).

Bağlam değişimi için ekranı doldur seçeneği seçilmişse, NVDA braille ekranda mümkün olduğunca çok bilgi göstermek için çalışır, ama içeriğin yalnızca değişen bölümleri için.
Yukarıdaki örnek üzerinden, bu demektir ki listeye gittiğinizde NVDA braille ekranda liste öğesini gösterir.
Ayrıca, braille ekranda yeterince yer kaldıysa NVDA öğenin bir listenin parçası olduğunu da göstermeye çalışır.
Sonra liste üzerinde yön tuşlarıyla hareket etmeye başlarsanız, bir liste içinde olduğunuzu bildiğiniz varsayılır.
Dolayısıyla, geri kalan liste üyeleri için NVDA sadece üzerinde olduğunuz öğeyi gösterir.
Bağlamı tekrar okumak için (yani bir listede olduğunuzu ve bu listenin bir iletişim kutusunun parçası olduğunu), braille ekranı tekrar geri kaydırmanız gerekecektir.

Bu seçenek her zaman ekranı doldur olarak ayarlandıysa, NVDA bu bilgiyi daha önce görüp görmediğinizden bağımsız olarak braille ekranda bağlam bilgisini her zaman göstermeye çalışacaktır.
Bunun avantajı braille ekranda mümkün olduğunca fazla bilgi gösterilmesidir.
Dezavantajı ise, odağın başının gösterildiği yer farklılaşabilir.
Bu, parmağınızı sürekli hareket ettirmek durumunda kalacağınız için uzun bir listede aradığınız bir öğeyi bulmanızı zorlaştırabilir.
Bu, NVDA 2017.2 ve Öncesi için varsayılan davranıştı.

Odak bağlam sunum tercihini bağlam bilgisini sadece geri kaydırırken göster olarak ayarlarsanız, NVDA bağlam bilgisini varsayılan olarak bir daha göstermez.
Dolayısıyla, yukarıdaki örnekte, NVDA yalnızca liste öğesini gösterecektir.
Ancak bağlamı tekrar okumak için (yani bir listede olduğunuzu ve bu listenin bir iletişim kutusunun parçası olduğunu anlamak istediğinizde), braille ekranı geri kaydırmanız gerekecektir.

Herhangi bir yerdeyken odak bağlam sunumunu değiştirmek için, [Girdi Hareketleri iletişim kutusu](#InputGestures) kullanarak özel bir girdi hareketi oluşturun.

##### Kaydırma sırasında konuşmayı durdur {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |Varsayılan (Etkin), Etkin, Devre Dışı|
|Varsayılan |Etkin|

Bu ayar, Braille ekranı geri/ileri kaydırıldığında konuşmanın durdurulup durdurulmayacağını ayarlamanızı sağlar.
Önceki/sonraki satır komutları her zaman konuşmayı durdurur.

Braille okurken ekran okuyucunun konuşması dikkati dağıtabilir.
Bu nedenle seçenek varsayılan olarak etkindir ve braille kaydırılırken konuşma durdurulur.

Bu seçeneğin devre dışı bırakılması, aynı anda Braille okunurken konuşmanın duyulmasını sağlar.

##### Seçimi göster {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |Varsayılan (Etkin), Etkin, Devre Dışı|
|Varsayılan |Etkin|

Bu seçenek, braille ekranda seçim göstergesinin (nokta 7 ve 8) gösterilip gösterilmeyeceğini belirler.
Bu seçenek varsayılan olarak etkindir ve seçim göstergesi gösterilir.
Okuma sırasında seçim göstergesi dikkat dağıtıcı olabilir.
Bu seçeneğin devre dışı bırakılması okunabilirliği artırabilir.

Seçimi göster seçeneğini herhangi bir yerden değiştirebilmek için [Girdi hareketleri iletişim kutusu](#InputGestures) üzerinden bir girdi atayabilirsiniz.

#### Braille ekran seçimi {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Braille Ekran Seç iletişim kutusunu aç {#OpenSelectBrailleDisplay}

Kısayol tuşu: `NVDA+kontrol+a`

> NVDA Ayarları iletişim kutusundan Braille kategorisinde Değiştir... düğmesini etkinleştirerek açılan braille ekran seçimi iletişim kutusu, NVDA'nın braille çıkışı için hangi braille ekranı kullanacağını seçmenizi sağlar.
Braile ekranı seçip tamam düğmesine bastığınızda NVDA ilgili braille ekranı yükler.
Braille ekran sürücülerinin yüklenmesi ile ilgili sorun oluşursa NVDA bildirimde bulunur ve önceki braille ekran kullanılmaya devam edilir.

##### Braille Ekran {#SelectBrailleDisplayDisplay}

Bu seçim kutusunda, sisteminizde hangi braille sürücülerin yüklü olduğuna bağlı olarak, size çeşitli seçenekler sunulacaktır.
Bu seçenekler arasında yön tuşlarını kullanarak dolaşın.

Otomatik seçeneği, NVDA'nın arkaplanda desteklenen braille ekranları aramasına olanak tanır.
Bu özellik etkinleştirildiğinde ve USB ya da bluetooth kullanarak desteklenen bir braille ekranna bağlandığınızda, NVDA bu ekranla otomatik olarak bağlantı kuracaktır.

"Braille Yok", braille kullanmadığınız anlamına gelir.

Lütfen desteklenen braille ekranlar ve bunların hangilerinin arkaplanda otomatik olarak tanınabildiğiyle ilgili daha fazla bilgi için [Desteklenen Braille Ekranlar](#SupportedBrailleDisplays) bölümüne bakın.

##### Otomatik algılanacak ekranlar {#SelectBrailleDisplayAutoDetect}

Braille ekranı "Otomatik" olarak ayarlandığında, bu listede bulunan onay kutuları, otomatik algılama sürecine dahil olacak ekran sürücülerini etkinleştirmenize ve devre dışı bırakmanıza yarar.
Bu, düzenli olarak kullanmadığınız braille ekran sürücülerini hariç tutmanızı sağlar.
Örneğin, sadece Baum sürücüsünün çalışmasını gerektiren bir ekranınız varsa, Baum sürücüsünü etkin bırakabilirken diğer sürücüleri devre dışı bırakabilirsiniz.

Varsayılan olarak otomatik algılamayı destekleyen tüm sürücüler etkindir.
NVDA'nın gelecekteki bir sürümüne veya bir eklentiyle yüklenen başka sürücüler de otomatik olarak bu listeye dahil edilip varsayılan olarak etkinleştirilecektir.

Listedeki bir sürücünün ekranların otomatik algılanmasını destekleyip desteklemediğini kontrol etmek için [desteklenen braille ekranlar](#SupportedBrailleDisplays) bölümünde Braille ekranınızın dokümantasyonuna başvurabilirsiniz.

##### Port {#SelectBrailleDisplayPort}

Bu seçenek, eğer mevcutsa, seçtiğiniz kabartma ekranla hangi port ya da bağlantı tipini kullanarak bağlantı kuracağınızı belirlemenizi sağlar.
Bu, kabartma ekranınız için mevcut seçeneklerin sunulduğu bir seçim kutusudur.

Varsayılan olarak, NVDA otomatik port belirlemeyi kullanır, yani kabartma ekranla bağlantı mevcut USB ve bluetooth araçları taranarak otomatik olarak belirlenir.
Ancak bazı kabartma ekranlar için, hangi bağlantıyı kullanacağınızı özel olarak belirleyebilmeniz de mümkündür.
Genel seçenekler (NVDA'ya varsayılan otomatik port seçme prosedürünü kullanmasını söyleyen) "Otomatik", "USB", "Bluetooth" ve eğer kabartma ekranınız destekliyorsa seri bağlantı portlarıdır.

Bu bölüm braille ekranınız yalnızca otomatik port belirlemeyi destekliyorsa gösterilmez.

Desteklenen bağlantı tipleri ve mevcut portlar için daha fazla detaya ulaşmak için [desteklenen braille ekranlar](#SupportedBrailleDisplays) bölümünde Braille ekranınızın dokümantasyonuna baş vurabilirsiniz.

Lütfen dikkat: Makinenize aynı anda aynı sürücüyü kullanan birden fazla Braille Ekranı bağlarsanız (Örneğin iki Seika ekranını bağlama),
NVDA'ya hangi ekranın kullanılacağını belirtmek  şu anda olanaklı değil.
Bu nedenle, makinenize aynı anda yalnızca belirli bir türde / üreticiye ait bir Braille Ekranı bağlamanız önerilir.

#### Ses {#AudioSettings}

<!-- KC:setting -->

##### Ses ayarlarını aç {#OpenAudioSettings}

Kısayol Tuşu: `NVDA+kontrol+u`

NVDA Ayarları iletişim kutusundaki Ses kategorisi, ses çıkışının çeşitli yönlerini değiştirmenizi sağlayan seçenekler içermektedir.

##### Çıktı Aygıtı {#SelectSynthesizerOutputDevice}

Bu seçenek, NVDA'nın seçilen sentezleyicinin üzerinden konuşacağı ses kartını seçmenizi sağlar.

<!-- KC:setting -->

##### Ses Zayıflaması Modu {#SelectSynthesizerDuckingMode}

Kısayol tuşu: `NVDA+şift+d`

Bu seçenek NVDA'nın diğer seslerin seviyesini düşürüp düşürmeyeceğini belirlemenizi sağlar.

* Ses zayıflaması, kapalı: NVDA, hiçbir zaman diğer seslerin seviyesini düşürmez. 
* Ses zayıflaması açık, konuşurken ya da ses çalarken: NVDA, diğer seslerin seviyesini yalnızca NVDA konuşurken ya da ses çalarken düşürür. Tüm sentezleyiciler desteklemeyebilir. 
* Ses zayıflaması açık, her zaman : NVDA, NVDA açıkken diğer seslerin seviyesini her zaman düşük tutar.

Bu seçenek yalnızca kurulu NVDA için geçerlidir.
NVDA taşınabilir ve geçici kopyaları için ses zayıflamasının desteği mümkün değildir.

##### NVDA seslerinin ses seviyesi konuşma ses seviyesine eşit olsun {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |devre dışı, etkin|
| Varsayılan |Etkin|

Bu seçenek etkinleştirildiğinde, NVDA seslerinin ve bip seslerinin düzeyi, kullandığınız sesin ses seviyesine göre belirlenir.
Eğer konuşma ses seviyesini azaltırsanız, NVDA seslerinin seviyesi de azalır.
Aynı şekilde konuşma ses seviyesini artırırsanız NVDA seslerinin seviyesi de artar.
Eğer NVDA'yı Gelişmiş Ayarlar'da [Ses Çıkışı için WASAPI Devre Dışı](#WASAPI) seçeneği ile başlattıysanız, bu seçenek kullanılamaz.

##### NVDA ses düzeyi {#SoundVolume}

Bu kaydırıcı NVDA seslerinin ve bip seslerinin seviyesini ayarlamanıza olanak tanır.
Bu seçenek sadece "NVDA seslerinin ses seviyesi konuşma ses seviyesine eşit olsun" seçeneği devre dışı bırakıldığında etkili olur.
Eğer NVDA'yı Gelişmiş Ayarlar'da [Ses Çıkışı için WASAPI Devre Dışı](#WASAPI) seçeneği ile başlattıysanız, bu seçenek kullanılamaz.

##### Ses Ayırma {#SelectSoundSplitMode}

Ses ayırma özelliği, kullanıcıların kulaklık ve hoparlör gibi stereo çıkış cihazlarını kullanmalarına olanak tanır.
Bu özellik, NVDA konuşmasının bir kanalda (örneğin sol) taraftan gelmesini ve diğer tüm uygulamaların seslerini sağ kanalda çalmasını mümkün kılar.
+Varsayılan olarak ses ayırma devre dışıdır.
Çeşitli ses ayırma modları arasında geçiş yapmak için bir girdi ahreketi bulunmaktadır.
<!-- KC:beginInclude -->

| Ad | Kısayol |Açıklama|
|---|---|---|
|Ses Ayırma Modları Arasında Geçiş Yap |`NVDA+alt+s` |Ses ayırma modları arasında geçiş yapar.|

<!-- KC:endInclude -->

Varsayılan olarak bu komut aşağıdaki modlar arasında geçiş yapacaktır:

* Ses ayırma devre dışı: NVDA sesleri ayırmaz.
* Solda NVDA ve sağda uygulamalar: NVDA sol kanalda konuşacak, diğer uygulamalar ise sesleri sağ kanalda çalacaktır.
* Sağda NVDA ve solda uygulamalar: NVDA sağ kanalda konuşacak, diğer uygulamalar ise sesleri sol kanalda çalacaktır.

NVDA ayarlarında daha gelişmiş ses ayırma modları mevcuttur.
Bu modlar arasında, "Her iki kanalda NVDA ve her iki kanalda uygulamalar" seçeneği tüm seslerin her iki kanala yönlendirilmesini sağlar. 
Ses ayırma devre dışı" modunda diğer ses işlemeleri ses seviyeleriyle  çakışabilir ancakk bu modda böyle bir sorun yaşanmaz.

Lütfen ses ayırmanın mikser olarak çalışmadığını unutmayın.
Örneğin, ses ayırma ayarı "NVDA solda, uygulamalar sağda" olarak ayarlanmışken bir uygulama stereo bir ses parçası çalıyorsa, yalnızca ses parçasının sağ kanalını duyarsınız. Sol kanal ise sessize çıkmaz.

NVDA'yı Gelişmiş Ayarlar'da [Ses çıkışı için WASAPI kullan](#WASAPI) ayarını devre dışı bırakarak çalıştırıyorsanız bu seçenek kullanılamaz.

Dikkat: NVDA çöktüğünde, uygulamalar ses seviyesini geri yükleyemez. Bu durum, NVDA çökmesinden sonra bazı uygulamaların yalnızca tek kanaldan duyulmaya devam etmesine neden olabilir.
Bu sorunu çözmek için lütfen NVDA'yı yeniden başlatın ve "Her iki kanalda NVDA ve her iki kanalda uygulamalar" modunu seçin.

##### Ses ayırma modlarını özelleştirme {#CustomizeSoundSplitModes}

Bu liste, `NVDA+alt+s` kullanılarak aralarında geçiş yapılırken hangi ses ayırma modlarının dahil edileceğini ayarlayacak onay kutularını içerir.
Onay kutusu işaretli olmayan modlar dahil edilmez.
Varsayılan olarak yalnızca üç mod dahildir.

* Ses ayırma devre dışı: Hem NVDA hem de uygulamalar, sesleri hem sol hem de sağ kanallarda çalar.
* Solda NVDA ve sağ kanalda diğer tüm uygulamalar.
* Sağda NVDA ve sol kanalda diğer tüm uygulamalar.

En az bir modun işaretli olması gerektiğini unutmayın.
NVDA'yı Gelişmiş Ayarlar'da [Ses çıkışı için WASAPI kullan](#WASAPI) ayarını devre dışı bırakarak çalıştırıyorsanız bu seçenek kullanılamaz.

##### Konuşmadan sonra ses cihazını uyanık tutma zamanı {#AudioAwakeTime}

Bu seçenek yazı alanı konuşma bittikten sonra NVDA'nın ses cihazını ne kadar uyanık tutacağını ayarlar.
Böylece konuşmanın kelimeler arasında kesilmesi veya bozuk gelmesi engellenmiş olur.
Bu durum ses cihazlarının (özellikle Bluetooth ve kablosuz cihazların) bekleme moduna girmesi nedeniyle meydana gelebilir.
Aynı zamanda NVDA'nın bir sanal makinede (örn. Citrix Virtual Desktop) veya belirli dizüstü bilgisayarlarda çalıştırılması gibi diğer durumlarda da yararlı olabilir.

Düşük değerler sesin daha sık kesilmesine neden olabilir. Çünkü cihaz çok erken bekleme moduna girerek, sonraki konuşmanın başlangıcının kesilmesine yol açabilir.
Değer çok yüksek ayarlanırsa, ses çıkış cihazının pili daha hızlı bitebilir. Çünkü cihaz, ses gönderilmediği zamanlarda bile daha uzun süre aktif kalır.

Bu özelliği devre dışı bırakmak için süreyi sıfıra ayarlayabilirsiniz.

#### Görsellik {#VisionSettings}

NVDA Ayarları iletişim kutusundaki görsellik kategorisi [görsel yardımları](#Vision) etkinleştirmenizi, devre dışı bırakmanızı ve yapılandırmanızı sağlar.

Bu kategori altında mevcut olan seçeneklerin [NVDA eklentileri](#AddonsManager) ile genişletilebileceğini unutmayın.
Varsayılan olarak, bu ayar kategorisi aşağıdaki seçenekleri içerir:

##### Görsel Vurgu {#VisionSettingsFocusHighlight}

Görsel vurgu grubundaki onay kutuları NVDA'nın [Görsel vurgu](#VisionFocusHighlight) özelliği ile ilgili yerleşik davranışını kontrol eter.

* Vurgulamayı Etkinleştir: Görsel Vurguyu açıp kapatır.
* Sistem odağını görselleştir: [sistem odağının](#SystemFocus) vurgulanıp vurgulanmayacağını değiştirir.
* Nesne sunucusunu görselleştir: [nesne sunucusunun](#ObjectNavigation)vurgulanıp vurgulanmayacağını değiştirir.
* Tarama kipi imlecini görselleştir: [tarama kipi sanal imlecinin](#BrowseMode)vurgulanıp vurgulanmayacağını değiştirir.

"Vurgulamayı Etkinleştir" onay kutusunun işaretlenip işaretlenmemesinin, ağaçtaki diğer onay kutularının durumunu da değiştireceğini unutmayın.
Bu nedenle, "Vurgulamayı Etkinleştir" kapalıysa ve bu onay kutusunu işaretlerseniz, diğer ağaç onay kutuları da otomatik olarak işaretlenir.
Yalnızca odağı görselleştirmek ve nesne sunucusu ve tarama kipi onay kutularını işaretlemeden bırakmak istiyorsanız, "Vurgulamayı Etkinleştir" onay kutusunun durumu yarı işaretli olur.

##### Ekran perdesi {#VisionSettingsScreenCurtain}

[Ekran perdesini](#VisionScreenCurtain) "Ekranı karart (anında devreye girer)" onay kutusunu işaretleyerek etkinleştirebilirsiniz.
Ekranın karartılacağıyla ilgili bir uyarı gösterilir.
Devam etmeden önce ("Evet" i seçerek), konuşma / braille özelliğini etkinleştirdiğinizden ve bilgisayarınızı ekran kullanmadan kontrol edebildiğinizden emin olun.
Ekran Perdesini etkinleştirmek istemiyorsanız "Hayır" ı seçin.
Eminseniz, ekran perdesini etkinleştirmek için Evet düğmesini seçebilirsiniz.
Her seferinde bu uyarı mesajıyla karşılaşmak istemiyorsanız, mesajı gösteren iletişim kutusundan bu davranışı değiştirebilirsiniz.
"Ekranı karart" onay kutusunun yanındaki "Ekran Perdesi'ni etkinleştirmeden önce daima uyar" onay kutusunu işaretleyerek uyarının  her durumda gösterilmesini tekrar sağlayabilirsiniz.

Varsayılan olarak, Ekran Perdesi statüsü değiştiğinde ses çalınır.
Bu davranışı değiştirmek isterseniz, "Ekran Perdesi statüsü değiştiğinde ses çal" onay kutusunun işaretini kaldırabilirsiniz.

##### Üçüncü taraf görsel yardım ayarları {#VisionSettingsThirdPartyVisualAids}

Ek görsellik geliştirme sağlayıcıları [NVDA eklentileri](#AddonsManager) ile sağlanabilir.
Bu sağlayıcılar değiştirilebilir ayarlara sahipse, bu ayarlar kategorisinde ayrı ayrı gruplandırılarak  gösterilecektir.
Sağlayıcı tarafından desteklenen ayarlar için lütfen söz konusu sağlayıcıya ait belgelere bakın.

#### Klavye {#KeyboardSettings}

<!-- KC:setting -->

##### Klavye ayarlarını aç {#OpenKeyboardSettings}

Kısayol Tuşu: `NVDA+kontrol+k`

NVDA Ayarları iletişim kutusundaki Klavye kategorisi, klavye kullanırken NVDA'nın nasıl davranacağıyla ilgili seçenekleri içerir.
Bu kategoride aşağıdaki seçenekler mevcuttur:

##### Klavye Düzeni {#KeyboardSettingsLayout}

Bu seçim kutusu, NVDA'nın hangi tür klavye düzenini kullanacağını seçmenizi sağlar. Şu an itibariyle NVDA ile gelen 2 düzen masaüstü ve dizüstü düzenleridir.

##### NVDA Değişken Tuşlarını Belirleyin {#KeyboardSettingsModifiers}

Bu listedeki onay kutuları hangi tuşların [NVDA değişken tuşları](#TheNVDAModifierKey) olarak kullanılabileceğini belirler. Aşağıdaki tuşlar belirlenebilir:

* Büyük harf tuşu (Caps lock)
* Sayısal tuş takımındaki ınsert tuşu
* Normal insert tuşu (genellikle ok tuşları üzerinde, home ve end tuşlarının yanında bulunur)

Hiçbir tuş NVDA tuşu olarak ayarlanmazsa, bazı NVDA komutları kullanılamaz. Dolayısıyla, en az bir tuşu NVDA tuşu olarak seçmelisiniz.

<!-- KC:setting -->

##### Yazılan Karakterleri Söyle {#KeyboardSettingsSpeakTypedCharacters}

Kısayol tuşu: NVDA+2

Etkinleştirildiğinde, NVDA yazdığınız her karakteri söyleyecektir.

<!-- KC:setting -->

##### Yazılan Sözcükleri Söyle {#KeyboardSettingsSpeakTypedWords}

Kısayol tuşu: NVDA+3

Etkinleştirildiğinde, NVDA yazdığınız her sözcüğü söyleyecektir.

##### Karakterlere Basıldığında Konuşmayı Durdur {#KeyboardSettingsSpeechInteruptForCharacters}

Açıksa,, bu seçenek bir karaktere basıldığında konuşmanın durmasına neden olur. Varsayılan olarak açıktır.

##### Enter tuşuna basıldığında konuşmayı durdur {#KeyboardSettingsSpeechInteruptForEnter}

Açıksa, bu seçenek enter tuşuna basıldığında konuşmanın durmasına neden olur. Varsayılan olarak açıktır.

##### Tümünü okurken atlamaya izin ver {#KeyboardSettingsSkimReading}

Açıksa, tümünü okuma komutu verildiğinde belli dolaşma komutları kullanıldığı zaman (örneğin tarama kipinde hızlı dolaşım tuşları ya da paragraf veya satır değiştirme komutları) konuşma durdurulmaz, yerine okuma atlanılan konumdan itibaren devam eder.

##### Büyük Harf Kilidi Açıkken, şifte basılarak küçük harf Yazılırsa Bip Sesi Çıkar {#KeyboardSettingsBeepLowercase}

Etkinleştirildiğinde, büyük harf kilidi açıkken şift tuşuyla birlikte bir harfe basıldığında uyarı bipi duyulacaktır.
Genellikle, büyük harf kilidi açıkken şiftle birlikte bir harf yazmak istem dışıdır ve çoğunlukla büyük harf kilidinin açık olduğunun farkında olunmamasından kaynaklanır.
Bu yüzden, bu konuda uyarılmak oldukça yararlı olabilir.

<!-- KC:setting -->

##### Komut Tuşlarını Söyle {#KeyboardSettingsSpeakCommandKeys}

Kısayol tuşu: NVDA+4

Etkinleştirildiğinde, NVDA bastığınız karakter olmayan (örnek, kontrol, Şift VS.) her tuşu söyleyecektir. Buna kontrolle birlikte basılan harflerden oluşan tuş kombinasyonları da dahildir.

##### Yazarken yazım hataları için ses çal {#KeyboardSettingsAlertForSpellingErrors}

Etkinleştirildiğinde, yazmakta olduğunuz kelime hatalı olarak yazılıyorsa, Kısa bir zil sesi çalınır.
Bu seçenek, yalnızca NVDA'nın [Belge format ayarları](#DocumentFormattingSettings) iletişim kutusundaki Yazım hatalarının bildirimi açıksa geçerlidir.

##### Diğer uygulamaların kullandığı tuşları işle {#KeyboardSettingsHandleKeys}

Bu seçenek kullanıcının ekran klavyeleri ve konuşma tanıma uygulamaları gibi yazılımların tuşlarının NVDA tarafından işlenip işlenmeyeceğini kontrol etmesini sağlar. 
Seçenek varsayılan olarak etkindir, bazı kullanıcılar bunu kapatmak isteyebilir, örneğin Vietnamca yazmak için Unikey yazma programı kullananlar.

#### Fare {#MouseSettings}

<!-- KC:setting -->

##### Fare ayarlarını aç {#OpenMouseSettings}

Kısayol Tuşu: `NVDA+kontrol+m`

NVDA Ayarları iletişim kutusundaki Fare kategorisi, NVDA'nın fare hareketlerini takip etmesini, fare koordinatlarına dayanarak kullanıcıyı sesli olarak bilgilendirmesini ve diğer fare seçenekleriyle ilgili değişiklikler yapılmasını sağlar.
Bu kategoride aşağıdaki seçenekler mevcuttur:

##### Fare Şekil Değişikliğini Bildir {#MouseSettingsShape}

Bu onay kutusu işaretlendiğinde, fare işaretleyicisinin şekli her değiştiğinde NVDA bunu bildirecektir.
Fare işaretleyicisi pencerelerde bir alanın yazılabilir olduğu veya bir şeyin yüklendiği gibi bilgileri vermek için şekil değiştirir.

<!-- KC:setting -->

##### Fare İzlemeyi Etkinleştir {#MouseSettingsTracking}

Kısayol tuşu: NVDA+m |

Etkinleştirildiğinde, fare ile ekranda dolaşırken, NVDA, fare işaretinin altında bulunan metni söyleyecektir. Bu, ekrandaki bir şeyi nesne dolaşımı yerine, fiziksel olarak fareyi hareket ettirerek bulmanızı sağlar.

##### Metin Birim Çözünürlüğü {#MouseSettingsTextUnit}

Eğer NVDA siz hareket ettikçe fare altındaki metni söyleyecek biçimde ayarlandıysa, bu seçenek, tam olarak ne kadar metnin söyleneceğini seçmenizi sağlar.
Seçenekler, karakter, sözcük, satır ve paragraftır.

Herhangi bir yerdeyken metin birim çözünürlüğünü değiştirmek için,   [Girdi Hareketleri iletişim kutusunu](#InputGestures) kullanarak özel bir kısayol atayın.

##### Fare içine girdiğinde nesneyi seslendir {#MouseSettingsRole}

Bu onay kutusu işaretlenirse, NVDA, fare nesnelerin içinde hareket ettikçe nesneler hakkındaki bilgileri bildirecektir.
Bu, nesneninne olduğunu  (tipini), durumunu (işaretli/basılı), tablolardaki hücre koordinatlarını vb. içerir.
Bazı nesne ayrıntılarının duyurulmasının [nesne sunucusu](#ObjectPresentationSettings) veya [belge formatları](#DocumentFormattingSettings)  gibi ayarların nasıl yapılandırıldığına bağlı olduğunu unutmayın.

##### Fare hareketlerinde Koordinatları Ses Çalarak Belirt {#MouseSettingsAudio}

Bu onay kutusunu işaretlemek, NVDA'nın fare hareket ettikçe bip sesi çıkarmasını sağlar ve böylece kullanıcı ekranda farenin nerede olduğunu anlayabilir.
Fare yukarı çıktıkça bip sesi incelir.
Fare imleci sola ve sağa kaydırıldıkça bip sesi de aynı doğrultuda sola ve sağa kayar. Tabii bunun anlaşılması için hoparlör ya da kulaklık steryo olmalıdır.

##### Seçili bölgelerde dolaşırken fare koordinat sesini yükselt {#MouseSettingsBrightness}

Eğer "fare hareket ettikçe ses çal" onay kutusu işaretliyse, bu onay kutusu işaretlendiğinde, sesli koordinatların miktarı ekranın parlaklığına göre kontrol edilir.
yani seçili bir bölgede ses daha yüksek çıkar. Bu, varsayılan olarak işaretli değildir.

##### Diğer uygulamalardan fare girişini yoksay {#MouseSettingsHandleMouseControl}

Bu seçenek, kullanıcının TeamViewer ve diğer uzaktan kontrol yazılımı gibi diğer uygulamalar tarafından oluşturulan fare olaylarını (fare hareketi ve düğme olayları dahil) yoksaymasını sağlar.
Bu seçenek varsayılan olarak işaretli değildir.
Bu seçeneği işaretlerseniz ve "Fare izlemeyi etkinleştir" seçeneği de etkinse, fare başka bir uygulama tarafından kullanılırken NVDA, farenin altında olanı seslendirmez.

#### Dokunmatik Etkileşim {#TouchInteraction}

Yalnızca dokunmatik özellikli bilgisayarlarda kullanılabilen bu ayarlar kategorisi, Bu ayar kategorisi, NVDA'nın dokunmatik ekranlarla nasıl etkileşeceğini yapılandırmanızı sağlar.
Bu kategori aşağıdaki seçenekleri içerir:

##### Dokunmatik etkileşim desteğini etkinleştir {#TouchSupportEnable}

Bu onay kutusu, NVDA'nın dokunmatik etkileşim desteğini etkinleştirir.
Etkinleştirilirse, dokunmatik ekranlı bir cihaz kullanarak ekrandaki öğelerde gezinmek ve etkileşimde bulunmak için parmaklarınızı kullanabilirsiniz.
Devre dışı bırakılırsa, NVDA çalışmıyormuş gibi dokunmatik ekran desteği devre dışı bırakılır.
Bu ayar, NVDA+kontrol+alt+t kullanılarak da değiştirilebilir. 

##### Dokunarak yazma kipi {#TouchTypingMode}

Bu onay kutusu dokunmatik ekrandan giriş yapma yönteminizi belirlemenize olanak tanır.
Onay kutusu işaretli ise, dokunmatik klavyede bir tuşu bulduktan sonra, parmağınızı ekrandan çektiğinizde bu tuşa basılır.
İşaretli değilse, tuşa basmak için ekrana çift dokunmanız gerekir.

#### İnceleme İmleci {#ReviewCursorSettings}

NVDA Ayarları iletişim kutusundaki İnceleme İmleci kategorisi, NVDA'nın inceleme imleci davranışını konfigüre etmek için kullanılır.
Bu kategoride aşağıdaki seçenekler mevcuttur:

<!-- KC:setting -->

##### Sistem Odağını Takip et {#ReviewCursorFollowFocus}

Kısayol tuşu: NVDA+7 |

Etkinleştirildiği zaman, odak değiştiğinde inceleme imleci de sistem odağının bulunduğu nesne üzerinde konumlanır.

<!-- KC:setting -->

##### Sistem Düzenleme İmlecini takip et {#ReviewCursorFollowCaret}

Kısayol tuşu: NVDA+6

Etkinleştirildiğinde, sistem düzenleme imleci hareket ettikçe, inceleme imleci de onun gittiği yere gidecektir.

##### Fare İmlecini Takip Et {#ReviewCursorFollowMouse}

Etkinleştirildiğinde, fare hareket ettikçe inceleme imleci de onu izleyecektir.

##### Basit İnceleme Kipi {#ReviewCursorSimple}

Etkinleştirildiğinde, görünmez nesneler ve sadece düzenleme amacıyla kullanılan nesneler vb kullanıcıyı ilgilendirmeyecek nesneleri yoksaymak için, NVDA dolaşılabilecek nesne hiyerarşisini filtreleyecektirr.

Herhangi bir yerde basit inceleme kipini açıp kapatmak için, lütfen [Girdi Hareketleri iletişim kutusunu](#InputGestures) kullanarak bir özel hareket atayın.

#### Nesne Sunumu {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Nesne Sunumu ayarlarını aç {#OpenObjectPresentationSettings}

Kısayol Tuşu: `NVDA+kontrol+o`

NVDA Ayarları iletişim kutusundaki Nesne Sunumu kategorisi, açıklama, konum bilgisi vb, NVDA'nın kontrollerle ilgili ne kadar bilgi sunacağının belirlenmesi için kullanılır.
Bu seçenekler genellikle tarama kipi için geçerli değildir.
Bu seçenekler genel olarak odak bildirimi ve NVDA nesne navigasyonu için geçerlidir, ancak metin içeriğini örneğin tarama kipinde okurken geçerli değildir.

##### İpuçlarını bildir {#ObjectPresentationReportToolTips}

İşaretlendiğinde NVDA'ya ekranda beliren  ipuçlarını bildirmesini söyleyen bir onay kutusudur.
Bir çok pencere ve kontrol fareyle üzerleriine gelindiğinde veya sistem imleciyle odaklanıldığında küçük mesajlar veya ipuçları (baloncuklar( göstermektedir.

##### Bildirimleri raporla {#ObjectPresentationReportNotifications}

Bu onay kutusu işaretlenirse NVDA'dan yardım balonlarını ve tost bildirimlerini belirdikleri anda  raporlaması istenmiş olur.

* Yardım Balonları araç ipuçlarına benzer, ancak genellikle boyutları daha büyüktür ve bir ağ kablosunun takılması ya da çıkarılması gibi sistem olaylarıyla veya belki de Windows güvenlik sorunları hakkında sizi uyarmasıyla ilişkilidir.
* Tost bildirimleri, Windows 10 ile tedavüle girmiştir ve sistem tepsisindeki bildirim merkezinde belirerek çeşitli  olaylar hakkında bilgi verir (örneğin, bir güncelleme indirildiğinde, gelen kutunuza yeni bir e-posta alındığında ​​vb.).

##### Nesne Kısayol Tuşlarını Bildir {#ObjectPresentationShortcutKeys}

Bu onay kutusu işaretlendiğinde, bir kontrol veya belirli bir nesne üzerine gelindiğinde NVDA ilgili kısayol tuşunu da söyler.
Örneğin, menü çubuğundaki dosya menüsünün kısayol tuşu alt+d olabilir.

##### Nesne Konum Bilgisini Bildir {#ObjectPresentationPositionInfo}

Bu seçenek, Nesnenin 1 bölü 4 gibi konum bilgisinin nesne dolaşımı veya klavye odağıyla üzerine gelindiğinde bildirilip bildirilmeyeceğini seçmenizi sağlar.

##### Mevcut Değilse Nesne Konum Bilgisini Tahmin Et {#ObjectPresentationGuessPositionInfo}

Eğer nesne konum bilgisinin bildirimi açıksa, Bu seçenek, NVDA'ya başka biçimde belirli bir kontrolde mevcut olmayan nesne konum bilgisini tahmin etme olanağı sağlar.

Açık olduğunda, NVDA, araç çubukları ve menü çubukları gibi daha fazla nesnenin konum bilgisini bildirecek, ancak verilen bilgilerde küçük hatalar meydana gelebilecektir.

##### Nesne Açıklamalarını Bildir {#ObjectPresentationReportDescriptions}

Nesne adıyla birlikte ilgili açıklamayı (diğer bir deyişle, arama önerileri, iletişim kutusunun açılmasından hemen sonra tüm iletişim penceresinin bildirilmesi vb.) duymak istemiyorsanız, bu onay kutusunun işaretini kaldırın.

<!-- KC:setting -->

##### Aşama Çubuğu bildirimi {#ObjectPresentationProgressBarOutput}

Kısayol tuşu: NVDA+u |

Bu seçenek Aşama çubuğu bilgilerini NVDA'nın size nasıl bildireceğini kontrol etmenizi sağlar.

içinde aşağıdaki seçenekler mevcuttur:

* Kapalı Aşama çubuğu güncellemeleri bildirilmez.
* Konuş Bu seçenek NVDA'ya aşama çubuğu güncellemelerini yüzde olarak sölemesini belirtir. Aşama çubuğu her değiştiğinde, NVDA yeni değeri söyleyecektir.
* Bip Sesi Çıkar: Bu, NVDA'ya aşama çubuğu her değiştiğinde bip sesi çıkarmasını söyler. Bip sesinin yükselmesi , aşama çubuğunun tamamlanmasının yaklaştığı anlamına gelir.
* Konuş ve Bip Sesi Çıkar Bu seçenek NVDA'ya aşama çubuğu güncelenirken, hem konuşup hem bip sesi çıkarmasını söyler.

##### Arka Plan Aşama çubuklarını Bildir {#ObjectPresentationReportBackgroundProgressBars}

Bu seçenek, NVDA'nın bir aşama çubuğu o an fiziksel olarak ekranda olmasa bile güncellemeleri takip edip belirtmesini sağlar.
Aşama çubuğu olan bir pencereyi küçülttüyseniz veya başka bir noktaya geçtiyseniz, NVDA bu çubuğu izler ve başka bir işle uğraşırken, aynı zamanda güncellemeleri de takip etmenizi sağlar.

<!-- KC:setting -->

##### Dinamik İçerik Değişimlerini Bildir {#ObjectPresentationReportDynamicContent}

Kısayol tuşu: NVDA+5

Terminal veya chat programlarının geçmiş alanları gibi belirli nesnelerdeki yeni içeriğin belirtilip belirtilmeyeceğini kontrol eder.

##### Otomatik öneriler için ses çal {#ObjectPresentationSuggestionSounds}

Otomatik önerilerin bildirimiyle ilgili değişiklik yapar ve etkinleştirilirse, NVDA listenin gösterildiğini belirtmek için bir ses çalar.
Otomatik öneriler belli bir alana girilen metne dayanılarak önerilen girdilerin listesidir.
Mesela, Windows Vista ve sonrasında Başlat Menüsünde arama kutusuna metin girdiğinizde, Windows yazdığınıza dayalı bir öneri listesi gösterir.
Çeşitli Windows 10 uygulamalarında bulunan arama alanları gibi bazı yazı alanlarında , NVDA siz yazdıkça listelenen seçenekler hakkında bildirimde bulunabilir.
Otomatik öneri listesi, yazı alanını kapattığınızda kapanır ve bazı alanlar için , NVDA BU gerçekleştiğinde bildirimde bulunabilir.

#### Girdi Kompozisyonu {#InputCompositionSettings}

Bu kategori NVDA'nın Çince, Japonca ve Korece gibi dillerle ilgili girişleri, IME veya Text Service girdi metodları, nasıl bildireceğini ayarlamanızı sağlar.
Taşıdıkları özellik ve bilgiler açısından girdi metodları farklılaştığından, daha verimli bir yazma deneyimi için bu seçenekleri her girdi metodu için ayrı ayrı konfigüre etmeniz gerekebilir.

##### Mevcut tüm önerileri otomatik olarak seslendir {#InputCompositionReportAllCandidates}

Varsayılan olarak açık olan bu seçenek, bir öneri listesi oluştuğunda, görünen tüm önerilerin seslendirilip seslendirilmeyeceğini ayarlamanızı sağlar.
Bu seçeneğin açık olması, chinese New ChangJie veya Boshiami gibi pictographic girdi metodları için faydalı olabilir.
Ancak chinese New Phonetic gibi phonetic girdi metodları için, seçeneğin kapalı olması daha faydalı olabilir. Tüm semboller benzer seslere sahip olduğu için öneri listesinde yön tuşlarını kullanarak seçim yapmak daha uygundur.

##### Seçili Öneriyi Seslendir {#InputCompositionAnnounceSelectedCandidate}

Varsayılan olarak açık olan bu seçenek, bir öneri listesi ortaya çıktığında ya da seçim değiştiğinde, seçili önerinin seslendirilip seslendirilmeyeceğini belirlemenizi sağlar.
Seçimin yön tuşlarıyla değiştirilebildiği (Chinese New Phonetic) gibi girdi metodları için bu gereklidir, ama bazı girdi metodları için bu seçeneğin kapalı olması daha verimli olacaktır.
Bu seçenek kapalı olsa dahi, nesne dolaşımı yoluyla önerileri manuel olarak inceleyebilmeniz için, inceleme imleci seçili önerinin üzerinde konumlandırılır.

##### Öneriler için daima kısa karakter tanımlarını da kullan {#InputCompositionCandidateIncludesShortCharacterDescription}

This option, which is on by default, allows you to choose whether or not NVDA should provide a short description for each character in a candidate, either when its selected or when its automatically read when the candidate list appears.
Note that for locales such as Chinese, the announcement of extra character descriptions for the selected candidate is not affected by this option.
Bu seçenek Korece ve Japonca girdi metodları için faydalı olabilir.

##### İfade okunuşlarındaki değişiklikleri bildir {#InputCompositionReadingStringChanges}

Chinese New Phonetic ve New ChangJie gibi bazı girdi metodları (kimi zaman precomposition string olarak bilinen) ifade okumalarına sahiptir.
Bu seçenekle, ifadelerin okunuşlarında yeni karakter girişlerinin seslendirilip seslendirilmeyeceğini ayarlayabilirsiniz.
Bu seçenek varsayılan olarak açıktır.
Chinese ChangJie gibi bazı eski girdi metodlarının ön kompozisyon ifade okumaları yerine doğrudan ifade kompozisyonlarını kullandığını not edin. Lütfen ifade kompozisyonunun seslendirilmesiyle ilgili ayar için sonraki seçeneğe bakın.

##### İfade Kompozisyonundaki Değişiklikleri Bildir {#InputCompositionCompositionStringChanges}

After reading or precomposition data has been combined into a valid pictographic symbol, most input methods place this symbol into a composition string for temporary storage along with other combined symbols before they are finally inserted into the document.
This option allows you to choose whether or not NVDA should report new symbols as they appear in the composition string.
Bu seçenek varsayılan olarak açıktır.

#### Tarama kipi {#BrowseModeSettings}

<!-- KC:setting -->

##### Tarama Kipi ayarlarını aç {#OpenBrowseModeSettings}

Kısayoll Tuşu: `NVDA+kontrol+b`

NVDA Ayarları iletişim kutusundaki Tarama Kipi  kategorisi, web sayfaları gibi karmaşık belgeleri okurken ya da dolaşırken NVDA'nın nasıl davranacağını belirlemek için kullanılır.
Tarama kipi kategorisinde aşağıdaki seçenekler mevcuttur:

##### Satır Başına Düşen Maksimum Karakter sayısı {#BrowseModeSettingsMaxLength}

Bu alan, tarama kipinde gösterilecek her bir satırın karakter cinsinden maksimum uzunluğunu ayarlar.

##### Sayfa Başına Düşen Maksimum Satır sayısı {#BrowseModeSettingsPageLines}

Bu değer, önceki sayfa ve sonraki sayfa tuşlarıyla tarama kipinde gösterilen belge içinde hareket ettiğinizde, kaç satır gidileceğini belirler.

<!-- KC:setting -->

##### Destekleniyorsa Ekran Düzenini Kullan {#BrowseModeSettingsScreenLayout}

Tuş: NVDA+v

Bu seçenek, tarama kipinin tıklanabilir içeriği (linkler, düğmeler ve alanlar) ayrı satırlara  mı yerleştirmesi yoksa görsel olarak ekranda görüldüğü gibi metin akışında mı tutması gerektiğini belirlemenizi sağlar. 
Bu seçeneğin, her zaman ekran düzenini kullanan Outlook ve Word gibi Microsoft Office uygulamaları için geçerli olmadığını unutmayın.
Örneğin, birden çok linkten oluşan bir satırda linkler aynı satırda farklı farklı linkler olarak gösterilecektir.
Eğer bu seçenek aktif değilse, bğlantılar orijinal halleriyle görüntülenecektir.
Bu, satır satır gezinme sırasında	 anlaşılmayı kolaylaştırabilir ve bazı kullanıcılar için öğelerle etkileşim kurmayı kolaylaştırabilir.
Ekran düzeni etkinleştirildiğinde, sayfa öğeleri görsel olarak gösterildiği gibi kalacaktır. Örneğin, birden çok linkin gösterildiği bir satır, konuşmaya ve braille'e de aynı şekilde aktarılır. Devre dışı bırakılırsa, öğeler ayrı satırlara yerleştirilecektir; bu, satır satır dolaşılırken  öğeler arasındaki farkı daha anlaşılabilir kılar ve bazı kullanıcılar için öğelerle etkileşimi kolaylaştırabilir.

##### Sayfa yüklendiğinde tarama kipini etkinleştir {#BrowseModeSettingsEnableOnPageLoad}

Bu onay kutusu, bir sayfa yüklendiğinde tarama kipinin otomatik olarak etkinleştirilip etkinleştirilmeyeceğini belirler.
Bu seçenek devre dışı bırakılsa bile, sayfalarda veya tarama kipinin desteklendiği belgelerde tarama kipi manuel olarak etkinleştirilebilir.
tarama kipinin  desteklendiği uygulamaların listesi için [tarama kipi bölümüne](#BrowseMode) bakın.
Bu seçeneğin, tarama kipinin her zaman isteğe bağlı olduğu durumlar için geçerli olmadığını unutmayın; mesela Microsoft Word'de.
Bu seçenek varsayılan olarak etkindir.

##### Sayfa yüklendiğinde Otomatik Olarak Hepsini Oku {#BrowseModeSettingsAutoSayAll}

Bu onay kutusu tarama kipinde yüklenen sayfanın otomatik olarak okunmaya başlanmasıyla ilgili ayarı değiştirir.
Bu seçenek varsayılan olarak etkindir.

##### Düzenleme Tablolarını Dahil Et {#BrowseModeSettingsIncludeLayoutTables}

Bu seçenek, sadece sayfa düzeniyle ilgili, veri içermeyen tablolarla karşılaştığında NVDA'nın nasıl davranacağını etkiler.
Açıksa, NVDA bu tablolarla karşılaştığında normal tablolara davrandığı gibi tepki verir, [Belge Format Ayarları](#DocumentFormattingSettings) nasıl yapıldıysa o şekilde belirtir ve tek tuş dolaşımı ile bu tablolara da ulaşılır.
Devre dışı bırakıldığında, NVDA sadece sayfa düzeniyle ilgili olarak oluşturulmuş tabloları bildirmez ve tek tuş dolaşımıyla da bu tablolara ulaşılmaz.
Ancak tablodaki metin normal metin olarak gösterilir.
Bu seçenek varsayılan olarak kapalıdır.

Herhangi bir yerde düzen tablolarının dahil edilmesini açıp kapatmak için, [girdi hareketleri iletişim kutusunu](#InputGestures) kullanarak özel bir komut belirleyebilirsiniz.

##### Başlık ve Link gibi alanların belirtilmesini ayarlama {#BrowseModeLinksAndHeadings}

Başlıklar, linkler, tablolar ve listeler gibi kontrollerin seslendirilmesiyle ilgili ayarlar için, lütfen [NVDA Ayarlarında](#NVDASettings)  [Belge Formatları İletişim Kutusu](#DocumentFormattingSettings) içerisindeki seçeneklere bakın.

##### Odak Değişiminde Otomatik Odak Kipi {#BrowseModeSettingsAutoPassThroughOnFocusChange}

Bu seçenek, odak değişiminde odak kipinin açılmasını sağlar.
Örneğin, Bir web sayfasında tab tuşuyla bir form alanına geldiyseniz ve bu seçenek işaretliyse, otomatik olarak odak kipi açılacaktır.

##### Düzenleme İmleci İçin Otomatik Odak Kipi {#BrowseModeSettingsAutoPassThroughOnCaretMove}

Bu seçenek işaretliyse, yön tuşlarıyla dolaşırken NVDA'nın odak kipine otomatik olarak girmesini ve çıkmasını sağlar.
Örneğin bir web sayfasında  yön tuşlarıyla  aşağı doğru inerken  bir yazı alanına gelirseniz, NVDA otomatik olarak odak kipine geçecektir.
Yön tuşlarıyla  yazı alanının dışına çıktığınızda ise tarama kipine otomatik olarak geçecektir.

##### Odak Kipiyle Tarama Kipi Arasındaki Geçişi Ses Çalarak bildir {#BrowseModeSettingsPassThroughAudioIndication}

Bu seçenek etkinse, odak kipi ve tarama kipi arasında geçiş yaparken NVDA bunu konuşarak değil, özel bir ses çalarak bildirecektir.

##### Komut tuşu olmayan tuşların belgeye gönderilmesini engelle {#BrowseModeSettingsTrapNonCommandGestures}

Bu seçenek varsayılan olarak etkindir ve NVDA komutu olarak kullanılmayan tuşların ve hareketlerin belgeye gönderilip gönderilmeyeceğini belirlemenizi sağlar. 
Etkinleştirildiğinde, örneğin ş harfine basılırsa, bu tuş ne NVDA komutu ne de aktif uygulama komutu olarak kullanıldığı için , tuşun belgeye ulaşması engellenecektir.
Bu durumda NVDA, Windows’a bu türden  bir tuşa basıldığında varsayılan bir ses çalmasını söyler.

<!-- KC:setting -->

##### Sistem Odağı Tarama Kipi İmlecini Takip Etsin {#BrowseModeSettingsAutoFocusFocusableElements}

Tuş: NVDA+8

Varsayılan olarak devre dışı bırakılan bu seçenek, tarama kipi imleciyle dolaşılırken sistem odağının otomatik olarak (linkler, form alanları vb.) odaklanılabilecek öğelere taşınıp taşınmayacağını belirlemenize olanak tanır.
Bu seçenek  devre dışı bırakılırsa, tarama kipi imleci ile üzerlerine gelindiğinde sistem imleci odaklanabilir öğelere otomatik olarak taşınmayacaktır.
Bu, daha hızlı tarama deneyimine ve tarama kipinde daha iyi yanıt verme hızına neden olabilir.
Yine de bir öğeyle etkileşim kurulduğunda (bir düğmeye basmak ya da bir onay kutusunu işaretlemek vb) sistem odağı otomatik olarak taşınır.
Bu seçeneğin etkinleştirilmesi, performans ve istikrar pahasına bazı web siteleri için desteği iyileştirebilir.

#### Belge Formatları {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Belge Formatları Ayarlarını Aç {#OpenDocumentFormattingSettings}

Kısayol Tuşu: `NVDA+kontrol+d`

Buradaki birçok onay kutusu belge içinde imleci hareket ettirirken hangi tür biçimlendirme bilgilerini otomatik olarak duymak istediğinizi ayarlamanızı sağlamak içindir.
Örneğin, yazı Tipi onay kutusunu işaretlerseniz, oklarla başka bir yazı tipiyle yazılan bir metne her gittiğinizde, yazı tipi adı bildirilecektir.

Belge biçimlendirme seçenekleri gruplar halinde düzenlenmiştir.
Şunların bildirimini ayarlayabilirsiniz:

* Yazı tipi
  * Yazı tipi adı
  * Yazı tipi boyutu
  * Yazı tipi özellikleri
  * Üst ve alt simgeler
  * Vurgu
  * Öne çıkarılmış (işaretli) metin
  * Stil
  * Renkler
* Belge Bilgileri
  * Açıklamalar
  * Yer imleri
  * Editör düzenlemeleri
  * Yazım hataları
* Sayfalar ve Aralık
  * Sayfa numaraları
  * Satır Numaraları
  * Satır girintilerinin bildirimi [(Kapalı, Konuşma, Ses çalarak, Konuşarak ve Ses çalarak)](#DocumentFormattingSettingsLineIndentation)
  * Satır girinti bildirimi için boş satırları yoksay
  * Paragraf girintisi (Örneğin, asılı girinti, ilk satır girintisi)
  * Satır aralığı (tek, çift vs)
  * Hizzalama
* Tablo bilgileri
  * Tablolar
  *  Satır/sütun başlıkları (Kapalı, Satırlar, Sütunlar, Satırlar ve sütunlar)
  * Hücre koordinatları
  * Hücre kenarlıkları [(Kapalı, stiller, renk ve stiller)
* Öğeler
  * Başlıklar
  * Linkler
  * Grafikler
  * Listeler
  * Alıntılar
  * Gruplandırmalar
  * Sınır imleri
  * Makaleler
  * Çerçeveler
  * Şekiller ve başlıklar
  * Bir ögenin tıklanabilir olup olmadığı

Bu ayarları herhangi bir yerdeyken değiştirebilmek için, lütfen [girdi hareketleri iletişim kutusunu](#InputGestures) kullanarak kısayol tuşu belirleyin.

##### imleçten sonraki biçim değişikliklerini bildir {#DocumentFormattingDetectFormatAfterCursor}

Bu seçenek NVDA'ya konuştuğu satırda herhangi bir biçim değişikliği varsa bildirmesini söyler. Ancak bu, performansı yavaşlatabilir.

Varsayılan olarak NVDA sistem düzenleme imleci veya inceleme imlecinin bulunduğu konumdaki biçim değişikliklerini bildirecektir, ve bazı durumlarda yalnızca performansı yavaşlatmayacaksa satırın geri kalanındaki değişiklikleri belirtebilir.

Biçimlendirmenin önemli olduğu Wordpad belgesi gibi belgelerde düzeltme yaparken bu seçeneği etkinleştirin.

##### Satır girintilerinin bildirimi {#DocumentFormattingSettingsLineIndentation}

Bu seçenek, satır başlarındaki boşlukların nasıl bildirileceğini belirlemenize olanak tanır.
Satır girintilerinin bildirimi seçim kutusunda dört seçenek bulunmaktadır.

* Kapalı: NVDA girintilerle ilgili herhangi bir bildirimde bulunmaz.
* Konuşma: Konuşma seçilirse, girinti miktarı değiştiğinde, NVDA "oniki aralık" veya "dört sekme" gibi bir şey söyler.
* Ses çalarak: Ses çalarak seçeneği tercih edilirse, girinti miktarı değiştiğinde, çalınan ses girindideki değişim miktarını belirtir.
Çalınan sesin perdesi her bir aralık için artar, ve her bir sekme için sesin perdesi dört aralığa karşılık gelecek şekilde artar.
* Konuşarak ve ses çalarak: Bu seçenek girintinin yukarıdaki iki yolla da bildirimini sağlar.

"Satır girinti bildirimi için boş satırları yoksay" onay kutusunu işaretlerseniz, boş satırlar için girinti değişiklikleri bildirilmeyecektir.
Bu, programlamada  kaynak kodu  gibi girintili metin bloklarını ayırmak için boş satırların kullanıldığı bir belgeyi okurken yararlı olabilir.

#### Belge dolaşımı {#DocumentNavigation}

Bu kategori belge dolaşımı ile ilgili çeşitli ayarlamaları yapmanıza yarar

##### Paragraf kipi {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |Varsayılan (Uygulama tarafından kontrol edilir), Uygulama tarafından kontrol edilir, Tek satır sonu, Çoklu satır sonu|
|Varsayılan |Uygulama tarafından kontrol edilir|

Bu seçim kutusu, `kontrol+yukarı ok` ve `kontrol+aşağı ok` tuşları ile paragraflarda gezinirken kullanılacak paragraf kipini seçmenize olanak tanır.
Kullanılabilir paragraf kipleri şunlardır:

* Uygulama tarafından kontrol edilir: NVDA mevcut uygulamanın bir önceki veya sonraki paragrafı belirlemesine izin verir ve gezinirken paragrafı okur. 
Bu seçenek varsayılan olarak seçilidir ve uygulamaların varsayılan olarak paragraf dolaşımını desteklediği durumlarda en iyi biçimde çalışır.
* Tek satır sonu: NVDA, paragraf göstergesi olarak tek bir satır sonu kullanarak önceki veya sonraki paragrafı belirlemeye çalışır.
Bu, Varsayılan olarak paragraf gezinmeyi desteklemeyen bir uygulamada belgeleri okurken en iyi biçimde çalışır ve belgedeki paragraflar `enter` tuşuna bir kez basılarak işaretlenir.
* Çoklu satır sonu: NVDA, paragrafları en az bir boş satır (`enter` tuşuna iki kez basılması) ile önceki veya sonraki paragrafı belirlemeye çalışır.
Bu seçenek, blok paragraflar kullanan belgelerle çalışırken en iyi biçimde çalışır.
Microsoft Word denetimlerine erişmek için UIA kullanmıyorsanız, bu paragraf stilinin Microsoft Word veya Microsoft Outlook'ta kullanılamayacağını unutmayın.

Mevcut paragraf kipleri arasında hızlıca geçiş yapmak için [Girdi hareketleri iletişim kutusu](#InputGestures) üzerinden bir kısayol atayabilirsiniz. 

#### Windows OCR Ayarları {#Win10OcrSettings}

Bu kategori altındaki seçenekler [Windows OCR ayarlarını](#Win10Ocr) yapılandırmanızı sağlar.
Kategori aşağıdaki seçenekleri içerir:

##### Tanıma dili {#Win10OcrSettingsRecognitionLanguage}

Bu seçim kutusu metin tanıma için kullanılacak dili seçmek içindir.
Mevcut diller arası hızlıca geçiş  yapabilmek için [Girdi hareketleri iletişim kutusu dialog](#InputGestures) üzerinden bir tuş atayabilirsiniz.

##### Tanınan içeriği periyodik olarak yenile {#Win10OcrSettingsAutoRefresh}

Bu onay kutusu işaretlendiğinde, tanıma sonucu penceresindeyken NVDA tanınan içeriği otomatik olarak yenileyecektir.
Altyazılı bir video gibi sürekli değişen bir içeriği takip etmek istediğiniz durumlarda bu özellik çok yararlı olabilir.
Yenileme her bir buçuk saniyede bir gerçekleşir.
Bu seçenek varsayılan olarak devre dışıdır.

#### Gelişmiş Ayarlar {#AdvancedSettings}

Uyarı! Bu kategorideki ayarlar ileri seviye kullanıcılar içindir ve yanlış şekilde yapılandırılmışsa NVDA'nın düzgün çalışmamasına neden olabilir.
Bu ayarlarda yalnızca, ne yaptığınızı bildiğinizden eminseniz veya bir NVDA geliştiricisi tarafından özel olarak talimat verildiyse değişiklik yapın.

##### Gelişmiş ayarlarda değişiklik yapma {#AdvancedSettingsMakingChanges}

Gelişmiş ayarlarda değişiklik yapmak için, kontrollerin bu ayarları değiştirmenin risklerini anladığınızı onaylayarak etkinleştirilmesi gerekir.

##### Varsayılan ayarları geri yükleme {#AdvancedSettingsRestoringDefaults}

Uyarı onay kutusu işaretli olmasa bile, düğme ayarların varsayılan değerlerini geri yükler.
Ayarları değiştirdikten sonra varsayılan değerlere dönmek isteyebilirsiniz.
Bu, ayarların değiştirilip değiştirilmediğinden emin değilseniz de söz konusu olabilir.

##### Developer Scratchpad Dizini'nden özel kod yüklemeyi etkinleştir {#AdvancedSettingsEnableScratchpad}

NVDA için eklentiler geliştirirken, kodu yazarken test edebilmek yararlı olabilir.
Bu seçenek etkinleştirildiğinde, NVDA'nın NVDA kullanıcı yapılandırma dizininizdeki özel bir geliştirici scratchpad dizininden özel appModules, globalPlugins, brailleDisplayDrivers ve synthDrivers yüklemesini sağlar.
Eklentilerle benzer şekilde bu modüller, NVDA başlatılırken veya appModules ve globalPlugins söz konusu olduğunda [eklentiler yeniden yüklendiğinde](#ReloadPlugins) yüklenir.
Bu seçenek varsayılan olarak kapalıdır ve NVDA'da, kullanıcının açık bilgisi dışında hiçbir test edilmemiş kodun çalıştırılmadığından emin olunması istenmektedir.
Özel kodu başkalarına dağıtmak istiyorsanız, onu bir NVDA eklentisi olarak paketlemelisiniz.

##### Geliştirici Scratchpad Dizinini Aç {#AdvancedSettingsOpenScratchpadDir}

Bu düğme, geliştirirken özel kod yerleştirebileceğiniz dizini açar.
Bu düğme yalnızca NVDA, Geliştirici Scratchpad Dizininden özel kod yüklenmesini sağlayacak şekilde yapılandırılmışsa etkindir.

##### UI Otomasyon etkinlikleri ve özellik değişiklikleri {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |Otomatik, Seçimli, global|
|varsayılan |Otomatik|

Bu seçenek, NVDA'nın Microsoft UI Otomasyon erişilebilirlik API'si tarafından tetiklenen olaylara nasıl kaydolacağını değiştirir.
Bu seçim kutusunda üç seçenek bulunmaktadır:

* Otomatik: "seçimli" Windows 11 Sun Valley 2 (sürüm 22H2) ve sonraki sürümlerde, veya veya "global".
* seçimli: NVDA, çoğu olay için olay kaydını sistem odağıyla sınırlayacaktır.
Bir veya daha fazla uygulamada performans sorunları yaşıyorsanız, performansın iyileşip iyileşmediğini görmek için bu işlevi denemenizi öneririz.
Ancak Windows'un eski sürümlerinde NVDA, bazı kontrollerde (görev yöneticisi ve emoji paneli gibi) odağı takibinde sorun yaşayabilir.
* Global: NVDA, NVDA'nın kendi içinde işlenen ve atılan birçok UIA olayı için kayıt yapar.
Odak takibi birçok durumda daha stabil olsa da, özellikle Microsoft Visual Studio gibi uygulamalarda performans önemli ölçüde düşer.

##### Microsoft Word belge kontrollerine erişmek için UI otomasyonunu kullan {#MSWordUIA}

NVDA'nın Microsoft Word belgelerine erişmek için eski Microsoft Word nesne modeli yerine UI Otomasyonu erişilebilirlik API'sini kullanıp kullanmayacağını belirler.
Bu, Microsoft word'ün kendisindeki belgeler ve Microsoft Outlook'taki mesajlar için geçerlidir.
Bu ayar aşağıdaki değerleri içerir:

* Varsayılan (uygun olduğunda)
* Sadece gerektiğinde: Microsoft Word nesne modelinin hiç mevcut olmadığı durumlarda
* Uygun olduğunda: Microsoft Word sürüm 16.0.15000 veya üzeri veya Microsoft Word nesne modelinin kullanılamadığı durumlarda
* Her zaman: UI otomasyonunun Microsoft word'de olduğu her yerde (tamamlanmamış olsa bile).

##### Uygunsa Microsoft &Excel elektronik tablo kontrollerine erişmek için UI Otomasyonu kullan {#UseUiaForExcel}

Bu seçenek etkinleştirildiğinde, NVDA, Microsoft Excel Elektronik Tablo kontrollerinden bilgi almak için Microsoft UI Automation erişilebilirlik API'sini kullanmayı deneyecektir.
Bu deneysel bir özelliktir ve Microsoft Excel'in bazı özellikleri bu modda kullanılamayabilir.
Örneğin, formülleri ve yorumları listelemek için NVDA'nın Öğe Listesini kullanabilme ve elektronik tablodaki form alanlarına atlamak için tarama kipinde hızlı gezinme özellikleri kullanılamaz.
Ancak, temel elektronik tablolarda gezinme / düzenleme için bu seçenek, büyük bir performans artışı sağlayabilir.
Microsoft Excel build 16.0.13522.10000 veya sonraki sürümlerini kullananların bu özelliği test etmesini ve geri bildirimde bulunmasını memnuniyetle karşılasak da, yine de kullanıcıların çoğunluğunun bunu varsayılan olarak açmasını önermiyoruz.
Microsoft Excel'in UI otomasyon uygulaması sürekli değişiyor ve Microsoft Office'in 16.0.13522.10000'den eski sürümleri, bu seçeneğin herhangi bir şekilde kullanılması için yeterli  olmayabilir.

##### Gelişmiş etkinlik izleme kullan {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |Varsayılan (Etkin), Devre Dışı, Etkin|
|Varsayılan |Etkin|

Bu seçenek etkinleştirildiğinde, NVDA bir terminalde büyük miktarda metin çıktısı gibi çok miktarda UI Otomasyon etkinliğiyle karşılaşırsa, NVDA'nın kararlı şekilde çalışmasına yardımcı olur.
Bu seçeneği değiştirdikten sonra, değişikliğin etkili olması için NVDA'yı yeniden başlatmanız gerekir.

##### Windows Konsol desteği {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |Otomatik, UIA kullanılabilir olduğunda, Eski|
|Varsayılan |Otomatik|

Bu seçenek, NVDA'nın komut istemi, PowerShell ve Linux için Windows Alt Sistemi tarafından kullanılan Windows Konsolu ile nasıl etkileşime gireceğini belirler.
Not: modern Windows Terminali etkilenmez.
Microsoft, Windows 10 sürüm 1709'da [UI Otomasyon API'si için konsola destek ekledi https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-](update/) Böylece bu özelliği destekleyen ekran okuyucular büyük ölçüde geliştirilmiş performans ve kararlılık geliştirmeleri sağlıyor.
UI Otomasyonunun kullanılamadığı veya istenmeyen bir kullanıcı deneyimiyle karşılaşılırsa, NVDA'nın eski konsol desteği kullanılabilir.
Windows Konsol destek seçim kutusunda üç seçenek vardır:

* Otomatik: Windows 11 sürüm 22H2 ve sonraki sürümlerde bulunan Windows Konsolu sürümünde UI Otomasyonunu kullanır.
Bu seçenek önerilir ve varsayılan olarak seçilidir.
* UIA kullanılabilir olduğunda: Eksik veya hatalı uygulamaları olan sürümler için bile mümkünse konsollarda UI Otomasyonunu kullanır.
Bu sınırlı işleve sahip seçenek sizin kullanımınız için yeterli) olsa da, bu seçeneğin kullanımı tamamen size aittir ve bunun için herhangi bir destek sağlanmayacaktır.
* Eski: Windows Konsolunda UI Otomasyonu tamamen devre dışı bırakılır.
UI Otomasyonunun geliştirilmiş bir kullanıcı deneyimi sunacağı durumlarda bile eski yedek her zaman kullanılabilir olacaktır.
Bu nedenle, ne yaptığınızı bilmiyorsanız bu seçeneği seçmeniz önerilmez.

##### Microsoft Edge ve diğer Chromium tabanlı tarayıcılar'la uygun olduğunda UIA kullan {#ChromiumUIA}

Microsoft Edge gibi Chromium tabanlı tarayıcılarda mevcut olduğunda UIA'nın ne zaman kullanılacağını belirlemenize izin verir.
Chromium tabanlı tarayıcılar için UIA desteği geliştirme aşamasındadır ve IA2 ile aynı düzeyde erişim sağlamayabilir.
Seçim kutusunda aşağıdaki seçenekler vardır:

* Varsayılan (Yalnızca gerekli olduğunda): NVDA varsayılanı, şu anda bu "Yalnızca gerektiğinde" dir. Bu varsayılan durum, teknoloji olgunlaştıkça gelecekte değişebilir.
* Yalnızca gerekli olduğunda: NVDA, IA2'yi kullanmak için tarayıcı sürecine enjekte edemediğinde ve UIA mevcut olduğunda, NVDA UIA kullanacaktır.
* Evet: Tarayıcı UIA'yı kullanılabilir hale getirirse, NVDA onu kullanır.
* Hayır: NVDA işlem sırasında enjekte edemese bile UIA'yı kullanmaz. Bu, geliştiriciler için IA2 ile ilgili sorunları gidermek için yararlı olabilir ve NVDA'nın UIA'ya geri dönmediğinden emin olmak isteyebilirler.

##### Bilgi notları {#Annotations}

Bu seçenek grubu, ARIA bilgi notları için deneysel destek ekleyen özellikleri etkinleştirmek için kullanılır.
Bu özelliklerden bazıları eksik sunuluyor olabilir.

<!-- KC:beginInclude -->
"sistem imleci konumundaki Tüm ek açıklama ayrıntılarının özetinin bildirimi" için, NVDA+d'ye basın.
<!-- KC:endInclude -->

Aşağıdaki seçenekler mevcuttur: 

* "Rapor, yapılandırılmış ek açıklamalar için 'ayrıntılara sahiptir'": metin veya kontrolde daha fazla ayrıntı varsa, raporlamayı etkinleştirir.
* "Aria açıklamasını her zaman bildir":
  `accDescription` kaynağı aria-description olduğunda, açıklama aktarılır.
  Bu, web'deki ek açıklamalar için kullanışlıdır.
  Not:
  * `accDescription` için birçok kaynak vardır, bunların birçoğu karışık veya güvenilmez anlamlara sahiptir.
    Tarihsel olarak AT, `accDescription` kaynaklarını ayırt edemedi, tipik olarak karışık anlambilim nedeniyle konuşulmadı.
  * Bu seçenek çok erken geliştirme aşamasındadır, henüz yaygın olarak bulunmayan tarayıcı özelliklerine dayanır.
  * Chromium 92.0.4479.0+ ile çalışması beklenirr

##### Canlı bölgeleri bildir {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |Varsayılan (Etkin), Devre Dışı, Etkin|
| Varsayılan |Etkin|

Bu seçenek, NVDA'nın bazı dinamik web içeriklerindeki değişiklikleri Braille ile bildirip bildirmeyeceğini belirler.
Bu seçeneği devre dışı bırakmak, NVDA'nın yalnızca konuşmadaki bu içerik değişikliklerini bildiren 2023.1 ve önceki sürümlerdeki çalışma biçimiyle aynı işlevi görür.

##### Tüm gelişmiş terminallerde parolaları söyle {#AdvancedSettingsWinConsoleSpeakPasswords}

Bu ayar  [yazılan karakterleri seslendir](#KeyboardSettingsSpeakTypedCharacters) veya [yazılan sözcükleri seslendir](#KeyboardSettingsSpeakTypedWords) UI otomasyon desteği etkinleştirilmiş Windows Konsolu ve Mintty gibi bazı terminal programlarında ekranın güncellenmediği (şifre girişi gibi) durumlarda karakterlerin söylenip söylenmeyeceğini kontrol eder.
Güvenlik düşünülerek bu ayar devre dışı bırakılmalıdır.
Ancak konsollarda yazılan karakter ve/veya sözcük seslendirmelerinde performans sorunları veya kararsızlık yaşıyorsanız veya güvenilir ortamlarda çalışıyorsanız ve parola bildirimini tercih ediyorsanız etkinleştirmeyi isteyebilirsiniz.

##### Mevcut olduğunda eski Windows Konsolunda geliştirilmiş yazılı karakter desteğini kullan {#AdvancedSettingsKeyboardSupportInLegacy}

Bu seçenek, eski Windows konsollarında yazılan karakterleri algılamak için alternatif bir yöntem sağlar.
Performansı artırıp bazı konsol çıktılarının hecelenmesini engellerken, bazı terminal programlarıyla uyumlu olmayabilir.
Bu özellik varsayılan olarak etkindir, Windows 10 1607 ve sonraki sürümlerde ve UI Automation kullanılamadığında veya devre dışı bırakıldığında kullanılabilir.
Dikkat: bu seçenek etkin durumdayken, şifreler gibi ekranda görünmeyen yazılan karakterler gizlenmez.
Güvensiz ortamlarda, parola girerken [karakterleri seslendir](#KeyboardSettingsSpeakTypedCharacters) ve [sözcükleri seslendir](#KeyboardSettingsSpeakTypedWords) işlevlerini geçici olarak devre dışı bırakabilirsiniz.

##### Diff algoritması {#DiffAlgo}

Bu ayar, NVDA'nın terminallerde  yeni metni nasıl konuşacağını kontrol eder.
diff algoritması seçim kutusunda üç seçenek vardır:

* Otomatik: Bu seçenek, NVDA'nın çoğu durumda Diff Match Patch'i tercih etmesine, ancak Windows Konsolu ve Mintty'nin eski sürümleri gibi sorunlu uygulamalarda Difflib'e geri dönmesine neden olur.
* Diff Match Patch: Bu seçenek, NVDA'nın, tavsiye edilmediği durumlarda bile, terminal metnindeki değişiklikleri karakter bazında hesaplamasına neden olur.
Konsola büyük hacimlerde metin girildiğinde  performansı artırabilir ve satırların ortasında yapılan değişikliklerin daha doğru raporlanmasına olanak tanır.
Ancak, bazı uygulamalarda yeni metnin okunması dalgalı veya tutarsız olabilir.
* Difflib: bu seçenek, NVDA'nın, tavsiye edilmediği durumlarda bile, terminal metnindeki değişiklikleri satır satır hesaplamasına neden olur.
NVDA'nın 2020.4 ve daha önceki sürümlerindeki davranışıyla aynıdır.
Bu ayar, bazı uygulamalarda gelen metnin okunmasını kararlı kılabilir.
Ancak, terminallerde, bir satırın ortasına bir karakter eklerken veya silerken, imleçten sonraki metin okunacaktır.

##### Windows Terminal'de yeni metin şunun aracılığıyla oku: {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |Varsayılan (fark bulma), fark bulma, UIA bildirimleri|
|Varsayılan |Fark bulma|

Bu seçenek, NVDA'nın Windows Terminal'de ve Visual Studio 2022'de kullanılan WPF Windows Terminal kontrolünde hangi metnin "yeni" olduğunu (ve dolayısıyla "dinamik içerik değişikliklerini bildir" etkinleştirildiğinde yeni metnin nasıl belirlenip bildirileceğini  ayarlamanıza yarar.
Windows Konsolunu (`conhost.exe`) etkilemez.
Mevcut üç seçenek bulunmaktadır:

* Varsayılan: Bu seçenek "Fark bulma" ile aynı işlevi yapar, ancak UIA bildirimleri için destek daha da geliştirildiğinde değişmesi beklenmektedir.
* Fark bulma: Bu seçenek, terminal her yeni metin oluşturduğunda değişiklikleri hesaplamak için seçilen diff algoritmasını kullanır.
Bu, NVDA'nın 2022.4 ve önceki sürümlerdeki davranışıyla aynıdır.
* UIA bildirimleri: Bu seçenek, konuşulacak metni belirleme sorumluluğunu Windows Terminal'e bırakır ve bu sayede NVDA'nın artık ekrandaki metnin yeni olup olmadığını belirlemesine gerek kalmaz.
Bu, Windows Terminal'in performansını ve kararlılığını önemli ölçüde artırmalıdır, ancak bu özellik henüz geliştirilme aşamasındadır.
Özellikle, şifreler gibi ekranda görüntülenmeyen yazılan karakterler bu seçenek seçildiğinde bildirilir.
Ayrıca, 1.000 karakterin üzerindeki sürekli metin çıktıları doğru bir şekilde bildirilmeyebilir.

##### Süresi dolmuş odak etkinlikleri için konuşmayı iptal etmeyi dene {#CancelExpiredFocusSpeech}

Bu seçenek, süresi dolmuş odak olayları için konuşmanın iptal edilmesi  davranışını etkinleştirir.
Özellikle Chrome ile Gmail'deki mesajlarda hızlı bir şekilde hareket etmek NVDA'nın artık geçerli olmayan bilgileri aktarmasına neden olabilir.
Bu işlev NVDA 2021.1'den itibaren varsayılan olarak etkindir.

##### Düzenleme imleci hareketi zaman aşımı (MS cinsinden) {#AdvancedSettingsCaretMoveTimeout}

Bu seçenek, NVDA'nın düzenleme imleci (ekleme noktası) düzenlenebilir metin kontrollerinde hareket etmesini bekleyeceği mili saniye sayısını ayarlamanızı sağlar.
NVDA’nın, düzenleme imlecini yanlış şekilde takip ettiğini fark ederseniz, her zaman arkasında bir karakter varmış gibi görünüyor veya satırları tekrarlıyorsa, o zaman bu değeri arttırmayı deneyebilirsiniz.

##### Renkler için saydamlığı bildir {#ReportTransparentColors}

Bu seçenek, renkler saydam olduğunda bildirime  olanak tanır ve 3. taraf bir uygulamayla kullanıcı deneyimini geliştirmek için bilgi toplayan addon/appModule geliştiricileri için yararlıdır.
Bazı GDI uygulamaları metni arka plan rengiyle vurgulayacaktır, NVDA (görüntüleme modeli aracılığıyla) bu rengi bildirmeye çalışır.
Bazı durumlarda, metin arka planı tamamen saydam olabilir ve metin başka bir GUI öğesinde katmanlanır.
Tarihsel olarak popüler olan birkaç GUI API'si ile metin saydam bir arka planla oluşturulabilir, ancak görsel olarak arka plan rengi doğrudur.

##### Ses çıkışı için WASAPI kullan {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Seçenekler |Varsayılan (Etkin), Devre Dışı, Etkin|
|Varsayılan |Etkin|

Bu seçenek, ses çıktısı için Windows Ses Oturumu API'si (WASAPI) kullanmanızı sağlar.
WASAPI, hem konuşma hem de sesler olmak üzere NVDA ses çıkışının hızını, performansını ve kararlılığını artırabilen bir ses çerçevesidir.
Bu seçeneği değiştirdikten sonra, değişikliğin etkin olabilmesi için NVDA'yı yeniden başlatmanız gerekir.
WASAPI'nin devre dışı bırakılması aşağıdaki seçenekleri devre dışı bırakır:

* [NVDA seslerinin ses seviyesi konuşma ses seviyesine eşit olsun volume](#SoundVolumeFollowsVoice)
* [NVDA ses düzeyi](#SoundVolume)

##### Hata ayıklama kategorileri {#AdvancedSettingsDebugLoggingCategories}

Bu listedeki onay kutuları, NVDA günlüğünde belirli hata ayıklama mesajı kategorilerini etkinleştirmenize izin verir.
Bu mesajların kaydedilmesi performansın düşmesine ve büyük günlük dosyalarının oluşturulmasına  neden olabilir.
Bunları yalnızca, bir NVDA geliştiricisi tarafından özellikle talimat verilmişse   açın. Örneğin Bir braille ekran sürücüsünün neden doğru çalışmadığını anlamaya çalışırken.

##### Günlüğe kaydedilen hatalar için ses çal {#PlayErrorSound}

Bu seçenek, bir hatanın kaydedilmesi durumunda NVDA'nın ses çalıp çalmayacağını belirlemenizi sağlar.
Yalnızca test sürümlerinde (varsayılan) seçilmesi, NVDA'nın yalnızca mevcut NVDA sürümü bir test sürümü (alfa, beta veya kaynaktan çalıştırma) olması durumunda hata seslerini çalmasına neden olur.
Evet'i seçmek, mevcut NVDA sürümünüz ne olursa olsun hata seslerini etkinleştirmenizi sağlar.

##### hızlı gezinme  Metin paragrafı için normal ifade komutları {#TextParagraphRegexEdit}

Bu alan, kullanıcıların tarama kipinde metin paragraflarını algılamak için normal ifadeyi özelleştirmesine olanak tanır.
[Metin paragrafında gezinme komutu](#TextNavigationCommand), bu normal ifadeyle eşleşen paragrafları arar.

### çeşitli Ayarlar {#MiscSettings}

[NVDA ayarları](#NVDASettings) iletişim kutusunun yanında, NVDA Menüsündeki Tercihler altmenüsü aşağıda verilen çeşitli diğer öğeleri de içerir.

#### Konuşma Sözlükleri {#SpeechDictionaries}

Tercihler menüsünde bulunan konuşma sözlükleri menüsü, belirli sözcük veya öbeklerin NVDA tarafından nasıl söyleneceğini ayarlayabileceğiniz iletişim kutularını içermektedir.
şu an itibariyle 3 farklı konuşma sözlüğü bulunmaktadır.
bunlar:

* varsayılan Bu sözlükteki kurallar tüm NVDA konuşmalarını etkiler.
* Ses Bu sözlükteki kurallar o an kullanılan sentezleyici sesini etkiler.
* Geçici Bu sözlükteki kurallar tüm NVDA konuşmalarını etkiler ancak sadece NVDA'nın açık olduğu o oturumda geçerlidir. Bu kurallar geçicidir ve NVDA yeniden başlatıldığında geçerli olmazlar.

Herhangi bir yerden bu sözlüklerle ilgili iletişim kutularını açabilmek için [Girdi hareketleri iletişim kutusunu](#InputGestures) kullanarak özel kısayol tuşları atamanız gerekir.

Tüm sözlük iletişim kutularında konuşma işlemlerinde kullanılacak kuralların bir listesi bulunmaktadır.
İletişim kutularında ayrıca, Kural Ekle, Düzenle, kaldır ve tümünü kaldır düğmeleri de mevcuttur.

Sözlüğe yeni bir kural eklemek için önce ekle düğmesine basın, iletişim kutusundaki alanları doldurun ve tamam düğmesine basın.
bundan sonra kural listesinde eklediğiniz yeni kuralı da göreceksiniz.
Ancak kurallarınızı kaydettiğinizden emin olabilmek için, kural ekleme/düzenleme işiniz bitikten sonra sözlük iletişim kutusunu tamam düğmesine basarak tümüyle kapamayı unutmayın.

NVDA konuşma sözlüklerindeki kurallar, bir sözcüğün telafuzunu farklı bir şeye dönüştürmenizi sağlar.
örneğin, NVDA'dan, kuş kelimesiyle her karşılaştığında buna "kurbağa" demesini isteyebilirsiniz.
Kural Ekle iletişim kutusunda bunun en basit yolu, ifade alanına kuş,"Olarak Değiştir" yazma alanına da "kurbağa" yazmaktır.
Ayrıca açıklama alanına kuralla ilgili şunun gibi bir tanım yazmak isteyebilirsiniz. Kuşu kurbağa olarak değiştirir.

Öte yandan, NVDA konuşma sözlükleri basit bir sözcük değişiminden çok daha güçlüdür.
Kural ekle diyaloğunda ayrıca, kuralın büyük küçük harf duyarlı olup olmamasını ayarlayabileceğiniz bir onay kutusu da yer almaktadır.
Yani NVDA sözcüğün büyük ya da küçük yazılışına bakabilir. Varsayılan olarak NVDA büyük küçük harfleri yoksaymaktadır.

Son olarak, bir dizi seçim düğmesi, NVDA'ya girdiğiniz ifadenin her yerde mi, ifadenin tamamı tek başına bir sözcük oluşturduğu taktirde mi tanımladığınız gibi seslendirileceğini ya da ifadeye kurallı ifade  olarak muamele edileceğini belirlemenizi sağlar.
İfade türünün sözcüğün tamamı olarak ayarlanması, yerine koyma işleminin ancak ifade daha geniş bir sözcüğün parçası değilse yapılacağı anlamına gelir.
Örneğin, girilen sözcüğün önünde ya da sonunda herhangi bir harf ya da sayı ya da alt çizgi  yoksa ifadenin yerine olarak değiştir alanına girilen ifade konur.
Öyleyse, yukarıdaki "kuş" ifadesini "kurbağa" ile değiştirme örneğini kullanırsak, ifadenin tamamı seçeneği tercih edildiyse, "kuşlar" ifadesi "kurbağalar" olarak seslendirilmez.

Bir kurallı ifade, içinde bir seferde birden fazla karakterle eşleştirme yapmanızı sağlayan özel karakterler barındıran bir öbektir. Bu eşleşme yalnızca rakamlar veya yalnızca harfler de olabilir. 
Kurallı ifadeler konusu bu kullanıcı rehberinde kapsanmamıştır.
Genel bilgi ve tanıtım için lütfen [Python'un Normal İfade Kılavuzuna](https://docs.python.org/3.11/howto/regex.html)  bakın.

#### Noktalama/imla sözlüğü {#SymbolPronunciation}

Bu iletişim kutusu, noktalama ve imla işaretlerinin nasıl seslendirileceğini belirlemenizin yanısıra bu işaretlerin seslendirilme düzeylerini ayarlamanızı sağlar.

Noktalama/imla telaffuzu iletişim kutusunun başlığında, düzenlemenin hangi dil için yapılacağı gösterilir.
Bu iletişim kutusunun , [NVDA ayarları iletişim kutusu](#NVDASettings) altındaki [konuşma kategorisi](#SpeechSettings) bulunan "Karakter ve sembolleri işlerken sentezleyici ve sesin diline güven" ayarını dikkate alacağını not edin; yani, bu seçenek işaretliyse, NVDA dili yerine seçili sentezleyicinin dili dikkate alınır.

Önce semboller listesinden değişiklik yapmak istediğiniz sembol/işareti bulun.
Sembolü veya sembolün  bir bölümünü, Filtreye göre düzenle kutusuna girerek sembolleri filtreleyebilirsiniz.

* Olarak değiştir alanı, NVDA'nın sözkonusu işaretle karşılaştığında ne demesi gerektiğini belirlemenizi sağlar.
* Düzey alanı ise, işaretin seslendirilmesini istediğiniz en düşük imla seslendirme düzeyini belirlemenize imkan verir (hiç biri, bağzıları, çoğu veya tümü).
Ayrıca düzeyi karakter olarak ayarlayabilirsiniz. Bu durumda, aşağıdaki iki durum harici semboller seslendirilmez:
  * Karakter karakter gezinirken.
  * NVDA bu sembolü içeren herhangi bir metni HARF HARF OKURKEN.
* Sentezleyiciye asıl sembolü gönder alanı sembol için belirlenen seslendirme değeri yerine sentezleyiciye sembolün kendisinin gönderilmesini sağlar.
Bu, sembolün sentezleyicinin duraksamasına ya da tonlamayı değiştirmesine neden olan bir sembol olması halinde faydalı olabilir.
Örneğin, virgül işareti sentezleyicinin duraksamasına yol açar.
Üç seçenek bulunmaktadır:
  * hiçbir zaman: Asıl sembolü hiçbir zaman sentezleyiciye gönderme.
  * her zaman: Asıl sembolü her zaman sentezleyiciye gönder.
  * Yalnızca noktalama / imla seslendirme düzeyinin altındaysa: Asıl sembolü sentezleyiciye, noktalama / imla seslendirme seviyesi buradakinden daha düşük seviyede ayarlanmışsa gönder.
  Örneğin, noktalama / imla seslendirme düzeyinden yüksek olarak ayarlanması halinde sembolün olarak değiştir alanındaki ifade kullanılarak seslendirilmesini, aksi halde bu sembolün sentezleyicinin konuşmasında duraksamaya neden olması sonucunda bu sembolün varlığının belirtilmesini sağlayabilirsiniz.

Ekle düğmesine basarak yeni işaretler ekleyebilirsiniz.
Açılacak iletişim kutusunda, işareti girin ve tamam düğmesine basın.
Daha sonra, başka işaretler için yaptığınız gibi, yeni işaretin olarak değiştir alanını ve seslendirme seviyesini düzenleyin.

Kaldır düğmesine basarak daha önce eklediğiniz işareti silebilirsiniz.

Bu ayarlamaları yaptıktan sonra tamam düğmesine basarak değişiklikleri kaydedebilir; iptal düğmesiyle de değişiklik öncesi ayarlara geri dönebilirsiniz.

Karmaşık semboller söz konusu olduğunda, Değiştirme alanı eşleşen metnin bazı grup referanslarını içermelidir. Örneğin, tam bir tarihle eşleşen bir desen için, \ 1, \ 2 ve \ 3'ün tarihin karşılık gelen bölümleriyle değiştirilmesi için alanda görünmesi gerekir.
Bu nedenle, değiştirme alanındaki Normal ters bölüler iki katına çıkarılmalıdır, örneğin "a\b" yerine geçmesi için "a\\b" yazılmalıdır.

#### Girdi Hareketleri {#InputGestures}

Bu iletişim kutusunda, NVDA komutları için kullanılan hareketleri (klavyedeki tuşlar, braille ekrandaki düğmeler , vs.) özelleştirebilirsiniz.

Sadece, iletişim kutusu açılmadan önce kullanılabilen komutlar gösterilir.
Örneğin, tarama kipiyle ilgili hareketleri özelleştirmek istiyorsanız, girdi hareketleri iletişim kutusunu tarama kipindeyken açmalısınız.

BU diyalogdaki ağaç, kullanılabilen NVDA komutlarını kategoriler altında gruplanmış olarak listeler.
Bunları, filtreleme kriteri alanına komutlarla ilgili olabilecek çeşitli kelimeler girerek filtreleyebilirsiniz.
Bir komutla ilişkili hareketler o komutun altında listelenir.

Bir komuta girdi hareketi eklemek için, komutun üzerindeyken ekle düğmesine basın.
Daha sonra, eklemek istediğiniz girdi hareketini yapın; örneğin klavyede tuş ya da tuş kombinasyonuna ya da braille ekranda düğmeye basın.
Çoğu kez, bir hareket birden fazla şekilde değerlendirilebilir.
Örneğin, klavyede bir tuşa bastıysanız, onun sadece mevcut klavye düzeni için geçerli olmasını isteyebilirsiniz (masaüstü ya da dizüstü düzenleri) ya da tüm düzenler için kaydedebilirsiniz.
Bu durumda,, seçim yapmanız için bir menü belirir.

Bir komutla ilgili hareketi silmek için, hareket seçiliyken kaldır tuşuna basın.

Taklit sistem klavye tuşları kategorisi, sistem klavyesindeki tuşları taklit etmek için  girilmiş olan ya da sizin girebileceğiniz NVDA komutlarını içerir.
Taklit sistem klavyesi tuşları, örneğin braille ekranınızdaki bazı tuşları kullanarak sistem klavyesinde bir tuşa ya da tuş kombinasyonuna basmak için  kullanılabilir.
Bu kategori altına bir komut eklemek için, taklit sistem klavye tuşları kategorisini seçin ve Ekle düğmesine basın.
Ardından, sistem klavyesinde  taklit etmek istediğiniz tuşa ya da tuş kombinasyonuna  basın.
Bundan sonra, tuş taklit sistem klavye tuşları kategorisi altına komut olarak eklenecek  ve ona yukarıda açıklandığı gibi bir girdi hareketi atayabileceksiniz..

Not:

* Taklit sistem klavye tuşu kategorisine eklediğiniz komutların, iletişim kutusunu kaydederken / kapatırken silinmemelerini istiyorsanız o komutlar için girdi hareketi atamalısınız. Başka deyişle, girdi hareketleri iletişim kutusunu eklediğiniz komut için girdi hareketi atamadan kapatırsanız, bu iletişim kutusunu tekrar açtığınızda eklediğiniz komutu bulamazsınız.
* Değişken tuşlara sahip bir giriş hareketi, değişken tuş olmadan taklit edilen bir hareketle eşlenemeyebilir.
Örneğin, taklit `a` girişini ayarlamak ve `kontrol + m` girdi hareketini yapılandırmak, uygulamanın `kontrol + a` gönderilmesine neden olabilir.

Değişiklikleri yaptıktan sonra, kaydetmek için tamam, vazgeçmek için iptal tuşuna basın.

### Konfigürasyonu Kaydetme ve Yeniden Yükleme {#SavingAndReloading}

Varsayılan olarak, NVDA kapatılırken, konfigürasyonda yaptığınız değişiklikler kalıcı olarak kaydedilir.
Ancak bu seçenek tercihler menüsündeki genel ayarlar altından değiştirilebilir.
Otomatik kaydetme ayarını değiştirdiyseniz, ayarları kalıcı olarak kaydetmek için NVDA menüsündeki Konfigürasyonu kaydet ögesini seçebilirsiniz.

Ayarlarınızda bir yanlışlık yaptığınızı düşünüyor ve eski ayarlarınıza geri dönmek istiyorsanız, NVDA menüsündeki "Kaydedilmiş Konfigürasyona Geri Dön" ögesini seçin.
Aynı zamanda, NVDA'yı kurduğunuz zamanki konfigürasyonu geri yüklemek için, NVDA menüsü altında da bulunan Fabrika Ayarlarına Dön ögesini seçebilirsiniz.

Ayrıca aşağıdaki NVDA tuş komutları da yararlıdır:
<!-- KC:beginInclude -->

| Ad |Masaüstü Kısayol tuşu |Dizüstü Kısayol tuşu |Tarif|
|---|---|---|---|
|Ayarları (Konfigürasyonu) kaydet |NVDA+kontrol+c |NVDA+kontrol+c |Ayarlarınızı kaydeder ve böylece NVDA'dan çıktığınızda ayarlarınız kaybolmaz|
|Kaydedilmiş ayarlara (konfigürasyona) geri dön |NVDA+kontrol+r |NVDA+kontrol+r |Bir kez basıldığında NVDA konfigürasyonunu en son kaydetmiş olduğunuz haline, üç kez basıldığında fabrika ayarlarına döndürür|

<!-- KC:endInclude -->

### Konfigürasyon Profilleri {#ConfigurationProfiles}

Bazen, farklı durumlar için farklı ayarlar kullanmak isteyebilirsiniz.
Örneğin, yazı yazarken satır girintilerinin bildirimini etkinleştirmek ya da düzeltme okuması yaparken yazı biçimi özelliklerinin bildirimini açmak isteyebilirsiniz.
NVDA konfigürasyon profillerini kullanarak bunu yapmanıza olanak tanır.

Bir konfigürasyon profili, sadece profil düzenlenirken değiştirilen ayarları kapsar.
Konfigürasyon profillerinde, NVDA bütünlüğü için geçerli olan [NVDA ayarları](#NVDASettings) iletişim kutusundaki Genel  kategorisindekiler hariç, çoğu ayar değiştirilebilir.

Konfigürasyon profilleri iletişim kutusu üzerinden manuel olarak  ya da atanacak özel bir kısayol ile etkinleştirilebilir.
Ayrıca, tetikleyuiciler vesilesiyle, örneğin belli bir uygulama açıldığında konfigürasyon profili otomatik olarak aktif hale getirilebilir.

#### Temel Yönetim {#ProfilesBasicManagement}

Konfigürasyon profillerini NVDA menüsü altından "Konfigürasyon profilleri" öğesini seçerek yönetebilirsiniz.
Ayrıca bunu bir tuş komutuyla yapabilirsiniz:
<!-- KC:beginInclude -->

* NVDA+kontrol+p: Konfigürasyon profilleri iletişim kutusunu göster.

<!-- KC:endInclude -->

Bu iletişim kutusundaki ilk kontrol, mevcut profillerden birini seçebileceğiniz profil listesidir.
İletişim kutusunu açtığınızda, o anda düzenlemekte olduğunuz profil seçilidir.
Aktif profiller için onların elle aktifleştirildiği, tetiklendiği veya düzenlenmekte olduğuyla ilgili ek bilgiler de gösterilir.

Bir profili yeniden adlandırmak veya silmek için, Yeniden adlandır veya Sil düğmelerine basın.

Iletişim kutusunu kapatmak için Kapat düğmesine basın.

#### Profil Oluşturma {#ProfilesCreating}

Bir profil oluşturmak için, Yeni düğmesine basın.

Yeni Profil iletişim kutusunda, profil için bir ad girebilirsiniz.
Ayrıca Bu profilin nasıl kullanılması gerektiğini seçebilirsiniz.
Bu profili yalnızca elle seçerek kullanmak istiyorsanız, varsayılan olan Manuel etkinleştirme seçeneğini tercih edin.
Aksi halde, bu profili otomatik olarak etkinleştirecek bir tetikleyici belirleyin.
Kolaylık sağlamak amacıyla, profil için isim girmediyseniz, tetikleyici seçtiğinizde isim alanı seçiminize uygun olarak doldurulacaktır. 
Tetikleyiciler hakkında daha fazla bilgi için [aşağıya](#ConfigProfileTriggers) bakın.

Tamam tuşuna basarak profili oluşturup yeni profili düzenlemek üzere konfigürasyon profilleri iletişim kutusunu kapatabilirsiniz.

#### Manuel Etkinleştirme {#ConfigProfileManual}

Manuel olarak etkinleştir düğmesine basarak bir profili elle etkinleştirebilirsiniz.
Etkinleştirildiğinde, başka profiller de tetikleyiciler nedeniyle aktifleştirilebilecektir, ama elle seçilen profildeki ayarlar tetiklenen profildeki ayarlardan farklıysa geçerli olan elle seçilen profildeki ayarlardır.
Örneğin, mevcut uygulama tarafından bir profil tetiklendiyse ve linklerin bildirimi bu profilde etkinleştirildiği halde manuel olarak etkinleştirilmiş profilde bildirim kapalıysa, linklerin bildirimi yapılmayacaktır.
Öte yandan, tetiklenen profilde normal konfigürasyondan farklı bir konuşmacı ayarladığınız halde manuel olarak etkinleştirdiğiniz profilde bu tür bir ayar yapmamışsanız, tetiklenen profildeki konuşmacı kullanılacaktır.
Bu arada, yapacağınız bir ayar değişikliği manuel profil için kaydedilecektir.
Manuel olarak aktifleştirilmiş profili devre dışı bırakmak için, profili konfigürasyon profilleri iletişim kutusunda seçtikten sonra Manuel devre dışı bırak düğmesine basın.

#### Tetikleyiciler {#ConfigProfileTriggers}

Konfigürasyon Profilleri iletişim kutusunda Tetikleyiciler düğmesine bastığınızda, çeşitli tetikleyiciler için otomatik olarak etkinleştirilecek profilleri belirleyebilirsiniz.

Listede gösterilen mevcut tetikleyiciler aşağıdaki gibidir :

* Aktif uygulama: uygulamaya geçtiğinizde tetiklenir.
* Tümünü oku: Tümünü oku komutu verildiğinde tetiklenir.

Bir tetikleyici için otomatik olarak etkinleştirilecek profili değiştirmek için, tetikleyiciyi seçtikten sonra Profil listesinden istediğiniz profili seçin.
Bir profil kullanılmasını istemiyorsanız (normal konfigürasyon) seçeniğini tercih etmelisiniz.

Konfigürasyon profilleri iletişim kutusuna dönmek için Kapat düğmesine basın.

#### Profil Düzenleme {#ConfigProfileEditing}

Bir profili manuel olarak etkinleştirdiyseniz, yapılacak değişiklikler bu profile kaydedilir.
Aksi takdirde, herhangi bir ayar değişikliği en son tetiklenen profile kaydedilir.
Örneğin, Not Dewfteri uygulaması için bir profil belirlemişseniz ve Not Defteri aktifse, NVDA ayarlarıyla ilgili değişiklikler bu profile kaydedilir.
Son olarak, manuel olarak etkinleştirilmiş ya da tetiklenmiş bir profil söz konusu değilse, yapılacak değişiklikler normal konfigürasyon profiline kaydedilecektir.

Tümünü oku tetikleyicisiyle ilişkili profili düzenlemek isterseniz, bu profili [manuel olarak](#ConfigProfileManual) etkinleştirmelisiniz.

#### Tetikleyicileri Geçici Olarak Devre Dışı Bırakma {#ConfigProfileDisablingTriggers}

Bazen, tüm tetikleyicileri geçici olarak devre dışı bırakmak yararlıdır.
Örneğin, manuel olarak etkinleştirdiğiniz bir profili ya da normal konfigürasyonu, herhangi bir tetikleyiciye atanmış bir profilin araya girmesini engelleyerek düzenlemek isteyebilirsiniz.
Bunu, Konfigürasyon Profilleri iletişim kutusunda bulunan , Tüm tetikliyiceleri geçici olarak devre dışı bırak onay kutusunu işaretleyerek yapabilirsiniz.

Tetikleyicilerin herhangi bir yerdeyken devre dışı bırakılması ya da tekrar etkinleştirilmesi için , [girdi hareketleri iletişim kutusunu](#InputGestures) kullanarak özel bir kısayol tuşu atayabilirsiniz.

#### Girdi hareketlerini kullanarak bir profili etkinleştirme {#ConfigProfileGestures}

Eklediğiniz her profil için, etkinleştirmek üzere bir veya daha fazla girdi hareketi atayabilirsiniz.
Varsayılan olarak, konfigürasyon profilleri için atanmış girdi hareketleri yoktur.
[Girdi Hareketleri iletişim kutusunu](#InputGestures) kullanarak Bir profili etkinleştirmek için girdi hareketi  ekleyebilirsiniz.
Konfigürasyon profilleri kategorisi altında  her profil için bir  giriş vardır.
Bir profili yeniden adlandırdığınızda, daha önce eklediğiniz herhangi bir hareket hala  kullanılabilir olacaktır.
Profillerden birini kaldırmak, onunla ilişkilendirilen hareketleri de otomatik olarak siler.

### Konfigürasyon Dosyalarının Konumu {#LocationOfConfigurationFiles}

NVDA taşınabilir sürümü, tüm ayarları, kişisel uygulama modüllerini ve kişisel sürücüleri NVDA dizininde bulunan ve UserConfig adı verilen dizinde saklamaktadır.

Kurulabilir NVDA sürümü ise, tüm ayarları, kişisel uygulama modülleri ve kişisel sürücüleri Windows kullanıcı profilinizde bulunan özel bir NVDA dizininde saklar.
Yani, sistemdeki her kullanıcının kendi NVDA ayarları olabilir.
Konfigürasyon dizinini herhangi bir yerden açmak için [girdi hareketleri iletişim kutusunu](#InputGestures) kullanarak bir kısayol tuşu atayabilirsiniz.
Kurulu bir NVDA sürümünde kullanıcı konfigürasyon  dizinine gitmek için, başlat menüsünden sırasıyla programlar -> NVDA -> Kullanıcı Konfigürasyon Dizinine Gözat bölümüne girebilirsiniz.

Logon ve Kullanıcı hesapları (UAC) gibi NVDA çalışırken kullanılan noktalardaki ayarlar, NVDA'nın kurulum dizinindeki systemConfig dizininde saklanmaktadır.
Genellikle bu ayarlara dokunulmamalıdır.
NVDA'nın logon ve kullanıcı hesapları ekranlarındaki ayarlarını değiştirmek için, önce NVDA ile Windows'da oturum açarken kullanılacak ayarları yapın, AYARLARI KAYDEDİP daha sonra [NVDA ayarları](#NVDASettings) iletişim kutusunda genel kategorisi  altında bulunan düğmeyi kullanarak NVDA'ya bu mevcut konfigürasyonu sistem konfigürasyonuna kopyalamasını söyleyin.

## Eklentiler ve Eklenti Mağazası {#AddonsManager}

Eklentiler, NVDA için yeni veya değiştirilmiş işlevsellik sağlayan yazılım paketleridir.
NVDA topluluğu ve ticari satıcılar gibi harici kuruluşlar tarafından geliştirilirler.
Eklentiler aşağıdakilerden herhangi birini yapabilir:

* Bazı uygulamalar için ek destek veya geliştirme sunma.
* Ekstra Braille ekranları veya konuşma sentezleyicileri için destek sağlama.
* NVDA'ya yeni özellikler ekleme veya değiştirme.

NVDA Eklenti Mağazası, eklenti paketlerine göz atmanıza ve yüklü eklentileri yönetmenize yarar.
Eklenti Mağazasında bulunan tüm eklentiler ücretsiz olarak indirilebilir.
Ancak bazı eklentiler kullanılmadan önce kullanıcıların bir lisans veya ek yazılım için ödeme yapmasını gerektirebilir.
Ücretli konuşma sentezleyicileri, bu tür eklentilere bir örnektir.
Ücretli bileşenler içeren bir eklenti yüklerseniz ve onu kullanma konusundaki fikrinizi değiştirirseniz, eklentiyi kolayca kaldırılabilir.

Eklenti Mağazasına gitmek için, NVDA menüsüne, ardından Araçlar alt menüsüne gidin.
Eklenti Mağazasına istediğiniz yerden ulaşmak için [Girdi hareketleri iletişim kutusu](#InputGestures) üzerinden bir girdi atayın.

### Eklentilere göz atma {#AddonStoreBrowsing}

Açıldığında, Eklenti Mağazası bir eklenti listesi görüntüler.
Daha önce bir eklenti kurmadıysanız, eklenti mağazası kurulabilir eklentilerin bir listesini gösterir.
Eğer bir eklenti yüklediyseniz, liste mevcut kurulu eklentileri gösterir.

Yukarı ve aşağı ok tuşlarıyla bir eklenti seçildiğinde, eklentinin ayrıntıları görüntülenir.
Eklentiler, [Eylemler menüsü](#AddonStoreActions) aracılığıyla erişilebilen 'Kur', 'Yardım', 'Devre Dışı Bırak' ve 'Kaldır' gibi seçeneklere sahiptir.
Kullanılabilir eylemler, eklentinin kurulu olup olmadığına ve etkin veya devre dışı olmasına bağlı olarak değişiklik gösterir.

#### Eklenti liste görünümleri {#AddonStoreFilterStatus}

Kurulu, güncellenebilir, kullanılabilir ve uyumsuz eklentiler için farklı liste görünümleri mevcuttur.
Eklenti görünümünü değiştirmek için, `kontrol+tab` tuşlarını kullanarak eklentiler listesinin etkin sekmesini değiştirin.
Ayrıca, görünümler listesinde gezinmek için `tab` tuşunu kullanarak ve ardından `solOK` ve `sağOk` tuşlarıyla seçimi değiştirebilirsiniz.

#### Etkin veya devre dışı eklentileri filtreleme {#AddonStoreFilterEnabled}

Genellikle, kurulu bir eklanti 'etkin' olarak kabul edilir, yani NVDA'da çalışır ve kullanılabilir durumdadır.
Ancak, kurulu eklentilerinizden bazılarını  devre dışı bırakmış olabilirsiniz.
Bu, eklentilerin mevcut NVDA oturumunuz sırasında işlevlerinin kullanılamayacağı anlamına gelir.
Bir eklentiyi, başka bir eklentiyle veya belirli bir uygulamayla çakıştığı için devre dışı bırakmış olabilirsiniz.
Ayrıca, NVDA güncelleme sırasında belirli eklentilerin uyumsuz olduğunu tespit ederse bunları devre dışı bırakabilir. Ancak, bu durumda sizi uyaracaktır.
Eklentiler, sadece uzun bir süreliğine ihtiyaç duyulmadığında, ancak gelecekte tekrar kullanmak istendiğinde kaldırmak istemediğiniz durumlar için de devre dışı bırakılabilir.

Kurulu ve uyumsuz eklentilerin listeleri, etkin veya devre dışı durumlarına göre filtrelenebilir.
Varsayılan olarak, hem etkin hem de devre dışı eklentiler gösterilir.

#### Uyumsuz eklentileri dahil etme {#AddonStoreFilterIncompatible}

Mevcut ve güncellenebilir eklentiler, kurulabilecek [uyumsuz eklentiler](#incompatibleAddonsManager)'i içerecek şekilde filtrelenebilir.

#### Eklentileri kategoriye göre filtrele {#AddonStoreFilterChannel}

Eklentiler dört kategoride dağıtılabilir:

* Kararlı: Geliştirici, bu eklentiyi test edilmiş bir eklenti olarak NVDA'nın yayınlanmış bir sürümüyle yayınlar.
* Beta: Bu eklentinin daha fazla test edilmesi gerekebilir, ancak kullanıcı geri bildirimi için yayınlanmıştır.
Öncelikli test etmek isteyenler için önerilir.
* Dev: Bu kategorinin eklenti geliştiricileri tarafından yayınlanmamış API değişikliklerini test etmek için kullanılması önerilir.
NVDA alfa sürümüyle test yapanların eklentilerinin bir "Dev" sürümünü kullanmaları gerekebilir.
* Harici: Eklenti mağazası dışından farklı kaynaklardan yüklenen eklentiler.

Eklentileri yalnızca belirli kategorilerde listelemek için kategori filtresi seçimini değiştirin.

#### Eklenti arama {#AddonStoreFilterSearch}

Eklentileri aramak için "Ara" metin kutusunu kullanın.
Arama kutusuna Eklentiler listesinden `şift+tab` tuşlarına basarak ulaşabilirsiniz.
Aradığınız eklenti türü için bir veya iki anahtar kelime yazın, ardından `tab` tuşuyla geri dönüp sonuçları kontrol edin.
Eğer aradığınız anahtar kelimeler eklenti kimliğinde, adında, yayıncıda veya açıklamada bulunursa listelenecektir.

### Eklenti eylemleri {#AddonStoreActions}

Eklentilerin kur, yardım, devre dışı bırak ve kaldır gibi eylemleri vardır.
Odaklanılmış bir eklenti üzerinde eylem menüsünü açmak için `uygulama` tuşuna veya `enter` tuşuna basabilirsiniz. Alternatif olarak, eklentiye sağ tıklayarak veya çift tıklayarak da erişebilirsiniz.
Ayrıca Bu menüye seçilen eklentinin ayrıntılarındaki Eylemler düğmesi aracılığıyla da erişilebilir.

#### Eklentileri kurma {#AddonStoreInstalling}

Bir eklentinin NVDA Eklenti Mağazasında mevcut olması, NV Access veya başka biri tarafından onaylandığı veya incelendiği anlamına gelmez.
Yalnızca güvendiğiniz kaynaklardan eklentiler kurmanız çok önemlidir.
Eklentiler, NVDA içinde kısıtlamalara tabi değildir.
Bu, eklentinin kişisel verilerinize veya hatta tüm sisteme erişimini içerebilir.

Eklentileri [Kullanılabilir eklentilere](#AddonStoreBrowsing) giderek yükleyebilir ve güncelleyebilirsiniz.
"Kullanılabilir eklentiler" veya "Güncellenebilir eklentiler" sekmesinden bir eklenti seçin.
Ardından, kurulumu başlatmak için güncelleme, kurulum veya değiştirme eylemini kullanın."

Aynı anda birden fazla eklenti de kurabilirsiniz.
Birden fazla eklenti kurmak için mevcut eklentiler sekmesinde birden fazla eklenti seçin. Ardından bağlam menüsüne gidin ve "Seçilen eklentileri kur" seçin.

Eklenti Mağazası dışından edindiğiniz bir eklentiyi kurmak için "Dış kaynaktan kur" düğmesine basın.
Bu, bilgisayarınızda veya bir ağ klasöründe (`.nvda-addon` dosyası) uzantılı eklenti paketlerini seçmenize olanak tanır.
Eklenti dosyasını açtıktan sonra kurulum işlemi başlayacaktır.

NVDA sisteminizde kurulu ve çalışıyorsa, kurulum sürecini başlatmak için doğrudan tarayıcıdan veya dosya sisteminden bir eklenti dosyası da açabilirsiniz.

Dış kaynaktan bir eklenti kurulurken, NVDA sizden kurulumu onaylamanızı isteyecektir.
Eklenti kurulduktan sonra, eklentinin çalışmaya başlaması için NVDA'nın yeniden başlatılması gerekir, ancak yüklemeniz veya güncellemeniz gereken başka eklentileriniz varsa NVDA'nın yeniden başlatılmasını erteleyebilirsiniz.

#### Eklentileri Kaldırma {#AddonStoreRemoving}

Bir eklentiyi kaldırmak için listeden eklentiyi seçin ve Kaldır eylemini kullanın.
NVDA, kaldırma işlemini onaylamanızı isteyecektir.
Kurulumda olduğu gibi, eklentinin sisteminizden kaldırılması için NVDA'nın yeniden başlatılması gerekir.
NVDA yeniden başlatılana kadar ilgili eklenti için liste üzerinde "yeniden başlatıldıktan sonra Kaldırılacak" ibaresi görüntülenecektir.
Aynı anda birden fazla eklenti kurabildiğiniz gibi, birden fazla eklentiyi de kaldırabilirsiniz.

#### Eklentileri Devre Dışı Bırakma ve Etkinleştirme {#AddonStoreDisablingEnabling}

Bir eklentiyi devre dışı bırakmak için "devre dışı bırak" eylemini kullanın.
Önceden devre dışı bırakılmış bir eklentiyi etkinleştirmek için "etkinleştir" eylemini kullanın.
Eklenti durumu "etkin" ise eklentiyi devre dışı bırakabilir veya eklenti durumu "devre dışı" ise etkinleştirebilirsiniz.
Etkinleştirme/devre dışı bırakma eyleminin her kullanımında, eklenti durumu NVDA yeniden başladığında ne olacağını gösterecek şekilde değişir.
Eğer eklenti önceden "etkin" durumdaysa, yeniden başlatma sonrasında durumu "devre dışı" olarak görüntülenir.
Eğer eklenti önceden "devre dışı" durumdaysa, yeniden başlatma sonrasında durumu "etkin" olarak görüntülenir.
Eklentileri yüklediğiniz veya kaldırdığınız gibi, bu değişikliklerin etkili olması için NVDA'yı yeniden başlatmanız gerekecektir.
Ayrıca, mevcut eklentiler sekmesinde birden fazla eklenti seçip ardından bağlam menüsü üzerinden uygun eylemi seçerek birden fazla eklentiyi aynı anda etkinleştirebilir veya devre dışı bırakabilirsiniz.

#### Eklentileri inceleme ve incelemeleri okuma {#AddonStoreReviews}

Bir eklenti kurmadan önce başkalarının yorumlarını okumak isteyebilirsiniz.
Ayrıca kullandığınız eklentiler hakkında incelemede bulunmak diğer kullanıcıların bir fikir sahibi olmalarına yardımcı olabilir.
Bir eklentinin incelemelerini okumak için Mevcut veya Güncellenebilir eklentiler sekmesinden bir eklenti seçin ve "Topluluk incelemeleri" eylemini kullanın.
Bu eylem sizi eklenti için incelemeleri okuyabileceğiniz ve inceleme yazabileceğiniz GitHub Tartışma web sayfasına yönlendirir.
Bu işlevin eklenti geliştiricileriyle doğrudan iletişimin yerine geçmediğini lütfen unutmayın.
Bu özelliğin kullanıcıların bir eklentinin kendileri için faydalı olup olmadığına karar vermelerine yardımcı olmak için geri bildirim paylaşılması için tasarlanmıştır.

### Uyumsuz Eklentiler {#incompatibleAddonsManager}

Bazı eski eklentiler artık kullandığınız NVDA sürümüyle uyumlu olmayabilir.
NVDA'nın daha eski bir sürümünü kullanıyorsanız, bazı yeni eklentiler de uyumlu olmayabilir.
Uyumsuz bir eklentiyi kurmaya çalışmak, eklentinin neden uyumsuz olarak değerlendirildiğini açıklayan bir hata mesajı görüntüler.

Eski eklentiler için, uyumsuzluk uyarısına rağmen sorumluluk size ait olmak üzere eklentiyi kurabilirsiniz.
Uyumsuz eklentiler, NVDA sürümünüzle çalışmayabilir ve çökme de dahil olmak üzere dengesiz veya beklenmeyen davranışlara neden olabilir.
Bir eklentiyi etkinleştirirken veya kurarken uyumluluk uyarısını devre dışı bırakabilirsiniz.
Uyumsuz eklenti daha sonra sorunlara neden olursa, devre dışı bırakabilir veya kaldırabilirsiniz.

NVDA'yı çalıştırırken sorun yaşıyorsanız ve yakın zamanda bir eklentiyi güncellediyseniz veya kurduysanız ve eklenti uyumsuz ise, NVDA'yı tüm eklentiler devre dışı bırakılmış şekilde geçici olarak çalıştırmayı deneyebilirsiniz.
NVDA'yı tüm eklentiler devre dışı bırakılmış olarak yeniden başlatmak için, NVDA'dan çıkarken uygun seçeneği seçin.
Alternatif olarak, [komut satırı seçeneği](#CommandLineOptions) `--disable-addons` seçeneğini kullanın.

[Kullanılabilir ve güncellenebilir eklentiler sekmeleri](#AddonStoreFilterStatus)'u kullanarak mevcut uyumsuz eklentilere göz atabilirsiniz.
Kurulu uyumsuz eklentilere [uyumsuz eklentiler sekmesi](#AddonStoreFilterStatus) kullanarak göz atabilirsiniz.

## Ekstra Araçlar {#ExtraTools}
### Log Görüntüleyicisi {#LogViewer}

Araçlar menüsü altında bulunan Log dosyasını göster öğesi, NVDA'yı en son başlattığınızdan şimdiye kadar gerçekleşen tüm NVDA oturum açma çıktılarını görmenizi sağlar.

İçeriği okuyabilmenin yanısıra, Kayıt dosyasının bir kopyasını farklı kaydedebilir ya da log dosyası açık olduğundan bu yana En son çıktı görüntüsünü görebilmek için ekranı güncelleyebilirsiniz.
Bu işlemler görüntüleyicinin Log menüsünde bulunmaktadır.

Log görüntüleyiciyi açtığınızda görüntülenen dosya bilgisayarınızda `%temp%\nvda.log` dosya konumuna kaydedilir.
NVDA her başlatıldığında yeni bir log dosyası oluşturulur.
Her başlatma sonrası eski log dosyası `%temp%\nvda-old.log` konumuna taşınır.

Ayrıca, log görüntüleyiciyi açmadan geçerli log dosyasının bir parçasını panoya kopyalayabilirsiniz.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu |açıklama|
|---|---|---|
|log görüntüleyiciyi aç |`NVDA+f1` |Log görüntüleyiciyi açar ve mevcut nesne hakkındaki geliştirici bilgilerini görüntüler.|
|Logun bir parçasını panoya kopyala |`NVDA+control+şift+f1` |Bu komuta bir kez basıldığında istenen log içeriği için bir başlangıç ​​noktası belirler. İkinci kez basıldığında başlangıç ​​noktasından itibaren log içeriğini panoya kopyalar.|

<!-- KC:endInclude -->

### Konuşma Görüntüleyicisi {#SpeechViewer}

Gören geliştiriciler ve NVDA'yı görenlere gösteren kişiler için, NVDA'nın söylediği tüm metinleri görmenizi sağlayan hareketli bir ekran mevcuttur.

Konuşma görüntüleyicisini etkinleştirmek için, NVDA menüsündeki araçlar menüsü altında bulunan "Konuşma Görüntüleyicisi" ögesini işaretleyin.
Devre dışı bırakmak için bu menü ögesinin işaretini kaldırın.

Konuşma Görüntüleyicisi penceresi "konuşma görüntüleyiciyi Başlangıçta göster" adlı bir onay kutusu içerir.
Bu işaretli ise, NVDA başlatıldığında konuşma görüntüleyici de açılır.
Kapatılırsa, konuşma görüntüleyici aynı boyutlarda ve konumda tekrar açılacaktır.

Konuşma görüntüleyicisi etkinken, konuşulan metinleri göstermek için düzenli bir biçimde güncellenecektir.
Ancak farenizle Görüntüleyiciye odaklanırsanız veya farenizi bir nesnenin üzerine getirirseniz, güncelleme geçici olarak duracak ve böylece mevcut içeriği kopyalama şansınız olacaktır.

Konuşma görüntüleyiciyi herhangi bir yerden açıp kapatmak için [Girdi Hareketleri iletişim kutusunu](#InputGestures) kullanarak kısayol tuşu belirleyebilirsiniz.

### Braille Görüntüleyici {#BrailleViewer}

Kör olmayan yazılım geliştiricileri veya NVDA'yı gören izleyicilere gösteren kişilerin kullanması için, braille çıktıyı ve her braille karakter için eşdeğer metni görüntülenmesini  sağlayan yüzer bir pencere kullanılabilir.
Braille görüntüleyici, fiziksel bir braille ekran ile aynı anda kullanılabilir, fiziksel cihazdaki hücre sayısıyla eşleşir.
Braille görüntüleyici etkin durumdayken, fiziksel braille ekranda olan  braillei gösterecek şekilde sürekli olarak güncellenir.

Braille görüntüleyiciyi etkinleştirmek için, NVDA menüsü Araçlar'ın altındaki "Braille Görüntüleyici" menü öğesini işaretleyin.
Devre dışı bırakmak için menü öğesinin işaretini kaldırın.

Fiziksel braille ekranlarında genellikle ileri veya geri kaydırma düğmeleri bulunur, Braille görüntüleme aracıyla kaydırmayı etkinleştirmek için [Girdi Hareketleri iletişim kutusu](#InputGestures)nu kullanarak "Braille ekranını geri kaydırır" ve "Braille ekranını ileri kaydırır" klavye kısayollarını atayın.

Braille görüntüleyici penceresinde "Başlangıçta braille görüntüleyicisini göster" adlı  bir onay kutusu bulunur.
Bu işaretliyse, NVDA başlatıldığında braille görüntüleyici açılacaktır.
Braille görüntüleme penceresi her zaman kapatıldığı zamanki boyut ve konumlarla yeniden açılmaya çalışır.

Braille görüntüleyici penceresi,  "Hücre yönlendirmesi için üzerine gelin"etiketli bir onay kutusu içerir, varsayılanı işaretli değildir.
İşaretlenirse, fareyi bir braille hücresinin üzerine getirmek, o hücre için "Braille hücresine yönlendir" komutunu tetikleyecektir.
Bu genellikle imleci hareket ettirmek veya bir kontrol için eylemi tetiklemek için kullanılır.
Bu, NVDA'NIN Braille hücresinden a haritasını doğru bir şekilde tersine çevirebileceğini test etmek için yararlı olabilir.
İstemeden hücrelere yönlendirmeyi önlemek için komut gecikir.
Hücre yeşile dönene kadar fare üzerinde olmalıdır.
Hücre açık sarı renkte başlar, turuncuya geçer, sonra aniden yeşile döner.

Braille görüntüleyiciyi herhangi bir yerden açıp kapatmak  için, lütfen [Girdi Hareketleri iletişim kutusunu](#InputGestures) kullanarak özel bir hareket atayın.

### Python Konsolu {#PythonConsole}

NVDA menüsündeki Araçlar altında bulunan NVDA Python konsolu, hata ayıklama, NVDA dahili bileşenlerinin genel denetimi veya bir uygulamanın erişilebilirlik hiyerarşisinin denetimi için yararlı olan bir geliştirme aracıdır.
Daha fazla bilgi için lütfen [NVDA Geliştirici Kılavuzuna](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html) bakın.

### Eklenti Mağazası {#AddonStoreMenuItem}

Bu, [NVDA Eklenti Mağazası](#AddonsManager)'ı açar.
Daha fazla bilgi için [Eklentiler ve Eklenti Mağazası](#AddonsManager) bölümüne göz atın.

### Taşınabilir kopya oluştur {#CreatePortableCopy}

Bu, kurulu sürümden NVDA'nın taşınabilir bir kopyasını oluşturmanıza izin veren bir iletişim kutusu açar.
Her iki şekilde de, NVDA'nın taşınabilir bir kopyasını çalıştırıyorsanız, ekstra araç alt menüsünde menü öğesine "taşınabilir kopya oluştur" yerine "NVDA'yı bu bilgisayara kur" adı verilir.

NVDA'nın taşınabilir bir kopyasını oluşturma veya bu bilgisayara NVDA'yı kurma iletişim kutusu, NVDA'nın taşınabilir kopyayı oluşturması gereken veya NVDA'nın yüklenmesi gereken bir klasör seçmenizi sağlayacaktır.

Bu iletişim kutusunda aşağıdakileri etkinleştirebilir veya devre dışı bırakabilirsiniz:

* Mevcut kullanıcı konfigürasyonunu kopyala (% appdata% \ roaming \ NVDA içindeki dosyaları veya taşınabilir kopyanızın kullanıcı yapılandırmasındaki dosyaları içerir ve ayrıca eklentileri ve diğer modülleri içerir)
* Oluşturulduktan sonra yeni taşınabilir kopyayı başlat veya kurulumdan sonra NVDA'yı başlat (taşınabilir kopya oluşturulduktan veya kurulumdan sonra NVDA'yı otomatik olarak başlatır)

### COM kayıt tamir aracını çalıştır... {#RunCOMRegistrationFixingTool}

Programların bilgisayara yüklenmesi ve kaldırılması, bazı durumlarda COM DLL dosyalarının kaydedilmemesine neden olabilir.
IAccessible gibi COM Arabirimleri doğru COM DLL kayıtlarına bağlı olduğundan, doğru kaydın eksik olması durumunda sorunlar yaşanabilir.

Bu, örneğin Adobe Reader, Math Player ve diğer programları yükleyip kaldırdıktan sonra ortaya çıkabilir.

Kayıp kayıt tarayıcılarda, masaüstü uygulamalarında, görev çubuğunda ve diğer arayüzlerde sorunlara neden olabilir.

Özellikle, bu araç çalıştırılarak aşağıdaki sorunlar çözülebilir:

* NVDA, Firefox, Thunderbird gibi tarayıcılarda gezinirken "bilinmeyen" diyorsa.
* NVDA odak kipi ile tarama kipi arasında geçiş yapamıyorsa
* Tarama kipini kullanırken tarayıcılarda gezinirken NVDA çok yavaşsa
* Ve muhtemelen diğer konular.

### Pluginleri Yeniden Yükle {#ReloadPlugins}

Bu öge etkinleştirildiğinde, uygulama modüllerini ve genel pluginleri NVDA'yı yeniden başlatmaya gerek duymadan yeniden yükler, ve bu, geliştiriciler için oldukça yararlıdır.
Uygulama modülleri NVDA'nın belirli uygulamalarla nasıl etkileşimde bulunduğunu yönetir.
Global pluginler, NVDA'nın tüm uygulamalarla nasıl etkileşimde bulunduğunu yönetir.

Aşağıdaki NVDA kısayolları da faydalı olabilir:
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu |Tarif|
|---|---|---|
|Pluginleri yeniden yükle |`NVDA+control+f3` |NVDA'nın global pluginlerini ve uygulama modüllerini yeniden yükler.|
|Yüklenen uygulama modülünü ve yürütülebilir dosyayı bildir |`NVDA+control+f1` |Varsa uygulama modülünün adını ve odaklı uygulamayla ilişkili yürütülebilir dosyanın adını bildirir.|

<!-- KC:endInclude -->

## Desteklenen Konuşma Sentezleyicileri {#SupportedSpeechSynths}

Bu bölümde NVDA tarafından desteklenen sentezleyici bilgileri yer almaktadır.
NVDA ile kullanılabilecek ticari ve ücretsiz konuşma sentezleyicileri satın alabilmeniz ya da indirebilmeniz için çok daha geniş bir listeyi, bu sayfada bulabilirsiniz [https://www.nvda-project.org/wiki/ExtraVoices](https://github.com/nvaccess/nvda/wiki/ExtraVoices).

### eSpeak NG {#eSpeakNG}

[eSpeak NG](https://github.com/espeak-ng/espeak-ng) sentezleyicisi Doğrudan NVDA içinde gömülüdür ve başka bir sürücü ya da bileşenin yüklenmesini gerektirmez.
Varsayılan olarak NVDA Windows 8.1'de eSpeak NG'yi kullanırken, windows 10'da [Windows OneCore](#OneCore) seslerini kullanır.
Bu sentezleyici NVDA içine gömülü olduğundan, NVDA'yı USB bellek vb medyalar üzerinden başka sistemlerde çalıştırmak için harika bir seçenektir.

ESpeak NG ile gelen her ses farklı bir dilde konuşmaktadır.
ESpeak NG tarafından desteklenen 43'den fazla dil bulunmaktadır.

Sesin duyuluşunu değiştirebilecek ayrıca bir çok konuşucu da bulunmaktadır.

### Microsoft Speech API sürüm 4 (SAPI 4) {#SAPI4}

SAPI 4, yazılım konuşma sentezleyicileri için Microsoft'un eski bir standardıdır.
NVDA, bu sentezleyicileri kullanmaya devam eden kullanıcılar için Sapi 4 desteğini sürdürmektedir.
Ancak Microsoft desteğini çekmiştir ve gerekli bileşenleri artık sağlamamaktadır.

Bu sentezleyicileri NVDA ile kullanırken, [NVDA ayarları](#NVDASettings) [konuşma kategorisi](#SpeechSettings) veya [Hızlı Sentezleyici Değiştir](#SynthSettingsRing)) bölümünden erişilebilen) mevcut sesler içinde, sisteminizde bulunan tüm SAPI 4 motorlarının sesleri yer alacaktır.

### Microsoft Speech API sürüm 5 (SAPI 5) {#SAPI5}

SAPI 5, yazılım konuşma sentezleyicileri için bir Microsoft standardıdır.
Büyük olasılıkla sisteminizin önceden kurulu bir SAPI 5 sesiyle gelmesine karşın, Birçok SAPI 5 sentezleyicisi şirketlerden satın alınabilir veya ücretsiz olarak çeşitli web sayfalarından indirilebilir.
Bu sentezleyicileri NVDA ile kullanırken, [NVDA ayarları](#NVDASettings) [konuşma kategorisinden](#SpeechSettings) veya [Hızlı Sentezleyici Değiştir](#SynthSettingsRing)) bölümünden erişilebilen) mevcut sesler içinde, sisteminizde bulunan tüm SAPI 5 motorlarının sesleri yer alacaktır.

### Microsoft Konuşma Platformu (Microsoft Speech Platform) {#MicrosoftSpeechPlatform}

Microsoft Konuşma Platformu normalde sunucu tabanlı konuşma uygulamaları geliştirilmesinde kullanılan bir çok dili destekleyen sesler sağlamaktadır.
Bu sesler NVDA tarafından da kullanılabilmektedir.

Bu sesleri kullanabilmek için iki bileşeni indirip kurmanız gerekmektedir:

* [Microsoft Speech Platform - Runtime (Version 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime Languages (Version 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * Bu sayfa, konuşma tanıma ve konuşma sentezlemeyle ilgili birçok dosyayı içermektedir.
 İstediğiniz dil ve seslerle ilgili konuşma sentezleme (TTS) verilerini içeren dosyaları seçin.
 Örneğin, MSSpeech_TTS_en-US_ZiraPro.msi adlı dosya, ABD İngilizcesi konuşan bir sestir.

### Windows OneCore Sesleri {#OneCore}

Windows 10 ve sonraki windows sürümleri "OneCore" ya da "mobile" sesler olarak bilinen yeni sesler içerir.
Bir çok dil için sesler mevcuttur, dahası Sapi 5 kullanan önceki Microsoft seslerine kıyasla daha hızlı tepki vermektedirler.
Windows 10 ve sonraki windows sürümlerinde, NVDA varsayılan olarak Windows OneCore seslerini kullanır ([[eSpeak NG](#eSpeakNG) diğer sürümlerde kullanılır).

Yeni Windows OneCore sesleri eklemek için, Windows sistem ayarlarında "Konuşma Ayarları"na gidin.
"Ses ekle" seçeneğini kullanın ve istediğiniz dili arayın.
Birçok dil birden çok aksan içerir.
"Birleşik Krallık" ve "Avustralya" İngilizce aksanlardan ikisidir.
"Fransa", "Kanada" ve "İsviçre", mevcut Fransızca aksanlardır.
Farklı aksanlara  sahip dili (İngilizce veya Fransızca gibi) arayın, ardından aksanı listede bulun.
İstediğiniz dilleri seçin ve eklemek için "ekle" düğmesini kullanın.
Ekledikten sonra NVDA'yı yeniden başlatın.

Lütfen [kullanılabilen sesler ve yükleme talimatları](https://support.microsoft.com/en-us/windows/appendix-a-supported-languages-and-voices-4486e345-7730-53da-fcfe-55cc64300f01) sayfasına bakın.

## Desteklenen braille ekranlar {#SupportedBrailleDisplays}

Bu bölümde NVDA tarafından desteklenen braille ekran bilgileri yer almaktadır.

### arka planda otomatik algılama işlevini destekleyen ekranlar {#AutomaticDetection}

NVDA, USB veya bluetooth üzerinden, arka planda otomatik olarak birçok braille ekranı  algılayabilir.
Bu sonuca, [Braille Ayarları iletişim kutusundan](#BrailleSettings) braille ekran olarak otomatik seçeneğini tercih ederek ulaşılabilir.
Bu seçenek varsayılan olarak seçilidir.

Aşağıdaki ekranlar otomatik algılama işlevini destekler.

* Handy Tech displays
* Baum/Humanware/APH/Orbit braille displays
* HumanWare Brailliant BI/B series
* HumanWare BrailleNote
* SuperBraille
* Optelec ALVA 6 series
* HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille Series
* Eurobraille Esys/Esytime/Iris displays
* Nattiq nBraille displays
* Seika Notetaker: MiniSeika (16, 24 cells), V6, and V6Pro (40 cells)
* Tivomatic Caiku Albatross 46/80 ekranlar
* Standart HID Braille protokolünü destekleyen herhangi bir Ekran

### Freedom Scientific Focus/PAC Mate Serisi {#FreedomScientificFocus}

USB veya bluetooth ile bağlandıklarında, [Freedom Scientific](https://www.freedomscientific.com/) tarafından üretilen tüm Focus ve PAC Mate ekranlar desteklenmektedir.
Freedom Scientific Braille Ekran sürücülerinin sisteminizde yüklü olması gerekecektir.
Eğer henüz bu sürücüler elinizde yoksa, bunları [Focus Blue Braille Display Sürücü sayfası](https://www2.freedomscientific.com/downloads/focus-40-blue/focus-40-14-blue-downloads.asp) adresinden edinebilirsiniz.
Bu sayfada Yalnızca Focus 40 Blue sürücülerinden bahsedilmesine karşın, bu sürücüler tüm Freedom Scientific ekranlarını desteklemektedir.

Varsayılan olarak, NVDA bu ekranları otomatik olarak bulup USB ya da bluetooth ile bağlanabilir.
Öte yandan, ekranla ilgili ayarları yaparken, "USB" ya da "Bluetooth" portlarını seçerek bağlantı tipine kendiniz karar verebilirsiniz.
Bu, örneğin ekranınıza bluetooth ile bağlanıp aynı zamanda USB üzerinden de cihazı şarj etmeye devam etmek istemeniz durumunda faydalı olabilir.
NVDA'nın otomatik braille ekran algılaması USB veya Bluetooth'la bağlı ekranı da tanıyacaktır.

Aşağıda bu ekranla kullanılabilecek tuş kombinasyonları yer almaktadır.
Lütfen bu tuşların nerede bulunacağıyla ilgili Braille ekran yardım belgelerine bakın.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu|
|---|---|
|Scroll braille display back |topRouting1 (first cell on display)|
|Scroll braille display forward |topRouting20/40/80 (last cell on display)|
|Scroll braille display back |leftAdvanceBar|
|Scroll braille display forward |rightAdvanceBar|
|Toggle braille tethered to |leftGDFButton+rightGDFButton|
|sol tekerlek hareketini açıp kapama |Sol tekerleğe basma|
|Sol tekerlek hareketini kullanarak geri gitme |Sol tekerlek yukarı|
|Sol tekerlek hareketini kullanarak ileri gitme |Sol tekerlek aşağı|
|sağ tekerlek hareketini açıp kapama |Sağ tekerleğe basma|
|Sağ tekerlek hareketini kullanarak geri gitme |Sağ tekerlek yukarı|
|Sağ tekerlek hareketini kullanarak ileri gitme |Sağ tekerlek aşağı|
|imleci parmağın üzerinde bulunduğu Braille hücresine taşıma |hücre üzerindeki braille iğnesi|
|şift+tab key |brailleSpaceBar+dot1+dot2|
|tab key |brailleSpaceBar+dot4+dot5|
|upArrow key |brailleSpaceBar+dot1|
|downArrow key |brailleSpaceBar+dot4|
|Control+leftArrow key |brailleSpaceBar+dot2|
|control+rightArrow key |brailleSpaceBar+dot5|
|leftArrow |brailleSpaceBar+dot3|
|rightArrow key |brailleSpaceBar+dot6|
|home key |brailleSpaceBar+dot1+dot3|
|end key |brailleSpaceBar+dot4+dot6|
|control+home key |brailleSpaceBar+dot1+dot2+dot3|
|control+end key |brailleSpaceBar+dot4+dot5+dot6|
|alt key |brailleSpaceBar+dot1+dot3+dot4|
|alt+tab key |brailleSpaceBar+dot2+dot3+dot4+dot5|
|alt+şift+tab key |brailleSpaceBar+dot1+dot2+dot5+dot6|
|windows+tab key |brailleSpaceBar+dot2+dot3+dot4|
|escape key |brailleSpaceBar+dot1+dot5|
|windows key |brailleSpaceBar+dot2+dot4+dot5+dot6|
|space key |brailleSpaceBar|
|Toggle control key |brailleSpaceBar+dot3+dot8|
|Toggle alt key |brailleSpaceBar+dot6+dot8|
|Toggle windows key |brailleSpaceBar+dot4+dot8|
|Toggle NVDA key |brailleSpaceBar+dot5+dot8|
|Toggle şift key |brailleSpaceBar+dot7+dot8|
|Toggle control and şift keys |brailleSpaceBar+dot3+dot7+dot8|
|Toggle alt and şift keys |brailleSpaceBar+dot6+dot7+dot8|
|Toggle windows and şift keys |brailleSpaceBar+dot4+dot7+dot8|
|Toggle NVDA and şift keys |brailleSpaceBar+dot5+dot7+dot8|
|Toggle control and alt keys |brailleSpaceBar+dot3+dot6+dot8|
|Toggle control, alt, and şift keys |brailleSpaceBar+dot3+dot6+dot7+dot8|
|windows+d key (minimize all applications) |brailleSpaceBar+dot1+dot2+dot3+dot4+dot5+dot6|
|Report Current Line |brailleSpaceBar+dot1+dot4|
|NVDA menu |brailleSpaceBar+dot1+dot3+dot4+dot5|

For newer Focus models that contain rocker bar keys (focus 40, focus 80 and focus blue):

| Name |Key|
|---|---|
|Move braille display to previous line |leftRockerBarUp, rightRockerBarUp|
|Move braille display to next line |leftRockerBarDown, rightRockerBarDown|

For Focus 80 only:

| Name |Key|
|---|---|
|Scroll braille display back |leftBumperBarUp, rightBumperBarUp|
|Scroll braille display forward |leftBumperBarDown, rightBumperBarDown|

<!-- KC:endInclude -->

### Optelec ALVA 6 serisi/protokol dönüştürücü {#OptelecALVA}

USB veya bluetooth ile bağlandıklarında, [Optelec](https://www.optelec.com/) tarafından üretilen ALVA BC640 ve BC680 ekranlarının her ikisi de desteklenmektedir.
Alternatif olarak, Braille Voyager gibi eski bir Optelec ekranı da Optelec tarafından sağlanan protokol dönüştürücüyü kullanarak bağlayabilirsiniz.
Bu ekranları kullanmak için belirli bir sürücüye gereksiniminiz bulunmamaktadır.
Yalnızca ekranı takın ve kullanmak için NVDA'yı ayarlayın.

Not: NVDA, ALVA Bluetooth yardımcı programı kullanılarak eşleştirildiği zaman Bluetooth üzerinden ALVA BC6 ekranı kullanamayabilir.
Bu program üzerinden eşleştirme yaptığınızda ve NVDA cihazınızı algılayamazsa, ALVA ekranınızı Windows bluetooth ayarlarını kullanarak eşleştirmenizi tavsiye ederiz.

Not: Bu ekranların bazılarında braille klavye olmasının yanında, braille metin çevirisi de varsayılan olarak bu ekranlar tarafından yapılır.
Dolayısıyla, varsayılan durumda NVDA'nın braille giriş sistemi, mesela girdi tablosu ayarı bu ekranları etkilemez.
Son sürüm üretici yazılımıyla gelen ALVA ekranlar için, bir girdi hareketiyle bu HID klavye simülasyonunu devre dışı bırakmak mümkündür.

Aşağıda bu ekranla kullanılabilecek tuş kombinasyonları yer almaktadır.
Lütfen bu tuşların nerede bulunacağıyla ilgili Braille ekran yardım belgelerine bakın.
<!-- KC:beginInclude -->

| Ad |Kısayol Tuşu|
|---|---|
|Scroll braille display back |t1, etouch1|
|Braille ekran önceki satır |t2|
|Move to current focus |t3|
|Braille ekran sonraki satır |t4|
|Scroll braille display forward |t5, etouch3|
|Odağı braille konumuna taşı |routing|
|braille hücre altındaki metin biçimlendirmesini bildir |secondary routing|
|HID klavye simülasyonunu açıp kapama |t1+spEnter|
|Move to top line in review |t1+t2|
|Move to bottom line in review |t4+t5|
|Toggle braille tethered to |t1+t3|
|Report title |etouch2|
|Report status bar |etouch4|
|şift+tab tuşu |sp1|
|alt tuşu |sp2, alt|
|esc tuşu |sp3|
|tab tuşu |sp4|
|Yukarı ok tuşu |spUp|
|Aşağı ok tuşu |spDown|
|Sol ok tuşu |spLeft|
|Sağ ok tuşu |spRight|
|enter tuşu |spEnter, enter|
|Saat/tarih bilgisi |sp2+sp3|
|NVDA Menüsü |sp1+sp3|
|windows+d tuşu (Tüm uygulamaları küçült) |sp1+sp4|
|windows+b key (focus system tray) |sp3+sp4|
|windows tuşu |sp1+sp2, windows|
|alt+tab tuşu |sp2+sp4|
|control+home key |t3+spUp|
|control+end key |t3+spDown|
|home key |t3+spLeft|
|end key |t3+spRight|
|control key |control|

<!-- KC:endInclude -->

### Handy Tech Displays {#HandyTech}

NVDA USB veya bluetooth ile bağlandıklarında [Handy Tech](https://www.handytech.de/) tarafından üretilen çoğu braille ekranı destekler.
Bazı daha eski USB ekranlar için Handy Tech sürücülerini sisteminize yüklemeniz gerekecektir.

Aşağıdaki ekranlar için anında destek sunulmaz, ancak [Handy Tech evrensel sürücüsü](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) ve NVDA add-on aracılığıyla kullanılabilir:

* Braillino
* Bookworm
* Modular displays with firmware version 1.13 or lower. Please note that the firmware of this displays can be updated.

Aşağıda Handy Tech ekranlarla kullanılabilecek tuş kombinasyonları yer almaktadır.
Lütfen bu tuşların nerede bulunacağıyla ilgili Braille ekran yardım belgelerine bakın.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu|
|---|---|
|Braille ekranı geri kaydırma |Sol, Yukarı, b3|
|Braille ekranı ileri kaydırma |Sağ, Aşağı, b6|
|Braille ekranı önceki satıra götürme |b4|
|Braille ekranı sonraki satıra götürme |b5|
|imleci parmağın üzerinde bulunduğu Braille hücresine taşıma |hücre üzerindeki braille iğnesi|
|Şift+tab tuşu |eskeyp tuşu, left triple action key up+down|
|alt tuşu |b2+b4+b5|
|eskeyp tuşu |b4+b6|
|tab tuşu |enter, right triple action key up+down|
|enter tuşu |eskeyp+enter, left+right triple action key up+down, joystickAction|
|Yukarı yön tuşu |joystickUp|
|Aşağı yön tuşu |joystickDown|
|SolOk tuşu |joystickLeft|
|SağOk tuşu |joystickRight|
|NVDA Menüsü |b2+b4+b5+b6|
|Toggle braille tethered to |b2|
|Toggle the braille cursor |b1|
|Toggle focus context presentation |b7|
|Toggle braille input |space+b1+b3+b4 (space+capital B)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

[MDV](https://www.mdvbologna.it/) tarafından üretilen Lilli braille ekranı desteklenmektedir.
Bu ekranı kullanmak için belirli bir sürücüye gereksiniminiz bulunmamaktadır.
Yalnızca ekranı takın ve kullanmak için NVDA'yı ayarlayın.

Bu ekran henüz NVDA'nın otomatik arka plan braille görüntü algılama işlevini desteklememektedir.

Aşağıda bu ekranla kullanılabilecek tuş kombinasyonları yer almaktadır.
Lütfen bu tuşların nerede bulunacağıyla ilgili Braille ekran yardım belgelerine bakın.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu|
|---|---|
|Braille ekranı geri kaydır |LF|
|Braille ekranı ileri kaydır |RG|
|Braille ekran önceki satır |UP|
|Braille ekran sonraki satır |DN|
|Odağı braille konumuna taşı |route|
|şift+tab tuşu |SLF|
|tab tuşu |SRG|
|alt+tab tuşu |SDN|
|alt+şift+tab tuşu |SUP|

<!-- KC:endInclude -->

### Baum/Humanware/APH Braille/Orbit Ekranlar {#Baum}

Birçok [Baum](https://www.baum.de/cms/en/), [HumanWare](https://www.humanware.com/), [APH](https://www.aph.org/) ve [Orbit](https://www.orbitresearch.com/) ekran USB veya Bluetooth ile bağlandıklarında desteklenmektedir.
Bunlardan bazıları şunlardır:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

henüz test edilmemelerine karşın, Baum tarafından desteklenen başka ekranlar da NVDA ile çalışabilir.

If connecting via USB to displays which do not use HID, you must first install the USB drivers provided by the manufacturer.
The VarioUltra and Pronto! use HID.
The Refreshabraille and Orbit Reader 20 can use HID if configured appropriately.

The USB serial mode of the Orbit Reader 20 is currently only supported in Windows 10 and later.
USB HID should generally be used instead.

Following are the key assignments for these displays with NVDA.
Please see your display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu|
|---|---|
|Braille ekranı geri kaydırma |`d2`|
|Braille ekranı ileri kaydırma |`d5`|
|Braille ekranı önceki satıra götürme |`d1`|
|Braille ekranı sonraki satıra götürme |`d3`|
|imleci parmağın üzerinde bulunduğu Braille hücresine taşıma |`hücre üzerindeki braille iğnesi`|
|`şift+tab` tuşu |`space+dot1+dot3`|
|`tab` tuşu |`space+dot4+dot6`|
|`alt` tuşu |`space+dot1+dot3+dot4` (`space+m`)|
|`escape` tuşu |`space+dot1+dot5` (`space+e`)|
|`windows` tuşu |`space+dot3+dot4`|
|`alt+tab` tuşu |`space+dot2+dot3+dot4+dot5` (`space+t`)|
|NVDA Menü |`space+dot1+dot3+dot4+dot5` (`space+n`)|
|`windows+d` tuşu (tüm uygulamaları simge durumuna küçült) |`space+dot1+dot4+dot5` (`space+d`)|
|Tümünü oku |`space+dot1+dot2+dot3+dot4+dot5+dot6`|

Kumanda kolu olan ekranlar için:

| Ad |Kısayol tuşu|
|---|---|
|Yukarı Yön Tuşu |yukarı|
|Aşağı Yön Tuşu |aşağı|
|sol Yön Tuşu |sol|
|sağ Yön Tuşu |sağ|
|Enter tuşu |seç|

<!-- KC:endInclude -->

### hedo ProfiLine USB {#HedoProfiLine}

Hedo ProfiLine USB, [hedo Reha-Technik](https://www.hedo.de/) desteklenmektedir.
Öncelikle üretici tarafından sağlanan USB sürücülerini kurmalısınız.

Bu ekran henüz NVDA'nın otomatik arka plan braille görüntü algılama işlevini desteklememektedir.

Aşağıda braille ekranı NVDA ile hangi tuşlarla kullanabileceğinizi bulabilirsiniz.
Tuşların yeri ve tarifi için Braille ekranın dokümantasyonunu inceleyin.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu|
|---|---|
|Braille geri kaydır |K1|
|Braille ileri kaydır |K3|
|Braille Önceki satır |B2|
|Braille Sonraki satır |B5|
|Braille konumuna taşı |routing|
|braille imlecin neyi takip edeceğini değiştir |K2|
|Hepsini oku |B6|

<!-- KC:endInclude -->

### hedo MobilLine USB {#HedoMobilLine}

hedo MobilLine USB, [hedo Reha-Technik](https://www.hedo.de/) desteklenmektedir.
Öncelikle üretici tarafından sağlanan USB sürücülerini kurmalısınız.

Bu ekran henüz NVDA'nın otomatik arka plan braille görüntü algılama işlevini desteklememektedir.

Aşağıda braille ekranı NVDA ile hangi tuşlarla kullanabileceğinizi bulabilirsiniz.
Tuşların yeri ve tarifi için Braille ekranın dokümantasyonunu inceleyin.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu|
|---|---|
|Braille geri kaydır |K1|
|Braille ileri kaydır |K3|
|Braille Önceki satır |B2|
|Braille Sonraki satır |B5|
|Braille konumuna taşı |routing|
|braille imlecin neyi takip edeceğini değiştir |K2|
|Hepsini oku |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant BI/B Serisi / BrailleNote Touch {#HumanWareBrailliant}

Brailliant BI ve B serisi braille ekranlar, [HumanWare](https://www.humanware.com/), BI 14, BI 32, BI 20X, BI 40, BI 40X ve B 80 dahil, USB ya da bluetooth ile bağlandığında desteklenmektedir.
USB bağlantısını ve HumanWare protokolünü kullanıyorsanız, öncelikle üretici tarafından sağlanan USB sürücülerini kurmalısınız.
OpenBraille protokolü için USB sürücüleri gerekmez.

Ek olarak aşağıdaki aygıtlar da desteklenir (ve herhangi bir özel sürücünün yüklenmesini gerektirmez):

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Aşağıda Brailliant BI/B ve BrailleNote touch braille ekranları NVDA ile hangi tuşlarla kullanabileceğinizi bulabilirsiniz.
Tuşların yeri ve tarifi için Braille ekranın dokümantasyonunu inceleyin.

#### Tüm modeller için tuş atamaları {#HumanWareBrailliantKeyAssignmentForAllModels}

<!-- KC:beginInclude -->

| Ad |Kısayol tuşu|
|---|---|
|Braille ekranı geri kaydır |sol|
|Braille ekranı İLERİ kaydır |SAĞ|
|braille ekranı önceki satıra taşı |yukarı|
|braille ekranı sonraki satıra taşı |aşağı|
|İmleci braille konumuna taşı |routing|
|Braille'in takip ettiği imleci değiştir |up+down|
|yukarı yön tuşu |space+dot1|
|aşağı yön tuşu |space+dot4|
|sol yön tuşu |space+dot3|
|sağ yön tuşu |space+dot6|
|şift+tab tuşu |space+dot1+dot3|
|tab tuşu |space+dot4+dot6|
|alt tuşu |space+dot1+dot3+dot4 (space+m)|
|escape tuşu |space+dot1+dot5 (space+e)|
|enter tuşu |dot8|
|windows tuşu |space+dot3+dot4|
|alt+tab tuşu |space+dot2+dot3+dot4+dot5 (space+t)|
|NVDA Menu |space+dot1+dot3+dot4+dot5 (space+n)|
|windows+d key (minimize all applications) |space+dot1+dot4+dot5 (space+d)|
|Say all |space+dot1+dot2+dot3+dot4+dot5+dot6|

<!-- KC:endInclude -->

#### Brailliant BI 32, BI 40 ve B 80 için tuş atamaları {#HumanWareBrailliantKeyAssignmentForBI32BI40AndB80}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|NVDA Menu |c1+c3+c4+c5 (command n)|
|windows+d key (minimize all applications) |c1+c4+c5 (command d)|
|Hepsini oku |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Brailliant BI 14 için tuş atamalar {#HumanWareBrailliantKeyAssignmentForBI14}

<!-- KC:beginInclude -->

| Ad |Tuş|
|---|---|
|up arrow key |joystick up|
|down arrow key |joystick down|
|left arrow key |joystick left|
|right arrow key |joystick right|
|enter key |joystick action|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille Serileri {#Hims}

USB ya da bluetooth üzerinden bağlandıklarında, NVDA [Hims](https://www.hims-inc.com/) tarafından üretilen Braille Sense, Braille EDGE, Smart Beetle ve Sync Braille kabartma ekranları destekler. 
USB üzerinden bağlıyorsanız, sisteminize [HIMS tarafından dağıtılan USB sürücülerini](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip) sayfasından indirip kurmanız gerekir.

Aşağıda braille ekranı NVDA ile hangi tuşlarla kullanabileceğinizi bulabilirsiniz.
Tuşların yeri ve tarifi için Braille ekranın dokümantasyonunu inceleyin.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu|
|---|---|
|Route to braille cell |routing|
|Scroll braille display back |leftSideScrollUp, rightSideScrollUp, leftSideScroll|
|Scroll braille display forward |leftSideScrollDown, rightSideScrollDown, rightSideScroll|
|Move braille display to previous line |leftSideScrollUp+rightSideScrollUp|
|Move braille display to next line |leftSideScrollDown+rightSideScrollDown|
|Move to previous line in review |rightSideUpArrow|
|Move to next line in review |rightSideDownArrow|
|Move to previous character in review |rightSideLeftArrow|
|Move to next character in review |rightSideRightArrow|
|Move to current focus |leftSideScrollUp+leftSideScrollDown, rightSideScrollUp+rightSideScrollDown, leftSideScroll+rightSideScroll|
|control key |smartbeetle:f1, brailleedge:f3|
|windows key |f7, smartbeetle:f2|
|alt key |dot1+dot3+dot4+space, f2, smartbeetle:f3, brailleedge:f4|
|şift key |f5|
|insert key |dot2+dot4+space, f6|
|applications key |dot1+dot2+dot3+dot4+space, f8|
|capsLock key |dot1+dot3+dot6+space|
|tab key |dot4+dot5+space, f3, brailleedge:f2|
|şift+alt+tab key |f2+f3+f1|
|alt+tab key |f2+f3|
|şift+tab key |dot1+dot2+space|
|end key |dot4+dot6+space|
|control+end key |dot4+dot5+dot6+space|
|home key |dot1+dot3+space, smartbeetle:f4|
|control+home key |dot1+dot2+dot3+space|
|alt+f4 key |dot1+dot3+dot5+dot6+space|
|leftArrow key |dot3+space, leftSideLeftArrow|
|control+şift+leftArrow key |dot2+dot8+space+f1|
|control+leftArrow key |dot2+space|
|şift+alt+leftArrow key |dot2+dot7+f1|
|`alt+leftArrow` key |`dot2+dot7`|
|rightArrow key |dot6+space, leftSideRightArrow|
|control+şift+rightArrow key |dot5+dot8+space+f1|
|control+rightArrow key |dot5+space|
|şift+alt+rightArrow key |dot5+dot7+f1|
|`alt+rightArrow` key |`dot5+dot7`|
|pageUp key |dot1+dot2+dot6+space|
|control+pageUp key |dot1+dot2+dot6+dot8+space|
|upArrow key |dot1+space, leftSideUpArrow|
|control+şift+upArrow key |dot2+dot3+dot8+space+f1|
|control+upArrow key |dot2+dot3+space|
|şift+alt+upArrow key |dot2+dot3+dot7+f1|
|`alt+upArrow key` |`dot2+dot3+dot7`|
|şift+upArrow key |leftSideScrollDown+space|
|pageDown key |dot3+dot4+dot5+space|
|control+pageDown key |dot3+dot4+dot5+dot8+space|
|downArrow key |dot4+space, leftSideDownArrow|
|control+şift+downArrow key |dot5+dot6+dot8+space+f1|
|control+downArrow key |dot5+dot6+space|
|şift+alt+downArrow key |dot5+dot6+dot7+f1|
|`alt+downArrow key` |`dot5+dot6+dot7`|
|şift+downArrow key |space+rightSideScrollDown|
|escape key |dot1+dot5+space, f4, brailleedge:f1|
|delete key |dot1+dot3+dot5+space, dot1+dot4+dot5+space|
|f1 key |dot1+dot2+dot5+space|
|f3 key |dot1+dot4+dot8+space|
|f4 key |dot7+f3|
|windows+b key |dot1+dot2+f1|
|windows+d key |dot1+dot4+dot5+f1|
|control+insert key |smartbeetle:f1+rightSideScroll|
|alt+insert key |smartbeetle:f3+rightSideScroll|

<!-- KC:endInclude -->

### Seika Braille Displays {#Seika}

Nippon Telesoft'un aşağıdaki Seika Braille ekranları, farklı işlevlere sahip iki grupta desteklenir:

* [Seika Version 3, 4, and 5 (40 cells), Seika80 (80 cells)](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 cells), V6, and V6Pro (40 cells)](#SeikaNotetaker)

Ekranlar hakkında daha fazla bilgiyi [Demo ve Sürücü İndirme sayfası](https://en.seika-braille.com/down/index.html) üzerinden edinebilirsiniz.

#### Seika Versiyon 3, 4 ve 5 (40 hücre), Seika80 (80 hücre) {#SeikaBrailleDisplays}

* Bu ekranlar henüz NVDA'nın otomatik arka plan braille ekran algılama işlevini desteklememektedir.
* Manuel olarak yapılandırmak için "Seika Braille Ekranları"nı seçin
* Seika v3/4/5/80'i kullanmadan önce bir aygıt sürücüsü kurulmalıdır.
[üretici tarafından sağlanan](https://en.seika-braille.com/down/index.html) sürücüler.

Seika Braille Ekran tuş atamaları aşağıdaki gibidir.
Tuşların yeri ve tarifi için Braille ekranın dokümantasyonunu inceleyin.
<!-- KC:beginInclude -->

| Ad |Kısayol tuşu|
|---|---|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to previous line |b3|
|Move braille display to next line |b4|
|Toggle braille tethered to |b5|
|Say all |b6|
|tab |b1|
|şift+tab |b2|
|alt+tab |b1+b2|
|NVDA Menu |left+right|
|Route to braille cell |routing|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 hücre), V6 ve V6Pro (40 hücre) {#SeikaNotetaker}

* NVDA'nın otomatik arka plan braille ekranı algılama işlevi, USB ve Bluetooth aracılığıyla desteklenir.
* Yapılandırmak için "Seika Notetaker" veya "auto" öğesini seçin.
* Seika Notetaker braille ekranı kullanırken ek bir  sürücü gerekmez.

Seika Notetaker tuş atamaları aşağıdaki gibidir.
Bu tuşların nerede bulunabileceğinin açıklamaları için lütfen ekranın belgelerine bakın.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Say all |space+Backspace|
|NVDA Menu |Left+Right|
|Move braille display to previous line |LJ up|
|Move braille display to next line |LJ down|
|Toggle braille tethered to |LJ center|
|tab |LJ right|
|şift+tab |LJ left|
|upArrow key |RJ up|
|downArrow key |RJ down|
|leftArrow key |RJ left|
|rightArrow key |RJ right|
|Route to braille cell |routing|
|şift+upArrow key |Space+RJ up, Backspace+RJ up|
|şift+downArrow key |Space+RJ down, Backspace+RJ down|
|şift+leftArrow key |Space+RJ left, Backspace+RJ left|
|şift+rightArrow key |Space+RJ right, Backspace+RJ right|
|enter key |RJ center, dot8|
|escape key |Space+RJ center|
|windows key |Backspace+RJ center|
|space key |Space, Backspace|
|backspace key |dot7|
|pageup key |space+LJ right|
|pagedown key |space+LJ left|
|home key |space+LJ up|
|end key |space+LJ down|
|control+home key |backspace+LJ up|
|control+end key |backspace+LJ down|

### Papenmeier BRAILLEX Yeni Modelleri {#Papenmeier}

Aşağıdaki Braille ekranlar desteklenmektedir: 

* BRAILLEX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB and bluetooth)
* BRAILLEX Live 20, BRAILLEX Live and BRAILLEX Live Plus (USB and bluetooth)

Bu ekranlar henüz NVDA'nın otomatik arka plan braille görüntü algılama işlevini desteklememektedir.
There is an option in the display's USB driver which can cause an issue with loading the display.
Please try the following:

1. Please make sure that you have installed the [latest driver](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Open the Windows Device Manager.
1. Scroll down the list to "USB Controllers" or "USB Devices".
1. Select "Papenmeier Braillex USB Device".
1. Open the properties and switch to the "Advanced" tab.
Sometimes the "Advanced" tab doesn't appear.
If this is the case, disconnect the braille display from the computer, exit NVDA, wait a moment and reconnect the braille display.
Repeat this 4 to 5 times if necessary.
If the "Advanced" tab is still not displayed, please restart the computer.
1. Disable the "Load VCP" option.

Most devices have an Easy Access Bar (EAB) that allows intuitive and fast operation.
The EAB can be moved in four directions where generally each direction has two switches.
The C and Live series are the only exceptions to this rule.

The c-series and some other displays have two routing rows whereby the upper row is used to report formatting information.
Holding one of the upper routing keys and pressing the EAB on c-series devices emulates the second switch state.
The live series displays have one routing row only and the EAB has one step per direction.
The second step may be emulated by pressing one of the routing keys and pressing the EAB in the corresponding direction.
Pressing and holding the up, down, right and left keys (or EAB) causes the corresponding action to be repeated.

Generally, the following keys are available on these braille displays:

| Name |Key|
|---|---|
|l1 |Left front key|
|l2 |Left rear key|
|r1 |Right front key|
|r2 |Right rear key|
|up |1 Step up|
|up2 |2 Steps up|
|left |1 Step left|
|left2 |2 Steps left|
|right |1 Step right|
|right2 |2 Steps right|
|dn |1 Step down|
|dn2 |2 Steps down|

Following are the Papenmeier command assignments for NVDA:
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to previous line |up|
|Move braille display to next line |dn|
|Route to braille cell |routing|
|Report current character in review |l1|
|Activate current navigator object |l2|
|Toggle braille tethered to |r2|
|Report title |l1+up|
|Report Status Bar |l2+down|
|Move to containing object |up2|
|Move to first contained object |dn2|
|Move to previous object |left2|
|Move to next object |right2|
|Report text formatting under braille cell |upper routing row|

<!-- KC:endInclude -->

The Trio model has four additional keys which are in front of the braille keyboard.
These are (ordered from left to right):

* left thumb key (lt)
* space
* space
* right thumb key (rt)

Currently, the right thumb key is not in use.
The inner keys are both mapped to space.

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|escape key |space with dot 7|
|upArrow key |space with dot 2|
|leftArrow key |space with dot 1|
|rightArrow key |space with dot 4|
|downArrow |space with dot 5|
|control key |lt+dot2|
|alt key |lt+dot3|
|control+escape key |space with dot 1 2 3 4 5 6|
|tab key |space with dot 3 7|

<!-- KC:endInclude -->

### Papenmeier Braille BRAILLEX Older Models {#PapenmeierOld}

The following Braille displays are supported: 

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Note that these displays can only be connected via a serial port.
Due to this, these displays do not support NVDA's automatic background braille display detection functionality.
You should select the port to which the display is connected after you have chosen this driver in the [Select Braille Display](#SelectBrailleDisplay) dialog.

Some of these devices have an Easy Access Bar (EAB) that allows intuitive and fast operation.
The EAB can be moved in four directions where generally each direction has two switches.
Pressing and holding the up, down, right and left keys (or EAB) causes the corresponding action to be repeated.
Older devices do not have an EAB; front keys are used instead.

Generally, the following keys are available on braille displays:

| Name |Key|
|---|---|
|l1 |Left front key|
|l2 |Left rear key|
|r1 |Right front key|
|r2 |Right rear key|
|up |1 Step up|
|up2 |2 Steps up|
|left |1 Step left|
|left2 |2 Steps left|
|right |1 Step right|
|right2 |2 Steps right|
|dn |1 Step down|
|dn2 |2 Steps down|

Following are the Papenmeier command assignments for NVDA:

<!-- KC:beginInclude -->
Devices with EAB:

| Name |Key|
|---|---|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to previous line |up|
|Move braille display to next line |dn|
|Route to braille cell |routing|
|Report current character in review |l1|
|Activate current navigator object |l2|
|Report title |l1up|
|Report Status Bar |l2down|
|Move to containing object |up2|
|Move to first contained object |dn2|
|Move to next object |right2|
|Move to previous object |left2|
|Report text formatting under braille cell |upper routing strip|

BRAILLEX Tiny:

| Name |Key|
|---|---|
|Report current character in review |l1|
|Activate current navigator object |l2|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to previous line |up|
|Move braille display to next line |dn|
|Toggle braille tethered to |r2|
|Move to containing object |r1+up|
|Move to first contained object |r1+dn|
|Move to previous object |r1+left|
|Move to next object |r1+right|
|Report text formatting under braille cell |upper routing strip|
|Report title |l1+up|
|Report status bar |l2+down|

BRAILLEX 2D Screen:

| Name |Key|
|---|---|
|Report current character in review |l1|
|Activate current navigator object |l2|
|Toggle braille tethered to |r2|
|Report text formatting under braille cell |upper routing strip|
|Move braille display to previous line |up|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to next line |dn|
|Move to next object |left2|
|Move to containing object |up2|
|Move to first contained object |dn2|
|Move to previous object |right2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

NVDA supports the BrailleNote notetakers from [Humanware](https://www.humanware.com) when acting as a display terminal for a screen reader.
The following models are supported:

* BrailleNote Classic (serial connection only)
* BrailleNote PK (Serial and bluetooth connections)
* BrailleNote MPower (Serial and bluetooth connections)
* BrailleNote Apex (USB and Bluetooth connections)

For BrailleNote Touch, please refer to  the [Brailliant BI Series / BrailleNote Touch](#HumanWareBrailliant) section.

Except for BrailleNote PK, both braille (BT) and QWERTY (QT) keyboards are supported.
For BrailleNote QT, PC keyboard emulation isn't supported.
You can also enter braille dots using the QT keyboard.
Please check the braille terminal section of the BrailleNote manual guide for details.

If your device supports more than one type of connection, when connecting your BrailleNote to NVDA, you must set the braille terminal port in braille terminal options.
Please check the BrailleNote manual for details.
In NVDA, you may also need to set the port in the [Select Braille Display](#SelectBrailleDisplay) dialog.
If you are connecting via USB or bluetooth, you can set the port to "Automatic", "USB" or "Bluetooth", depending on the available choices.
If connecting using a legacy serial port (or a USB to serial converter) or if none of the previous options appear, you must explicitly choose the communication port to be used from the list of hardware ports.

Before connecting your BrailleNote Apex using its USB client interface, you must install the drivers provided by HumanWare.

On the BrailleNote Apex BT, you can use the scroll wheel located between dots 1 and 4 for various NVDA commands.
The wheel consists of four directional dots, a center click button, and a wheel that spins clockwise or counterclockwise.

Following are the BrailleNote command assignments for NVDA.
Please check your BrailleNote's documentation to find where these keys are located.

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |back|
|Scroll braille display forward |advance|
|Move braille display to previous line |previous|
|Move braille display to next line |next|
|Route to braille cell |routing|
|NvDA menu |space+dot1+dot3+dot4+dot5 (space+n)|
|Toggle braille tethered to |previous+next|
|Up arrow key |space+dot1|
|Down arrow key |space+dot4|
|Left Arrow key |space+dot3|
|Right arrow key |space+dot6|
|Page up key |space+dot1+dot3|
|Page down key |space+dot4+dot6|
|Home key |space+dot1+dot2|
|End key |space+dot4+dot5|
|Control+home keys |space+dot1+dot2+dot3|
|Control+end keys |space+dot4+dot5+dot6|
|Space key |space|
|Enter |space+dot8|
|Backspace |space+dot7|
|Tab key |space+dot2+dot3+dot4+dot5 (space+t)|
|şift+tab keys |space+dot1+dot2+dot5+dot6|
|Windows key |space+dot2+dot4+dot5+dot6 (space+w)|
|Alt key |space+dot1+dot3+dot4 (space+m)|
|Toggle input help |space+dot2+dot3+dot6 (space+lower h)|

Following are commands assigned to BrailleNote QT when it is not in braille input mode.

| Name |Key|
|---|---|
|NvDA menu |read+n|
|Up arrow key |upArrow|
|Down arrow key |downArrow|
|Left Arrow key |leftArrow|
|Right arrow key |rightArrow|
|Page up key |function+upArrow|
|Page down key |function+downArrow|
|Home key |function+leftArrow|
|End key |function+rightArrow|
|Control+home keys |read+t|
|Control+end keys |read+b|
|Enter key |enter|
|Backspace key |backspace|
|Tab key |tab|
|şift+tab keys |şift+tab|
|Windows key |read+w|
|Alt key |read+m|
|Toggle input help |read+1|

Following are commands assigned to the scroll wheel:

| Name |Key|
|---|---|
|Up arrow key |upArrow|
|Down arrow key |downArrow|
|Left Arrow key |leftArrow|
|Right arrow key |rightArrow|
|Enter key |center button|
|Tab key |scroll wheel clockwise|
|şift+tab keys |scroll wheel counterclockwise|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA supports EcoBraille displays from [ONCE](https://www.once.es/).
The following models are supported:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

In NVDA, you can set the serial port to which the display is connected in the [Select Braille Display](#SelectBrailleDisplay) dialog.
These displays do not support NVDA's automatic background braille display detection functionality.

Following are the key assignments for EcoBraille displays.
Please see the [EcoBraille documentation](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) for descriptions of where these keys can be found.

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |T2|
|Scroll braille display forward |T4|
|Move braille display to previous line |T1|
|Move braille display to next line |T5|
|Route to braille cell |Routing|
|Activate current navigator object |T3|
|Switch to next review mode |F1|
|Move to containing object |F2|
|Switch to previous review mode |F3|
|Move to previous object |F4|
|Report current object |F5|
|Move to next object |F6|
|Move to focus object |F7|
|Move to first contained object |F8|
|Move System focus or caret to current review position |F9|
|Report review cursor location |F0|
|Toggle braille tethered to |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

The SuperBraille device, mostly available in Taiwan, can be connected to by either USB or serial.
As the SuperBraille does not have any physical typing keys or scrolling buttons, all input must be performed via a standard computer keyboard.
Due to this, and to maintain compatibility with other screen readers in Taiwan, two key bindings for scrolling the braille display have been provided:
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |numpadMinus|
|Scroll braille display forward |numpadPlus|

<!-- KC:endInclude -->

### Eurobraille displays {#Eurobraille}

The b.book, b.note, Esys, Esytime and Iris displays from Eurobraille are supported by NVDA.  
These devices have a braille keyboard with 10 keys. 
Please refer to the display's documentation for descriptions of these keys.
Of the two keys placed like a space bar, the left key is corresponding to the backspace key and the right key to the space key.

These devices are connected via USB and have one stand-alone USB keyboard. 
It is possible to enable/disable this keyboard by toggling "HID Keyboard simulation" using an input gesture.
The braille keyboard functions described directly below is when "HID Keyboard simulation" is disabled. 

#### Braille keyboard functions {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Erase the last entered braille cell or character |`backspace`|
|Translate any braille input and press the enter key |`backspace+space`|
|Toggle `NVDA` key |`dot3+dot5+space`|
|`insert` key |`dot1+dot3+dot5+space`, `dot3+dot4+dot5+space`|
|`delete` key |`dot3+dot6+space`|
|`home` key |`dot1+dot2+dot3+space`|
|`end` key |`dot4+dot5+dot6+space`|
|`leftArrow` key |`dot2+space`|
|`rightArrow` key |`dot5+space`|
|`upArrow` key |`dot1+space`|
|`downArrow` key |`dot6+space`|
|`pageUp` key |`dot1+dot3+space`|
|`pageDown` key |`dot4+dot6+space`|
|`numpad1` key |`dot1+dot6+backspace`|
|`numpad2` key |`dot1+dot2+dot6+backspace`|
|`numpad3` key |`dot1+dot4+dot6+backspace`|
|`numpad4` key |`dot1+dot4+dot5+dot6+backspace`|
|`numpad5` key |`dot1+dot5+dot6+backspace`|
|`numpad6` key |`dot1+dot2+dot4+dot6+backspace`|
|`numpad7` key |`dot1+dot2+dot4+dot5+dot6+backspace`|
|`numpad8` key |`dot1+dot2+dot5+dot6+backspace`|
|`numpad9` key |`dot2+dot4+dot6+backspace`|
|`numpadInsert` key |`dot3+dot4+dot5+dot6+backspace`|
|`numpadDecimal` key |`dot2+backspace`|
|`numpadDivide` key |`dot3+dot4+backspace`|
|`numpadMultiply` key |`dot3+dot5+backspace`|
|`numpadMinus` key |`dot3+dot6+backspace`|
|`numpadPlus` key |`dot2+dot3+dot5+backspace`|
|`numpadEnter` key |`dot3+dot4+dot5+backspace`|
|`escape` key |`dot1+dot2+dot4+dot5+space`, `l2`|
|`tab` key |`dot2+dot5+dot6+space`, `l3`|
|`şift+tab` keys |`dot2+dot3+dot5+space`|
|`printScreen` key |`dot1+dot3+dot4+dot6+space`|
|`pause` key |`dot1+dot4+space`|
|`applications` key |`dot5+dot6+backspace`|
|`f1` key |`dot1+backspace`|
|`f2` key |`dot1+dot2+backspace`|
|`f3` key |`dot1+dot4+backspace`|
|`f4` key |`dot1+dot4+dot5+backspace`|
|`f5` key |`dot1+dot5+backspace`|
|`f6` key |`dot1+dot2+dot4+backspace`|
|`f7` key |`dot1+dot2+dot4+dot5+backspace`|
|`f8` key |`dot1+dot2+dot5+backspace`|
|`f9` key |`dot2+dot4+backspace`|
|`f10` key |`dot2+dot4+dot5+backspace`|
|`f11` key |`dot1+dot3+backspace`|
|`f12` key |`dot1+dot2+dot3+backspace`|
|`windows` key |`dot1+dot2+dot4+dot5+dot6+space`|
|Toggle `windows` key |`dot1+dot2+dot3+dot4+backspace`, `dot2+dot4+dot5+dot6+space`|
|`capsLock` key |`dot7+backspace`, `dot8+backspace`|
|`numLock` key |`dot3+backspace`, `dot6+backspace`|
|`şift` key |`dot7+space`|
|Toggle `şift` key |`dot1+dot7+space`, `dot4+dot7+space`|
|`control` key |`dot7+dot8+space`|
|Toggle `control` key |`dot1+dot7+dot8+space`, `dot4+dot7+dot8+space`|
|`alt` key |`dot8+space`|
|Toggle `alt` key |`dot1+dot8+space`, `dot4+dot8+space`|
|Toggle HID Keyboard simulation |`switch1Left+joystick1Down`, `switch1Right+joystick1Down`|

<!-- KC:endInclude -->

#### b.book keyboard commands {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |`backward`|
|Scroll braille display forward |`forward`|
|Move to current focus |`backward+forward`|
|Route to braille cell |`routing`|
|`leftArrow` key |`joystick2Left`|
|`rightArrow` key |`joystick2Right`|
|`upArrow` key |`joystick2Up`|
|`downArrow` key |`joystick2Down`|
|`enter` key |`joystick2Center`|
|`escape` key |`c1`|
|`tab` key |`c2`|
|Toggle `şift` key |`c3`|
|Toggle `control` key |`c4`|
|Toggle `alt` key |`c5`|
|Toggle `NVDA` key |`c6`|
|`control+Home` key |`c1+c2+c3`|
|`control+End` key |`c4+c5+c6`|

<!-- KC:endInclude -->

#### b.note keyboard commands {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |`leftKeypadLeft`|
|Scroll braille display forward |`leftKeypadRight`|
|Route to braille cell |`routing`|
|Report text formatting under braille cell |`doubleRouting`|
|Move to next line in review |`leftKeypadDown`|
|Switch to previous review mode |`leftKeypadLeft+leftKeypadUp`|
|Switch to next review mode |`leftKeypadRight+leftKeypadDown`|
|`leftArrow` key |`rightKeypadLeft`|
|`rightArrow` key |`rightKeypadRight`|
|`upArrow` key |`rightKeypadUp`|
|`downArrow` key |`rightKeypadDown`|
|`control+home` key |`rightKeypadLeft+rightKeypadUp`|
|`control+end` key |`rightKeypadLeft+rightKeypadUp`|

<!-- KC:endInclude -->

#### Esys keyboard commands {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |`switch1Left`|
|Scroll braille display forward |`switch1Right`|
|Move to current focus |`switch1Center`|
|Route to braille cell |`routing`|
|Report text formatting under braille cell |`doubleRouting`|
|Move to previous line in review |`joystick1Up`|
|Move to next line in review |`joystick1Down`|
|Move to previous character in review |`joystick1Left`|
|Move to next character in review |`joystick1Right`|
|`leftArrow` key |`joystick2Left`|
|`rightArrow` key |`joystick2Right`|
|`upArrow` key |`joystick2Up`|
|`downArrow` key |`joystick2Down`|
|`enter` key |`joystick2Center`|

<!-- KC:endInclude -->

#### Esytime keyboard commands {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |`l1`|
|Scroll braille display forward |`l8`|
|Move to current focus |`l1+l8`|
|Route to braille cell |`routing`|
|Report text formatting under braille cell |`doubleRouting`|
|Move to previous line in review |`joystick1Up`|
|Move to next line in review |`joystick1Down`|
|Move to previous character in review |`joystick1Left`|
|Move to next character in review |`joystick1Right`|
|`leftArrow` key |`joystick2Left`|
|`rightArrow` key |`joystick2Right`|
|`upArrow` key |`joystick2Up`|
|`downArrow` key |`joystick2Down`|
|`enter` key |`joystick2Center`|
|`escape` key |`l2`|
|`tab` key |`l3`|
|Toggle `şift` key |`l4`|
|Toggle `control` key |`l5`|
|Toggle `alt` key |`l6`|
|Toggle `NVDA` key |`l7`|
|`control+home` key |`l1+l2+l3`, `l2+l3+l4`|
|`control+end` key |`l6+l7+l8`, `l5+l6+l7`|
|Toggle HID Keyboard simulation |`l1+joystick1Down`, `l8+joystick1Down`|

<!-- KC:endInclude -->

### Nattiq nBraille Displays {#NattiqTechnologies}

NVDA, USB ile bağlandığında, [Nattiq Technologies](https://www.nattiq.com/) tarafından üretilen ekranları destekler.
Windows 10 ve sonraki sürümleri, bağlandıktan sonra Braille Ekranlarını algılar, Windows'un eski sürümlerini kullanıyorsanız (Win10'un altında) USB sürücülerini yüklemeniz gerekebilir.
Bunları üreticinin web sitesinden edinebilirsiniz.

Aşağıda, NVDA ile Nattiq Technologies ekranları için temel atamalar verilmiştir.
Bu tuşların nerede bulunacağına ilişkin açıklamalar için lütfen braille ekran belgelerine bakın.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |up|
|Scroll braille display forward |down|
|Move braille display to previous line |left|
|Move braille display to next line |right|
|Route to braille cell |routing|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.com/) çok daha fazla farklı braille ekranı destekleyebilmek için kullanılan ayrı bir programdır.
bunu kullanabilmek için,[BRLTTY for Windows](https://www.brltty.com/download.html) programını yüklemeniz gerekecektir.
En son kurulum sürümünü indirip kurmalısınız. bunun adı şu biçimde olabilir: brltty-win-4.2-2.exe.
Ekranı ve kullanılacak portu ayarlarken, özellikle USB sürücüleri kullanıyorsanız ve elinizde üreticilerin sürücüleri varsa, yönergeleri yakından takip ettiğinizden emin olun.

Kabartma klavyesi bulunan ekranlar için, BRLTTY şuanda braille girişini kendisi yönetmektedir.
Dolayısıyla, NVDA'nın braille girdi tablosu ayarı bu ekranları etkilemez.

BRLTTY henüz NVDA'nın otomatik arka plan braille ekran algılama işlevini desteklememektedir.

Aşağıda NVDA için BRLTTY tuş komutları bulunmaktadır.
Lütfen [BRLTTY tuş komutları listesine](http://mielke.cc/brltty/doc/KeyBindings/) BRLTTY komutlarının braille ekran kontrollerinde nasıl konumlandığı hakkında daha fazla bilgi almak için bakın.
<!-- KC:beginInclude -->

| Ad |BRLTTY komutu|
|---|---|
|Braille ekranı geri kaydırma |`fwinlt` (bir pencere sola git)|
|Braille ekranı ileri kaydırma |`fwinrt` (bir pencere sağa git)|
|Braille ekranı önceki satıra götürme |`lnup` (bir satır yukarı git)|
|Braille ekranı sonraki satıra götürme |`lndn` (bir satır aşağı git)|
|imleci parmağın üzerinde bulunduğu Braille hücresine taşıma |`route` (imleci karektere götür)|
|Toggle input help |`learn` (enter/leave command learn mode)|
|Open the NVDA menu |`prefmenu` (enter/leave preferences menu)|
|Revert configuration |`prefload` (restore preferences from disk)|
|Save configuration |`prefsave` (save preferences to disk)|
|Report time |`time` (show current date and time)|
|Speak the line where the review cursor is located |`say_line` (speak current line)|
|Say all using review cursor |`say_below` (speak from current line through bottom of screen)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

Tivomatic tarafından üretilen ve Finlandiya'da satışa sunulan Caiku Albatross cihazları USB veya seri olarak bağlanabilmektedir.
Bu ekranları kullanmak için herhangi bir özel sürücünün yüklenmesi gerekmez.
Ekranı bağlamanız ve sonrasında gerekli ayarları yapmanız yeterli olacaktır.

Not: Baud hızının 19200 olması önerilir.
Gerekirse braille ekran menüsünden Baud hızını 19200 olarak değiştirin.
Sürücü 9600 baud hızını desteklese de, ekranın kullandığı baud hızını kontrol etmenin bir yolu yoktur.
Ekranın varsayılan baud hızı 19200 olduğundan, sürücü önce bunu dener.
Eğer baud hızları eşit olmazsa, sürücü beklenmedik şekilde davranabilir.

Aşağıda braille ekranı NVDA ile hangi tuşlarla kullanabileceğinizi bulabilirsiniz.
Tuşların yeri ve tarifi için Braille ekranın dokümantasyonunu inceleyin.
<!-- KC:beginInclude -->

| Ad |Kısayol|
|---|---|
|Move to top line in review |`home1`, `home2`|
|Move to bottom line in review |`end1`, `end2`|
|Sets the navigator object to the current focus |`eCursor1`, `eCursor2`|
|Move to current focus |`cursor1`, `cursor2`|
|Moves the mouse pointer to the current navigator object |`home1+home2`|
|Sets the navigator object to the current object under the mouse pointer and speaks it |`end1+end2`|
|Moves focus to current navigator object |`eCursor1+eCursor2`|
|Toggle braille tethered to |`cursor1+cursor2`|
|Move braille display to previous line |`up1`, `up2`, `up3`|
|Move braille display to next line |`down1`, `down2`, `down3`|
|Scroll braille display back |`left`, `lWheelLeft`, `rWheelLeft`|
|Scroll braille display forward |`right`, `lWheelRight`, `rWheelRight`|
|Route to braille cell |`routing`|
|Report text formatting under braille cell |`secondary routing`|
|Toggle the way context information is presented in braille |`attribute1+attribute3`|
|Cycles between speech modes |`attribute2+attribute4`|
|Switches to the previous review mode (e.g. object, document or screen) |`f1`|
|Switches to the next review mode (e.g. object, document or screen) |`f2`|
|Moves the navigator object to the object containing it |`f3`|
|Moves the navigator object to the first object inside it |`f4`|
|Moves the navigator object to the previous object |`f5`|
|Moves the navigator object to the next object |`f6`|
|Reports the current navigator object |`f7`|
|Reports information about the location of the text or object at the review cursor |`f8`|
|Shows braille settings |`f1+home1`, `f9+home2`|
|Reads status bar and moves navigator object into it |`f1+end1`, `f9+end2`|
|Cycle the braille cursor shape |`f1+eCursor1`, `f9+eCursor2`|
|Toggle the braille cursor |`f1+cursor1`, `f9+cursor2`|
|Cycle the braille show messages mode |`f1+f2`, `f9+f10`|
|Cycle the braille show selection state |`f1+f5`, `f9+f14`|
|Cycle the "braille move system caret when routing review cursor" states |`f1+f3`, `f9+f11`|
|Performs the default action on the current navigator object |`f7+f8`|
|Reports date/time |`f9`|
|Reports battery status and time remaining if AC is not plugged in |`f10`|
|Reports title |`f11`|
|Reports status bar |`f12`|
|Reports the current line under the application cursor |`f13`|
|Say all |`f14`|
|Reports current character under review cursor |`f15`|
|Reports the line of the current navigator object where the review cursor is situated |`f16`|
|Speaks the word of the current navigator object where the review cursor is situated |`f15+f16`|
|Moves the review cursor to the previous line of the current navigator object and speaks it |`lWheelUp`, `rWheelUp`|
|Moves the review cursor to the next line of the current navigator object and speaks it |`lWheelDown`, `rWheelDown`|
|`Windows+d` key (minimize all applications) |`attribute1`|
|`Windows+e` key (this computer) |`attribute2`|
|`Windows+b` key (focus system tray) |`attribute3`|
|`Windows+i` key (Windows settings) |`attribute4`|

<!-- KC:endInclude -->

### Standard HID Braille displays {#HIDBraille}

This is an experimental driver for the new Standard HID Braille Specification, agreed upon in 2018 by Microsoft, Google, Apple and several assistive technology companies including NV Access. 
The hope is that all future Braille Display models created by any manufacturer, will use this standard protocol which will remove the need for manufacturer-specific Braille drivers.

NVDA's automatic braille display detection will also recognize any display that supports this protocol.

Following are the current key assignments for these displays.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |pan left or rocker up|
|Scroll braille display forward |pan right or rocker down|
|Route to braille cell |routing set 1|
|Toggle braille tethered to |up+down|
|upArrow key |joystick up, dpad up or space+dot1|
|downArrow key |joystick down, dpad down or space+dot4|
|leftArrow key |space+dot3, joystick left  or dpad left|
|rightArrow key |space+dot6, joystick right or dpad right|
|şift+tab key |space+dot1+dot3|
|tab key |space+dot4+dot6|
|alt key |space+dot1+dot3+dot4 (space+m)|
|enter key |dot8, joystick center or dpad center|
|escape key |space+dot1+dot5 (space+e)|
|windows key |space+dot3+dot4|
|alt+tab key |space+dot2+dot3+dot4+dot5 (space+t)|
|NVDA Menu |space+dot1+dot3+dot4+dot5 (space+n)|
|windows+d key (minimize all applications) |space+dot1+dot4+dot5 (space+d)|
|Say all |space+dot1+dot2+dot3+dot4+dot5+dot6|

<!-- KC:endInclude -->

## İleri Düzey Konular {#AdvancedTopics}
### Güvenli Mcod {#SecureMode}

Sistem yöneticileri, yetkisiz sistem erişimini kısıtlamak için NVDA'yı yapılandırmak isteyebilir.
NVDA, yönetici ayrıcalıklarına yükseltildiği durumlar da dahil olmak üzere isteğe bağlı kod çalıştırabilen özel eklentilerin yüklenmesine izin verir.
Bununla birlikte, kullanıcılar NVDA Python Konsolu aracılığıyla isteğe bağlı kod yürütebilr.
NVDA güvenli modu, kullanıcıların NVDA konfigurasyonlarını değiştirmelerini engeller ve yetkisiz sistem erişimini sınırlar.

NVDA, `serviceDebug` [Sistem Çapında Geçerli Parametreleri](#SystemWideParameters) etkinleştirilmedikçe [güvenli ekranlarda](#SecureScreens) yürütüldüğünde güvenli modda çalışır.
NVDA'yı her zaman güvenli modda başlatmaya zorlamak için `forceSecureMode` [sistem çapında geçerli parametrelerini](#SystemWideParameters) ayarlayın.
Ayrıca NVDA, `-s` [komut satırı seçenekleri](#CommandLineOptions) ile güvenli modda başlatılabilir.

Güvenli mod şu özellikleri devre dışı bırakır:

* Konfigurasyonu ve diğer ayarları diske kaydetme
* Girdi hareketlerini diske kaydetme
* [Konfigürasyon profilleri](#ConfigurationProfiles) özellikleri örneğin; oluşturma, silme vb.
* `-c`  [komut satır seçeneğini kullanarak](#CommandLineOptions) konfigurasyonları yükleme
* NVDA'yı güncelleme ve taşınabilir kopyalar oluşturma
* [Eklenti Mağazası](#AddonsManager)
*  [Python konsolu](#PythonConsole)
*  [Log dosyasını göster](#LogViewer) ve günlük tutma
* The [Braille Görüntüleyici](#BrailleViewer) ve [Konuşma Görüntüleyici](#SpeechViewer)
* Kullanım kılavuzu veya katkıda bulunanlar dosyası gibi harici belgeleri NVDA menüsünden açma.

NVDA'nın kurulu kopyaları, eklentiler dahil yapılandırmalarını `%APPDATA%\nvda` klasöründe saklar.
NVDA kullanıcılarının yapılandırmalarını veya eklentilerini doğrudan değiştirmelerini önlemek için, bu klasöre kullanıcı erişimi de kısıtlanmalıdır.

Güvenli mod, NVDA'nın taşınabilir kopyalarında geçerli değildir.
Bu sınırlama aynı zamanda kurulumu başlatırken çalışan NVDA'nın geçici kopyası için de geçerlidir.
Güvenli ortamlarda, bir kullanıcının taşınabilir bir yürütülebilir dosyayı çalıştırabilmesi, güvenli moddan bağımsız olarak aynı güvenlik riskidir.
Sistem yöneticilerinin, NVDA'nın taşınabilir kopyaları da dahil olmak üzere yetkisiz yazılımların sistemlerinde çalışmasını kısıtlaması beklenmektedir.

NVDA kullanıcıları genellikle NVDA profilini ihtiyaçlarına göre yapılandırmayı tercih ederler.
Bu, NVDA'dan bağımsız olarak incelenmesi gereken özel eklentilerin yüklenmesini ve yapılandırılmasını gerektirebilir.
Güvenli mod, NVDA yapılandırmasındaki değişiklikleri dondurur, bu yüzden lütfen güvenli modu etkinleştirmeden önce NVDA'nın uygun şekilde yapılandırıldığından emin olun.

### Güvenli Ekranlar {#SecureScreens}

NVDA, `serviceDebug` [Sistem Çapında Geçerli Parametreleri](#SystemWideParameters) etkinleştirilmedikçe güvenli ekranlarda çalıştırıldığında [güvenli mod](#SecureMode)'da çalışır.

Güvenli bir ekranda çalıştırırken, NVDA tercihler için bir sistem profili kullanır.
Güvenli ekranlarda kullanım için [kullanıcı tercihleri](#GeneralSettingsCopySettings) kopyalanabilir.

Güvenli ekranlar şunları içerir::

* Windows oturum açma ekranı
* Kullanıcı hesabı denetimi iletişim kutusu: bir eylemi yönetici olarak çalıştırmanız gerektiğinde görünür
  * Bu, programların yüklenmesi olabilir

### Komut Satırı Seçenekleri {#CommandLineOptions}

NVDA başladığında onun davranışını değiştirecek bir veya daha fazla ek seçenek kabul edebilir.
İhtiyaç duyduğunuz kadar seçenek kullanabilirsiniz.
Bu seçenekler kısayol üzerinden (kısayol özelliklerinden), çalıştır iletişim kutusundan (başlat menüsü -> Çalıştır ya da Windows+r) veya Windows komut konsolu üzerinden kullanılabilir.
Seçenekler NVDA çalıştırılabilir dosyasından ve diğer seçeneklerden aralık ile ayrılarak kullanılmalıdır.
Örneğin, kullanışlı bir seçenek, NVDA’NIN çalışan tüm eklentileri askıya almasını sağlayan `--disable-addons` seçeneğidir.
Bu, bir eklentinin herhangi bir probleme neden olup olmadığını anlamanıza ya da eklentilerden birinin neden olduğu sorunlu durumdan kurtulmanıza yardımcı olur.

Bir örnek olarak, çalıştır iletişim kutusuna aşağıdaki komutu girerek NVDA'yı kapatabilirsiniz:

    nvda -q

Komut satırı seçeneklerinin bazılarının uzun ve kısa versiyonları bulunurken; bazılarının yalnızca uzun versiyonları vardır.
Kısa versiyonu olanlar için, aşağıdaki gibi onları birleştirebilirsiniz:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc CONFIGPATH` |Bu NVDA'yı başlangıç sesleri ve mesajlar devre dışı bırakılarak ve belirtilen yapılandırma ile başlatır|
|`nvda -mc CONFIGPATH --disable-addons` |Yukarıdakiyle aynı, ancak eklentiler devre dışı bırakılır|

Bazı komut satırı seçenekleri ek parametrelerle kullanılabilir; Örneğin, günlük seviyesi ya da kullanıcı konfigürasyon dizini.
Bu parametreler seçenekten sonra kullanılmalıdır, kısa versiyon için seçenek sonrası bir aralık ile ayrılarak ya da uzun versiyon için eşittir (`=`) işareti ile.

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -l 10` |NVDA'ya günlük seviyesi debug olarak başlamasını söyler|
|`nvda --log-file=c:\nvda.log` |NVDA'ya günlüğü `c:\nvda.log` dosyasına kaydetmesini söyler|
|`nvda --log-level=20 -f c:\nvda.log` |NVDA'nın bilgi seviyesinde günlük tutarak başlamasını ve günlüğü `c:\nvda.log` dosyasına kaydetmesini söyler|

Aşağıdakiler NVDA komut satırı seçenekleridir:

| Kısa |Uzun |Açıklama|
|---|---|---|
|`-h` |`--help` |Komut satırı yardımını göster ve çık|
|`-q` |`--quit` |Halihazırda çalışan NVDA kopyasını kapat|
|`-k` |`--check-running` |Çıkış kodu aracılığıyla NVDA'nın çalışıp çalışmadığını bildirir; çalışıyorsa 0, çalışmıyorsa 1|
|`-f LOGFILENAME` |`--log-file=LOGFILENAME` |Log mesajlarının yazılması gereken dosya. Güvenli mod etkinse günlük kaydı her zaman devre dışı bırakılır.|
|`-l LOGLEVEL` |`--log-level=LOGLEVEL` |Günlüğe kaydedilen en düşük mesaj düzeyi (hata ayıklama 10, giriş/çıkış 12, hata ayıklama uyarısı 15, bilgi 20, devre dışı 100). Güvenli mod etkinse günlük kaydı her zaman devre dışı bırakılır.|
|`-c Konfigurasyon YOLU` |`--config-path=CONFIGPATH` |NVDA'ya ilişkin tüm ayarların saklandığı yol. Güvenli mod etkinleştirilirse varsayılan değer zorlanır.|
|None |`--lang=LANGUAGE` |Yapılandırılmış NVDA dilini geçersiz kılın. Geçerli kullanıcı varsayılanı için "Windows", İngilizce için "en" vb. olarak ayarlayın.|
|`-m` |`--minimal` |Ses, arayüz, başlangıç mesajı vb olmaz|
|`-s` |`--secure` |NVDA'yı [Güvenli Mod](#SecureMode)'da başlatır|
|None |`--disable-addons` |Eklentiler etkisizdir|
|None |`--debug-logging` |Yalnızca bu çalıştırma için hata ayıklama seviyesi günlüğünü etkinleştirin. Bu ayar, herhangi bir kayıt seçeneği de dahil olmak üzere verilen herhangi bir günlük seviyesi (` --loglevel `, `-l`) argümanını geçersiz kılar.|
|None |`--no-logging` |NVDA'yı kullanırken günlüğü tamamen devre dışı bırakın. Komut satırından bir günlük seviyesi (`--loglevel`, `-l`) belirtilirse veya hata ayıklama günlüğü açıksa bu ayarın üzerine yazılabilir.|
|None |`--no-sr-flag` |Global ekran okuyucu bayrağını devre dışı bırakmaz|
|None |`--install` |NVDA'yı kurar (yeni kurulmuş kopyayı çalıştırarak)|
|None |`--install-silent` |NVDA'yı sessizce kurar (yeni kurulmuş kopyayı başlatmaz)|
|None |--`enable-start-on-logon=True|False` |Yüklerken, NVDA'nın [oturum açma ekranında başlamasını](#StartAtWindowsLogon) etkinleştirir|
|None |`--copy-portable-config` |Yüklerken, taşınabilir yapılandırmayı sağlanan yoldan (`config-path`, `-c`) geçerli kullanıcı hesabına kopyalar|
|None |`--create-portable` |NVDA'nın taşınabilir bir kopyasını oluşturur (işlem sonunda yeni kopya çalıştırılır). `--portable-path` belirtilmesi gerekir|
|None |`--create-portable-silent` |NVDA'nın taşınabilir bir kopyasını oluşturur (işlem sonunda yeni kopya çalıştırılmaz). `--portable-path` belirtilmesi gerekir|
|None |--`portable-path=PORTABLEPATH` |taşınabilir kopyanın oluşturulacağı adres|

### Sistem Çapında Geçerli Parametreler {#SystemWideParameters}

NVDA, NVDA'nın sistem genelindeki davranışını değiştiren sistem kayıt defterinde bazı değerlerin ayarlanmasına olanak tanır.
Bu değerler kayıt defterinde aşağıdaki anahtarlardan birinin altında tutulur:

* 32-bit sistem: `HKEY_LOCAL_MACHINE\SOFTWARE\nvda`
* 64-bit sistem: `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda`

Bu kayıt defteri anahtarı altında aşağıdaki değerler ayarlanabilir:

| Ad |Tür |Olası değerler |Açıklama|
|---|---|---|---|
|`configInLocalAppData` |DWORD |devre dışı bırakmak için 0 (varsayılan), etkinleştirmek için 1 |etkinleştirilirse, NVDA kullanıcı konfigürasyonunu roaming application data  yerine local application data  altında tutar|
|`serviceDebug` |DWORD |devre dışı bırakmak için 0 (varsayılan), etkinleştirmek için 1 |Etkinse, [güvenlli mod](#SecureMode)'u [güvenli ekranlarda](#SecureScreens) devre dışı bırakır. Güvenlik açısından birkaç önemli sonuç nedeniyle, bu seçeneğin kullanılması kesinlikle önerilmez.|
|`forceSecureMode` |DWORD |Devre dışı bırakmak için 0 (varsayılan), etkinleştirmek için 1 |Etkinleştirilirse, NVDA çalıştırılırken [Güvenli Mod](#SecureMode) öğesinin etkinleştirilmesini zorlar.|

## Daha Detaylı Bilgi {#FurtherInformation}

NVDA ile ilgili daha fazla bilgiye veya yardıma ihtiyaç duyarsanız, NVDA_URL adresini ziyaret edebilirsiniz.
Burada, ek belgeleri, ve teknik destek ile açık kaynak kodlarını bulabilirsiniz.
Bu sayfa ayrıca NVDA geliştirmesiyle ilgili olarak bilgi ve kaynaklar da sağlamaktadır. 
