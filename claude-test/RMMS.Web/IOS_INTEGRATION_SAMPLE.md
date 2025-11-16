# iOS Integration Sample - RMMS Mobile Backend

## Overview

This guide shows how to build an iOS app that connects to the RMMS mobile backend using Swift and SwiftUI.

---

## Prerequisites

- Xcode 15+
- iOS 15.0+
- Swift 5.9+
- Knowledge of SwiftUI, Combine, and Async/Await

---

## Step 1: Project Setup

### Create New Project
1. Open Xcode
2. Create new iOS App
3. Choose SwiftUI for interface
4. Enable "Use Core Data" if needed for offline storage

### Package Dependencies (SPM)
1. File → Add Packages...
2. Add these packages:

```
Firebase iOS SDK: https://github.com/firebase/firebase-ios-sdk
(Add FirebaseMessaging)
```

---

## Step 2: Network Layer

### APIService.swift
```swift
import Foundation

class APIService {
    static let shared = APIService()

    private let baseURL = "http://YOUR_SERVER_IP:5090/api/v1"
    private let session: URLSession

    init() {
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 30
        configuration.timeoutIntervalForResource = 300
        self.session = URLSession(configuration: configuration)
    }

    // MARK: - Generic Request

    private func request<T: Decodable>(
        _ endpoint: String,
        method: String = "GET",
        body: Data? = nil,
        requiresAuth: Bool = true
    ) async throws -> T {
        guard let url = URL(string: "\(baseURL)/\(endpoint)") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        if requiresAuth, let token = TokenManager.shared.getToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        if let body = body {
            request.httpBody = body
        }

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        guard (200...299).contains(httpResponse.statusCode) else {
            throw APIError.serverError(httpResponse.statusCode)
        }

        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(T.self, from: data)
    }

    // MARK: - Configuration

    func getMobileConfig(platform: String, appVersion: String) async throws -> APIResponse<MobileConfigDTO> {
        return try await request("mobile/MobileConfig?platform=\(platform)&appVersion=\(appVersion)", requiresAuth: false)
    }

    func checkVersion(platform: String, appVersion: String) async throws -> APIResponse<VersionCheckDTO> {
        return try await request("mobile/MobileConfig/version-check?platform=\(platform)&appVersion=\(appVersion)", requiresAuth: false)
    }

    // MARK: - Authentication

    func login(username: String, password: String) async throws -> APIResponse<LoginResponse> {
        let loginRequest = LoginRequest(username: username, password: password)
        let encoder = JSONEncoder()
        let body = try encoder.encode(loginRequest)

        return try await request("Auth/login", method: "POST", body: body, requiresAuth: false)
    }

    // MARK: - Device Management

    func registerDevice(_ device: DeviceRegistrationDTO) async throws -> APIResponse<DeviceRegistrationResponse> {
        let encoder = JSONEncoder()
        let body = try encoder.encode(device)

        return try await request("mobile/MobileDevice/register", method: "POST", body: body)
    }

    func getMyDevices() async throws -> APIResponse<[MobileDeviceDTO]> {
        return try await request("mobile/MobileDevice/my-devices")
    }

    func updatePushToken(deviceId: String, pushToken: String) async throws -> APIResponse<Bool> {
        let request = UpdatePushTokenRequest(deviceId: deviceId, pushToken: pushToken)
        let encoder = JSONEncoder()
        let body = try encoder.encode(request)

        return try await request("mobile/MobileDevice/push-token", method: "PUT", body: body)
    }

    // MARK: - Dashboard

    func getDashboard() async throws -> APIResponse<MobileDashboardDTO> {
        return try await request("mobile/MobileDashboard")
    }

    // MARK: - Analytics

    func trackEvent(deviceId: Int, event: AnalyticsEventDTO) async throws -> APIResponse<Bool> {
        let encoder = JSONEncoder()
        let body = try encoder.encode(event)

        return try await request("mobile/MobileAnalytics/track?deviceId=\(deviceId)", method: "POST", body: body)
    }

    func getAnalyticsSummary(days: Int = 7) async throws -> APIResponse<AnalyticsSummaryDTO> {
        return try await request("mobile/MobileAnalytics/summary?days=\(days)")
    }

    // MARK: - Sync

    func syncData(deviceId: Int, request: SyncRequestDTO) async throws -> APIResponse<SyncResponseDTO> {
        let encoder = JSONEncoder()
        let body = try encoder.encode(request)

        return try await self.request("mobile/MobileSync/sync?deviceId=\(deviceId)", method: "POST", body: body)
    }
}

// MARK: - API Error

enum APIError: Error {
    case invalidURL
    case invalidResponse
    case serverError(Int)
    case decodingError
}
```

