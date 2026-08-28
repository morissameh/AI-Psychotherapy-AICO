import 'package:flutter/material.dart';
import '../../core/app_export.dart';
import '../../core/utils/validation_functions.dart';
import '../../domain/facebookauth/facebook_auth_helper.dart';
import '../../domain/googleauth/google_auth_helper.dart';
import '../../widgets/custom_elevated_button.dart';
import '../../widgets/custom_text_form_field.dart';
import 'provider/log_in_provider.dart';
import 'package:http/http.dart' as http;
import 'dart:convert'; // Import dart:convert for jsonDecode

class LogInScreen extends StatefulWidget {
  const LogInScreen({Key? key})
      : super(
    key: key,
  );

  @override
  LogInScreenState createState() => LogInScreenState();
  static Widget builder(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => LogInProvider(),
      child: LogInScreen(),
    );
  }
}
/// ignore_for_file: must_be_immutable

/// ignore_for_file: must_be_immutable
class LogInScreenState extends State<LogInScreen> {
  GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController _emailFieldController = TextEditingController();
  final TextEditingController _passwordFieldController = TextEditingController();

  String email = ""; // Variable to store email
  String password = ""; // Variable to store password

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: appTheme.blue10001,
        resizeToAvoidBottomInset: false,
        body: SizedBox(
          width: SizeUtils.width,
          child: SingleChildScrollView(
            padding: EdgeInsets.only(
              bottom: MediaQuery.of(context).viewInsets.bottom,
            ),
            child: Form(
              key: _formKey,
              child: SizedBox(
                width: double.maxFinite,
                child: Column(
                  children: [
                    CustomImageView(
                      imagePath: ImageConstant.imgEllipse1,
                      height: 128.v,
                      width: 158.h,
                      alignment: Alignment.centerLeft,
                    ),
                    SizedBox(height: 32.v),
                    Text(
                      "lbl_welcome_back".tr,
                      style: theme.textTheme.headlineSmall,
                    ),
                    SizedBox(height: 40.v),
                    _buildEmailField(context),
                    SizedBox(height: 48.v),
                    _buildPasswordField(context),
                    SizedBox(height: 68.v),
                    _buildLoginButton(context),
                    SizedBox(height: 25.v),
                    _buildRowVectorOne(context),
                    SizedBox(height: 12.v),
                    _buildLoginWithGoogleButton(context),
                    SizedBox(height: 37.v),
                    _buildLoginWithFacebookButton(context),
                    SizedBox(height: 41.v),
                    GestureDetector(
                      onTap: () {
                        onTapTxtForgotpassword(context);
                      },
                      child: Text(
                        "msg_forgot_password".tr,
                        style: theme.textTheme.headlineSmall,
                      ),
                    ),
                    SizedBox(height: 29.v),
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Padding(
                        padding: EdgeInsets.only(
                          left: 36.h,
                          right: 58.h,
                        ),
                        child: Row(
                          children: [
                            GestureDetector(
                              onTap: () {
                                onTapTxtConfirmation(context);
                              },
                              child: Padding(
                                padding: EdgeInsets.only(bottom: 2.v),
                                child: Text(
                                  "msg_don_t_have_an_account".tr,
                                  style: CustomTextStyles.titleLargeRegular,
                                ),
                              ),
                            ),
                            GestureDetector(
                              onTap: () {
                                onTapTxtSignup(context);
                              },
                              child: Padding(
                                padding: EdgeInsets.only(
                                  left: 20.h,
                                  top: 2.v,
                                ),
                                child: Text(
                                  "lbl_sign_up".tr,
                                  style: CustomTextStyles.titleLargeRegular,
                                ),
                              ),
                            )
                          ],
                        ),
                      ),
                    ),
                    SizedBox(height: 5.v)
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  /// Section Widget
  Widget _buildEmailField(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 25.h),
      child: Selector<LogInProvider, TextEditingController?>(
        selector: (context, provider) => provider.emailFieldController,
        builder: (context, emailFieldController, child) {
          return CustomTextFormField(
            controller: emailFieldController,
            hintText: "lbl_enter_e_mail".tr,
            textInputType: TextInputType.emailAddress,
            validator: (value) {
              if (value == null || (!isValidEmail(value, isRequired: true))) {
                return "err_msg_please_enter_valid_email".tr;
              }
              return null;
            },
          );
        },
      ),
    );
  }

  /// Section Widget
  Widget _buildPasswordField(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 25.h),
      child: Selector<LogInProvider, TextEditingController?>(
        selector: (context, provider) => provider.passwordFieldController,
        builder: (context, passwordFieldController, child) {
          return CustomTextFormField(
            controller: passwordFieldController,
            hintText: "lbl_enter_password".tr,
            textInputAction: TextInputAction.done,
            textInputType: TextInputType.visiblePassword,
            validator: (value) {
              //if (value == null || (!isValidPassword(value, isRequired: true))) {return "err_msg_please_enter_valid_password".tr;}
              //return null;
            },
            obscureText: true,
          );
        },
      ),
    );
  }

  /// Section Widget
  Widget _buildLoginButton(BuildContext context) {
    return CustomElevatedButton(
      text: "lbl_log_in2".tr,
      margin: EdgeInsets.symmetric(horizontal: 25.h),
      buttonTextStyle: theme.textTheme.titleLarge!,
      onPressed: () async {
        if (_formKey.currentState!.validate()) {
          // Form is valid, proceed with login logic
          password = context.read<LogInProvider>().passwordFieldController.text;
          email = context.read<LogInProvider>().emailFieldController.text;

          // Your login API call and logic here
          final url = Uri.parse("https://46e2-41-237-156-184.ngrok-free.app/signin");
          final body = jsonEncode({'email': email, 'password': password});
          final response = await http.post(url, headers: {'Content-Type': 'application/json'}, body: body);
          if (response.body == "Successfully logged in!") {
            print('Response data: ${response.body}');
            NavigatorService.pushNamed(AppRoutes.chatScreen);
          }

          //if isauthenticated == true


          //else {
          // Form is invalid, show error message or something
         // print("Form validation failed");
        }
      },
    );
  }

  /// Section Widget
  Widget _buildRowVectorOne(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: 12.h,
        right: 20.h,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Padding(
            padding: EdgeInsets.only(
              top: 20.v,
              bottom: 13.v,
            ),
            child: SizedBox(
              width: 118.h,
              child: Divider(),
            ),
          ),
          Spacer(
            flex: 53,
          ),
          Text(
            "lbl_or".tr,
            style: CustomTextStyles.headlineSmallRegular,
          ),
          Spacer(
            flex: 46,
          ),
          Padding(
            padding: EdgeInsets.only(
              top: 20.v,
              bottom: 13.v,
            ),
            child: SizedBox(
              width: 118.h,
              child: Divider(),
            ),
          )
        ],
      ),
    );
  }

  /// Section Widget
  Widget _buildLoginWithGoogleButton(BuildContext context) {
    return CustomElevatedButton(
      text: "msg_login_with_google".tr,
      margin: EdgeInsets.only(
        left: 19.h,
        right: 31.h,
      ),
      leftIcon: Container(
        margin: EdgeInsets.only(right: 30.h),
        child: CustomImageView(
          imagePath: ImageConstant.imgGooglelogo8250061,
          height: 39.v,
          width: 45.h,
        ),
      ),
      buttonTextStyle: theme.textTheme.titleLarge!,
      onPressed: () {
        onTapLoginWithGoogleButton(context);
      },
    );
  }

  /// Section Widget
  Widget _buildLoginWithFacebookButton(BuildContext context) {
    return CustomElevatedButton(
      text: "msg_login_with_facebook".tr,
      margin: EdgeInsets.only(
        left: 19.h,
        right: 31.h,
      ),
      leftIcon: Container(
        margin: EdgeInsets.only(right: 11.h),
        child: CustomImageView(
          imagePath: ImageConstant.imgGooglelogo825006150x57,
          height: 50.v,
          width: 57.h,
        ),
      ),
      buttonTextStyle: theme.textTheme.titleLarge!,
      onPressed: () {
        onTapLoginWithFacebookButton(context);
      },
    );
  }

  onTapLoginWithGoogleButton(BuildContext context) async {
    await GoogleAuthHelper().googleSignInProcess().then((googleUser) {
      if (googleUser != null) {
      } else {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text('user data is empty')));
      }
    }).catchError((onError) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(onError.toString())));
    });
  }

  onTapLoginWithFacebookButton(BuildContext context) async {
    await FacebookAuthHelper()
        .facebookSignInProcess()
        .then((facebookUser) {})
        .catchError((onError) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(onError.toString())));
    });
  }

  /// Navigates to the forgotPasswordScreen when the action is triggered.
  onTapTxtForgotpassword(BuildContext context) {
    NavigatorService.pushNamed(
      AppRoutes.forgotPasswordScreen,
    );
  }

  /// Navigates to the registrationScreen when the action is triggered.
  onTapTxtConfirmation(BuildContext context) {
    NavigatorService.pushNamed(
      AppRoutes.registrationScreen,
    );
  }

  /// Navigates to the registrationScreen when the action is triggered.
  onTapTxtSignup(BuildContext context) {
    NavigatorService.pushNamed(AppRoutes.registrationScreen,);
  }
}
