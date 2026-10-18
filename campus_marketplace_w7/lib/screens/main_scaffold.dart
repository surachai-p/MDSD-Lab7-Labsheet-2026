
import 'package:flutter/material.dart';

import 'home_page.dart';
import 'sell_item_page.dart';
import 'favorites_page.dart';
import 'my_drafts_page.dart';

import '../repositories/item_repository.dart';
import '../repositories/item_repository_firestore.dart';
import '../repositories/favorites_repository.dart';
import '../repositories/listing_draft_repository.dart';

class MainScaffold extends StatefulWidget {
  final List<ItemRepository> itemRepositories;
  final FavoritesRepository favoritesRepository;
  final ListingDraftRepository draftRepository;

  const MainScaffold({
    super.key,
    required this.itemRepositories,
    required this.favoritesRepository,
    required this.draftRepository,
  });

  @override
  State<MainScaffold> createState() => _MainScaffoldState();
}

class _MainScaffoldState extends State<MainScaffold> {
  int _selectedIndex = 0;

  late final List<Widget> _pages;

  @override
  void initState() {
    super.initState();

    final firestoreRepository = widget.itemRepositories
        .where(
          (repository) => repository is ItemRepositoryFirestore,
        )
        .firstOrNull;

    if (firestoreRepository == null) {
      throw StateError(
        'ไม่พบ ItemRepositoryFirestore ใน itemRepositories',
      );
    }

    _pages = [
      HomePage(
        repository: firestoreRepository,
        favoritesRepository: widget.favoritesRepository,
        draftRepository: widget.draftRepository,
      ),
      SellItemPage(
        draftRepository: widget.draftRepository,
      ),
      FavoritesPage(
        repository: widget.favoritesRepository,
      ),
      MyDraftsPage(
        repository: widget.draftRepository,
      ),
    ];
  }

  // เปลี่ยนเฉพาะแท็บที่เลือก ไม่สร้างหน้าใหม่
  void _onTabSelected(int index) {
    if (index == _selectedIndex) return;

    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedIndex,
        children: _pages,
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onTabSelected,
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.storefront),
            label: 'หน้าหลัก',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.add_a_photo),
            label: 'ลงประกาศขาย',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.favorite),
            label: 'รายการโปรด',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.drafts),
            label: 'ร่างประกาศของฉัน',
          ),
        ],
      ),
    );
  }
}
