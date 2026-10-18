
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';

import '../database/app_database.dart';
import '../repositories/item_repository_api.dart';
import '../repositories/item_repository_firestore.dart';
import '../repositories/favorites_repository_drift.dart';
import '../repositories/listing_draft_repository_drift.dart';
import 'login_page.dart';
import 'main_scaffold.dart';

class AuthGate extends StatelessWidget {
  final AppDatabase db;

  const AuthGate({
    super.key,
    required this.db,
  });

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: FirebaseAuth.instance.authStateChanges(),
      builder: (context, snapshot) {
        // กำลังตรวจสอบสถานะการเข้าสู่ระบบ
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(
              child: CircularProgressIndicator(),
            ),
          );
        }

        // ยังไม่ได้เข้าสู่ระบบ
        if (!snapshot.hasData) {
          return const LoginPage();
        }

        // เข้าสู่ระบบแล้ว แสดงสินค้าจาก API และ Firestore
        return MainScaffold(
          itemRepositories: [
            ItemRepositoryApi(),
            ItemRepositoryFirestore(),
          ],
          favoritesRepository: FavoritesRepositoryDrift(db),
          draftRepository: ListingDraftRepositoryDrift(db),
        );
      },
    );
  }
}
