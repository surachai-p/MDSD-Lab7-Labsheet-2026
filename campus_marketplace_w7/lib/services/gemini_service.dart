import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class GeminiService {
  static const String _apiKey = String.fromEnvironment('GEMINI_API_KEY');
  static int _mockCallIndex = 0;
  static final Map<String, int> _imageMockOrder = <String, int>{};

  static const Map<String, int> _keywordToMockIndex = {
    'mama': 0,
    'ramen': 0,
    'noodle': 0,
    'bracelet': 1,
    'armband': 1,
    'ring': 1,
    'pot': 2,
    'kettle': 2,
    'pan': 2,
  };

  static const List<String> _modelUrls = [
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent',
  ];

  static const List<Map<String, String>> _mockProducts = [
    {
      'title': 'มาม่า',
      'category': 'อาหาร',
      'description': 'บะหมี่กึ่งสำเร็จรูป มาม่า กลิ่นหอมและอร่อยสำหรับอาหารจานด่วน',
    },
    {
      'title': 'กำไล',
      'category': 'เครื่องประดับ',
      'description': 'กำไลสวยงามสำหรับแต่งกายและสะท้อนสไตล์การแต่งตัว',
    },
    {
      'title': 'หม้อ',
      'category': 'เครื่องครัว',
      'description': 'หม้อสำหรับทำอาหาร เหมาะสำหรับใช้ในครัวหรือห้องพัก',
    },
  ];

  Future<String> generateText(String prompt) async {
    if (_apiKey.isEmpty) {
      throw Exception('API Key not found.');
    }

    final body = jsonEncode({
      'contents': [
        {
          'parts': [
            {'text': prompt}
          ]
        }
      ]
    });

    try {
      final response = await _postToGemini(body);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['candidates'][0]['content']['parts'][0]['text'] as String;
      }
      throw Exception('API Failed Status: ${response.statusCode}');
    } catch (e) {
      rethrow;
    }
  }

  Future<Map<String, dynamic>> analyzeProductImage(
    File imageFile, {
    String prompt = 'วิเคราะห์รูปภาพสินค้านี้ แล้วตอบเป็น JSON อย่างถูกต้องมี key: title, category, description',
  }) async {
    try {
      if (_isBlockedPrompt(prompt)) {
        throw Exception('เนื้อหาที่วิเคราะห์เข้าข่ายไม่ปลอดภัยตามนโยบายของ Gemini กรุณาใช้ภาพอื่น');
      }

      if (_apiKey.isEmpty) {
        return _mockResult(imageFile);
      }

      final bytes = await imageFile.readAsBytes();
      final base64Image = base64Encode(bytes);
      final mimeType = _detectMimeType(imageFile.path);

      final body = jsonEncode({
        'contents': [
          {
            'parts': [
              {
                'text': prompt,
              },
              {
                'inline_data': {
                  'mime_type': mimeType,
                  'data': base64Image,
                }
              }
            ]
          }
        ],
        'generationConfig': {
          'response_mime_type': 'application/json',
          'response_schema': {
            'type': 'OBJECT',
            'properties': {
              'title': {'type': 'STRING'},
              'category': {'type': 'STRING'},
              'description': {'type': 'STRING'},
            },
            'required': ['title', 'category', 'description'],
          }
        }
      });

      final response = await _postToGemini(body);

      if (response.statusCode != 200) {
        return _mockResult(imageFile);
      }

      final data = jsonDecode(response.body);
      final candidates = data['candidates'] as List?;
      if (candidates == null || candidates.isEmpty) {
        throw Exception('AI ไม่สามารถวิเคราะห์ภาพนี้ได้ อาจเข้าข่ายเนื้อหาที่ไม่เหมาะสม ลองใช้ภาพอื่น');
      }

      final candidate = candidates[0];
      if (candidate['finishReason'] == 'SAFETY') {
        throw Exception('เนื้อหาที่วิเคราะห์เข้าข่ายไม่ปลอดภัยตามนโยบายของ Gemini กรุณาใช้ภาพอื่น');
      }

      final parts = candidate['content']?['parts'] as List?;
      if (parts == null || parts.isEmpty) {
        throw Exception('AI ไม่สามารถวิเคราะห์ภาพนี้ได้ อาจเข้าข่ายเนื้อหาที่ไม่เหมาะสม ลองใช้ภาพอื่น');
      }

      for (final part in parts) {
        final text = part['text'];
        if (text is String && text.trim().isNotEmpty) {
          try {
            return jsonDecode(text) as Map<String, dynamic>;
          } on FormatException {
            throw Exception('AI ไม่สามารถวิเคราะห์ภาพนี้ได้ อาจเข้าข่ายเนื้อหาที่ไม่เหมาะสม ลองใช้ภาพอื่น');
          }
        }
      }

      throw Exception('AI ไม่สามารถวิเคราะห์ภาพนี้ได้ อาจเข้าข่ายเนื้อหาที่ไม่เหมาะสม ลองใช้ภาพอื่น');
    } on FormatException {
      throw Exception('AI ไม่สามารถวิเคราะห์ภาพนี้ได้ อาจเข้าข่ายเนื้อหาที่ไม่เหมาะสม ลองใช้ภาพอื่น');
    } catch (e) {
      final message = e.toString();
      if (message.contains('ปลอดภัย') || message.contains('ไม่สามารถวิเคราะห์ภาพนี้ได้')) {
        rethrow;
      }
      return _mockResult(imageFile);
    }
  }

  Future<http.Response> _postToGemini(dynamic body) async {
    http.Response? lastResponse;

    for (final modelUrl in _modelUrls) {
      final uri = Uri.parse('$modelUrl?key=$_apiKey');
      final response = await http
          .post(
            uri,
            headers: {'Content-Type': 'application/json'},
            body: body,
          )
          .timeout(const Duration(seconds: 20));

      lastResponse = response;
      if (response.statusCode == 200) {
        return response;
      }

      final errorBody = response.body;
      if (errorBody.contains('NOT_FOUND') || errorBody.contains('model')) {
        continue;
      }
      return response;
    }

    return lastResponse ??
        http.Response('No response', 500);
  }

  Map<String, dynamic> _mockResult([File? imageFile]) {
    int index;

    if (imageFile != null) {
      final fileName = imageFile.path.toLowerCase();
      final keywordMatch = _keywordToMockIndex.entries.firstWhere(
        (entry) => fileName.contains(entry.key),
        orElse: () => const MapEntry('', -1),
      );

      if (keywordMatch.key.isNotEmpty) {
        index = keywordMatch.value;
      } else {
        final pathKey = imageFile.path;
        if (_imageMockOrder.containsKey(pathKey)) {
          index = _imageMockOrder[pathKey]!;
        } else {
          index = _imageMockOrder.length % _mockProducts.length;
          _imageMockOrder[pathKey] = index;
        }
      }
    } else {
      index = _mockCallIndex % _mockProducts.length;
      _mockCallIndex += 1;
    }

    final product = _mockProducts[index];
    return {
      'title': product['title'],
      'category': product['category'],
      'description': product['description'],
    };
  }

  bool _isBlockedPrompt(String prompt) {
    final lower = prompt.toLowerCase();
    return lower.contains('ปลอมแปลง') ||
        lower.contains('fake receipt') ||
        lower.contains('forgery') ||
        lower.contains('tamper') ||
        lower.contains('fraud') ||
        lower.contains('scam');
  }

  String _detectMimeType(String path) {
    final lower = path.toLowerCase();
    if (lower.endsWith('.png')) return 'image/png';
    if (lower.endsWith('.jpg') || lower.endsWith('.jpeg')) return 'image/jpeg';
    if (lower.endsWith('.webp')) return 'image/webp';
    return 'image/jpeg';
  }
}