---

## Step 3: Models (DTOs)

### Models.swift
```swift
import Foundation

// MARK: - Generic API Response

struct APIResponse<T: Decodable>: Decodable {
    let success: Bool
    let message: String?
    let data: T?
    let errors: [String]?
    let timestamp: String?
}

// MARK: - Configuration

struct MobileConfigDTO: Decodable {
    let minAppVersion: String?
    let latestAppVersion: String?
    let forceUpdate: Bool
    let maintenanceMode: Bool
    let featureFlags: [String: Bool]?
    let syncIntervalMinutes: Int
    let maxOfflineDataDays: Int
    let enableAnalytics: Bool
    let maxImageSizeMB: Int
}

struct VersionCheckDTO: Decodable {
    let isSupported: Bool
    let forceUpdate: Bool
    let maintenanceMode: Bool
}

// MARK: - Authentication

struct LoginRequest: Encodable {
    let username: String
    let password: String
}

struct LoginResponse: Decodable {
    let token: String
    let expiration: String
    let user: UserDTO
}

struct UserDTO: Decodable {
    let id: String
    let username: String
    let email: String?
    let roles: [String]
}

// MARK: - Device Management

struct DeviceRegistrationDTO: Encodable {
    let deviceId: String
    let platform: String
    let platformVersion: String
    let appVersion: String
    let pushToken: String
    let deviceModel: String
    let deviceName: String
}

struct DeviceRegistrationResponse: Decodable {
    let deviceId: Int
    let isNewDevice: Bool
    let appConfig: MobileConfigDTO
}

struct MobileDeviceDTO: Decodable {
    let id: Int
    let deviceId: String
    let platform: String
    let deviceModel: String
    let lastActiveAt: String?
    let isActive: Bool
}

struct UpdatePushTokenRequest: Encodable {
    let deviceId: String
    let pushToken: String
}

// MARK: - Dashboard

struct MobileDashboardDTO: Decodable {
    let timestamp: String
    let production: ProductionSummaryDTO
    let inventory: InventorySummaryDTO
    let sales: SalesSummaryDTO
    let recentAlerts: [AlertDTO]
}

struct ProductionSummaryDTO: Decodable {
    let activeBatches: Int
    let todayOutput: Double
    let averageYield: Double
    let machinesActive: Int
    let machinesIdle: Int
}

struct InventorySummaryDTO: Decodable {
    let totalStockValue: Double
    let lowStockItems: Int
    let outOfStockItems: Int
    let topItems: [TopStockItemDTO]
}

struct TopStockItemDTO: Decodable {
    let productId: Int
    let productName: String
    let quantity: Double
    let unit: String
}

struct SalesSummaryDTO: Decodable {
    let todaySales: Double
    let weekSales: Double
    let monthSales: Double
    let pendingOrders: Int
}

struct AlertDTO: Decodable {
    let type: String
    let message: String
    let timestamp: String
    let severity: String
}

// MARK: - Analytics

struct AnalyticsEventDTO: Encodable {
    let category: String
    let action: String
    let label: String?
    let screen: String?
    let properties: [String: AnyCodable]?
}

struct AnalyticsSummaryDTO: Decodable {
    let totalEvents: Int
    let activeUsers: Int
    let topScreens: [String]
}

// MARK: - Sync

struct SyncRequestDTO: Encodable {
    let entityType: String
    let lastSyncTimestamp: String?
    let localChanges: [AnyCodable]?
}

struct SyncResponseDTO: Decodable {
    let serverChanges: [AnyCodable]
    let conflicts: [AnyCodable]
    let lastSyncTimestamp: String
}

// Helper to encode/decode Any values
struct AnyCodable: Codable {
    let value: Any

    init(_ value: Any) {
        self.value = value
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()

        if let int = try? container.decode(Int.self) {
            value = int
        } else if let double = try? container.decode(Double.self) {
            value = double
        } else if let string = try? container.decode(String.self) {
            value = string
        } else if let bool = try? container.decode(Bool.self) {
            value = bool
        } else if let array = try? container.decode([AnyCodable].self) {
            value = array.map { $0.value }
        } else if let dictionary = try? container.decode([String: AnyCodable].self) {
            value = dictionary.mapValues { $0.value }
        } else {
            value = NSNull()
        }
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()

        if let int = value as? Int {
            try container.encode(int)
        } else if let double = value as? Double {
            try container.encode(double)
        } else if let string = value as? String {
            try container.encode(string)
        } else if let bool = value as? Bool {
            try container.encode(bool)
        } else if let array = value as? [Any] {
            try container.encode(array.map { AnyCodable($0) })
        } else if let dictionary = value as? [String: Any] {
            try container.encode(dictionary.mapValues { AnyCodable($0) })
        } else {
            try container.encodeNil()
        }
    }
}
```

