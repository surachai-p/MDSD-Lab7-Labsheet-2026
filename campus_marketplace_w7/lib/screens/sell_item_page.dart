
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../models/listing_draft.dart';
import '../repositories/listing_draft_repository.dart';
import '../services/gemini_vision_service.dart';
import 'my_drafts_page.dart';

class SellItemPage extends StatefulWidget {
  final ListingDraftRepository draftRepository;

  const SellItemPage({
    super.key,
    required this.draftRepository,
  });

  @override
  State<SellItemPage> createState() => _SellItemPageState();
}

class _SellItemPageState extends State<SellItemPage> {
  final ImagePicker _picker = ImagePicker();
  final GeminiVisionService _visionService = GeminiVisionService();

  static const String _prompt = '''
คุณคือผู้ช่วยวิเคราะห์รูปภาพสินค้าเพื่อสร้างประกาศขายสินค้าออนไลน์

โปรดวิเคราะห์รูปภาพสินค้าและตอบเป็นภาษาไทย

ข้อกำหนด:
1. title: ชื่อสินค้าสั้น กระชับ
2. category: หมวดหมู่สินค้าที่เหมาะสม
3. description: คำบรรยายจากสิ่งที่มองเห็นในภาพเท่านั้น
4. ห้ามเดายี่ห้อ รุ่น ราคา หรือคุณสมบัติที่มองไม่เห็น
5. หากไม่แน่ใจ ให้ใช้คำอธิบายทั่วไป
6. ตอบกลับเป็น JSON ที่ถูกต้องเท่านั้น

รูปแบบคำตอบ:
{
  "title": "ชื่อสินค้า",
  "category": "หมวดหมู่สินค้า",
  "description": "คำบรรยายสินค้า"
}
''';

  final TextEditingController _titleController =
      TextEditingController();
  final TextEditingController _categoryController =
      TextEditingController();
  final TextEditingController _descriptionController =
      TextEditingController();

  File? _imageFile;
  ListingDraft? _draft;
  String? _errorMessage;

  bool _isAnalyzing = false;
  bool _isSavingDraft = false;

