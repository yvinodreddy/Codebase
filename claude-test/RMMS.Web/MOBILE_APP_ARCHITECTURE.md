# RMMS Mobile App Architecture
**Phase 4.4.2: Mobile Architecture Documentation**

## Overview
This document outlines the architecture for the RMMS Mobile Application, designed to provide field workers, supervisors, and managers with real-time access to the Rice Mill Management System.

## Technology Stack

### Frontend
- **Framework**: React Native (recommended) or Flutter
- **State Management**: Redux Toolkit / MobX
- **Navigation**: React Navigation
- **UI Components**: React Native Paper / Material UI
- **Charts**: Victory Native / React Native Charts
- **Offline Storage**: Redux Persist + AsyncStorage / SQLite

### Backend Integration
- **API Communication**: Axios / Fetch API
- **Authentication**: JWT Bearer Tokens
- **Real-time Updates**: SignalR Client
- **Push Notifications**: Firebase Cloud Messaging (FCM)

## Architecture Patterns

### 1. Clean Architecture Layers
```
├── Presentation Layer (UI Components)
├── Application Layer (Business Logic / State Management)
├── Domain Layer (Models / Entities)
└── Infrastructure Layer (API Services / Local Storage)
```

### 2. Key Features

#### Offline-First Capability
- Local SQLite database for offline data access
- Background sync when connection restored
- Conflict resolution strategies
- Optimistic UI updates

#### Authentication Flow
1. User logs in with credentials
2. App receives JWT access token + refresh token
3. Tokens stored securely (KeyChain iOS / KeyStore Android)
4. Auto-refresh token before expiration
5. Biometric authentication (Face ID / Touch ID)

#### Real-Time Features
- Live production updates via SignalR
- Push notifications for critical events
- Real-time inventory alerts
- Machine status monitoring

## Mobile API Endpoints

### Base URL
```
Production: https://api.rmms.com
Development: http://localhost:5090
```

### Core Endpoints (Task 4.4.3)

#### Dashboard
```
GET /api/v1/mobile/dashboard
Response: {
  todayProduction: number,
  activeOrders: number,
  lowStockItems: number,
  alerts: Alert[]
}
```

#### Production
```
GET /api/v1/mobile/production/active
GET /api/v1/mobile/production/{id}
POST /api/v1/mobile/production/{id}/update-status
POST /api/v1/mobile/production/batch/{id}/record-yield
```

#### Inventory
```
GET /api/v1/mobile/inventory/stock?warehouseId={id}
GET /api/v1/mobile/inventory/lowstock
POST /api/v1/mobile/inventory/adjustment
POST /api/v1/mobile/inventory/scan-barcode
```

#### Sales
```
GET /api/v1/mobile/sales/orders?status=pending
GET /api/v1/mobile/sales/{id}
POST /api/v1/mobile/sales/create
POST /api/v1/mobile/sales/{id}/update-delivery-status
```

#### Notifications
```
GET /api/v1/mobile/notifications?page={n}
POST /api/v1/mobile/notifications/register-device
PUT /api/v1/mobile/notifications/{id}/mark-read
DELETE /api/v1/mobile/notifications/unregister-device
```

## Data Synchronization Strategy

### Sync Triggers
1. **App Launch**: Full sync if connected
2. **Background Sync**: Every 15 minutes
3. **User Action**: After critical operations
4. **Push Notification**: On data change events

### Sync Process
```javascript
1. Check network connectivity
2. Get last sync timestamp from local storage
3. Fetch changes from server (delta sync)
4. Merge with local data (conflict resolution)
5. Push pending local changes to server
6. Update last sync timestamp
7. Notify user of sync completion
```

## Security Implementation

### Data Security
- All API calls over HTTPS only
- Certificate pinning for production
- JWT tokens stored in secure storage
- Encrypted local database
- No sensitive data in logs

### Authentication
```javascript
// Token Management
class AuthService {
  async login(username, password) {
    const response = await api.post('/api/v1/auth/login', { username, password });
    await SecureStore.setItemAsync('accessToken', response.data.accessToken);
    await SecureStore.setItemAsync('refreshToken', response.data.refreshToken);
  }

  async refreshToken() {
    const refreshToken = await SecureStore.getItemAsync('refreshToken');
    const response = await api.post('/api/v1/auth/refresh', { refreshToken });
    await SecureStore.setItemAsync('accessToken', response.data.accessToken);
  }

  async isAuthenticated() {
    const token = await SecureStore.getItemAsync('accessToken');
    return token !== null && !this.isTokenExpired(token);
  }
}
```

## Push Notifications (Task 4.4.4)

### Firebase Integration
```javascript
// Initialize Firebase
import messaging from '@react-native-firebase/messaging';

async function requestUserPermission() {
  const authStatus = await messaging().requestPermission();
  return authStatus === messaging.AuthorizationStatus.AUTHORIZED;
}

async function registerDeviceToken() {
  const fcmToken = await messaging().getToken();
  await api.post('/api/v1/mobile/notifications/register-device', {
    deviceToken: fcmToken,
    platform: Platform.OS
  });
}

// Handle foreground notifications
messaging().onMessage(async remoteMessage => {
  showLocalNotification(remoteMessage.notification);
});

// Handle background notifications
messaging().setBackgroundMessageHandler(async remoteMessage => {
  console.log('Background message:', remoteMessage);
});
```

### Notification Types
1. **Production Alerts**: Machine down, batch complete, quality issues
2. **Inventory Alerts**: Low stock, reorder required, stock received
3. **Sales Alerts**: New order, payment received, delivery scheduled
4. **System Alerts**: Scheduled maintenance, system updates

## Performance Optimization

### Best Practices
1. **Lazy Loading**: Load screens on demand
2. **Image Optimization**: WebP format, progressive loading, caching
3. **List Virtualization**: For long lists (FlatList / RecyclerView)
4. **Code Splitting**: Separate bundles per module
5. **Memoization**: Cache expensive computations
6. **Debouncing**: For search and form inputs

### Caching Strategy
```javascript
// API Response Caching
const cache = new Map();

async function fetchWithCache(url, ttl = 300000) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < ttl) {
    return cached.data;
  }

  const response = await api.get(url);
  cache.set(url, { data: response.data, timestamp: Date.now() });
  return response.data;
}
```

## Testing Strategy

### Unit Tests
- Service layer business logic
- Utility functions
- State management (reducers, actions)

### Integration Tests
- API service interactions
- Database operations
- Sync mechanisms

### E2E Tests
- Critical user flows (login, create order, record production)
- Offline scenarios
- Push notification handling

## Deployment

### iOS
1. Configure App Store Connect
2. Set up certificates and provisioning profiles
3. Configure push notifications capability
4. Submit via Xcode / Fastlane

### Android
1. Configure Google Play Console
2. Generate signing key
3. Enable Firebase Cloud Messaging
4. Submit via Play Console / Fastlane

## Future Enhancements
1. Barcode/QR code scanning for inventory
2. Voice commands for hands-free operation
3. Augmented Reality for warehouse navigation
4. Machine learning for predictive alerts
5. Offline map support for delivery tracking

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Author**: RMMS Development Team
