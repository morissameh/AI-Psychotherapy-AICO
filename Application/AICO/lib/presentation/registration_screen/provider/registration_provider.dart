import 'package:flutter/material.dart';
import '../../../core/app_export.dart';
import '../models/registration_model.dart';

/// A provider class for the RegistrationScreen.
///
/// This provider manages the state of the RegistrationScreen, including the
/// current registrationModelObj
// ignore_for_file: must_be_immutable

// ignore_for_file: must_be_immutable
class RegistrationProvider extends ChangeNotifier {
  TextEditingController fullNameController = TextEditingController();

  TextEditingController userNameController = TextEditingController();

  TextEditingController emailController = TextEditingController();

  TextEditingController passwordController = TextEditingController();

  TextEditingController password1Controller = TextEditingController();

  RegistrationModel registrationModelObj = RegistrationModel();

  @override
  void dispose() {
    super.dispose();
    fullNameController.dispose();
    userNameController.dispose();
    emailController.dispose();
    passwordController.dispose();
    password1Controller.dispose();
  }
}