  // เลือกรูปภาพสินค้า
  Future<void> _pickImage() async {
    if (_isAnalyzing || _isSavingDraft) return;

    try {
      final XFile? pickedFile = await _picker.pickImage(
        source: ImageSource.gallery,
      );

      if (!mounted || pickedFile == null) return;

      setState(() {
        _imageFile = File(pickedFile.path);
        _draft = null;
        _errorMessage = null;

        _titleController.clear();
        _categoryController.clear();
        _descriptionController.clear();
      });
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('เลือกรูปภาพไม่สำเร็จ: $e'),
        ),
      );
    }
  }

  // วิเคราะห์รูปภาพด้วย Gemini API
  Future<void> _analyzeProductImage() async {
    if (_imageFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('กรุณาเลือกรูปภาพสินค้าก่อน'),
        ),
      );
      return;
    }

    if (_isAnalyzing || _isSavingDraft) return;

    final File imageToAnalyze = _imageFile!;

    setState(() {
      _isAnalyzing = true;
      _draft = null;
      _errorMessage = null;
    });

    try {
      final ListingDraft result =
          await _visionService.analyzeProductImage(
        imageToAnalyze,
        prompt: _prompt,
      );

      if (!mounted) return;

      setState(() {
        _draft = result;
        _titleController.text = result.title;
        _categoryController.text = result.category;
        _descriptionController.text = result.description;
        _isAnalyzing = false;
        _errorMessage = null;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        _draft = null;
        _isAnalyzing = false;
        _errorMessage =
            'AI ไม่สามารถวิเคราะห์รูปภาพได้ในขณะนี้\n'
            'คุณสามารถกรอกข้อมูลสินค้าด้วยตนเองได้\n'
            'รายละเอียดข้อผิดพลาด: $e';
      });
    }
  }

  // บันทึกร่างหลังผู้ใช้ตรวจสอบข้อมูลแล้ว
  Future<void> _confirmDraft() async {
    if (_isAnalyzing || _isSavingDraft) return;

    final File? image = _imageFile;

    if (image == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('กรุณาเลือกรูปภาพสินค้าก่อน'),
        ),
      );
      return;
    }

    final String title = _titleController.text.trim();
    final String category = _categoryController.text.trim();
    final String description =
        _descriptionController.text.trim();

    if (title.isEmpty ||
        category.isEmpty ||
        description.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'กรุณากรอกชื่อสินค้า หมวดหมู่ และคำบรรยายให้ครบ',
          ),
        ),
      );
      return;
    }

    final ListingDraft draft = ListingDraft.fromJson({
      'title': title,
      'category': category,
      'description': description,
    });

    setState(() {
      _isSavingDraft = true;
    });

    try {
      await widget.draftRepository.saveDraft(
        draft,
        image.path,
      );

      if (!mounted) return;

      setState(() {
        _imageFile = null;
        _draft = null;
        _errorMessage = null;

        _titleController.clear();
        _categoryController.clear();
        _descriptionController.clear();

        _isSavingDraft = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('บันทึกร่างประกาศเรียบร้อยแล้ว'),
        ),
      );
    } catch (e) {
      if (!mounted) return;

      setState(() {
        _isSavingDraft = false;
        _errorMessage = 'บันทึกร่างประกาศไม่สำเร็จ: $e';
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('บันทึกร่างประกาศไม่สำเร็จ: $e'),
        ),
      );
    }
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
    // ปิดปุ่มเฉพาะช่วงที่กำลังทำงาน
    final bool isBusy = _isAnalyzing || _isSavingDraft;

    // แก้ไขข้อมูลได้เมื่อเลือกรูปแล้วและไม่ได้กำลังทำงาน
    final bool canEdit = _imageFile != null && !isBusy;

    return Scaffold(
      appBar: AppBar(
        title: const Text('ลงประกาศขายสินค้า'),
        centerTitle: true,
        actions: [
          IconButton(
            tooltip: 'ร่างประกาศของฉัน',
            icon: const Icon(Icons.history),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute<void>(
                  builder: (_) => MyDraftsPage(
                    repository: widget.draftRepository,
                  ),
                ),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'รูปภาพสินค้า',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),

            Container(
              height: 240,
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.grey.shade100,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: Colors.grey.shade400,
                ),
              ),
              child: _imageFile == null
                  ? const Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.image_outlined,
                          size: 64,
                          color: Colors.grey,
                        ),
                        SizedBox(height: 8),
                        Text(
                          'ยังไม่ได้เลือกรูปภาพ',
                          style: TextStyle(color: Colors.grey),
                        ),
                      ],
                    )
                  : ClipRRect(
                      borderRadius: BorderRadius.circular(12),
                      child: Image.file(
                        _imageFile!,
                        fit: BoxFit.contain,
                        width: double.infinity,
                      ),
                    ),
            ),

            const SizedBox(height: 20),

            // สำคัญ: ปุ่มนี้กดได้แม้ยังไม่มีรูปภาพ
            ElevatedButton.icon(
              onPressed: isBusy ? null : _pickImage,
              icon: const Icon(Icons.photo_library_outlined),
              label: const Text('เลือกรูปภาพสินค้า'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),

            const SizedBox(height: 16),

            // ปุ่ม AI กดได้เมื่อเลือกรูปภาพแล้ว
            OutlinedButton.icon(
              onPressed: canEdit ? _analyzeProductImage : null,
              icon: const Icon(Icons.auto_awesome),
              label: const Text('ให้ AI ช่วยแนะนำ'),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),

            const SizedBox(height: 20),

            if (_isAnalyzing)
              const Card(
                child: Padding(
                  padding: EdgeInsets.all(20),
                  child: Column(
                    children: [
                      CircularProgressIndicator(),
                      SizedBox(height: 16),
                      Text(
                        'AI กำลังวิเคราะห์ภาพสินค้า...',
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ),

            if (_isSavingDraft)
              const Card(
                child: Padding(
                  padding: EdgeInsets.all(20),
                  child: Column(
                    children: [
                      CircularProgressIndicator(),
                      SizedBox(height: 16),
                      Text(
                        'กำลังบันทึกร่างประกาศ...',
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ),

            // แสดงฟอร์มหลังเลือกรูป แม้ AI วิเคราะห์ไม่สำเร็จ
            if (_imageFile != null && !_isAnalyzing)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            _draft != null
                                ? Icons.check_circle
                                : Icons.edit_note,
                            color: _draft != null
                                ? Colors.green
                                : Colors.orange,
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              _draft != null
                                  ? 'ผลการวิเคราะห์จาก AI'
                                  : 'กรอกข้อมูลสินค้าด้วยตนเอง',
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),

                      const SizedBox(height: 8),

                      Text(
                        _draft != null
                            ? 'ตรวจสอบและแก้ไขข้อมูลก่อนบันทึกร่าง'
                            : 'AI ยังวิเคราะห์ไม่ได้ กรุณากรอกข้อมูลด้วยตนเอง',
                        style: const TextStyle(color: Colors.grey),
                      ),

                      const Divider(height: 24),

                      const Text(
                        'ชื่อประกาศ',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 6),
                      TextField(
                        controller: _titleController,
                        enabled: canEdit,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          hintText: 'กรอกชื่อประกาศ',
                        ),
                        maxLines: 2,
                      ),

                      const SizedBox(height: 16),

                      const Text(
                        'หมวดหมู่',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 6),
                      TextField(
                        controller: _categoryController,
                        enabled: canEdit,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          hintText: 'กรอกหมวดหมู่',
                        ),
                      ),

                      const SizedBox(height: 16),

                      const Text(
                        'คำบรรยาย',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 6),
                      TextField(
                        controller: _descriptionController,
                        enabled: canEdit,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          hintText: 'กรอกคำบรรยายสินค้า',
                        ),
                        maxLines: 5,
                      ),

                      const SizedBox(height: 20),

                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: canEdit ? _confirmDraft : null,
                          icon: const Icon(Icons.check),
                          label: const Text('ยืนยันร่างประกาศ'),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(
                              vertical: 16,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),

            if (_errorMessage != null)
              Card(
                color: Colors.orange.shade50,
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Row(
                        children: [
                          Icon(
                            Icons.info_outline,
                            color: Colors.deepOrange,
                          ),
                          SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              'เกิดข้อผิดพลาด',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.deepOrange,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      SelectableText(_errorMessage!),
                      const SizedBox(height: 12),
                      Align(
                        alignment: Alignment.centerRight,
                        child: TextButton.icon(
                          onPressed:
                              canEdit ? _analyzeProductImage : null,
                          icon: const Icon(Icons.refresh),
                          label: const Text('ลองวิเคราะห์อีกครั้ง'),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
