import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../models/listing_draft.dart';
import '../services/gemini_vision_service.dart';

class SellItemPage extends StatefulWidget {
  const SellItemPage({super.key});

  @override
  State<SellItemPage> createState() => _SellItemPageState();
}

class _SellItemPageState extends State<SellItemPage> {
  static const _prompt = '''
คุณคือผู้ช่วยเขียนประกาศขายของมือสองในตลาดนัดออนไลน์สำหรับนักศึกษามหาวิทยาลัย
จากรูปภาพสินค้าที่แนบมา ให้วิเคราะห์แล้วตอบกลับเป็น JSON เท่านั้น ตามโครงสร้างนี้:
{
  "title": "ชื่อประกาศสั้นกระชับ ไม่เกิน 40 ตัวอักษร",
  "category": "หมวดหมู่ที่เหมาะสมที่สุด เลือกจาก: หนังสือเรียน, อุปกรณ์อิเล็กทรอนิกส์, ของแต่งหอพัก, เสื้อผ้า, อื่นๆ",
  "description": "คำบรรยายสินค้า 2-3 ประโยค ที่ดึงดูดผู้ซื้อและบอกสภาพของสินค้าตามที่เห็นในภาพ"
}
ห้ามตอบข้อความอื่นนอกเหนือจาก JSON ดังกล่าว
''';

  File? _selectedImage;
  bool _isLoading = false;
  String? _error;
  ListingDraft? _draft;

  final _titleController = TextEditingController();
  final _categoryController = TextEditingController();
  final _descriptionController = TextEditingController();

  // ร่างประกาศที่ผู้ใช้ยืนยันแล้ว (เก็บใน State ชั่วคราว ยังไม่บันทึกถาวร)
  final List<ListingDraft> _confirmedDrafts = [];

  @override
  void dispose() {
    _titleController.dispose();
    _categoryController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  Future<void> _pickImage() async {
    final picked = await ImagePicker().pickImage(source: ImageSource.gallery);
    if (picked == null) return;
    setState(() {
      _selectedImage = File(picked.path);
      _draft = null;
      _error = null;
    });
  }

  Future<void> _analyze() async {
    final image = _selectedImage;
    if (image == null) return;

    setState(() {
      _isLoading = true;
      _error = null;
      _draft = null;
    });

    try {
      final json =
          await GeminiVisionService().analyzeProductImage(image, _prompt);
      final draft = ListingDraft.fromJson(json);
      if (!mounted) return;
      // นำค่าที่ AI แนะนำไปใส่ในช่องที่แก้ไขได้ (ข้อ 5.1)
      _titleController.text = draft.title;
      _categoryController.text = draft.category;
      _descriptionController.text = draft.description;
      setState(() => _draft = draft);
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = e.toString().replaceFirst('Exception: ', ''));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  // ข้อ 5.2: เก็บค่าจากฟอร์ม (ที่อาจถูกแก้แล้ว) เป็นร่างฉบับสุดท้าย
  void _confirmDraft() {
    final finalDraft = ListingDraft(
      title: _titleController.text.trim(),
      category: _categoryController.text.trim(),
      description: _descriptionController.text.trim(),
    );

    setState(() {
      _confirmedDrafts.add(finalDraft);
      _selectedImage = null;
      _draft = null;
      _error = null;
      _titleController.clear();
      _categoryController.clear();
      _descriptionController.clear();
    });

    print('ร่างที่ยืนยันแล้ว: ${_confirmedDrafts.length} รายการ, '
        'ล่าสุด: ${finalDraft.title} / ${finalDraft.category}');

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('บันทึกร่างประกาศเรียบร้อยแล้ว')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ลงประกาศขายสินค้า')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Container(
              height: 240,
              width: double.infinity,
              color: Colors.grey[300],
              child: _selectedImage != null
                  ? Image.file(_selectedImage!, fit: BoxFit.contain)
                  : const Icon(Icons.image, size: 64, color: Colors.grey),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isLoading ? null : _pickImage,
              child: const Text('เลือกรูปภาพสินค้า'),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed:
                  (_selectedImage == null || _isLoading) ? null : _analyze,
              child: const Text('ให้ AI ช่วยแนะนำ'),
            ),
            const SizedBox(height: 16),
            if (_isLoading)
              const Column(
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 8),
                  Text('AI กำลังวิเคราะห์ภาพสินค้า...'),
                ],
              )
            else if (_error != null)
              Text(_error!, style: const TextStyle(color: Colors.red))
            else if (_draft != null)
              Column(
                children: [
                  TextField(
                    controller: _titleController,
                    decoration: const InputDecoration(
                      labelText: 'ชื่อประกาศ',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: _categoryController,
                    decoration: const InputDecoration(
                      labelText: 'หมวดหมู่',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: _descriptionController,
                    maxLines: 4,
                    decoration: const InputDecoration(
                      labelText: 'คำบรรยาย',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 12),
                  ElevatedButton(
                    onPressed: _confirmDraft,
                    child: const Text('ยืนยันร่างประกาศ'),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}