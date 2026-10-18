
import 'package:flutter/foundation.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  // Google Sign-In
  final GoogleSignIn _googleSignIn = GoogleSignIn.instance;
  bool _googleReady = false;

  Future<void> _ensureGoogleReady() async {
    if (_googleReady) return;

    await _googleSignIn.initialize();
    _googleReady = true;
  }

  Future<void> signUp({
    required String email,
    required String password,
  }) async {
    try {
      await _auth.createUserWithEmailAndPassword(
        email: email.trim(),
        password: password,
      );
    } on FirebaseAuthException catch (e) {
      throw Exception(_getThaiErrorMessage(e.code));
    } catch (_) {
      throw Exception('สมัครสมาชิกไม่สำเร็จ กรุณาลองใหม่อีกครั้ง');
    }
  }

  Future<void> signIn({
    required String email,
    required String password,
  }) async {
    try {
      await _auth.signInWithEmailAndPassword(
        email: email.trim(),
        password: password,
      );
    } on FirebaseAuthException catch (e) {
      throw Exception(_getThaiErrorMessage(e.code));
    } catch (_) {
      throw Exception('เข้าสู่ระบบไม่สำเร็จ กรุณาลองใหม่อีกครั้ง');
    }
  }

  Future<void> signInWithGoogle() async {
    try {
      await _ensureGoogleReady();

      final googleUser = await _googleSignIn.authenticate();
      final idToken = googleUser.authentication.idToken;

      final authorization = await googleUser.authorizationClient
          .authorizationForScopes(['email']);

      final credential = GoogleAuthProvider.credential(
        idToken: idToken,
        accessToken: authorization?.accessToken,
      );

      await _auth.signInWithCredential(credential);
    } on FirebaseAuthException catch (e) {
      throw Exception(_getThaiErrorMessage(e.code));
    } catch (e, stackTrace) {
      debugPrint('Google sign-in failed: $e');
      debugPrintStack(stackTrace: stackTrace);
      throw Exception(
        'เข้าสู่ระบบด้วย Google ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง',
      );
    }
  }

  Future<void> signOut() async {
    try {
      await _auth.signOut();
    } on FirebaseAuthException catch (e) {
      throw Exception(_getThaiErrorMessage(e.code));
    } catch (_) {
      throw Exception('ออกจากระบบไม่สำเร็จ กรุณาลองใหม่อีกครั้ง');
    }
  }

  String _getThaiErrorMessage(String code) {
    switch (code) {
      case 'email-already-in-use':
        return 'อีเมลนี้ถูกใช้สมัครสมาชิกแล้ว';
      case 'weak-password':
        return 'รหัสผ่านไม่ปลอดภัยเพียงพอ';
      case 'invalid-email':
        return 'รูปแบบอีเมลไม่ถูกต้อง';
      case 'user-not-found':
        return 'ไม่พบบัญชีผู้ใช้นี้';
      case 'wrong-password':
      case 'invalid-credential':
        return 'อีเมลหรือรหัสผ่านไม่ถูกต้อง';
      case 'user-disabled':
        return 'บัญชีนี้ถูกระงับการใช้งาน';
      case 'too-many-requests':
        return 'ลองหลายครั้งเกินไป กรุณารอสักครู่';
      case 'operation-not-allowed':
        return 'ยังไม่ได้เปิดใช้งานวิธีเข้าสู่ระบบนี้';
      case 'network-request-failed':
        return 'เชื่อมต่อเครือข่ายไม่ได้ กรุณาตรวจสอบอินเทอร์เน็ต';
      default:
        return 'เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง';
    }
  }
}
