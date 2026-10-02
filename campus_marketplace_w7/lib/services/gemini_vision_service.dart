import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import '../models/listing_draft.dart';

class GeminiVisionService {
  static const _apiKey = String.fromEnvironment('GEMINI_API_KEY', defaultValue: 'YOUR_API_KEY');
  static const _model = 'gemini-3.8-flash';
  static const _baseUrl = 'https://generativelanguage.googleapis.com/v1beta/models/$_model:generateContent';

  Future<ListingDraft> analyzeProductImage({
    dynamic imageFile,
    Uint8List? imageBytes,
    required String prompt,
    String mimeType = 'image/jpeg',
  }) async {
    // 1. อ่านข้อมูลภาพเป็นไบต์
    Uint8List bytes;
    if (imageBytes != null) {
      bytes = imageBytes;
    } else if (imageFile != null) {
      bytes = await imageFile.readAsBytes();
    } else {
      throw Exception('กรุณาระบุไฟล์รูปภาพหรือไบต์ของภาพ');
    }

    // 2. แปลงเป็น Base64
    final base64Image = base64Encode(bytes);

    // 3. กำหนด URI และ Request Body พร้อม responseSchema
    final uri = Uri.parse('$_baseUrl?key=$_apiKey');

    final payload = {
      'contents': [
        {
          'parts': [
            {'text': prompt},
            {
              'inlineData': {
                'mimeType': mimeType,
                'data': base64Image,
              }
            }
          ]
        }
      ],
      'generationConfig': {
        'responseMimeType': 'application/json',
        'responseSchema': {
          'type': 'OBJECT',
          'properties': {
            'title': {
              'type': 'STRING',
              'description': 'ชื่อประกาศสั้นกระชับ ไม่เกิน 40 ตัวอักษร',
            },
            'category': {
              'type': 'STRING',
              'description': 'หมวดหมู่ที่เหมาะสมที่สุด เลือกจาก: หนังสือเรียน, อุปกรณ์อิเล็กทรอนิกส์, ของแต่งหอพัก, เสื้อผ้า, อื่นๆ',
            },
            'description': {
              'type': 'STRING',
              'description': 'คำบรรยายสินค้า 2-3 ประโยค ที่ดึงดูดผู้ซื้อและบอกสภาพของสินค้าตามที่เห็นในภาพ',
            },
          },
          'required': ['title', 'category', 'description'],
        },
      },
    };

    try {
      final response = await http
          .post(
            uri,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(payload),
          )
          .timeout(const Duration(seconds: 30));

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        final candidates = data['candidates'] as List<dynamic>?;

        if (candidates == null || candidates.isEmpty) {
          throw Exception('AI ไม่สามารถวิเคราะห์ภาพนี้ได้ อาจเข้าข่ายเนื้อหาที่ไม่เหมาะสม ลองใช้ภาพอื่น');
        }

        final candidate = candidates[0] as Map<String, dynamic>;
        final finishReason = candidate['finishReason'] as String?;

        if (finishReason == 'SAFETY') {
          throw Exception('เนื้อหาที่วิเคราะห์เข้าข่ายไม่ปลอดภัยตามนโยบายของ Gemini กรุณาใช้ภาพอื่น');
        }

        final content = candidate['content'] as Map<String, dynamic>?;
        final parts = content?['parts'] as List<dynamic>?;

        if (parts == null || parts.isEmpty) {
          throw Exception('ไม่พบผลลัพธ์ข้อความจาก Gemini');
        }

        final rawText = parts[0]['text'] as String;

        // ถอดรหัส JSON ชั้นที่สอง (Double jsonDecode)
        final Map<String, dynamic> parsedJson = jsonDecode(rawText);
        return ListingDraft.fromJson(parsedJson);
      } else if (response.statusCode == 400) {
        // ตรวจสอบกรณี prompt โดน safety block หรือ request ผิด
        final Map<String, dynamic> errData = jsonDecode(response.body);
        final errMsg = errData['error']?['message'] ?? '400 Bad Request';
        if (errMsg.toString().toLowerCase().contains('safety') ||
            errMsg.toString().toLowerCase().contains('blocked')) {
          throw Exception('เนื้อหาที่วิเคราะห์เข้าข่ายไม่ปลอดภัยตามนโยบายของ Gemini กรุณาใช้ภาพอื่น');
        }
        throw Exception('คำขอไม่ถูกต้องหรือ API Key ผิดพลาด: $errMsg');
      } else if (response.statusCode == 403) {
        throw Exception('สิทธิ์การเข้าถึงถูกปฏิเสธ (403 Forbidden) กรุณาตรวจสอบ API Key');
      } else if (response.statusCode == 429) {
        throw Exception('ใช้งานเกินโควตาคำขอฟรีต่อนาที (429 Too Many Requests) กรุณารอสักครู่');
      } else if (response.statusCode == 503) {
        throw Exception('เซิร์ฟเวอร์ Gemini กำลังทำงานหนักชั่วคราว (503 Service Unavailable)');
      }

      throw Exception('ไม่สามารถวิเคราะห์ภาพได้ (สถานะ ${response.statusCode})');
    } on TimeoutException {
      throw Exception('การวิเคราะห์ภาพหมดเวลา (30 วินาที) กรุณาลองใหม่อีกครั้ง');
    } on http.ClientException {
      throw Exception('ไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้ กรุณาตรวจสอบการเชื่อมต่อ');
    } on FormatException {
      throw Exception('โครงสร้าง JSON ที่ได้รับจาก Gemini ไม่ถูกต้อง');
    } catch (e) {
      rethrow;
    }
  }
}