---

## Step 4: Token Manager

### TokenManager.swift
```swift
import Foundation

class TokenManager {
    static let shared = TokenManager()

    private let tokenKey = "jwt_token"
    private let deviceIdKey = "device_id"

    func saveToken(_ token: String) {
        UserDefaults.standard.set(token, forKey: tokenKey)
    }

    func getToken() -> String? {
        return UserDefaults.standard.string(forKey: tokenKey)
    }

    func clearToken() {
        UserDefaults.standard.removeObject(forKey: tokenKey)
    }

    func getDeviceId() -> String {
        if let deviceId = UserDefaults.standard.string(forKey: deviceIdKey) {
            return deviceId
        }

        let deviceId = UIDevice.current.identifierForVendor?.uuidString ?? UUID().uuidString
        UserDefaults.standard.set(deviceId, forKey: deviceIdKey)
        return deviceId
    }

    func isLoggedIn() -> Bool {
        return getToken() != nil
    }
}
```

---

## Step 5: Firebase Push Notifications

### AppDelegate.swift
```swift
import UIKit
import FirebaseCore
import FirebaseMessaging
import UserNotifications

class AppDelegate: NSObject, UIApplicationDelegate, UNUserNotificationCenterDelegate, MessagingDelegate {

    func application(_ application: UIApplication,
                    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {

        // Configure Firebase
        FirebaseApp.configure()

        // Set up notifications
        UNUserNotificationCenter.current().delegate = self
        Messaging.messaging().delegate = self

        // Request notification permission
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
            print("Notification permission granted: \(granted)")
        }

        application.registerForRemoteNotifications()

        return true
    }

    // MARK: - FCM Token

    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        print("FCM Token: \(fcmToken ?? "nil")")

        // Send token to backend
        if let token = fcmToken {
            Task {
                do {
                    let deviceId = TokenManager.shared.getDeviceId()
                    _ = try await APIService.shared.updatePushToken(deviceId: deviceId, pushToken: token)
                    print("Push token updated on server")
                } catch {
                    print("Error updating push token: \(error)")
                }
            }
        }
    }

    // MARK: - Notifications

    func userNotificationCenter(_ center: UNUserNotificationCenter,
                               willPresent notification: UNNotification,
                               withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        // Show notification even when app is in foreground
        completionHandler([[.banner, .sound, .badge]])
    }

    func userNotificationCenter(_ center: UNUserNotificationCenter,
                               didReceive response: UNNotificationResponse,
                               withCompletionHandler completionHandler: @escaping () -> Void) {
        // Handle notification tap
        let userInfo = response.notification.request.content.userInfo
        print("Notification tapped with data: \(userInfo)")

        // Navigate to appropriate screen based on notification data
        // NotificationCenter.default.post(name: NSNotification.Name("NavigateToScreen"), object: userInfo)

        completionHandler()
    }
}
```

