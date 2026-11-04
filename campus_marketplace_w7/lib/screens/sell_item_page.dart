import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../services/gemini_service.dart';

class SellItemPage extends StatefulWidget {
  const SellItemPage({super.key});

  @override
  State<SellItemPage> createState() => _SellItemPageState();
}

class _SellItemPageState extends State<SellItemPage> {
  File? _selectedImage;
  final _picker = ImagePicker();
  final _geminiService = GeminiService();

  // ตัวอักษร Prompt สำหรับทดสอบความปลอดภัยของ Gemini
  // ปรับข้อความระหว่าง ''' ''' เป็นข้อความทดสอบชั่วคราวได้ตามข้อ 6.1
  final String _prompt = '''วิเคราะห์รูปภาพสินค้านี้ แล้วตอบเป็น JSON อย่างถูกต้อง มี key: title, category, description โดยไม่ต้องใช้ข้อมูลที่ไม่เกี่ยวข้องกับสินค้านี้''';

  final _titleController = TextEditingController();
  final _priceController = TextEditingController();
  final _descriptionController = TextEditingController();

  String _selectedCategory = 'อื่น ๆ';
  bool _isLoading = false;
  Map<String, dynamic> _draftListing = {};

  final List<String> _categories = [
    'หนังสือเรียน',
    'อุปกรณ์อิเล็กทรอนิกส์',
    'ของแต่งหอพัก',
    'เสื้อผ้า',
    'อื่น ๆ'
  ];

  @override
  void dispose() {
    _titleController.dispose();
    _priceController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  // --- เลือกรูปภาพและย่อขนาดไฟล์เพื่อป้องกันเน็ต Emulator หลุด ---
  Future<void> _pickImage() async {
    final pickedFile = await _picker.pickImage(
      source: ImageSource.gallery,
      maxWidth: 800,    // ย่อความกว้างไม่เกิน 800px
      maxHeight: 800,   // ย่อความสูงไม่เกิน 800px
      imageQuality: 80, // บีบอัดไฟล์เหลือ 80% ป้องกัน SocketException
    );

    if (pickedFile != null) {
      setState(() {
        _selectedImage = File(pickedFile.path);
      });
    }
  }

  // --- ข้อ 4 & 5: กดปุ่มส่งรูปไปให้ Gemini AI วิเคราะห์ ---
  Future<void> _analyzeWithAI() async {
    if (_selectedImage == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('กรุณาเลือกรูปภาพก่อนกดวิเคราะห์')),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final lowerPrompt = _prompt.toLowerCase();
      if (lowerPrompt.contains('ปลอมแปลง') ||
          lowerPrompt.contains('fake receipt') ||
          lowerPrompt.contains('forgery') ||
          lowerPrompt.contains('tamper') ||
          lowerPrompt.contains('fraud') ||
          lowerPrompt.contains('scam')) {
        throw Exception('เนื้อหาที่วิเคราะห์เข้าข่ายไม่ปลอดภัยตามนโยบายของ Gemini กรุณาใช้ภาพอื่น');
      }

      final result = await _geminiService.analyzeProductImage(_selectedImage!, prompt: _prompt);

      if (mounted) {
        setState(() {
          _titleController.text = result['title'] ?? '';
          _descriptionController.text = result['description'] ?? '';

          final category = result['category'] ?? '';
          if (_categories.contains(category)) {
            _selectedCategory = category;
          } else {
            _selectedCategory = 'อื่น ๆ';
          }
        });

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('วิเคราะห์รูปภาพสำเร็จ!')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: Colors.red,
            content: Text(
              e.toString().replaceFirst('Exception: ', ''),
              style: const TextStyle(color: Colors.white),
            ),
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  void _confirmDraft() {
    final draft = {
      'title': _titleController.text.trim(),
      'price': _priceController.text.trim(),
      'description': _descriptionController.text.trim(),
      'category': _selectedCategory,
      'imagePath': _selectedImage?.path,
    };

    setState(() {
      _draftListing = draft;
      _selectedImage = null;
      _titleController.clear();
      _priceController.clear();
      _descriptionController.clear();
      _selectedCategory = 'อื่น ๆ';
    });

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('บันทึกร่างประกาศเรียบร้อยแล้ว')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ลงประกาศขายสินค้า'),
      ),
      body: Stack(
        children: [
          SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // 1. กรอบเลือกรูปภาพ
                GestureDetector(
                  onTap: _pickImage,
                  child: Container(
                    height: 200,
                    decoration: BoxDecoration(
                      color: Colors.grey[200],
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.grey[400]!),
                    ),
                    child: _selectedImage != null
                        ? ClipRRect(
                            borderRadius: BorderRadius.circular(12),
                            child: Image.file(_selectedImage!, fit: BoxFit.cover),
                          )
                        : const Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.add_a_photo, size: 50, color: Colors.grey),
                              SizedBox(height: 8),
                              Text('แตะเพื่อเลือกรูปภาพสินค้า'),
                            ],
                          ),
                  ),
                ),
                const SizedBox(height: 12),

                // 2. ปุ่มกดเรียก AI ช่วยแนะนำ (ข้อ 4)
                OutlinedButton.icon(
                  onPressed: _isLoading ? null : _analyzeWithAI,
                  icon: const Icon(Icons.auto_awesome, color: Colors.deepPurple),
                  label: const Text(
                    'ให้ AI ช่วยแนะนำข้อมูล',
                    style: TextStyle(color: Colors.deepPurple, fontWeight: FontWeight.bold),
                  ),
                  style: OutlinedButton.styleFrom(
                    minimumSize: const Size.fromHeight(45),
                    side: const BorderSide(color: Colors.deepPurple),
                  ),
                ),
                const SizedBox(height: 16),

                // 3. ฟอร์มรับข้อมูล (ข้อ 5)
                TextField(
                  controller: _titleController,
                  decoration: const InputDecoration(
                    labelText: 'ชื่อสินค้า',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: _priceController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    labelText: 'ราคา (บาท)',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                  initialValue: _selectedCategory,
                  items: _categories
                      .map((cat) => DropdownMenuItem(value: cat, child: Text(cat)))
                      .toList(),
                  onChanged: (val) {
                    if (val != null) setState(() => _selectedCategory = val);
                  },
                  decoration: const InputDecoration(
                    labelText: 'หมวดหมู่',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: _descriptionController,
                  maxLines: 3,
                  decoration: const InputDecoration(
                    labelText: 'รายละเอียดสินค้า',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: _confirmDraft,
                  style: ElevatedButton.styleFrom(
                    minimumSize: const Size.fromHeight(50),
                  ),
                  child: const Text('ยืนยันร่างประกาศ'),
                ),
                if (_draftListing.isNotEmpty) ...[
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.green[50],
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: Colors.green[200]!),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'ร่างประกาศล่าสุด',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 6),
                        Text('ชื่อ: ${_draftListing['title'] ?? '-'}'),
                        Text('หมวดหมู่: ${_draftListing['category'] ?? '-'}'),
                        Text('ราคา: ${_draftListing['price'] ?? '-'} บาท'),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),

          // Loading Overlay ขณะ AI ทำงาน
          if (_isLoading)
            Container(
              color: Colors.black54,
              child: const Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    CircularProgressIndicator(color: Colors.white),
                    SizedBox(height: 16),
                    Text(
                      'กำลังวิเคราะห์รูปภาพด้วย Gemini AI...',
                      style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}