
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
  File? _image;
  ListingDraft? _draft;
  ListingDraft? _confirmedDraft;

  bool _isAnalyzing = false;
  String? _errorMessage;

  final TextEditingController _titleController =
      TextEditingController();

  final TextEditingController _categoryController =
      TextEditingController();

  final TextEditingController _descriptionController =
      TextEditingController();

  @override
  void dispose() {
    _titleController.dispose();
    _categoryController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  Future<void> _pickImage() async {
    try {
      final pickedFile = await ImagePicker().pickImage(
        source: ImageSource.gallery,
      );

      if (pickedFile == null || !mounted) return;

      setState(() {
        _image = File(pickedFile.path);
        _draft = null;
        _errorMessage = null;

        _titleController.clear();
        _categoryController.clear();
        _descriptionController.clear();
      });
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('เลือกรูปไม่สำเร็จ: $e')),
      );
    }
  }

  Future<void> _analyzeImage() async {
    if (_image == null || _isAnalyzing) return;

    setState(() {
      _isAnalyzing = true;
      _draft = null;
      _errorMessage = null;
    });

    try {
      final result = await GeminiVisionService()
          .analyzeProductImage(_image!);

      if (!mounted) return;

      setState(() {
        _draft = result;

        // นำผล AI ใส่ฟอร์มเพื่อให้ผู้ใช้แก้ไขได้
        _titleController.text = result.title;
        _categoryController.text = result.category;
        _descriptionController.text = result.description;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        _errorMessage = e.toString();
      });
    } finally {
      if (mounted) {
        setState(() {
          _isAnalyzing = false;
        });
      }
    }
  }

  void _confirmDraft() {
    if (_draft == null) return;

    // เก็บค่าจากฟอร์มหลังผู้ใช้ตรวจทานหรือแก้ไขแล้ว
    final finalDraft = ListingDraft(
      title: _titleController.text.trim(),
      category: _categoryController.text.trim(),
      description: _descriptionController.text.trim(),
    );

    if (finalDraft.title.isEmpty ||
        finalDraft.category.isEmpty ||
        finalDraft.description.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('กรุณากรอกข้อมูลให้ครบทุกช่อง'),
        ),
      );
      return;
    }

    setState(() {
      // เก็บร่างที่ยืนยันไว้ใน State ของแอป
      _confirmedDraft = finalDraft;

      // ล้างข้อมูลเพื่อเริ่มประกาศใหม่
      _image = null;
      _draft = null;
      _errorMessage = null;

      _titleController.clear();
      _categoryController.clear();
      _descriptionController.clear();
    });

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('บันทึกร่างประกาศเรียบร้อยแล้ว'),
      ),
    );

    // ไม่ใช้ Navigator.pop()
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ลงประกาศขายสินค้า'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              height: 260,
              color: Colors.grey.shade200,
              alignment: Alignment.center,
              child: _image != null
                  ? Image.file(
                      _image!,
                      fit: BoxFit.contain,
                    )
                  : const Icon(
                      Icons.image,
                      size: 80,
                      color: Colors.grey,
                    ),
            ),

            const SizedBox(height: 16),

            ElevatedButton.icon(
              onPressed: _isAnalyzing ? null : _pickImage,
              icon: const Icon(Icons.photo_library),
              label: const Text('เลือกรูปภาพสินค้า'),
            ),

            const SizedBox(height: 8),

            ElevatedButton.icon(
              onPressed: _image == null || _isAnalyzing
                  ? null
                  : _analyzeImage,
              icon: const Icon(Icons.auto_awesome),
              label: const Text('ให้ AI ช่วยแนะนำ'),
            ),

            if (_isAnalyzing) ...[
              const SizedBox(height: 20),
              const Center(
                child: CircularProgressIndicator(),
              ),
              const SizedBox(height: 8),
              const Center(
                child: Text('AI กำลังวิเคราะห์ภาพสินค้า...'),
              ),
            ],

            if (_errorMessage != null) ...[
              const SizedBox(height: 16),
              Text(
                'วิเคราะห์ไม่สำเร็จ\n$_errorMessage',
                style: const TextStyle(color: Colors.red),
              ),
            ],

            if (_draft != null) ...[
              const SizedBox(height: 24),

              const Text(
                'ตรวจทานและแก้ไขร่างประกาศ',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 8),

              const Text(
                'AI ช่วยแนะนำข้อมูลเบื้องต้น '
                'กรุณาตรวจสอบก่อนยืนยัน',
              ),

              const SizedBox(height: 16),

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
                  labelText: 'คำบรรยายสินค้า',
                  alignLabelWithHint: true,
                  border: OutlineInputBorder(),
                ),
              ),

              const SizedBox(height: 16),

              ElevatedButton.icon(
                onPressed: _confirmDraft,
                icon: const Icon(Icons.check_circle),
                label: const Text('ยืนยันร่างประกาศ'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
