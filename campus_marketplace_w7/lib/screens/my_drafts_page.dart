
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';

import '../database/app_database.dart';
import '../models/item.dart';
import '../repositories/listing_draft_repository.dart';
import '../repositories/item_repository_firestore.dart';

class MyDraftsPage extends StatefulWidget {
  final ListingDraftRepository repository;

  const MyDraftsPage({
    super.key,
    required this.repository,
  });

  @override
  State<MyDraftsPage> createState() => _MyDraftsPageState();
}

class _MyDraftsPageState extends State<MyDraftsPage> {
  late Future<List<ListingDraftRow>> _draftsFuture;

  final Set<int> _postingDraftIds = <int>{};
  final Set<int> _openingPriceDialogIds = <int>{};
  final Set<int> _deletingDraftIds = <int>{};

  @override
  void initState() {
    super.initState();
    _loadDrafts();
  }

  void _loadDrafts() {
    _draftsFuture = widget.repository.getAllDrafts();
  }

  Future<void> _reloadDrafts() async {
    if (!mounted) return;

    final future = widget.repository.getAllDrafts();

    setState(() {
      _draftsFuture = future;
    });

    try {
      await future;
    } catch (_) {
      // FutureBuilder จะแสดงข้อความเมื่อโหลดรายการไม่สำเร็จ
    }
  }

