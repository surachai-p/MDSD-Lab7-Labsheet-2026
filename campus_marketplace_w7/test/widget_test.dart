import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:campus_marketplace_w7/main.dart';
import 'package:campus_marketplace_w7/models/cart_model.dart';
import 'package:campus_marketplace_w7/models/item.dart';
import 'package:campus_marketplace_w7/repositories/item_repository.dart';

class _FakeItemRepository implements ItemRepository {
  @override
  Future<List<Item>> getItems() async => const [
    Item(
      id: 1,
      title: 'หนังสือทดสอบ',
      price: 100,
      description: 'สำหรับทดสอบ',
      category: 'หนังสือเรียน',
      imageUrl: 'https://example.com/image.png',
    ),
  ];
}

void main() {
  testWidgets('แสดงสินค้าและเพิ่มลงตะกร้าได้', (tester) async {
    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (_) => CartModel(),
        child: MyApp(repository: _FakeItemRepository()),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('หนังสือทดสอบ'), findsOneWidget);
    await tester.tap(find.text('เพิ่ม'));
    await tester.pump();
    expect(find.text('1'), findsOneWidget);
  });
}