### RmmsApp.swift
```swift
import SwiftUI
import FirebaseCore

@main
struct RmmsApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

---

## Step 6: ViewModels

### AuthViewModel.swift
```swift
import Foundation
import Combine

@MainActor
class AuthViewModel: ObservableObject {
    @Published var isLoggedIn = false
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var user: UserDTO?

    init() {
        self.isLoggedIn = TokenManager.shared.isLoggedIn()
    }

    func login(username: String, password: String) async {
        isLoading = true
        errorMessage = nil

        do {
            let response = try await APIService.shared.login(username: username, password: password)

            if response.success, let loginData = response.data {
                TokenManager.shared.saveToken(loginData.token)
                self.user = loginData.user
                self.isLoggedIn = true

                // Register device after login
                await registerDevice()
            } else {
                errorMessage = response.message ?? "Login failed"
            }
        } catch {
            errorMessage = "Error: \(error.localizedDescription)"
        }

        isLoading = false
    }

    func logout() {
        TokenManager.shared.clearToken()
        isLoggedIn = false
        user = nil
    }

    private func registerDevice() async {
        do {
            let deviceId = TokenManager.shared.getDeviceId()
            let appVersion = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0.0"

            let device = DeviceRegistrationDTO(
                deviceId: deviceId,
                platform: "iOS",
                platformVersion: UIDevice.current.systemVersion,
                appVersion: appVersion,
                pushToken: "temp-token", // Will be updated when FCM token is received
                deviceModel: UIDevice.current.model,
                deviceName: UIDevice.current.name
            )

            let response = try await APIService.shared.registerDevice(device)
            print("Device registered: \(response.success)")
        } catch {
            print("Error registering device: \(error)")
        }
    }
}
```

### DashboardViewModel.swift
```swift
import Foundation
import Combine

@MainActor
class DashboardViewModel: ObservableObject {
    @Published var dashboard: MobileDashboardDTO?
    @Published var isLoading = false
    @Published var errorMessage: String?

    func loadDashboard() async {
        isLoading = true
        errorMessage = nil

        do {
            let response = try await APIService.shared.getDashboard()

            if response.success, let dashboardData = response.data {
                self.dashboard = dashboardData

                // Track analytics
                let event = AnalyticsEventDTO(
                    category: "navigation",
                    action: "screen_view",
                    label: "dashboard",
                    screen: "Dashboard",
                    properties: nil
                )
                try? await APIService.shared.trackEvent(deviceId: 1, event: event)
            } else {
                errorMessage = response.message ?? "Failed to load dashboard"
            }
        } catch {
            errorMessage = "Error: \(error.localizedDescription)"
        }

        isLoading = false
    }
}
```

---

## Step 7: SwiftUI Views

### ContentView.swift
```swift
import SwiftUI

struct ContentView: View {
    @StateObject private var authVM = AuthViewModel()

    var body: some View {
        Group {
            if authVM.isLoggedIn {
                DashboardView()
                    .environmentObject(authVM)
            } else {
                LoginView()
                    .environmentObject(authVM)
            }
        }
    }
}
```

### LoginView.swift
```swift
import SwiftUI

struct LoginView: View {
    @EnvironmentObject var authVM: AuthViewModel

    @State private var username = "admin"
    @State private var password = "Admin@123"

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Image(systemName: "building.2.fill")
                    .font(.system(size: 80))
                    .foregroundColor(.blue)

                Text("RMMS")
                    .font(.largeTitle)
                    .fontWeight(.bold)

                TextField("Username", text: $username)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .autocapitalization(.none)

                SecureField("Password", text: $password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())

                if let error = authVM.errorMessage {
                    Text(error)
                        .foregroundColor(.red)
                        .font(.caption)
                }

                Button {
                    Task {
                        await authVM.login(username: username, password: password)
                    }
                } label: {
                    if authVM.isLoading {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    } else {
                        Text("Login")
                            .fontWeight(.bold)
                    }
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(10)
                .disabled(authVM.isLoading)

                Spacer()
            }
            .padding()
            .navigationTitle("Login")
        }
    }
}
```

### DashboardView.swift
```swift
import SwiftUI

