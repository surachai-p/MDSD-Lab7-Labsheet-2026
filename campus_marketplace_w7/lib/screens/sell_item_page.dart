import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../models/listing_draft.dart';
import '../services/gemini_vision_service.dart';

enum _AiStatus { idle, loading, success, error }

class SellItemPage extends StatefulWidget {
  const SellItemPage({super.key});

  @override
  State<SellItemPage> createState() => _SellItemPageState();
}

class _SellItemPageState extends State<SellItemPage> {
  // Prompt ที่ใช้งานจริง (ทดสอบ Safety ในส่วนที่ 6 จะมาแก้ตรงนี้ชั่วคราว)
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
  _AiStatus _status = _AiStatus.idle;
  String? _errorMessage;

  final _titleController = TextEditingController();
  final _categoryController = TextEditingController();
  final _descriptionController = TextEditingController();

  Future<void> _pickImage() async {
    final result = await ImagePicker().pickImage(source: ImageSource.gallery);
    if (result == null) {
      return;
    }
    setState(() {
      _selectedImage = File(result.path);
    });
  }

  Future<void> _analyzeWithAi() async {
    if (_selectedImage == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('กรุณาเลือกรูปภาพสินค้าก่อน')),
      );
      return;
    }

    setState(() {
      _status = _AiStatus.loading;
      _errorMessage = null;
    });

    try {
      final jsonText =
          await GeminiVisionService().analyzeProductImage(_selectedImage!, _prompt);
      final json = jsonDecode(jsonText) as Map<String, dynamic>;
      final draft = ListingDraft.fromJson(json);

      setState(() {
        _status = _AiStatus.success;
        _titleController.text = draft.title;
        _categoryController.text = draft.category;
        _descriptionController.text = draft.description;
      });
    } catch (e) {
      setState(() {
        _status = _AiStatus.error;
        _errorMessage = e.toString().replaceFirst('Exception: ', '');
      });
    }
  }

  void _confirmListing() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('บันทึกร่างประกาศเรียบร้อยแล้ว')),
    );
    setState(() {
      _selectedImage = null;
      _status = _AiStatus.idle;
      _titleController.clear();
      _categoryController.clear();
      _descriptionController.clear();
    });
  }

  @override
  void dispose() {
    _titleController.dispose();
    _categoryController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ลงประกาศขายสินค้า')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            if (_selectedImage != null)
              Image.file(_selectedImage!, height: 200, fit: BoxFit.cover)
            else
              Container(
                height: 200,
                color: Colors.grey.shade300,
                child: const Center(child: Icon(Icons.image, size: 64)),
              ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _pickImage,
              child: const Text('เลือกรูปภาพสินค้า'),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _status == _AiStatus.loading ? null : _analyzeWithAi,
              child: const Text('ให้ AI ช่วยแนะนำ'),
            ),
            const SizedBox(height: 16),

            if (_status == _AiStatus.loading)
              const Column(
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 8),
                  Text('AI กำลังวิเคราะห์ภาพสินค้า...'),
                ],
              ),

            if (_status == _AiStatus.error && _errorMessage != null)
              Text(
                _errorMessage!,
                style: const TextStyle(color: Colors.red),
              ),

            if (_status == _AiStatus.success) ...[
              TextField(
                controller: _titleController,
                decoration: const InputDecoration(labelText: 'ชื่อประกาศ'),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _categoryController,
                decoration: const InputDecoration(labelText: 'หมวดหมู่'),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _descriptionController,
                decoration: const InputDecoration(labelText: 'คำบรรยาย'),
                maxLines: 3,
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _confirmListing,
                child: const Text('ยืนยันร่างประกาศ'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}