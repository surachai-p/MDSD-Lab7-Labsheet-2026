import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../services/gemini_vision_service.dart';
import '../models/listing_draft.dart';

class SellItemPage extends StatefulWidget {
  const SellItemPage({super.key});

  @override
  State<SellItemPage> createState() => _SellItemPageState();
}

class _SellItemPageState extends State<SellItemPage> {
  File? _imageFile;
  bool _isLoading = false;
  
  // Controllers สำหรับฟอร์มให้ผู้ใช้ตรวจทานและแก้ไข (Human-in-the-loop)
  final _titleController = TextEditingController();
  final _categoryController = TextEditingController();
  final _descriptionController = TextEditingController();

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

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);
    
    if (pickedFile != null) {
      setState(() {
        _imageFile = File(pickedFile.path);
        // ล้างข้อมูลเก่าเมื่อเปลี่ยนรูปภาพใหม่
        _titleController.clear();
        _categoryController.clear();
        _descriptionController.clear();
      });
    }
  }

  Future<void> _analyzeByAI() async {
    if (_imageFile == null) return;

    setState(() => _isLoading = true); // แสดงสถานะกำลังโหลด

    try {
      final service = GeminiVisionService();
      final resultJson = await service.analyzeProductImage(_imageFile!, _prompt);
      
      final draft = ListingDraft.fromJson(resultJson);
      
      // นำข้อมูลที่ AI วิเคราะห์ได้ มาใส่ในช่อง TextField ให้ผู้ใช้แก้ไข
      setState(() {
        _titleController.text = draft.title;
        _categoryController.text = draft.category;
        _descriptionController.text = draft.description;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString()), backgroundColor: Colors.red),
      );
    } finally {
      setState(() => _isLoading = false); // ปิดสถานะโหลด
    }
  }

  void _submitDraft() {
    if (_titleController.text.isEmpty || _categoryController.text.isEmpty || _descriptionController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('กรุณากรอกข้อมูลให้ครบถ้วนก่อนบันทึก')),
      );
      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('บันทึกร่างประกาศเรียบร้อยแล้ว'),
        backgroundColor: Colors.green,
      ),
    );

    // ล้างหน้าจอกลับสู่สถานะเริ่มต้น
    setState(() {
      _imageFile = null;
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
      appBar: AppBar(title: const Text('ลงประกาศขาย')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (_imageFile != null)
              Image.file(_imageFile!, height: 250, fit: BoxFit.cover)
            else
              Container(
                height: 250,
                color: Colors.grey[200],
                child: const Icon(Icons.image_not_supported, size: 64, color: Colors.grey),
              ),
            
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _pickImage, // ล็อกปุ่มขณะโหลด
              icon: const Icon(Icons.photo_library),
              label: const Text('เลือกรูปภาพสินค้า'),
            ),
            const SizedBox(height: 8),
            
            ElevatedButton.icon(
              onPressed: (_imageFile == null || _isLoading) ? null : _analyzeByAI,
              icon: _isLoading 
                  ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2)) 
                  : const Icon(Icons.auto_awesome),
              label: Text(_isLoading ? 'AI กำลังวิเคราะห์ภาพสินค้า...' : 'ให้ AI ช่วยแนะนำ'),
            ),
            const Divider(height: 32),
            
            // ฟอร์มสำหรับการตรวจทานและแก้ไข (Human-in-the-loop)
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(labelText: 'ชื่อประกาศ', border: OutlineInputBorder()),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _categoryController,
              decoration: const InputDecoration(labelText: 'หมวดหมู่', border: OutlineInputBorder()),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _descriptionController,
              maxLines: 4,
              decoration: const InputDecoration(labelText: 'คำบรรยายสินค้า', border: OutlineInputBorder()),
            ),
            
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _submitDraft,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('ยืนยันร่างประกาศ', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }
}