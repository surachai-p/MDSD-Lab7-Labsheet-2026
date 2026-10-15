
import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import '../models/listing_draft.dart';

class GeminiVisionService {
  static const String _apiKey =
      String.fromEnvironment('GEMINI_API_KEY');

  // ใช้ชื่อโมเดลที่ตรวจสอบแล้วว่า API key ของคุณเรียกใช้งานได้
  static const String _model = 'gemini-3.8-flash';

  // เปลี่ยนข้อความนี้เป็น Prompt เดียวกับที่ใช้ในส่วนที่ 1
  static const String _prompt = '''
วิเคราะห์ภาพสินค้ามือสองสำหรับประกาศขายในตลาดนักศึกษา
สร้างชื่อสินค้า หมวดหมู่ และคำอธิบายสินค้าเป็นภาษาไทย
หากข้อมูลบางอย่างมองไม่เห็น อย่าคาดเดารายละเอียดที่ไม่ปรากฏในภาพ
''';

  Future<ListingDraft> analyzeProductImage(File imageFile) async {
    if (_apiKey.isEmpty) {
      throw Exception(
        'ไม่พบ GEMINI_API_KEY กรุณาตรวจสอบคำสั่ง flutter run',
      );
    }

    final imageBytes = await imageFile.readAsBytes();
    final base64Image = base64Encode(imageBytes);

    final uri = Uri.parse(
      'https://generativelanguage.googleapis.com/v1beta/'
      'models/$_model:generateContent',
    );

    final response = await http
        .post(
          uri,
          headers: {
            'Content-Type': 'application/json',
            'x-goog-api-key': _apiKey,
          },
          body: jsonEncode({
            'contents': [
              {
                'parts': [
                  {'text': _prompt},
                  {
                    'inline_data': {
                      'mime_type': 'image/jpeg',
                      'data': base64Image,
                    },
                  },
                ],
              },
            ],
            'generationConfig': {
              'responseMimeType': 'application/json',
              'responseSchema': {
                'type': 'OBJECT',
                'properties': {
                  'title': {'type': 'STRING'},
                  'category': {'type': 'STRING'},
                  'description': {'type': 'STRING'},
                },
                'required': [
                  'title',
                  'category',
                  'description',
                ],
              },
            },
          }),
        )
        .timeout(const Duration(seconds: 60));

    if (response.statusCode != 200) {
      debugPrint('Gemini status: ${response.statusCode}');
      debugPrint('Gemini body: ${response.body}');

      throw Exception(
        'Gemini ตอบกลับรหัส ${response.statusCode}: '
        '${response.body}',
      );
    }

    // jsonDecode ครั้งที่ 1: แปลง response จาก API
    final Map<String, dynamic> apiJson =
        jsonDecode(response.body) as Map<String, dynamic>;

    final candidates = apiJson['candidates'] as List<dynamic>?;

    if (candidates == null || candidates.isEmpty) {
      throw Exception('Gemini ไม่ส่งผลการวิเคราะห์กลับมา');
    }

    final candidate = candidates.first as Map<String, dynamic>;
    final content = candidate['content'] as Map<String, dynamic>;
    final parts = content['parts'] as List<dynamic>;

    if (parts.isEmpty) {
      throw Exception('ไม่พบข้อมูลผลการวิเคราะห์');
    }

    final resultText =
        (parts.first as Map<String, dynamic>)['text'] as String?;

    if (resultText == null || resultText.isEmpty) {
      throw Exception('Gemini ส่งผลลัพธ์ว่างเปล่า');
    }

    // jsonDecode ครั้งที่ 2: แปลง JSON ที่ Gemini สร้าง
    final Map<String, dynamic> resultJson =
        jsonDecode(resultText) as Map<String, dynamic>;

    return ListingDraft.fromJson(resultJson);
  }
}
