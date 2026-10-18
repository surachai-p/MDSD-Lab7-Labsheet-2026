
import 'dart:io';

import 'package:firebase_storage/firebase_storage.dart';

class StorageService {
  final FirebaseStorage _storage;

  StorageService({FirebaseStorage? storage})
      : _storage = storage ?? FirebaseStorage.instance;

  Future<String> uploadListingImage(
    File imageFile,
    String sellerId,
  ) async {
    // สร้างชื่อไฟล์ใหม่ ไม่ใช้ชื่อไฟล์เดิมจากเครื่อง
    final timestamp = DateTime.now().millisecondsSinceEpoch;
    final extension = imageFile.path.contains('.')
        ? imageFile.path.split('.').last
        : 'jpg';

    final fileName = '${sellerId}_$timestamp.$extension';

    // กำหนดตำแหน่งจัดเก็บรูปใน Firebase Storage
    final storageRef = _storage
        .ref()
        .child('listing_images')
        .child(fileName);

    // อัปโหลดรูปและรอจนเสร็จสมบูรณ์
    await storageRef.putFile(imageFile);

    // ขอ Download URL หลังจากอัปโหลดสำเร็จแล้วเท่านั้น
    final downloadUrl = await storageRef.getDownloadURL();

    return downloadUrl;
  }
}
