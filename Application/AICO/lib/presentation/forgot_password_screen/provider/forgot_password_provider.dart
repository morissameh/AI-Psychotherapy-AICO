import 'package:flutter/material.dart';
import '../../../core/app_export.dart';
import '../models/forgot_password_model.dart';

/// A provider class for the ForgotPasswordScreen.
///
/// This provider manages the state of the ForgotPasswordScreen, including the
/// current forgotPasswordModelObj
// ignore_for_file: must_be_immutable

// ignore_for_file: must_be_immutable
class ForgotPasswordProvider extends ChangeNotifier {
  TextEditingController emailFieldController = TextEditingController();

  TextEditingController newPasswordFieldController = TextEditingController();

  TextEditingController confirmPasswordFieldController =
      TextEditingController();

  ForgotPasswordModel forgotPasswordModelObj = ForgotPasswordModel();

  @override
  void dispose() {
    super.dispose();
    emailFieldController.dispose();
    newPasswordFieldController.dispose();
    confirmPasswordFieldController.dispose();
  }
}