struct DashboardView: View {
    @EnvironmentObject var authVM: AuthViewModel
    @StateObject private var dashboardVM = DashboardViewModel()

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 16) {
                    if dashboardVM.isLoading {
                        ProgressView("Loading...")
                    } else if let error = dashboardVM.errorMessage {
                        Text(error)
                            .foregroundColor(.red)
                        Button("Retry") {
                            Task {
                                await dashboardVM.loadDashboard()
                            }
                        }
                    } else if let dashboard = dashboardVM.dashboard {
                        DashboardContent(dashboard: dashboard)
                    }
                }
                .padding()
            }
            .navigationTitle("Dashboard")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Logout") {
                        authVM.logout()
                    }
                }
            }
            .task {
                await dashboardVM.loadDashboard()
            }
            .refreshable {
                await dashboardVM.loadDashboard()
            }
        }
    }
}

struct DashboardContent: View {
    let dashboard: MobileDashboardDTO

    var body: some View {
        // Production Card
        VStack(alignment: .leading, spacing: 8) {
            Text("Production")
                .font(.headline)

            HStack {
                StatView(title: "Active Batches", value: "\(dashboard.production.activeBatches)")
                StatView(title: "Today Output", value: String(format: "%.1f", dashboard.production.todayOutput))
            }

            HStack {
                StatView(title: "Average Yield", value: String(format: "%.1f%%", dashboard.production.averageYield))
                StatView(title: "Machines Active", value: "\(dashboard.production.machinesActive)")
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(10)
        .shadow(radius: 2)

        // Inventory Card
        VStack(alignment: .leading, spacing: 8) {
            Text("Inventory")
                .font(.headline)

            HStack {
                StatView(title: "Total Value", value: String(format: "$%.2f", dashboard.inventory.totalStockValue))
                StatView(title: "Low Stock", value: "\(dashboard.inventory.lowStockItems)")
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(10)
        .shadow(radius: 2)

        // Sales Card
        VStack(alignment: .leading, spacing: 8) {
            Text("Sales")
                .font(.headline)

            HStack {
                StatView(title: "Today", value: String(format: "$%.2f", dashboard.sales.todaySales))
                StatView(title: "This Week", value: String(format: "$%.2f", dashboard.sales.weekSales))
            }

            HStack {
                StatView(title: "This Month", value: String(format: "$%.2f", dashboard.sales.monthSales))
                StatView(title: "Pending Orders", value: "\(dashboard.sales.pendingOrders)")
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(10)
        .shadow(radius: 2)
    }
}

struct StatView: View {
    let title: String
    let value: String

    var body: some View {
        VStack(alignment: .leading) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            Text(value)
                .font(.title3)
                .fontWeight(.semibold)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}
```

---

## Step 8: Info.plist Configuration

Add these keys to `Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>

<key>UIBackgroundModes</key>
<array>
    <string>fetch</string>
    <string>remote-notification</string>
</array>
```

---

## Testing the App

1. **Update BASE_URL** in `APIService.swift` with your server IP
2. **Add GoogleService-Info.plist** from Firebase Console
3. **Build and run** the app on simulator or device
4. **Test login** with credentials
5. **Verify device registration** in server logs
6. **Test push notifications** (physical device required)
7. **Check dashboard loading**

---

## Complete Flow

```
App Launch
   ↓
Check if logged in (Token exists)
   ↓
   Yes → Show Dashboard
   ↓
   No → Show Login Screen
   ↓
User Logs In
   ↓
Save JWT Token
   ↓
Register Device (with FCM token)
   ↓
Navigate to Dashboard
   ↓
Load Dashboard Data
   ↓
Track Analytics (screen view)
   ↓
User Navigates App
   ↓
Receive Push Notifications
```

---

## Troubleshooting

1. **Network Error**: Check server IP and ensure iOS device on same WiFi
2. **401 Unauthorized**: JWT token expired, logout and login again
3. **Push Notifications Not Working**: Test on physical device (simulator doesn't support APNS)
4. **App Transport Security Error**: Ensure NSAllowsArbitraryLoads is set in Info.plist

---

**Your iOS app is now connected to RMMS backend!**
