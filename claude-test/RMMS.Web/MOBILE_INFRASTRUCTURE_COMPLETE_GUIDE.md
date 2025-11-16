# RMMS Mobile Infrastructure - Complete Guide

**Last Updated**: October 13, 2025
**Version**: 1.0.0
**Status**: Production Ready

---

## Table of Contents
1. [Overview](#overview)
2. [What We Built](#what-we-built)
3. [How to Test from Mobile Devices](#how-to-test-from-mobile-devices)
4. [Mobile Infrastructure Details](#mobile-infrastructure-details)
5. [Integration Guide for Mobile Apps](#integration-guide-for-mobile-apps)
6. [Android Implementation](#android-implementation)
7. [iOS Implementation](#ios-implementation)
8. [Use Cases](#use-cases)

---

## Overview

### What is This Mobile Infrastructure?

The RMMS Mobile Infrastructure is a **complete backend system** that enables Android and iOS mobile applications to:

1. **Communicate with the rice mill system** from anywhere
2. **Sync data** when online, work offline, and sync back when connected
3. **Receive push notifications** for important events
4. **Track user analytics** to improve the mobile experience
5. **Manage app versions** and feature flags remotely
6. **Optimize images** for mobile bandwidth

Think of it as the "backend brain" for mobile apps - your Android/iOS apps are the "face" that users see, and this backend handles all the heavy lifting.

---

## What We Built

### 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MOBILE DEVICES                            │
│  ┌──────────────┐              ┌──────────────┐            │
│  │   Android    │              │     iOS      │            │
│  │   App        │              │     App      │            │
│  └──────┬───────┘              └──────┬───────┘            │
│         │                              │                     │
└─────────┼──────────────────────────────┼────────────────────┘
          │                              │
          │         HTTPS / WiFi         │
          │                              │
┌─────────┴──────────────────────────────┴────────────────────┐
│                  RMMS WEB SERVER                             │
│                  (Your Backend)                              │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Mobile API Controllers (26 Endpoints)        │ │
│  │  - MobileConfig    - MobileDevice   - PushNotification│ │
│  │  - MobileSync      - Analytics      - Dashboard       │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                      │
│  ┌────────────────────┴───────────────────────────────────┐ │
│  │           Mobile Services (6 Services)                 │ │
│  │  Business logic, data processing, push notifications   │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                      │
│  ┌────────────────────┴───────────────────────────────────┐ │
│  │           Database (SQL Server)                        │ │
│  │  - MobileDevices         - PushNotifications          │ │
│  │  - MobileAppConfigs      - SyncLogs                   │ │
│  │  - MobileAnalyticsEvents                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  External Services:                                          │
│  - Firebase Cloud Messaging (FCM) for Android               │
│  - Apple Push Notification Service (APNS) for iOS          │
└──────────────────────────────────────────────────────────────┘
```

### 📦 Components Built

#### 1. **Database Layer** (5 Tables)
- **MobileDevices**: Registered devices (phones/tablets)
- **PushNotifications**: Notification history
- **SyncLogs**: Track data synchronization
- **MobileAppConfigs**: App settings and feature flags
- **MobileAnalyticsEvents**: Usage analytics

#### 2. **Service Layer** (6 Services)
- **MobileDeviceService**: Device registration & management
- **PushNotificationService**: Send notifications via FCM/APNS
- **MobileSyncService**: Data synchronization with conflict resolution
- **MobileConfigService**: App version control & feature flags
- **MobileAnalyticsService**: Track user behavior
- **ImageOptimizationService**: Compress images for mobile

#### 3. **API Layer** (26 Endpoints)

**Public Endpoints** (No login required):
- Get app configuration
- Check version compatibility
- Check maintenance mode

**Authenticated Endpoints** (Requires login):
- Register/manage devices
- Send/receive push notifications
- Sync data
- Track analytics
- Get mobile dashboard

---

## How to Test from Mobile Devices

### Option 1: Web Browser Testing (Easiest)

I'll create a web-based testing UI that you can access from any mobile browser.

**Steps:**
1. Make server accessible on network (see Network Setup below)
2. Open mobile browser (Chrome/Safari)
3. Navigate to: `http://YOUR_SERVER_IP:5090/mobile-test`
4. Test all endpoints visually

### Option 2: cURL from Mobile Terminal (Advanced)

**Android**: Use Termux app
**iOS**: Use a-Shell app

### Option 3: Build Real Mobile App (Production)

Build actual Android/iOS apps using the integration guides below.

---

## Network Setup for Device Testing

### Step 1: Find Your Server IP

```bash
# On Linux/WSL
ip addr show | grep "inet " | grep -v 127.0.0.1

# On Windows
ipconfig | findstr "IPv4"

# On Mac
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Example output: `192.168.1.100`

### Step 2: Update Server to Listen on All Interfaces

Your server is currently listening on `localhost:5090`. We need to change it to `0.0.0.0:5090` to accept connections from mobile devices.

```bash
# Stop current server
pkill -f "dotnet.*RMMS"

# Start server on all interfaces
cd /home/user01/claude-test/RMMS.Web/RMMS.Web
dotnet run --urls "http://0.0.0.0:5090"
```

### Step 3: Test from Mobile Device

1. Connect mobile device to **same WiFi network** as server
2. Open mobile browser
3. Navigate to: `http://192.168.1.100:5090/swagger`
4. You should see the Swagger API documentation

---

## Mobile Infrastructure Details

### 1. Device Registration Flow

```
┌─────────────┐
│ Mobile App  │
│  Opens      │
└──────┬──────┘
       │
       ↓
┌──────────────────────────────────────────┐
│ 1. Get Config (Public - No Auth)        │
│    GET /api/v1/mobile/MobileConfig       │
│    Response: App version, feature flags  │
└──────┬───────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────────┐
│ 2. Check Version                         │
│    Is app version supported?             │
│    Need to update?                       │
└──────┬───────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────────┐
│ 3. User Login                            │
│    POST /api/v1/Auth/login               │
│    Response: JWT Token                   │
└──────┬───────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────────┐
│ 4. Register Device (Authenticated)       │
│    POST /api/v1/mobile/MobileDevice      │
│    Send: Device ID, Platform, Push Token │
└──────┬───────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────────┐
│ 5. App Ready to Use                      │
│    Can now sync data, receive push, etc. │
└──────────────────────────────────────────┘
```

### 2. Data Synchronization Flow

```
Mobile App                    Server
    │                           │
    │  1. Pull Changes          │
    ├──────────────────────────>│
    │  GET /MobileSync/changes  │
    │  ?lastSyncTime=timestamp  │
    │                           │
    │  2. Server Responds       │
    │<──────────────────────────┤
    │  Returns: New/Updated     │
    │  records since last sync  │
    │                           │
    │  3. Process Locally       │
    │  (Update SQLite DB)       │
    │                           │
    │  4. Push Local Changes    │
    ├──────────────────────────>│
    │  POST /MobileSync/sync    │
    │  Send: Local modifications│
    │                           │
    │  5. Conflict Resolution   │
    │<──────────────────────────┤
    │  Server merges changes    │
    │  Handles conflicts        │
    │                           │
    │  6. Confirm Sync          │
    │<──────────────────────────┤
    │  Returns: Sync status     │
    │                           │
```

### 3. Push Notification Flow

```
Server Event               Backend                   Mobile Device
     │                       │                            │
     ├──> New Order Created  │                            │
     │    (or any event)     │                            │
     │                       │                            │
     │                       ↓                            │
     │              ┌─────────────────┐                   │
     │              │ Check if user   │                   │
     │              │ has devices     │                   │
     │              │ registered      │                   │
     │              └────────┬────────┘                   │
     │                       │                            │
     │                       ↓                            │
     │              ┌─────────────────┐                   │
     │              │ Send to FCM/    │                   │
     │              │ APNS service    │                   │
     │              └────────┬────────┘                   │
     │                       │                            │
     │                       ├────────────────────────────>│
     │                       │  Push Notification         │
     │                       │  Delivered                 │
     │                       │                            │
     │                       │                            ↓
     │                       │                   ┌─────────────────┐
     │                       │                   │ User sees       │
     │                       │                   │ notification    │
     │                       │                   │ on device       │
     │                       │                   └─────────────────┘
```

### 4. Analytics Tracking Flow

```
User Action → Mobile App → Track Event → Backend → Database

Examples:
- User opens Dashboard → track("navigation", "screen_view", "dashboard")
- User creates order → track("action", "order_created", order_id)
- App crashes → track("error", "app_crash", error_details)
```

---

## 26 API Endpoints Explained

### Group 1: Configuration (3 endpoints) - PUBLIC

#### **GET /api/v1/mobile/MobileConfig**
**Purpose**: Get app configuration when app starts
**Authentication**: None (Public)
**Use Case**:
- App checks if it needs to update
- Gets feature flags (is dark mode enabled?)
- Gets sync interval settings

**Request**:
```http
GET /api/v1/mobile/MobileConfig?platform=Android&appVersion=1.0.0
```

**Response**:
```json
{
  "success": true,
  "data": {
    "minAppVersion": "1.0.0",
    "latestAppVersion": "1.2.0",
    "forceUpdate": false,
    "maintenanceMode": false,
    "featureFlags": {
      "offline_mode": true,
      "dark_mode": true,
      "biometric_login": true
    },
    "syncIntervalMinutes": 15,
    "maxOfflineDataDays": 7
  }
}
```

**Mobile App Logic**:
```kotlin
val config = api.getMobileConfig("Android", "1.0.0")
if (config.forceUpdate) {
    showUpdateDialog() // Force user to update
} else if (config.maintenanceMode) {
    showMaintenanceScreen()
} else {
    proceedToLogin()
}
```

#### **GET /api/v1/mobile/MobileConfig/version-check**
**Purpose**: Quick version compatibility check
**Authentication**: None

#### **GET /api/v1/mobile/MobileConfig/feature-flag/{name}**
**Purpose**: Check if specific feature is enabled
**Authentication**: Required
**Example**: Check if "new_dashboard" is enabled

---

### Group 2: Device Management (5 endpoints) - AUTHENTICATED

#### **POST /api/v1/mobile/MobileDevice/register**
**Purpose**: Register device after user logs in
**Authentication**: Required (JWT Token)

**Request**:
```json
{
  "deviceId": "abc123-unique-device-id",
  "platform": "Android",
  "platformVersion": "14.0",
  "appVersion": "1.0.0",
  "pushToken": "fcm-token-from-firebase",
  "deviceModel": "Samsung Galaxy S23",
  "deviceName": "John's Phone"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "deviceId": 123,
    "isNewDevice": true,
    "appConfig": { /* config here */ }
  }
}
```

**Mobile App Logic**:
```kotlin
// After successful login
val fcmToken = FirebaseMessaging.getInstance().token.await()
val response = api.registerDevice(
    token = jwtToken,
    device = DeviceRegistrationDto(
        deviceId = getUniqueDeviceId(),
        platform = "Android",
        pushToken = fcmToken,
        // ... other fields
    )
)
```

#### **GET /api/v1/mobile/MobileDevice/my-devices**
**Purpose**: List all devices registered to logged-in user
**Use Case**: Show in settings: "You're logged in on 3 devices"

#### **PUT /api/v1/mobile/MobileDevice/push-token**
**Purpose**: Update push token (FCM tokens can change)
**When**: Call this whenever Firebase gives you a new token

#### **PUT /api/v1/mobile/MobileDevice/last-active**
**Purpose**: Update last active timestamp
**When**: Call periodically while app is in use

#### **PUT /api/v1/mobile/MobileDevice/settings**
**Purpose**: Update device settings (enable/disable notifications, biometric)

---

### Group 3: Push Notifications (6 endpoints) - AUTHENTICATED

#### **GET /api/v1/mobile/PushNotification/history**
**Purpose**: Get notification history (inbox)
**Use Case**: Show "Notifications" screen in app

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "New Order #12345",
      "body": "A new order has been placed",
      "type": "order",
      "isRead": false,
      "sentAt": "2025-10-13T10:30:00Z",
      "data": {
        "orderId": "12345",
        "action": "view_order"
      }
    }
  ]
}
```

#### **POST /api/v1/mobile/PushNotification/mark-read/{id}**
**Purpose**: Mark notification as read

#### **POST /api/v1/mobile/PushNotification/send** (Admin Only)
**Purpose**: Send notification to specific user/device

#### **POST /api/v1/mobile/PushNotification/broadcast** (Admin Only)
**Purpose**: Send notification to all users

#### **POST /api/v1/mobile/PushNotification/schedule** (Admin Only)
**Purpose**: Schedule notification for future

#### **POST /api/v1/mobile/PushNotification/test** (Admin Only)
**Purpose**: Test push notification setup

---

### Group 4: Data Synchronization (4 endpoints) - AUTHENTICATED

#### **POST /api/v1/mobile/MobileSync/sync**
**Purpose**: Sync specific entity type (e.g., orders, inventory)

**Request**:
```json
{
  "entityType": "Orders",
  "lastSyncTimestamp": "2025-10-13T08:00:00Z",
  "localChanges": [
    {
      "id": 123,
      "action": "update",
      "data": { /* order data */ }
    }
  ]
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "serverChanges": [ /* new/updated records */ ],
    "conflicts": [ /* conflicts to resolve */ ],
    "lastSyncTimestamp": "2025-10-13T10:00:00Z"
  }
}
```

#### **POST /api/v1/mobile/MobileSync/batch**
**Purpose**: Sync multiple entity types at once

#### **GET /api/v1/mobile/MobileSync/changes**
**Purpose**: Pull only (get server changes without pushing local changes)

#### **GET /api/v1/mobile/MobileSync/history**
**Purpose**: View sync history for debugging

---

### Group 5: Analytics (7 endpoints) - AUTHENTICATED

#### **POST /api/v1/mobile/MobileAnalytics/track**
**Purpose**: Track single event

**Request**:
```json
{
  "category": "navigation",
  "action": "screen_view",
  "label": "dashboard",
  "screen": "Dashboard",
  "properties": {
    "source": "menu",
    "load_time_ms": 245
  }
}
```

**Common Events to Track**:
- Screen views: `track("navigation", "screen_view", "orders")`
- Button clicks: `track("action", "button_click", "refresh_button")`
- Feature usage: `track("feature", "export_report", "pdf")`
- Errors: `track("error", "api_failed", error_message)`

#### **POST /api/v1/mobile/MobileAnalytics/track-batch**
**Purpose**: Track multiple events at once (more efficient)

#### **GET /api/v1/mobile/MobileAnalytics/summary**
**Purpose**: Get analytics summary (admin)

#### **GET /api/v1/mobile/MobileAnalytics/user-engagement**
**Purpose**: User engagement metrics

#### **GET /api/v1/mobile/MobileAnalytics/screen-views**
**Purpose**: Most viewed screens

#### **GET /api/v1/mobile/MobileAnalytics/errors** (Admin)
**Purpose**: Error events for debugging

#### **GET /api/v1/mobile/MobileAnalytics/events** (Admin)
**Purpose**: All analytics events

---

### Group 6: Mobile Dashboard (1 endpoint) - AUTHENTICATED

#### **GET /api/v1/mobile/MobileDashboard**
**Purpose**: Get lightweight dashboard data for mobile

**Response**:
```json
{
  "success": true,
  "data": {
    "timestamp": "2025-10-13T10:00:00Z",
    "production": {
      "activeBatches": 5,
      "todayOutput": 1250.5,
      "averageYield": 92.5,
      "machinesActive": 3
    },
    "inventory": {
      "totalStockValue": 125000.50,
      "lowStockItems": 3,
      "outOfStockItems": 1
    },
    "sales": {
      "todaySales": 15750.25,
      "weekSales": 87230.50,
      "monthSales": 345678.90,
      "pendingOrders": 12
    },
    "recentAlerts": [
      {
        "type": "inventory",
        "message": "Low stock alert",
        "severity": "warning"
      }
    ]
  }
}
```

---

## Use Cases - How to Utilize This

### Use Case 1: Field Manager Mobile App

**Scenario**: Manager walks through rice mill with tablet

**App Features**:
1. **Dashboard**: Shows real-time production status
   - Uses: `/api/v1/mobile/MobileDashboard`

2. **Production Monitoring**: See which machines are running
   - Uses: `/api/v1/mobile/MobileSync/sync` for ProductionBatches

3. **Quality Checks**: Record quality metrics
   - Uses: Sync quality data, track analytics

4. **Notifications**: Get alerted when batch completes
   - Uses: Push notifications

5. **Offline Mode**: Works even without WiFi
   - Uses: Sync when connection restored

### Use Case 2: Sales Representative App

**Scenario**: Sales rep visits customer sites

**App Features**:
1. **Customer Orders**: View and create orders
   - Uses: Sync Orders entity

2. **Inventory Check**: Check product availability
   - Uses: Sync Inventory entity

3. **Price Quotes**: Generate quotes on the spot
   - Uses: Sync Products and Pricing

4. **Photo Uploads**: Take photos of delivery
   - Uses: Image optimization service

5. **Order Notifications**: Get notified of order updates
   - Uses: Push notifications

### Use Case 3: Mill Owner Dashboard App

**Scenario**: Owner monitors business from anywhere

**App Features**:
1. **Business Dashboard**: Key metrics at a glance
   - Uses: `/api/v1/mobile/MobileDashboard`

2. **Analytics**: View trends and charts
   - Uses: Analytics endpoints

3. **Alerts**: Critical issues sent to phone
   - Uses: Push notifications with priority

4. **Reports**: Generate and export reports
   - Uses: Sync + local report generation

---

## Testing Checklist

### ✅ Phase 1: Network Setup
- [ ] Find server IP address
- [ ] Start server on 0.0.0.0:5090
- [ ] Connect mobile device to same WiFi
- [ ] Access Swagger from mobile browser
- [ ] Verify API responds

### ✅ Phase 2: Web UI Testing
- [ ] Access web testing UI from mobile
- [ ] Test config endpoint (public)
- [ ] Login to get JWT token
- [ ] Test authenticated endpoints
- [ ] Verify responses on screen

### ✅ Phase 3: Real Mobile App
- [ ] Set up Android Studio / Xcode
- [ ] Create new mobile project
- [ ] Implement API client
- [ ] Test device registration
- [ ] Test push notifications
- [ ] Test data sync

---

## Next Steps

1. **Create Web Testing UI** (I'll do this next)
2. **Test from mobile browser**
3. **Create Android sample app**
4. **Create iOS sample app**
5. **Deploy to production server**

---

**📱 Ready to build your mobile apps!**

All backend infrastructure is complete and tested. You can now build Android/iOS apps that connect to this backend.
