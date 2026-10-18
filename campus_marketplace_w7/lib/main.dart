
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_core/firebase_core.dart';

import 'firebase_options.dart';
import 'models/cart_model.dart';
import 'database/app_database.dart';
import 'screens/auth_gate.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  final db = AppDatabase();

  runApp(
    ChangeNotifierProvider(
      create: (context) => CartModel(),
      child: MyApp(db: db),
    ),
  );
}

class MyApp extends StatelessWidget {
  final AppDatabase db;

  const MyApp({
    super.key,
    required this.db,
  });

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Campus Marketplace',
      debugShowCheckedModeBanner: false,

      // Lab 9: ใช้หน้า Login เพื่อทดสอบ Firebase Authentication
      home: AuthGate(db: db),

      // เก็บหน้าเดิมจาก Lab 8 ไว้ก่อน ยังไม่ลบ
      /*
      home: MainScaffold(
        itemRepository: ItemRepositoryApi(),
        favoritesRepository: FavoritesRepositoryDrift(db),
        draftRepository: ListingDraftRepositoryDrift(db),
      ),
      */
    );
  }
}
