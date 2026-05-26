import open3d as o3d
import numpy as np

class LidarProcessor:
    def __init__(self, pcd_path=None):
        """
        LiDAR veri işleme sınıfı. 
        Eğer özel bir .pcd/.ply dosya yolu verilmezse Open3D'nin hazır test verisini yükler.
        """
        if pcd_path:
            self.cloud = o3d.io.read_point_cloud(pcd_path)
        else:
            print("[BİLGİ] Özel bir dosya yolu verilmedi, örnek PLY nokta bulutu yükleniyor...")
            pcd_data = o3d.data.PLYPointCloud()
            self.cloud = o3d.io.read_point_cloud(pcd_data.path)
            
        print(f"[BİLGİ] Nokta bulutu başarıyla yüklendi. Toplam nokta sayısı: {len(self.cloud.points)}")

    def remove_noise(self, nb_neighbors=20, std_ratio=2.0):
        """
        Statistical Outlier Removal (İstatistiki Aykırı Değer Temizleme) kullanarak
        sensör kaynaklı gürültüleri ve hatalı noktaları temizler.
        """
        print("[İŞLEM] İstatistiki gürültü temizleme başlatıldı...")
        cl, ind = self.cloud.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
        clean_cloud = self.cloud.select_by_index(ind)
        
        diff = len(self.cloud.points) - len(clean_cloud.points)
        print(f"[BAŞARI] {diff} adet gürültülü nokta buluttan uzaklaştırıldı.")
        return clean_cloud

    def filter_roi(self, min_bound, max_bound):
        """
        [Gelecek Planı] Bölge Filtreleme (Region of Interest) buraya eklenecek.
        Sürüş koridoru dışındaki noktaları kırpmak için kullanılacak.
        """
        pass

    def segment_ground(self):
        """
        [Gelecek Planı] RANSAC ile Yer Düzlemi Ayrıştırma buraya eklenecek.
        Yol ile engelleri birbirinden ayırmak için kullanılacak.
        """
        pass

    def visualize(self, cloud_to_show=None, window_name="LiDAR Görselleştirme"):
        """
        Nokta bulutunu 3B ekranda görselleştirir. 
        Açılan pencereyi kapatmak için klavyeden 'Q' tuşuna basabilirsiniz.
        """
        target = cloud_to_show if cloud_to_show else self.cloud
        o3d.visualization.draw_geometries([target], window_name=window_name)

if __name__ == "__main__":
    # Sınıfı örnek veriyle başlatıyoruz
    processor = LidarProcessor()
    
    # 1. Adım: Ham Nokta Bulutunu Görselleştir
    print("\n--- Orijinal Veri Görselleştiriliyor (Kapatmak için 'Q' tuşuna basın) ---")
    processor.visualize(window_name="Ham LiDAR Nokta Bulutu")
    
    # 2. Adım: Gürültü Filtreleme Algoritmasını Çalıştır
    cleaned_pcd = processor.remove_noise(nb_neighbors=20, std_ratio=2.0)
    
    # 3. Adım: Temizlenmiş Nokta Bulutunu Görselleştir
    print("\n--- Temizlenmiş Veri Görselleştiriliyor (Kapatmak için 'Q' tuşuna basın) ---")
    processor.visualize(cleaned_pcd, window_name="Temizlenmiş LiDAR Nokta Bulutu")