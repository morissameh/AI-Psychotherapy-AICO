import 'package:flutter/material.dart';
import '../../core/app_export.dart';
import '../../core/utils/validation_functions.dart';
import '../../widgets/custom_elevated_button.dart';
import '../../widgets/custom_text_form_field.dart';
///import 'models/registration_model.dart';
import 'provider/registration_provider.dart';
import 'package:http/http.dart' as http;
import 'dart:convert'; // Import dart:convert for jsonDecode

class RegistrationScreen extends StatefulWidget {
  const RegistrationScreen({Key? key})
      : super(
          key: key,
        );

  @override
  RegistrationScreenState createState() => RegistrationScreenState();
  static Widget builder(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => RegistrationProvider(),
      child: RegistrationScreen(),

    );
  }
}
/// ignore_for_file: must_be_immutable

class RegistrationScreenState extends State<RegistrationScreen> {
  GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  String fullName = ""; // Variable to store full name
  String userName = ""; // Variable to store username
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
        backgroundColor: appTheme.blue100,
        resizeToAvoidBottomInset: false,
        body: SizedBox(
          width: SizeUtils.width,
          child: SingleChildScrollView(
            padding: EdgeInsets.only(
              bottom: MediaQuery.of(context).viewInsets.bottom,
            ),
            child: Form(
              key: _formKey,
              child: Container(
                width: double.maxFinite,
                padding: EdgeInsets.symmetric(
                  horizontal: 22.h,
                  vertical: 41.v,
                ),
                child: Column(
                  children: [
                    SizedBox(height: 30.v),
                    Text(
                      "lbl_welcome".tr,
                      style: theme.textTheme.headlineSmall,
                    ),
                    SizedBox(height: 7.v),
                    CustomImageView(
                      imagePath: ImageConstant.imgImage5,
                      height: 143.v,
                      width: 153.h,
                    ),
                    SizedBox(height: 25.v),
                    _buildFullName(context),
                    SizedBox(height: 50.v),
                    _buildUserName(context),
                    SizedBox(height: 46.v),
                    _buildEmail(context),
                    SizedBox(height: 46.v),
                    _buildPassword(context),
                    SizedBox(height: 37.v),
                    _buildPassword1(context),
                    SizedBox(height: 46.v),
                    _buildSignUp(context)
                  ],
                ),
              ),
            ),
          ),
        ),
        bottomNavigationBar: _buildRowConfirmation(context),
      ),
    );
  }

  /// Section Widget full name
  Widget _buildFullName(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(right: 6.h),
      child: Selector<RegistrationProvider, TextEditingController?>(
        selector: (context, provider) => provider.fullNameController,
        builder: (context, fullNameController, child) {
          return CustomTextFormField(
            controller: fullNameController,
            hintText: "lbl_enter_full_name".tr,
            validator: (value) {
              if (!isText(value)) {
                return "please enter valid full name".tr;
              }
              return null;
            },
          );
        },
      ),
    );
  }

  /// Section Widget username
  Widget _buildUserName(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(right: 6.h),
      child: Selector<RegistrationProvider, TextEditingController?>(
        selector: (context, provider) => provider.userNameController,
        builder: (context, userNameController, child) {
          return CustomTextFormField(
            controller: userNameController,
            hintText: "lbl_enter_username".tr,
            validator: (value) {
              if (!isText(value)) {
                return "please enter valid username".tr;
              }
              return null;
            },
          );
        },
      ),
    );
  }

  /// Section Widget Email
  Widget _buildEmail(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(right: 6.h),
      child: Selector<RegistrationProvider, TextEditingController?>(
        selector: (context, provider) => provider.emailController,
        builder: (context, emailController, child) {
          return CustomTextFormField(
            controller: emailController,
            hintText: "lbl_enter_e_mail".tr,
            textInputType: TextInputType.emailAddress,
            validator: (value) {
              if (value == null || (!isValidEmail(value, isRequired: true))) {
                return "please enter valid email".tr;
              }
              return null;
            },
          );
        },
      ),
    );
  }

  /// Section Widget  password
  Widget _buildPassword(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(right: 6.h),
      child: Selector<RegistrationProvider, TextEditingController?>(
        selector: (context, provider) => provider.passwordController,
        builder: (context, passwordController, child) {
          return CustomTextFormField(
            controller: passwordController,
            hintText: "lbl_enter_password".tr,
            textInputType: TextInputType.visiblePassword,
            validator: (value) {
              if (value == null ||
                  (!isValidPassword(value, isRequired: true))) {
                return "please enter valid password".tr;
              }
              return null;
            },
            obscureText: true,
          );
        },
      ),
    );
  }

  /// Section Widget password confirmation
  Widget _buildPassword1(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(right: 6.h),
      child: Selector<RegistrationProvider, TextEditingController?>(
        selector: (context, provider) => provider.password1Controller,
        builder: (context, password1Controller, child) {
          return CustomTextFormField(
            controller: password1Controller,
            hintText: "re_enter password".tr,
            hintStyle: theme.textTheme.bodyMedium!,
            textInputAction: TextInputAction.done,
            textInputType: TextInputType.visiblePassword,
            validator: (value) {
              if (value == null ||
                  (!isValidPassword(value, isRequired: true))) {
                return "please enter a valid password".tr;
              }
              return null;
            },
            obscureText: true,
          );
        },
      ),
    );
  }

  /// Section Widget
  ///Navigates to the logInScreen when the button is pressed and all fields are filled and password matches password 1 then continue.
  Widget _buildSignUp(BuildContext context) {
    return CustomElevatedButton(
      text: "lbl_sign_up".tr,
      margin: EdgeInsets.symmetric(horizontal: 3.h),
      buttonTextStyle: theme.textTheme.titleLarge!,
        onPressed: ()async {
          if (_formKey.currentState!.validate()) {
            password = context.read<RegistrationProvider>().passwordController.text;
            fullName = context.read<RegistrationProvider>().fullNameController.text;
            userName = context.read<RegistrationProvider>().userNameController.text;
            email = context.read<RegistrationProvider>().emailController.text;

            final url = Uri.parse("https://46e2-41-237-156-184.ngrok-free.app/signup");
            final body = jsonEncode({'email': email, 'password': password, 'fullName': fullName, 'userName': userName,});
            final response = await http.post(url, headers: {'Content-Type': 'application/json'}, body: body,);

            print(response);
            NavigatorService.pushNamed(AppRoutes.logInScreen,);
          }else {
            // Form is invalid, show error message
            print("Form validation failed");
          }
        }
      );
    }
         /// Section Widget
  Widget _buildRowConfirmation(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: 50.h,
        right: 44.h,
        bottom: 34.v,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Padding(
            padding: EdgeInsets.only(top: 2.v),
            child: Text(
              "msg_already_have_an".tr,
              style: CustomTextStyles.titleLargeRegular,
            ),
          ),
          GestureDetector(
            onTap: () {
              onTapTxtLogin(context);
            },
            child: Padding(
              padding: EdgeInsets.only(
                left: 12.h,
                bottom: 2.v,
              ),
              child: Text(
                "lbl_login".tr, ///login link navigates to login page
                style: CustomTextStyles.titleLargeSecondaryContainer,
              ),
            ),
          )
        ],
      ),
    );
  }

 ///Navigates to the logInScreen if already has account
  onTapTxtLogin(BuildContext context) {
    NavigatorService.pushNamed(
      AppRoutes.logInScreen,
    );
  }
}