  void _showMessage(String message) {
    if (!mounted) return;

    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(content: Text(message)),
      );
  }

  Future<void> _deleteDraft(int id) async {
    if (_postingDraftIds.contains(id) ||
        _openingPriceDialogIds.contains(id) ||
        _deletingDraftIds.contains(id)) {
      return;
    }

    setState(() {
      _deletingDraftIds.add(id);
    });

    try {
      await widget.repository.deleteDraft(id);

      if (!mounted) return;

      await _reloadDrafts();
      _showMessage('ลบร่างประกาศแล้ว');
    } catch (e) {
      _showMessage('ลบร่างประกาศไม่สำเร็จ กรุณาลองอีกครั้ง');
    } finally {
      if (mounted) {
        setState(() {
          _deletingDraftIds.remove(id);
        });
      }
    }
  }

  // เปิด Dialog กำหนดราคาสินค้า
  Future<double?> _askPrice() async {
    if (!mounted) return null;

    return showDialog<double>(
      context: context,
      barrierDismissible: false,
      builder: (_) => const _PriceDialog(),
    );
  }

  // โพสต์ร่างสินค้าไปยัง Firestore
  Future<void> _postDraft(ListingDraftRow draft) async {
    final id = draft.id;

    if (_postingDraftIds.contains(id) ||
        _openingPriceDialogIds.contains(id) ||
        _deletingDraftIds.contains(id)) {
      return;
    }

    if (FirebaseAuth.instance.currentUser == null) {
      _showMessage('กรุณาเข้าสู่ระบบก่อนโพสต์สินค้า');
      return;
    }

    setState(() {
      _openingPriceDialogIds.add(id);
    });

    double? price;

    try {
      price = await _askPrice();
    } catch (e) {
      _showMessage('เปิดหน้ากำหนดราคาไม่สำเร็จ กรุณาลองอีกครั้ง');
      return;
    } finally {
      if (mounted) {
        setState(() {
          _openingPriceDialogIds.remove(id);
        });
      }
    }

    // ผู้ใช้ยกเลิก Dialog หรือหน้าออกจากหน้าจอแล้ว
    if (!mounted || price == null) return;

    final currentUser = FirebaseAuth.instance.currentUser;

    if (currentUser == null) {
      _showMessage('เซสชันหมดอายุ กรุณาเข้าสู่ระบบอีกครั้ง');
      return;
    }

    setState(() {
      _postingDraftIds.add(id);
    });

    var firestoreSaved = false;

    try {
      final item = Item(
        id: DateTime.now().millisecondsSinceEpoch,
        title: draft.title,
        price: price,
        description: draft.description,
        category: draft.category,
        imageUrl: '',
        sellerId: currentUser.uid,
      );

      // บันทึกสินค้าไปยัง Firestore
      await ItemRepositoryFirestore().postItem(item);
      firestoreSaved = true;

      // ลบร่างในเครื่องหลังบันทึก Firestore สำเร็จแล้วเท่านั้น
      await widget.repository.deleteDraft(id);

      if (!mounted) return;

      await _reloadDrafts();

      _showMessage(
        'บันทึก "${draft.title}" ลง Firestore สำเร็จ '
        '(ยังไม่ได้อัปโหลดรูป)',
      );
    } catch (e) {
      if (!mounted) return;

      if (firestoreSaved) {
        _showMessage(
          'โพสต์สินค้าใน Firestore แล้ว แต่ลบร่างในเครื่องไม่สำเร็จ '
          'กรุณารีเฟรชรายการร่าง',
        );
      } else {
        _showMessage(
          'บันทึกสินค้าไม่สำเร็จ กรุณาตรวจสอบอินเทอร์เน็ต '
          'แล้วลองโพสต์ร่างนี้อีกครั้ง',
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _postingDraftIds.remove(id);
        });
      }
    }
  }

  String _formatDateTime(DateTime dateTime) {
    final local = dateTime.toLocal();

    final day = local.day.toString().padLeft(2, '0');
    final month = local.month.toString().padLeft(2, '0');
    final year = local.year;
    final hour = local.hour.toString().padLeft(2, '0');
    final minute = local.minute.toString().padLeft(2, '0');

    return '$day/$month/$year $hour:$minute น.';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ร่างประกาศของฉัน'),
        actions: [
          IconButton(
            tooltip: 'รีเฟรชรายการ',
            icon: const Icon(Icons.refresh),
            onPressed: _reloadDrafts,
          ),
        ],
      ),
      body: FutureBuilder<List<ListingDraftRow>>(
        future: _draftsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(
                      Icons.error_outline,
                      size: 48,
                    ),
                    const SizedBox(height: 12),
                    const Text(
                      'โหลดร่างประกาศไม่สำเร็จ',
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 12),
                    FilledButton(
                      onPressed: _reloadDrafts,
                      child: const Text('ลองอีกครั้ง'),
                    ),
                  ],
                ),
              ),
            );
          }

          final drafts = snapshot.data ?? <ListingDraftRow>[];

          if (drafts.isEmpty) {
            return RefreshIndicator(
              onRefresh: _reloadDrafts,
              child: ListView(
                physics: const AlwaysScrollableScrollPhysics(),
                children: const [
                  SizedBox(height: 180),
                  Icon(
                    Icons.description_outlined,
                    size: 64,
                    color: Colors.grey,
                  ),
                  SizedBox(height: 16),
                  Center(
                    child: Text(
                      'ยังไม่มีร่างประกาศ\n'
                      'สร้างร่างใหม่จากหน้าลงประกาศขายสินค้า',
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: _reloadDrafts,
            child: ListView.builder(
              physics: const AlwaysScrollableScrollPhysics(),
              itemCount: drafts.length,
              itemBuilder: (context, index) {
                final draft = drafts[index];
                final id = draft.id;

                final isPosting = _postingDraftIds.contains(id);
                final isOpeningPrice =
                    _openingPriceDialogIds.contains(id);
                final isDeleting = _deletingDraftIds.contains(id);

                final isBusy =
                    isPosting || isOpeningPrice || isDeleting;

                return Card(
                  margin: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  child: ListTile(
                    leading: const CircleAvatar(
                      child: Icon(Icons.description_outlined),
                    ),
                    title: Text(
                      draft.title,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    subtitle: Padding(
                      padding: const EdgeInsets.only(top: 6),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('หมวดหมู่: ${draft.category}'),
                          const SizedBox(height: 4),
                          Text(
                            'แก้ไขล่าสุด: '
                            '${_formatDateTime(draft.updatedAt)}',
                          ),
                          const SizedBox(height: 10),
                          if (isPosting || isDeleting)
                            Row(
                              children: [
                                const SizedBox(
                                  width: 20,
                                  height: 20,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                  ),
                                ),
                                const SizedBox(width: 10),
                                Expanded(
                                  child: Text(
                                    isPosting
                                        ? 'กำลังบันทึกสินค้าลง Firestore...'
                                        : 'กำลังลบร่างประกาศ...',
                                  ),
                                ),
                              ],
                            )
                          else
                            SizedBox(
                              width: double.infinity,
                              child: FilledButton.icon(
                                onPressed: isBusy
                                    ? null
                                    : () => _postDraft(draft),
                                icon: isOpeningPrice
                                    ? const SizedBox(
                                        width: 18,
                                        height: 18,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 2,
                                        ),
                                      )
                                    : const Icon(
                                        Icons.cloud_upload_outlined,
                                      ),
                                label: Text(
                                  isOpeningPrice
                                      ? 'กำลังเปิดกำหนดราคา...'
                                      : 'บันทึกสินค้าใน Firestore',
                                ),
                              ),
                            ),
                        ],
                      ),
                    ),
                    trailing: IconButton(
                      tooltip: 'ลบร่างประกาศ',
                      icon: const Icon(Icons.delete_outline),
                      onPressed: isBusy
                          ? null
                          : () => _deleteDraft(id),
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

// ======================================================
// Dialog กำหนดราคาสินค้า
// ต้องอยู่นอกคลาส _MyDraftsPageState
// ======================================================

class _PriceDialog extends StatefulWidget {
  const _PriceDialog();

  @override
  State<_PriceDialog> createState() => _PriceDialogState();
}

class _PriceDialogState extends State<_PriceDialog> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _confirmPrice() {
    final form = _formKey.currentState;

    if (form == null || !form.validate()) {
      return;
    }

    final price = double.tryParse(_controller.text.trim());

    if (price == null || !price.isFinite || price <= 0) {
      return;
    }

    Navigator.of(context).pop(price);
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('กำหนดราคาสินค้า'),
      content: Form(
        key: _formKey,
        child: TextFormField(
          controller: _controller,
          keyboardType: const TextInputType.numberWithOptions(
            decimal: true,
          ),
          autofocus: true,
          decoration: const InputDecoration(
            labelText: 'ราคาสินค้า (บาท)',
            hintText: 'เช่น 150 หรือ 99.50',
            prefixIcon: Icon(Icons.payments_outlined),
            border: OutlineInputBorder(),
          ),
          validator: (value) {
            if (value == null || value.trim().isEmpty) {
              return 'กรุณากรอกราคาสินค้า';
            }

            final price = double.tryParse(value.trim());

            if (price == null || !price.isFinite || price <= 0) {
              return 'กรุณากรอกราคามากกว่า 0';
            }

            return null;
          },
          onFieldSubmitted: (_) => _confirmPrice(),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('ยกเลิก'),
        ),
        FilledButton(
          onPressed: _confirmPrice,
          child: const Text('ยืนยันราคา'),
        ),
      ],
    );
  }
}
