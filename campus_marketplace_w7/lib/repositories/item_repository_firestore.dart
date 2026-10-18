
import 'package:cloud_firestore/cloud_firestore.dart';

import '../models/item.dart';
import 'item_repository.dart';

class ItemRepositoryFirestore implements ItemRepository {
  final FirebaseFirestore _firestore;

  ItemRepositoryFirestore({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  CollectionReference<Map<String, dynamic>> get _itemsCollection =>
      _firestore.collection('items');

  // ดึงสินค้าทั้งหมดจาก Firestore
  @override
  Future<List<Item>> getItems() async {
    final snapshot = await _itemsCollection.get();

    return snapshot.docs.map((doc) {
      return Item.fromFirestore(doc);
    }).toList();
  }

  // โพสต์สินค้าลง Firestore
  Future<void> postItem(Item item) async {
    final data = item.toFirestore();

    data['createdAt'] = FieldValue.serverTimestamp();

    await _itemsCollection.add(data);
  }

  // ติดตามสินค้าที่ผู้ใช้คนนี้โพสต์
  Stream<List<Item>> watchMyListings(String sellerId) {
    return _itemsCollection
        .where('sellerId', isEqualTo: sellerId)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs.map((doc) {
        return Item.fromFirestore(doc);
      }).toList();
    });
  }
}
