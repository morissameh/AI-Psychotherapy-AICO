import 'package:flutter/material.dart';
import '../../../core/app_export.dart';
import '../models/log_in_model.dart';

/// A provider class for the LogInScreen.
///
/// This provider manages the state of the LogInScreen, including the
/// current logInModelObj

class LogInProvider extends ChangeNotifier {
  TextEditingController emailFieldController = TextEditingController();

  TextEditingController passwordFieldController = TextEditingController();

  LogInModel logInModelObj = LogInModel();

  @override
  void dispose() {
    super.dispose();
    emailFieldController.dispose();
    passwordFieldController.dispose();
  }
}
