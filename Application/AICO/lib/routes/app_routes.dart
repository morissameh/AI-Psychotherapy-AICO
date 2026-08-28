import 'package:flutter/material.dart';
import '../core/app_export.dart';
import '../presentation/app_navigation_screen/app_navigation_screen.dart';
import '../presentation/chat_screen/chat_screen.dart';
import '../presentation/forgot_password_screen/forgot_password_screen.dart';
import '../presentation/log_in_screen/log_in_screen.dart';
import '../presentation/registration_screen/registration_screen.dart';
import '../presentation/splash_screen/splash_screen.dart';

class AppRoutes {
  static const String splashScreen = '/splash_screen';

  static const String registrationScreen = '/registration_screen';

  static const String logInScreen = '/log_in_screen';

  static const String forgotPasswordScreen = '/forgot_password_screen';

  static const String chatScreen = '/chat_screen';

  static const String appNavigationScreen = '/app_navigation_screen';

  static const String initialRoute = '/initialRoute';

  static Map<String, WidgetBuilder> get routes => {
        splashScreen: SplashScreen.builder,
        registrationScreen: RegistrationScreen.builder,
        logInScreen: LogInScreen.builder,
        forgotPasswordScreen: ForgotPasswordScreen.builder,
       // chatScreen: ChatScreen.builder,
        chatScreen: (context) => ChatScreen(),
        appNavigationScreen: AppNavigationScreen.builder,
        initialRoute: SplashScreen.builder
      };
}
