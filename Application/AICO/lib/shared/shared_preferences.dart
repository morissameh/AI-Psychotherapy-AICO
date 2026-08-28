// shared_preferences.dart
import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:AICO/presentation/log_in_screen/log_in_screen.dart';
 /*
class SharedPrefConstants {
  static const String kSavedFullName = "";
  static const String kSavedUserName = "";
  static const String kSavedEmail = "";
  static const String kSavedPassword = "";
}
*/
class SharedPrefConstants {
  static const String kSavedFullName = "saved_full_name";
  static const String kSavedUserName = "saved_username";
  static const String kSavedEmail = "saved_email";
  static const String kSavedPassword = "saved_password";
}

Future<String?> getSavedFullName() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString(SharedPrefConstants.kSavedFullName);
}

Future<String?> getSavedUserName() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString(SharedPrefConstants.kSavedUserName);
}

Future<String?> getSavedEmail() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString(SharedPrefConstants.kSavedEmail);
}

Future<String?> getSavedPassword() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString(SharedPrefConstants.kSavedPassword);
}


