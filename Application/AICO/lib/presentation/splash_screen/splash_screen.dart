import 'package:flutter/material.dart';
import '../../core/app_export.dart';
import '../../widgets/custom_elevated_button.dart';
// import 'models/splash_model.dart';
import 'provider/splash_provider.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({Key? key})
      : super(
          key: key,
        );

  @override
  SplashScreenState createState() => SplashScreenState();
  static Widget builder(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => SplashProvider(),
      child: SplashScreen(),
    );
  }
}

class SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    //Future.delayed(const Duration(milliseconds: 3000), () {
      //NavigatorService.popAndPushNamed(
       // AppRoutes.registrationScreen,
     // );
   // });
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: SizedBox(
          width: double.maxFinite,
          child: Column(
            children: [
              SizedBox(
                height: 700.v,
                width: double.maxFinite,
                child: Stack(
                  alignment: Alignment.bottomCenter,
                  children: [
                    CustomImageView(
                      imagePath: ImageConstant.imgEllipse1,
                      height: 153.v,
                      width: 164.h,
                      alignment: Alignment.topLeft,
                    ),
                    Align(
                      alignment: Alignment.bottomCenter,
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              CustomImageView(
                                imagePath: ImageConstant.imgUser,
                                height: 43.v,
                                width: 56.h,
                              ),
                              Padding(
                                padding: EdgeInsets.only(
                                  left: 9.h,
                                  top: 3.v,
                                  bottom: 3.v,
                                ),
                                child: Text(
                                  "lbl_aico".tr,
                                  style: CustomTextStyles.headlineSmallBlack900,
                                ),
                              )
                            ],
                          ),
                          SizedBox(height: 9.v),
                          CustomImageView(
                            imagePath: ImageConstant.imgMindfulnessCuate,
                            height: 547.v,
                            width: 428.h,
                          )
                        ],
                      ),
                    )
                  ],
                ),
              ),
              SizedBox(height: 37.v),
              Text(
                "lbl_welcome_to_aico".tr,
                textAlign: TextAlign.center,
                style: CustomTextStyles.headlineSmallOpenSansPrimary,
              ),
              SizedBox(height: 5.v)
            ],
          ),
        ),
        bottomNavigationBar: _buildGetStartedButton(context),
      ),
    );
  }

  /// Section Widget
  Widget _buildGetStartedButton(BuildContext context) {
    return CustomElevatedButton(
      text: "lbl_get_started".tr,
      margin: EdgeInsets.only(
        left: 25.h,
        right: 25.h,
        bottom: 44.v,
      ),
      buttonTextStyle: CustomTextStyles.bodyLargeOnPrimary,
      onPressed: () {
        NavigatorService.popAndPushNamed(
          AppRoutes.registrationScreen,
        );
      },
    );
  }
}
