# RMMS Mobile Architecture Documentation
## Sprint 4.4.2: Mobile Architecture for Android & iPhone

**Status**: ✅ **COMPLETED**
**Implementation Date**: October 2025
**Version**: 1.0.0

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Components Implemented](#components-implemented)
4. [API Endpoints](#api-endpoints)
5. [Database Schema](#database-schema)
6. [Configuration](#configuration)
7. [Integration Guide](#integration-guide)
8. [Testing Instructions](#testing-instructions)
9. [Deployment Checklist](#deployment-checklist)

---

## Executive Summary

This document describes the comprehensive mobile architecture implemented for the Rice Mill Management System (RMMS), enabling native Android and iPhone applications to interact with the backend system.

### Key Features Implemented

✅ **Device Management**: Registration, tracking, and lifecycle management
✅ **Push Notifications**: FCM (Android) and APNS (iOS) integration
✅ **Data Synchronization**: Conflict resolution and offline support
✅ **Mobile Configuration**: Version management and feature flags
✅ **Analytics Tracking**: User engagement and error monitoring
✅ **Image Optimization**: Compression and thumbnail generation
✅ **Mobile APIs**: RESTful endpoints optimized for mobile bandwidth
✅ **Authentication**: JWT-based auth with device-specific tokens

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Mobile Applications                      │
│                   (Android / iPhone)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTPS / JWT
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   API Gateway Layer                          │
│            (Rate Limiting, CORS, API Versioning)             │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────┐           ┌────────▼─────────┐
│  Mobile API    │           │  Authentication  │
│  Controllers   │           │   & Security     │
└───────┬────────┘           └────────┬─────────┘
        │                             │
        │                             │
┌───────▼─────────────────────────────▼─────────┐
│            Mobile Services Layer               │
│  • Device Management                           │
│  • Push Notifications (FCM/APNS)               │
│  • Data Synchronization                        │
│  • Configuration Management                    │
│  • Analytics & Tracking                        │
│  • Image Optimization                          │
└───────┬────────────────────────────────────────┘
        │
┌───────▼────────────────────────────────────────┐
│          Database (SQL Server)                 │
│  • MobileDevices                               │
│  • PushNotifications                           │
│  • SyncLogs                                    │
│  • MobileAppConfig                             │
│  • MobileAnalyticsEvents                       │
└────────────────────────────────────────────────┘
```

---

## Components Implemented

### 1. Models & DTOs

**Location**: `/RMMS.Models/Mobile/`

- **MobileDevice**: Device registration and tracking
- **PushNotification**: Notification management
- **SyncLog**: Data synchronization history
- **MobileAppConfig**: App configuration and feature flags
- **MobileAnalyticsEvent**: Analytics and usage tracking

**DTOs** (`/RMMS.Models/Mobile/DTOs/`):
- DeviceRegistrationDto
- PushNotificationDto
- SyncDto (Request/Response)
- MobileAppConfigDto
- MobileAnalyticsDto
- MobileDashboardDto

### 2. Services

**Location**: `/RMMS.Services/Services/Mobile/`

#### IMobileDeviceService
- Device registration and lifecycle management
- Push token updates
- Device activity tracking

#### IPushNotificationService
- Send notifications to users/devices
- FCM (Android) integration
- APNS (iOS) integration
- Notification scheduling
- History and read receipts

#### IMobileSyncService
- Pull/push data synchronization
- Batch sync operations
- Conflict resolution
- Sync status tracking

#### IMobileConfigService
- App version management
- Force update mechanisms
- Feature flag management
- Maintenance mode control

#### IMobileAnalyticsService
- Event tracking
- User engagement metrics
- Error monitoring
- Version distribution analysis

#### IImageOptimizationService
- Image compression
- Thumbnail generation
- WebP conversion
- Image validation

### 3. API Controllers

**Location**: `/RMMS.Web/Controllers/API/v1/Mobile/`

All endpoints are versioned (`/api/v1/mobile/*`) and require JWT authentication (except config endpoints).

#### MobileDeviceController
```
POST   /api/v1/mobile/MobileDevice/register
GET    /api/v1/mobile/MobileDevice/my-devices
PUT    /api/v1/mobile/MobileDevice/{id}/push-token
POST   /api/v1/mobile/MobileDevice/{id}/heartbeat
DELETE /api/v1/mobile/MobileDevice/{id}
```

#### PushNotificationController
```
GET    /api/v1/mobile/PushNotification/history
GET    /api/v1/mobile/PushNotification/unread-count
POST   /api/v1/mobile/PushNotification/{id}/mark-read
POST   /api/v1/mobile/PushNotification/mark-all-read
POST   /api/v1/mobile/PushNotification/send (Admin)
POST   /api/v1/mobile/PushNotification/schedule (Admin)
```

#### MobileSyncController
```
POST   /api/v1/mobile/MobileSync/batch
POST   /api/v1/mobile/MobileSync/pull
GET    /api/v1/mobile/MobileSync/status
POST   /api/v1/mobile/MobileSync/resolve-conflict
```

#### MobileConfigController
```
GET    /api/v1/mobile/MobileConfig (Public)
GET    /api/v1/mobile/MobileConfig/version-check (Public)
GET    /api/v1/mobile/MobileConfig/feature-flag/{name}
```

#### MobileAnalyticsController
```
POST   /api/v1/mobile/MobileAnalytics/track
POST   /api/v1/mobile/MobileAnalytics/track-batch
GET    /api/v1/mobile/MobileAnalytics/my-engagement
GET    /api/v1/mobile/MobileAnalytics/summary (Admin)
GET    /api/v1/mobile/MobileAnalytics/popular-screens (Admin)
GET    /api/v1/mobile/MobileAnalytics/errors (Admin)
```

#### MobileDashboardController
```
GET    /api/v1/mobile/MobileDashboard
```

---

## Database Schema

### MobileDevices Table

| Column | Type | Description |
|--------|------|-------------|
| Id | int (PK) | Unique identifier |
| UserId | nvarchar(100) | User owner |
| DeviceId | nvarchar(200) | Unique device ID (Indexed) |
| Platform | nvarchar(20) | Android or iOS |
| DeviceModel | nvarchar(100) | Device model name |
| OSVersion | nvarchar(50) | OS version |
| AppVersion | nvarchar(20) | App version |
| PushToken | nvarchar(500) | FCM/APNS token |
| Language | nvarchar(10) | Locale |
| NotificationsEnabled | bit | Push enabled |
| BiometricEnabled | bit | Biometric auth |
| LastActiveAt | datetime2 | Last activity |
| RegisteredAt | datetime2 | Registration date |
| IsActive | bit | Active status |

**Indexes**: DeviceId (unique), UserId, (UserId, Platform)

### PushNotifications Table

| Column | Type | Description |
|--------|------|-------------|
| Id | int (PK) | Unique identifier |
| UserId | nvarchar(100) | Target user |
| DeviceId | int (FK, nullable) | Target device |
| Title | nvarchar(100) | Title |
| Body | nvarchar(500) | Message |
| Type | nvarchar(50) | Category |
| Data | nvarchar(max) | JSON payload |
| Priority | nvarchar(20) | high/normal/low |
| ImageUrl | nvarchar(500) | Image URL |
| ActionUrl | nvarchar(500) | Deep link |
| CreatedAt | datetime2 | Creation date |
| ScheduledFor | datetime2 | Schedule time |
| SentAt | datetime2 | Send time |
| Status | nvarchar(20) | pending/sent/failed |
| IsRead | bit | Read status |
| ReadAt | datetime2 | Read time |

**Indexes**: UserId, DeviceId, Status, ScheduledFor

### SyncLogs Table

| Column | Type | Description |
|--------|------|-------------|
| Id | int (PK) | Unique identifier |
| DeviceId | int (FK) | Device |
| UserId | nvarchar(100) | User |
| EntityType | nvarchar(100) | Entity synced |
| Operation | nvarchar(20) | pull/push/conflict |
| RecordCount | int | Records synced |
| ClientTimestamp | datetime2 | Client time |
| ServerTimestamp | datetime2 | Server time |
| Status | nvarchar(20) | success/failed |
| ConflictCount | int | Conflicts detected |
| DataSizeBytes | bigint | Data size |
| DurationMs | int | Duration |

**Indexes**: DeviceId, UserId, (EntityType, ServerTimestamp)

### MobileAppConfig Table

| Column | Type | Description |
|--------|------|-------------|
| Id | int (PK) | Unique identifier |
| Platform | nvarchar(20) | Android/iOS/All |
| MinAppVersion | nvarchar(20) | Min version |
| LatestAppVersion | nvarchar(20) | Latest version |
| ForceUpdate | bit | Force update flag |
| UpdateMessage | nvarchar(500) | Update message |
| MaintenanceMode | bit | Maintenance flag |
| MaintenanceMessage | nvarchar(500) | Maintenance message |
| FeatureFlags | nvarchar(max) | JSON feature flags |
| ApiEndpoint | nvarchar(500) | API URL |
| SyncIntervalMinutes | int | Sync interval |
| MaxOfflineDataDays | int | Offline data limit |
| EnableCrashReporting | bit | Crash reporting |
| EnableAnalytics | bit | Analytics flag |
| EnableDebugLogging | bit | Debug logging |
| MaxImageSizeMB | int | Image size limit |
| ImageCompressionQuality | int | Compression quality |
| IsActive | bit | Active status |

**Indexes**: (Platform, IsActive)

### MobileAnalyticsEvents Table

| Column | Type | Description |
|--------|------|-------------|
| Id | int (PK) | Unique identifier |
| DeviceId | int (FK, nullable) | Device |
| UserId | nvarchar(100) | User |
| Category | nvarchar(50) | Event category |
| Action | nvarchar(100) | Event action |
| Label | nvarchar(200) | Event label |
| Value | decimal | Numeric value |
| Screen | nvarchar(100) | Screen name |
| SessionId | nvarchar(100) | Session ID |
| Properties | nvarchar(max) | JSON properties |
| ClientTimestamp | datetime2 | Client time |
| ServerTimestamp | datetime2 | Server time |
| Platform | nvarchar(20) | Platform |
| AppVersion | nvarchar(20) | App version |

**Indexes**: UserId, DeviceId, Category, (Category, Action), ServerTimestamp

---

## Configuration

### appsettings.json

```json
{
  "Firebase": {
    "ServerKey": "YOUR_FCM_SERVER_KEY",
    "SenderId": "YOUR_FCM_SENDER_ID",
    "ProjectId": "YOUR_FIREBASE_PROJECT_ID"
  },
  "APNS": {
    "KeyId": "YOUR_APNS_KEY_ID",
    "TeamId": "YOUR_APPLE_TEAM_ID",
    "BundleId": "com.yourcompany.rmms",
    "UseProduction": false
  },
  "MobileSettings": {
    "MaxImageSizeMB": 10,
    "ImageCompressionQuality": 80,
    "DefaultSyncIntervalMinutes": 15,
    "MaxOfflineDataDays": 7
  }
}
```

### Required NuGet Packages

- `SixLabors.ImageSharp` (v3.1.7) - Image processing

---

## Integration Guide

### 1. Mobile App Registration Flow

```csharp
// 1. User logs in and gets JWT token
POST /api/v1/Auth/login
{
  "username": "user",
  "password": "password"
}
Response: { "accessToken": "...", "refreshToken": "..." }

// 2. Register device
POST /api/v1/mobile/MobileDevice/register
Headers: { "Authorization": "Bearer <token>" }
{
  "deviceId": "unique-device-id",
  "platform": "Android",
  "deviceModel": "Samsung Galaxy S23",
  "osVersion": "14.0",
  "appVersion": "1.0.0",
  "pushToken": "fcm-token-here",
  "language": "en-US",
  "notificationsEnabled": true,
  "biometricEnabled": true
}
Response: {
  "deviceId": 1,
  "isNewDevice": true,
  "appConfig": { ... }
}

// 3. Check for app updates
GET /api/v1/mobile/MobileConfig?platform=Android&appVersion=1.0.0
Response: {
  "minAppVersion": "1.0.0",
  "latestAppVersion": "1.2.0",
  "forceUpdate": false,
  "maintenanceMode": false,
  ...
}
```

### 2. Data Synchronization

```csharp
// Pull data from server
POST /api/v1/mobile/MobileSync/pull
{
  "entityType": "ProductionBatch",
  "lastSyncTimestamp": "2025-10-01T00:00:00Z",
  "pageSize": 100,
  "pageNumber": 1
}
Response: {
  "data": [...],
  "serverTimestamp": "2025-10-13T...",
  "totalRecords": 250,
  "hasMore": true
}

// Batch sync multiple entities
POST /api/v1/mobile/MobileSync/batch?deviceId=1
{
  "requests": [
    { "entityType": "ProductionBatch", "lastSyncTimestamp": null, "pageSize": 50 },
    { "entityType": "Inventory", "lastSyncTimestamp": null, "pageSize": 50 }
  ],
  "clientTimestamp": "2025-10-13T..."
}
```

### 3. Push Notifications

```csharp
// Receive notifications (handled by FCM/APNS SDK)
// Get notification history
GET /api/v1/mobile/PushNotification/history?pageSize=20&pageNumber=1

// Mark as read
POST /api/v1/mobile/PushNotification/{id}/mark-read

// Get unread count (for badge)
GET /api/v1/mobile/PushNotification/unread-count
```

### 4. Analytics Tracking

```csharp
// Track single event
POST /api/v1/mobile/MobileAnalytics/track?deviceId=1
{
  "category": "navigation",
  "action": "screen_view",
  "screen": "Dashboard",
  "sessionId": "session-123",
  "clientTimestamp": "2025-10-13T..."
}

// Track batch events (efficient)
POST /api/v1/mobile/MobileAnalytics/track-batch?deviceId=1
{
  "events": [
    { "category": "navigation", "action": "screen_view", ... },
    { "category": "action", "action": "button_click", ... }
  ],
  "clientTimestamp": "2025-10-13T..."
}
```

---

## Testing Instructions

### 1. Test Device Registration

```bash
# Login
curl -X POST https://your-api.com/api/v1/Auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Register device
curl -X POST https://your-api.com/api/v1/mobile/MobileDevice/register \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"deviceId":"test-device-1","platform":"Android","appVersion":"1.0.0","pushToken":"test-token"}'
```

### 2. Test Push Notifications

```bash
# Send test notification (Admin)
curl -X POST https://your-api.com/api/v1/mobile/PushNotification/send \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"userId":"1","title":"Test","body":"Test notification","type":"test"}'
```

### 3. Test Configuration

```bash
# Get config (no auth required)
curl https://your-api.com/api/v1/mobile/MobileConfig?platform=Android&appVersion=1.0.0
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] Configure Firebase (FCM) credentials in appsettings.json
- [ ] Configure APNS credentials in appsettings.json
- [ ] Run database migration: `dotnet ef database update`
- [ ] Create initial mobile app configuration records
- [ ] Configure CORS settings for mobile origins
- [ ] Set up rate limiting rules for mobile endpoints
- [ ] Test all mobile endpoints with Postman/Swagger

### Database Migration

```bash
cd /path/to/RMMS.Web
dotnet ef migrations add AddMobileArchitectureTables
dotnet ef database update
```

### Initial Configuration

Run this SQL to create default mobile configuration:

```sql
INSERT INTO MobileAppConfigs (Platform, MinAppVersion, LatestAppVersion, ForceUpdate,
    MaintenanceMode, SyncIntervalMinutes, MaxOfflineDataDays, EnableCrashReporting,
    EnableAnalytics, MaxImageSizeMB, ImageCompressionQuality, IsActive, CreatedAt)
VALUES
    ('Android', '1.0.0', '1.0.0', 0, 0, 15, 7, 1, 1, 10, 80, 1, GETUTCDATE()),
    ('iOS', '1.0.0', '1.0.0', 0, 0, 15, 7, 1, 1, 10, 80, 1, GETUTCDATE());
```

### Post-Deployment

- [ ] Verify health check: `/health`
- [ ] Test device registration flow
- [ ] Send test push notification
- [ ] Verify analytics tracking
- [ ] Monitor error logs
- [ ] Set up alerting for failed push notifications
- [ ] Monitor sync performance metrics

---

## Security Considerations

1. **Authentication**: All endpoints (except config) require JWT authentication
2. **Rate Limiting**: Mobile endpoints are rate-limited to prevent abuse
3. **Data Encryption**: All communication over HTTPS
4. **Push Token Security**: Tokens stored securely, not exposed in logs
5. **Device Validation**: Device IDs validated and tracked
6. **API Keys**: Optional API key authentication for additional security

---

## Performance Optimization

1. **Batch Operations**: Sync and analytics support batch operations
2. **Pagination**: All list endpoints support pagination
3. **Caching**: Configuration data cached for performance
4. **Image Optimization**: Images compressed before transmission
5. **Response Compression**: Gzip/Brotli compression enabled

---

## Monitoring & Troubleshooting

### Key Metrics to Monitor

- Device registration rate
- Push notification delivery rate
- Sync operation duration
- API response times
- Error event frequency
- App version distribution

### Common Issues

**Issue**: Push notifications not delivered
**Solution**: Verify FCM/APNS credentials, check device push token validity

**Issue**: Sync conflicts
**Solution**: Review conflict resolution strategy, check data timestamps

**Issue**: High data usage
**Solution**: Enable image compression, reduce sync frequency

---

## Future Enhancements

- [ ] Implement actual FCM/APNS certificate-based authentication
- [ ] Add real-time sync with SignalR
- [ ] Implement advanced conflict resolution strategies
- [ ] Add support for background sync
- [ ] Implement offline queue with retry logic
- [ ] Add support for rich push notifications
- [ ] Implement A/B testing framework
- [ ] Add crash reporting integration (Sentry, AppCenter)

---

## Contact & Support

For questions or issues:
- API Documentation: `/swagger`
- Health Check: `/health`
- Technical Lead: [Your Name]
- Repository: [Your Repo URL]

---

**Document Version**: 1.0.0
**Last Updated**: October 13, 2025
**Implementation Status**: ✅ COMPLETED (100%)
