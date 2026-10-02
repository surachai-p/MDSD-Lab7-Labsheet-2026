import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class GeminiVisionService {
  static const _apiKey = String.fromEnvironment('GEMINI_API_KEY');
  static const _model = 'gemini-flash-lite-latest';
  static const _baseUrl =
      'https://generativelanguage.googleapis.com/v1beta/models/$_model:generateContent';

  Future<String> analyzeProductImage(File imageFile, String prompt) async {
    final uri = Uri.parse('$_baseUrl?key=$_apiKey');

    try {
      // 1. อ่านไฟล์ภาพเป็นไบต์ แล้วเข้ารหัส Base64
      final imageBytes = await imageFile.readAsBytes();
      final base64Image = base64Encode(imageBytes);

      final response = await http
          .post(
            uri,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'contents': [
                {
                  'parts': [
                    {'text': prompt},
                    {
                      'inline_data': {
                        'mime_type': 'image/jpeg',
                        'data': base64Image,
                      }
                    }
                  ]
                }
              ],
              // บังคับให้ตอบกลับเป็น JSON ตามโครงสร้างที่กำหนด
              'generationConfig': {
                'responseMimeType': 'application/json',
                'responseSchema': {
                  'type': 'OBJECT',
                  'properties': {
                    'title': {'type': 'STRING'},
                    'category': {'type': 'STRING'},
                    'description': {'type': 'STRING'},
                  },
                  'required': ['title', 'category', 'description'],
                },
              },
            }),
          )
          .timeout(const Duration(seconds: 30));

      if (response.statusCode != 200) {
        throw Exception('เซิร์ฟเวอร์ Gemini ตอบกลับผิดพลาด (รหัส ${response.statusCode})');
      }

      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final candidates = data['candidates'] as List<dynamic>?;

      // เช็คว่า candidates มีข้อมูลจริง ก่อนเข้าถึง [0]
      if (candidates == null || candidates.isEmpty) {
        throw Exception('AI ไม่สามารถวิเคราะห์ภาพนี้ได้ อาจเข้าข่ายเนื้อหาที่ไม่เหมาะสม ลองใช้ภาพอื่น');
      }

      final firstCandidate = candidates[0] as Map<String, dynamic>;
      final finishReason = firstCandidate['finishReason'] as String?;

      if (finishReason == 'SAFETY') {
        throw Exception('เนื้อหาที่วิเคราะห์เข้าข่ายไม่ปลอดภัยตามนโยบายของ Gemini กรุณาใช้ภาพอื่น');
      }

      final content = firstCandidate['content'] as Map<String, dynamic>;
      final parts = content['parts'] as List<dynamic>;
      // jsonDecode ชั้นที่ 1: แกะ response ทั้งก้อนของ Gemini
      final jsonText = parts[0]['text'] as String;
      // jsonDecode ชั้นที่ 2: แกะ text ที่เป็น JSON ของ title/category/description
      return jsonText;
    } on TimeoutException {
      throw Exception('การเชื่อมต่อหมดเวลา กรุณาลองใหม่อีกครั้ง');
    } on http.ClientException {
      throw Exception('ไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้ กรุณาตรวจสอบการเชื่อมต่อ');
    } on FormatException {
      throw Exception('ข้อมูลที่ได้รับจาก Gemini ไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง');
    } catch (e) {
      rethrow;
    }
  }
}