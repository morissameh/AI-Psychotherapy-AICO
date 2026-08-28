import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'core/app_export.dart';
import 'package:AICO/helper/helper_functions.dart';
///import 'package:firebase_core/firebase_core.dart';
import 'package:AICO/presentation/chat_screen/chat_screen.dart';
import 'package:AICO/presentation/log_in_screen/log_in_screen.dart';
//import 'package:sara_s_application1/presentation/provider/forgot_password_provider.dart';
//import '../../log_in_screen/log_in_provider.dart';


var globalMessengerKey = GlobalKey<ScaffoldMessengerState>();
void main() async {

  //await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform,); //added and it is deprecated
  //await Firebase.initializeApp();
  WidgetsFlutterBinding.ensureInitialized();
  Future.wait([
    SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]),
    PrefUtils().init()
  ]).then((value) {
    runApp(MyApp());
  });
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();

}

class _MyAppState extends State<MyApp> {
  bool _isSignedIn = false;

  @override
  void initState() {
    super.initState();
    getUserLoggedInStatus(); // Assuming this fetches user signed-in state
  }

  getUserLoggedInStatus() async {
    await HelperFunctions.getUserLoggedInStatus().then((value) {
      if (value != null) {
        setState(() {
          _isSignedIn = value;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Sizer(
      builder: (context, orientation, deviceType) {
        return ChangeNotifierProvider<ThemeProvider>(
          create: (context) => ThemeProvider(),
          child: Consumer<ThemeProvider>(
            builder: (context, provider, child) {
              return MaterialApp(
                title: 'AICO',
                debugShowCheckedModeBanner: false,
                theme: theme,
                home: _isSignedIn ? const ChatScreen() : const LogInScreen(),
                navigatorKey: NavigatorService.navigatorKey,
                localizationsDelegates: [
                  AppLocalizationDelegate(),
                  GlobalMaterialLocalizations.delegate,
                  GlobalWidgetsLocalizations.delegate,
                  GlobalCupertinoLocalizations.delegate
                ],
                supportedLocales: [Locale('en', '')],
                initialRoute: AppRoutes.initialRoute,
                routes: AppRoutes.routes,
              );
            },
          ),
        );
      },
    );
  }
}
