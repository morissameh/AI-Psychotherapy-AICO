import 'package:flutter/material.dart';
import '../../core/app_export.dart';

class AppbarTitleImage extends StatelessWidget {
  AppbarTitleImage({Key? key, this.imagePath, this.margin, this.onTap})
      : super(
          key: key,
        );

  String? imagePath;

  EdgeInsetsGeometry? margin;

  Function? onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {
        onTap?.call();
      },
      child: Padding(
        padding: margin ?? EdgeInsets.zero,
        child: CustomImageView(
          imagePath: imagePath!,
          height: 13.v,
          width: 15.h,
          fit: BoxFit.contain,
        ),
      ),
    );
  }
}
