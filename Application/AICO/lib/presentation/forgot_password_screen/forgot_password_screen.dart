import 'package:flutter/material.dart';
import '../../core/app_export.dart';
import '../../core/utils/validation_functions.dart';
import '../../widgets/custom_elevated_button.dart';
import '../../widgets/custom_text_form_field.dart';
import 'models/forgot_password_model.dart';
import 'provider/forgot_password_provider.dart';

class ForgotPasswordScreen extends StatefulWidget {
  const ForgotPasswordScreen({Key? key})
      : super(
          key: key,
        );

  @override
  ForgotPasswordScreenState createState() => ForgotPasswordScreenState();
  static Widget builder(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => ForgotPasswordProvider(),
      child: ForgotPasswordScreen(),
    );
  }
}
// ignore_for_file: must_be_immutable

// ignore_for_file: must_be_immutable
class ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: appTheme.lightBlue100,
        resizeToAvoidBottomInset: false,
        body: SizedBox(
          width: SizeUtils.width,
          child: SingleChildScrollView(
            padding: EdgeInsets.only(
              bottom: MediaQuery.of(context).viewInsets.bottom,
            ),
            child: SizedBox(
              height: SizeUtils.height,
              child: Form(
                key: _formKey,
                child: SizedBox(
                  width: double.maxFinite,
                  child: Column(
                    children: [
                      CustomImageView(
                        imagePath: ImageConstant.imgEllipse1,
                        height: 110.v,
                        width: 174.h,
                        alignment: Alignment.centerLeft,
                      ),
                      SizedBox(height: 56.v),
                      Text(
                        "msg_forgot_password2".tr,
                        style: theme.textTheme.headlineSmall,
                      ),
                      SizedBox(height: 58.v),
                      _buildEmailField(context),
                      Spacer(
                        flex: 32,
                      ),
                      _buildNewPasswordField(context),
                      Spacer(
                        flex: 32,
                      ),
                      _buildConfirmPasswordField(context),
                      Spacer(
                        flex: 34,
                      ),
                      _buildLoginButton(context),
                      SizedBox(height: 52.v),
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
                      SizedBox(height: 41.v)
                    ],
                  ),
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
      child: Selector<ForgotPasswordProvider, TextEditingController?>(
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
  Widget _buildNewPasswordField(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 25.h),
      child: Selector<ForgotPasswordProvider, TextEditingController?>(
        selector: (context, provider) => provider.newPasswordFieldController,
        builder: (context, newPasswordFieldController, child) {
          return CustomTextFormField(
            controller: newPasswordFieldController,
            hintText: "msg_enter_new_password".tr,
            textInputType: TextInputType.visiblePassword,
            validator: (value) {
              if (value == null ||
                  (!isValidPassword(value, isRequired: true))) {
                return "err_msg_please_enter_valid_password".tr;
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
  Widget _buildConfirmPasswordField(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 25.h),
      child: Selector<ForgotPasswordProvider, TextEditingController?>(
        selector: (context, provider) =>
            provider.confirmPasswordFieldController,
        builder: (context, confirmPasswordFieldController, child) {
          return CustomTextFormField(
            controller: confirmPasswordFieldController,
            hintText: "msg_re_enter_new_password".tr,
            textInputAction: TextInputAction.done,
            textInputType: TextInputType.visiblePassword,
            validator: (value) {
              if (value == null ||
                  (!isValidPassword(value, isRequired: true))) {
                return "err_msg_please_enter_valid_password".tr;
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
  Widget _buildLoginButton(BuildContext context) {
    return CustomElevatedButton(
      text: "lbl_log_in2".tr,
      margin: EdgeInsets.symmetric(horizontal: 25.h),
      buttonTextStyle: theme.textTheme.titleLarge!,
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
    NavigatorService.pushNamed(
      AppRoutes.registrationScreen,
    );
  }
}
