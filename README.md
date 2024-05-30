Kitsune
Ben-Gurion Üniversitesi'nden Yisroel Mirsky ve ekibi tarafından geliştirilen  çevrimiçi ağ saldırılarını tespit edebilen bir ağ saldırı tespit sistemidir. Kitsune'nin temel  algoritması olan KitNET; autoencoder adı verilen sinir ağlarından oluşan bir ansambl kullanarak normal ve anormal trafik desenlerini ayırt eder. Ağ güvenliği alanında yenilikçi ve etkili bir çözüm sunarak, ağ trafiğini sürekli olarak izleyebilir ve anormallikleri tespit ederek olası saldırılara karşı koruma sağlar. Bu özellikleri sayesinde farklı ağ ortamlarında kullanılabilecek esnek ve güçlü bir NIDS çözümüdür.



Kitsune Mimarisi
[https://raw.githubusercontent.com/ymirsky/Kitsune-py/master/Kitsune_fig.png
](https://raw.githubusercontent.com/ymirsky/Kitsune-py/master/Kitsune_fig.png)
External Libs: Kitsune ağ paketlerini yakalamak ve işlemek için dış kütüphanelere (libs) bağımlıdır. Bu kütüphaneler paket yakalama ve analiz etme işlevlerini sağlar. 
Packet Capturer: Ağ üzerinden geçen paketleri yakalar. Bu modül ağ trafiğini dinler ve ileri işlem için gerekli olan ham paket verilerini toplar. 
Packet Parser: Yakalanan paketlerden gerekli bilgileri çıkarır. Bu aşama paketlerin içeriğini anlamak ve kullanılabilir verilere dönüştürmek için kritik öneme sahiptir. 
Feature Extractor (FE): Paket parser tarafından işlenen verilerden özellikler çıkarır. Özellik çıkarma verilerin model tarafından işlenmesi için uygun hale getirilmesini sağlar. 
Feature Mapper (FM): Çıkarılan özellikleri otoenkoderler tarafından işlenebilecek formata dönüştürür. Bu modül özelliklerin uygun bir şekilde haritalanmasını ve gruplandırılmasını sağlar. 
Ensemble Layer: Çoklu otoenkoderlerin yer aldığı katmandır. Her bir otoenkoder belirli özellik grupları üzerinde çalışarak anomali tespiti yapar. Bu katman çeşitli otoenkoderlerin bir araya gelmesiyle oluşur ve her biri farklı türden veri anomalilerini tespit etmek için özelleştirilmiştir. 
Output Layer: Ensemble layer'dan gelen bilgileri alır ve son anomali tespit kararını verir. Bu katman tüm otoenkoderlerden gelen çıktıları birleştirerek nihai bir skor veya alarm üretir. 
ILog: Anomali tespit sonuçlarını kaydeder. Bu loglar tespit edilen olayların incelenmesi, raporlanması ve arşivlenmesi için kullanılır. 



Yapılan Çalışma 

Kitsune, ağ trafiğindeki zararlı saldırıları (DOS, DDOS gibi) izleyen ve bu saldırılara bağlı RMSE değerleri üreten bir NIDS tabanlı sistemdir. Sistemi örnek kod ile çalıştırdığımızda oldukça yavaş ve hantal olduğunu fark ettik. Bu sorunu çözmek için araştırmalar yaparak hızlandırma yöntemleri üzerine yoğunlaştık. Grafik işlemcilerde paralel işlem yapmanın sistemi hızlandırabileceğini öğrendik ve bu doğrultuda CUDA (cupy) kütüphanesini kullanmaya başladık. Bu değişiklikler sonucunda sistemin daha hızlı çalıştığını gözlemledik. Sonrasında kendi Wi-Fi ağ trafiğimizde olaşabilecek anomalileri Kitsune nasıl izleyebiliriz sorusu aklımıza ve araştırmalarımızı bu yönde derinleştirdik. WireShark kullanarak ağ trafiğini izleyebileceğimizi ve elde ettiğimiz metrikleri programımızda işleyebileceğimizi keşfettik. Canlı trafikten elde edilen RMSE değelerinin çıktısını canlı olarak grafikte izlemek  için PyQt5 kütüphanesini kullanmamız gerektiğini öğrendik ve programımıza bu özelliği ekledik.





Kaynak Repository: https://github.com/ymirsky/Kitsune-py
