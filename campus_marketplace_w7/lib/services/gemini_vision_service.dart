import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import '../models/listing_draft.dart';

class GeminiVisionService {
  static const String _apiKey = String.fromEnvironment('GEMINI_API_KEY');
  static const String _model = 'gemini-3.6-flash';
  static const String _baseUrl =
      'https://generativelanguage.googleapis.com/v1beta/models/$_model:generateContent';

  Future<ListingDraft> analyzeProductImage({
    required File imageFile,
    required String prompt,
  }) async {
    if (_apiKey.isEmpty) {
      throw Exception(
        'ไม่พบ GEMINI_API_KEY กรุณาระบุผ่าน --dart-define=GEMINI_API_KEY=your_key',
      );
    }

    final imageBytes = await imageFile.readAsBytes();
    final imageBase64 = base64Encode(imageBytes);
    final mimeType = _mimeTypeFor(imageFile.path);
    final url = Uri.parse(_baseUrl);
    final body = jsonEncode({
      'contents': [
        {
          'parts': [
            {
              'inlineData': {'mimeType': mimeType, 'data': imageBase64},
            },
            {'text': prompt},
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
          'required': ['title', 'category', 'description'],
        },
      },
    });

    try {
      final response = await http
          .post(
            url,
            headers: {
              'Content-Type': 'application/json',
              'x-goog-api-key': _apiKey,
            },
            body: body,
          )
          .timeout(const Duration(seconds: 60));

      if (response.statusCode == 401 || response.statusCode == 403) {
        throw Exception(
          'Gemini API ปฏิเสธ API key กรุณาสร้าง key ใหม่จาก Google AI Studio และตรวจสอบว่าเปิดใช้ Gemini API แล้ว',
        );
      }
      if (response.statusCode != 200) {
        throw Exception(
          'เกิดข้อผิดพลาดจาก Gemini API (สถานะ ${response.statusCode}): ${response.body}',
        );
      }

      final responseJson = jsonDecode(response.body) as Map<String, dynamic>;
      final candidates = responseJson['candidates'] as List?;
      if (candidates == null || candidates.isEmpty) {
        final blockReason = responseJson['promptFeedback']?['blockReason'];
        throw Exception(_safetyRefusalMessage(blockReason?.toString()));
      }

      final candidate = candidates.first as Map<String, dynamic>;
      final finishReason = candidate['finishReason'] as String?;
      if (finishReason == 'SAFETY' ||
          finishReason == 'PROHIBITED_CONTENT' ||
          finishReason == 'BLOCKLIST') {
        throw Exception(_safetyRefusalMessage(finishReason));
      }

      final parts = candidate['content']?['parts'] as List?;
      final responseText = parts
          ?.map((part) => part['text'])
          .whereType<String>()
          .firstOrNull;
      if (responseText == null) {
        throw Exception('ไม่พบ JSON ในคำตอบจาก Gemini');
      }

      final listingJson = jsonDecode(responseText) as Map<String, dynamic>;
      return ListingDraft.fromJson(listingJson);
    } on TimeoutException {
      throw Exception('การเชื่อมต่อ Gemini API หมดเวลา กรุณาลองใหม่อีกครั้ง');
    } on http.ClientException {
      throw Exception(
        'ไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้ กรุณาตรวจสอบการเชื่อมต่อ',
      );
    } on FormatException {
      throw Exception('ข้อมูลที่ได้รับจาก Gemini ไม่ใช่ JSON ที่ถูกต้อง');
    }
  }

  String _mimeTypeFor(String path) {
    final extension = path.split('.').last.toLowerCase();
    return switch (extension) {
      'png' => 'image/png',
      'webp' => 'image/webp',
      'heic' || 'heif' => 'image/heic',
      _ => 'image/jpeg',
    };
  }

  String _safetyRefusalMessage(String? reason) {
    if (reason == null) {
      return 'AI ไม่สามารถวิเคราะห์ภาพนี้ได้ อาจเข้าข่ายเนื้อหาที่ไม่เหมาะสม ลองใช้ภาพอื่น';
    }
    return 'เนื้อหาที่วิเคราะห์เข้าข่ายไม่ปลอดภัยตามนโยบายของ Gemini กรุณาใช้ภาพอื่น';
  }
}
