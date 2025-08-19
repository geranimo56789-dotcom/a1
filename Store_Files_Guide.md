# Store Files Generation Guide for VAR6 Betting App

## Overview
This guide explains how to generate the necessary files for publishing the VAR6 Betting App to iOS App Store and Google Play Store.

## Prerequisites

### For iOS App Store:
- **Apple Developer Account** ($99/year)
- **Xcode** installed on macOS
- **iOS Development Certificate**
- **App Store Distribution Certificate**
- **Provisioning Profile**

### For Google Play Store:
- **Google Play Console Account** ($25 one-time)
- **Android SDK** installed
- **Java Development Kit (JDK)**
- **Android Studio** (recommended)

## Build Commands

### iOS App Store Files

#### 1. Build for iOS Device (macOS required):
```bash
# Navigate to project directory
cd MauiApp1

# Build iOS archive for App Store
dotnet build -c Release -f net8.0-ios -p:ArchiveOnBuild=true -p:BuildIpa=true -p:Platform=iPhone -p:Configuration=Release

# Alternative command for specific device
dotnet build -c Release -f net8.0-ios -p:ArchiveOnBuild=true -p:BuildIpa=true -p:Platform=iPhone -p:Configuration=Release -p:RuntimeIdentifier=ios-arm64
```

#### 2. Expected Output:
- **Location**: `MauiApp1/bin/Release/net8.0-ios/ios-arm64/`
- **Files**: 
  - `MauiApp1.ipa` (iOS App Store Package)
  - Archive files for App Store Connect

### Android Google Play Store Files

#### 1. Build Android App Bundle (AAB):
```bash
# Navigate to project directory
cd MauiApp1

# Build AAB for Play Store
dotnet build -c Release -f net8.0-android -p:AndroidPackageFormat=aab -p:AndroidKeyStore=true -p:AndroidSigningKeyStore=your-keystore.jks -p:AndroidSigningKeyAlias=your-key-alias -p:AndroidSigningKeyPass=your-key-password -p:AndroidSigningStorePass=your-store-password
```

#### 2. Build Android APK (for testing):
```bash
# Build APK for testing
dotnet build -c Release -f net8.0-android -p:AndroidPackageFormat=apk
```

#### 3. Expected Output:
- **Location**: `MauiApp1/bin/Release/net8.0-android/android-x64/`
- **Files**:
  - `MauiApp1-Signed.aab` (Android App Bundle for Play Store)
  - `MauiApp1-Signed.apk` (APK for testing)

## Required Store Assets

### iOS App Store Assets:
1. **App Icon** (1024x1024px)
2. **Screenshots** (various device sizes):
   - iPhone 6.7" (1290x2796px)
   - iPhone 6.5" (1242x2688px)
   - iPhone 5.5" (1242x2208px)
   - iPad Pro 12.9" (2048x2732px)
3. **App Preview Videos** (optional)
4. **App Description**
5. **Privacy Policy URL**

### Google Play Store Assets:
1. **App Icon** (512x512px)
2. **Feature Graphic** (1024x500px)
3. **Screenshots** (various device densities):
   - Phone screenshots (minimum 2)
   - Tablet screenshots (if applicable)
4. **App Description**
5. **Privacy Policy URL**

## Configuration Files

### iOS Configuration (Info.plist):
```xml
<key>CFBundleDisplayName</key>
<string>VAR6 Betting App</string>
<key>CFBundleIdentifier</key>
<string>com.yourcompany.var6betting</string>
<key>CFBundleVersion</key>
<string>1.0</string>
<key>CFBundleShortVersionString</key>
<string>1.0</string>
<key>LSRequiresIPhoneOS</key>
<true/>
<key>UILaunchStoryboardName</key>
<string>LaunchScreen</string>
<key>UIRequiredDeviceCapabilities</key>
<array>
    <string>armv7</string>
</array>
<key>UISupportedInterfaceOrientations</key>
<array>
    <string>UIInterfaceOrientationPortrait</string>
    <string>UIInterfaceOrientationLandscapeLeft</string>
    <string>UIInterfaceOrientationLandscapeRight</string>
</array>
```

### Android Configuration (AndroidManifest.xml):
```xml
<application android:label="VAR6 Betting App" android:supportsRtl="true">
    <activity android:name="microsoft.maui.essentials.fileProvider" android:exported="false" android:grantUriPermissions="true" android:theme="@android:style/Theme.Translucent.NoTitleBar">
        <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths" />
    </activity>
</application>
```

## Store-Specific Requirements

### iOS App Store:
- **Content Rating**: 17+ (Gambling content)
- **Age Restrictions**: Required
- **Gambling License**: May be required depending on region
- **Payment Processing**: Must comply with App Store guidelines
- **Review Process**: 1-7 days

### Google Play Store:
- **Content Rating**: Teen or higher
- **Gambling Policy**: Must comply with Google Play gambling policy
- **Regional Availability**: May be restricted in certain countries
- **Payment Processing**: Must use Google Play Billing
- **Review Process**: 1-3 days

## Important Notes for Betting Apps

### Legal Considerations:
1. **Gambling Laws**: Ensure compliance with local gambling regulations
2. **Age Verification**: Implement proper age verification systems
3. **Responsible Gambling**: Include responsible gambling features
4. **Licensing**: Obtain necessary gambling licenses

### Store Policy Compliance:
1. **iOS**: Betting apps face strict review process
2. **Android**: Must follow Google Play gambling policy
3. **Regional Restrictions**: Many countries restrict gambling apps
4. **Payment Methods**: Must use approved payment processors

## Troubleshooting

### Common iOS Build Issues:
- **Certificate Issues**: Ensure valid certificates and provisioning profiles
- **Archive Problems**: Use Xcode for complex archive issues
- **Code Signing**: Verify code signing settings

### Common Android Build Issues:
- **SDK Issues**: Install Android SDK and set ANDROID_HOME
- **Keystore Problems**: Create and configure signing keystore
- **Build Tools**: Ensure latest Android build tools

## Next Steps

1. **Set up developer accounts** for both stores
2. **Create app listings** with required metadata
3. **Generate store assets** (icons, screenshots, descriptions)
4. **Test builds** on physical devices
5. **Submit for review** following store guidelines

## Support Resources

- **Apple Developer Documentation**: https://developer.apple.com/
- **Google Play Console Help**: https://support.google.com/googleplay/
- **MAUI Documentation**: https://docs.microsoft.com/dotnet/maui/
- **Store Policy Guidelines**: Check respective store documentation
