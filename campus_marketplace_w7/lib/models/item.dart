
import 'package:cloud_firestore/cloud_firestore.dart';

class Item {
  final int id;
  final String title;
  final double price;
  final String description;
  final String category;
  final String imageUrl;
  final String? sellerId;

  const Item({
    required this.id,
    required this.title,
    required this.price,
    required this.description,
    required this.category,
    required this.imageUrl,
    this.sellerId,
  });

  // แปลงข้อมูลจาก Fake Store API
  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      id: json['id'] as int,
      title: json['title'] as String,
      price: (json['price'] as num).toDouble(),
      description: json['description'] as String,
      category: json['category'] as String,
      imageUrl: (json['image'] ?? json['imageUrl']) as String,
      sellerId: json['sellerId'] as String?,
    );
  }

  // แปลง Item เป็นข้อมูลสำหรับบันทึกลง Firestore
  Map<String, dynamic> toFirestore() {
    return {
      'title': title,
      'price': price,
      'description': description,
      'category': category,
      'imageUrl': imageUrl,
      'sellerId': sellerId,
    };
  }

  // อ่าน Item จากเอกสาร Firestore
  factory Item.fromFirestore(
    DocumentSnapshot<Map<String, dynamic>> doc,
  ) {
    final data = doc.data();

    if (data == null) {
      throw StateError('ไม่พบข้อมูลสินค้าใน Firestore');
    }

    return Item(
      id: int.tryParse(doc.id) ?? doc.id.hashCode.abs(),
      title: data['title'] as String? ?? '',
      price: (data['price'] as num?)?.toDouble() ?? 0.0,
      description: data['description'] as String? ?? '',
      category: data['category'] as String? ?? '',
      imageUrl: data['imageUrl'] as String? ?? '',
      sellerId: data['sellerId'] as String?,
    );
  }
}
