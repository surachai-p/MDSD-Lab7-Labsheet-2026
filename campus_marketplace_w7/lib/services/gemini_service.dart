import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class GeminiService {
  static const _apiKey = String.fromEnvironment('GEMINI_API_KEY', defaultValue: 'YOUR_API_KEY');
  static const _model = 'gemini-3.8-flash';
  static const _baseUrl = 'https://generativelanguage.googleapis.com/v1beta/models/$_model:generateContent';

  Future<String> generateText(String prompt) async {
    final uri = Uri.parse('$_baseUrl?key=$_apiKey');

    try {
      final response = await http
          .post(
            uri,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'contents': [
                {
                  'parts': [
                    {'text': prompt}
                  ]
                }
              ]
            }),
          )
          .timeout(const Duration(seconds: 20));

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        final candidates = data['candidates'] as List<dynamic>?;

        if (candidates == null || candidates.isEmpty) {
          throw Exception('Gemini ไม่ส่งคำตอบกลับมา (candidates ว่างเปล่า)');
        }

        final content = candidates[0]['content'] as Map<String, dynamic>?;
        final parts = content?['parts'] as List<dynamic>?;
        if (parts == null || parts.isEmpty) {
          throw Exception('ไม่พบเนื้อหาข้อความในคำตอบของ Gemini');
        }

        return parts[0]['text'] as String;
      } else if (response.statusCode == 400) {
        throw Exception('API Key ไม่ถูกต้อง หรือรูปแบบคำขอผิดพลาด (400 Bad Request)');
      } else if (response.statusCode == 403) {
        throw Exception('สิทธิ์การเข้าถึงถูกปฏิเสธ (403 Forbidden) ตรวจสอบ Gemini API Key');
      } else if (response.statusCode == 429) {
        throw Exception('ใช้งานเกินโควตาคำขอที่กำหนด (429 Too Many Requests)');
      } else if (response.statusCode == 503) {
        throw Exception('เซิร์ฟเวอร์ Gemini กำลังทำงานหนักชั่วคราว (503 Service Unavailable)');
      }

      throw Exception('เรียกใช้งาน Gemini API ไม่สำเร็จ (สถานะ ${response.statusCode})');
    } on TimeoutException {
      throw Exception('การเชื่อมต่อกับ Gemini API หมดเวลา (20 วินาที) กรุณาลองใหม่อีกครั้ง');
    } on http.ClientException {
      throw Exception('ไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้ กรุณาตรวจสอบการเชื่อมต่อ');
    } on FormatException {
      throw Exception('ข้อมูล JSON ที่ได้รับจาก Gemini API ไม่ถูกต้อง');
    } catch (e) {
      rethrow;
    }
  }
}
