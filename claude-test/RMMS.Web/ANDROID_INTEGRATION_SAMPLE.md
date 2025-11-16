# Android Integration Sample - RMMS Mobile Backend

## Overview

This guide shows how to build an Android app that connects to the RMMS mobile backend.

---

## Prerequisites

- Android Studio (latest version)
- Android SDK 24+ (Android 7.0+)
- Kotlin 1.8+
- Knowledge of Retrofit, Coroutines, and Jetpack Compose (or XML layouts)

---

## Step 1: Project Setup

### build.gradle (Project level)
```groovy
buildscript {
    ext.kotlin_version = "1.9.0"
    ext.retrofit_version = "2.9.0"
    ext.coroutines_version = "1.7.3"
}
```

### build.gradle (App level)
```groovy
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'com.google.gms.google-services' // For FCM
}

android {
    namespace 'com.yourcompany.rmms'
    compileSdk 34

    defaultConfig {
        applicationId "com.yourcompany.rmms"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }

    buildFeatures {
        compose true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.0"
    }
}

dependencies {
    // Networking
    implementation "com.squareup.retrofit2:retrofit:$retrofit_version"
    implementation "com.squareup.retrofit2:converter-gson:$retrofit_version"
    implementation "com.squareup.okhttp3:logging-interceptor:4.11.0"

    // Coroutines
    implementation "org.jetbrains.kotlinx:kotlinx-coroutines-android:$coroutines_version"

    // Firebase Cloud Messaging
    implementation platform('com.google.firebase:firebase-bom:32.3.1')
    implementation 'com.google.firebase:firebase-messaging-ktx'

    // Jetpack
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.2'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.6.2'
    implementation 'androidx.datastore:datastore-preferences:1.0.0'

    // Compose (optional - use if building with Jetpack Compose)
    implementation platform('androidx.compose:compose-bom:2023.10.00')
    implementation 'androidx.compose.ui:ui'
    implementation 'androidx.compose.material3:material3'
    implementation 'androidx.compose.ui:ui-tooling-preview'
    implementation 'androidx.activity:activity-compose:1.8.0'
}
```

---

## Step 2: Network Layer

### ApiService.kt
```kotlin
package com.yourcompany.rmms.network

import retrofit2.Response
import retrofit2.http.*

interface RmmsApiService {

    // Configuration (Public)
    @GET("mobile/MobileConfig")
    suspend fun getMobileConfig(
        @Query("platform") platform: String,
        @Query("appVersion") appVersion: String
    ): Response<ApiResponse<MobileConfigDto>>

    @GET("mobile/MobileConfig/version-check")
    suspend fun checkVersion(
        @Query("platform") platform: String,
        @Query("appVersion") appVersion: String
    ): Response<ApiResponse<VersionCheckDto>>

    // Authentication
    @POST("Auth/login")
    suspend fun login(@Body request: LoginRequest): Response<ApiResponse<LoginResponse>>

    // Device Management
    @POST("mobile/MobileDevice/register")
    suspend fun registerDevice(
        @Header("Authorization") token: String,
        @Body device: DeviceRegistrationDto
    ): Response<ApiResponse<DeviceRegistrationResponse>>

    @GET("mobile/MobileDevice/my-devices")
    suspend fun getMyDevices(
        @Header("Authorization") token: String
    ): Response<ApiResponse<List<MobileDeviceDto>>>

    @PUT("mobile/MobileDevice/push-token")
    suspend fun updatePushToken(
        @Header("Authorization") token: String,
        @Body request: UpdatePushTokenRequest
    ): Response<ApiResponse<Boolean>>

    // Dashboard
    @GET("mobile/MobileDashboard")
    suspend fun getDashboard(
        @Header("Authorization") token: String
    ): Response<ApiResponse<MobileDashboardDto>>

    // Analytics
    @POST("mobile/MobileAnalytics/track")
    suspend fun trackEvent(
        @Header("Authorization") token: String,
        @Query("deviceId") deviceId: Int,
        @Body event: AnalyticsEventDto
    ): Response<ApiResponse<Boolean>>

    // Sync
    @POST("mobile/MobileSync/sync")
    suspend fun syncData(
        @Header("Authorization") token: String,
        @Query("deviceId") deviceId: Int,
        @Body request: SyncRequestDto
    ): Response<ApiResponse<SyncResponseDto>>
}
```

### DTOs (Data Transfer Objects)
```kotlin
package com.yourcompany.rmms.network

import com.google.gson.annotations.SerializedName

// Generic API Response
data class ApiResponse<T>(
    val success: Boolean,
    val message: String?,
    val data: T?,
    val errors: List<String>?,
    val timestamp: String?
)

// Configuration
data class MobileConfigDto(
    val minAppVersion: String?,
    val latestAppVersion: String?,
    val forceUpdate: Boolean,
    val maintenanceMode: Boolean,
    val featureFlags: Map<String, Boolean>?,
    val syncIntervalMinutes: Int,
    val maxOfflineDataDays: Int
)

data class VersionCheckDto(
    val isSupported: Boolean,
    val forceUpdate: Boolean,
    val maintenanceMode: Boolean
)

// Authentication
data class LoginRequest(
    val username: String,
    val password: String
)

data class LoginResponse(
    val token: String,
    val expiration: String,
    val user: UserDto
)

data class UserDto(
    val id: String,
    val username: String,
    val email: String?,
    val roles: List<String>
)

// Device Registration
data class DeviceRegistrationDto(
    val deviceId: String,
    val platform: String,
    val platformVersion: String,
    val appVersion: String,
    val pushToken: String,
    val deviceModel: String,
    val deviceName: String
)

data class DeviceRegistrationResponse(
    val deviceId: Int,
    val isNewDevice: Boolean,
    val appConfig: MobileConfigDto
)

// Mobile Dashboard
data class MobileDashboardDto(
    val timestamp: String,
    val production: ProductionSummaryDto,
    val inventory: InventorySummaryDto,
    val sales: SalesSummaryDto,
    val recentAlerts: List<AlertDto>
)

data class ProductionSummaryDto(
    val activeBatches: Int,
    val todayOutput: Double,
    val averageYield: Double
)

data class InventorySummaryDto(
    val totalStockValue: Double,
    val lowStockItems: Int,
    val outOfStockItems: Int
)

data class SalesSummaryDto(
    val todaySales: Double,
    val weekSales: Double,
    val monthSales: Double
)

data class AlertDto(
    val type: String,
    val message: String,
    val severity: String
)

// Analytics
data class AnalyticsEventDto(
    val category: String,
    val action: String,
    val label: String?,
    val screen: String?,
    val properties: Map<String, Any>?
)

// Sync
data class SyncRequestDto(
    val entityType: String,
    val lastSyncTimestamp: String?,
    val localChanges: List<Any>?
)

data class SyncResponseDto(
    val serverChanges: List<Any>,
    val conflicts: List<Any>,
    val lastSyncTimestamp: String
)

data class UpdatePushTokenRequest(
    val deviceId: String,
    val pushToken: String
)
```

### RetrofitClient.kt
```kotlin
package com.yourcompany.rmms.network

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitClient {

    private const val BASE_URL = "http://YOUR_SERVER_IP:5090/api/v1/"

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    val apiService: RmmsApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(RmmsApiService::class.java)
    }
}
```

---

## Step 3: Repository Layer

### RmmsRepository.kt
```kotlin
package com.yourcompany.rmms.repository

import android.content.Context
import android.provider.Settings
import com.yourcompany.rmms.network.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class RmmsRepository(private val context: Context) {

    private val api = RetrofitClient.apiService
    private val prefs = context.getSharedPreferences("rmms_prefs", Context.MODE_PRIVATE)

    // Token management
    fun saveToken(token: String) {
        prefs.edit().putString("jwt_token", token).apply()
    }

    fun getToken(): String? {
        return prefs.getString("jwt_token", null)
    }

    fun clearToken() {
        prefs.edit().remove("jwt_token").apply()
    }

    private fun getAuthHeader(): String {
        return "Bearer ${getToken()}"
    }

    // Get unique device ID
    fun getDeviceId(): String {
        var deviceId = prefs.getString("device_id", null)
        if (deviceId == null) {
            deviceId = Settings.Secure.getString(
                context.contentResolver,
                Settings.Secure.ANDROID_ID
            )
            prefs.edit().putString("device_id", deviceId).apply()
        }
        return deviceId
    }

    // Configuration
    suspend fun getMobileConfig(appVersion: String): Result<MobileConfigDto> {
        return try {
            val response = api.getMobileConfig("Android", appVersion)
            if (response.isSuccessful && response.body()?.success == true) {
                Result.success(response.body()!!.data!!)
            } else {
                Result.failure(Exception(response.body()?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun checkVersion(appVersion: String): Result<VersionCheckDto> {
        return try {
            val response = api.checkVersion("Android", appVersion)
            if (response.isSuccessful && response.body()?.success == true) {
                Result.success(response.body()!!.data!!)
            } else {
                Result.failure(Exception(response.body()?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // Authentication
    suspend fun login(username: String, password: String): Result<LoginResponse> {
        return try {
            val response = api.login(LoginRequest(username, password))
            if (response.isSuccessful && response.body()?.success == true) {
                val loginResponse = response.body()!!.data!!
                saveToken(loginResponse.token)
                Result.success(loginResponse)
            } else {
                Result.failure(Exception(response.body()?.message ?: "Login failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // Device Registration
    suspend fun registerDevice(
        appVersion: String,
        pushToken: String
    ): Result<DeviceRegistrationResponse> {
        return try {
            val deviceDto = DeviceRegistrationDto(
                deviceId = getDeviceId(),
                platform = "Android",
                platformVersion = android.os.Build.VERSION.RELEASE,
                appVersion = appVersion,
                pushToken = pushToken,
                deviceModel = "${android.os.Build.MANUFACTURER} ${android.os.Build.MODEL}",
                deviceName = android.os.Build.MODEL
            )

            val response = api.registerDevice(getAuthHeader(), deviceDto)
            if (response.isSuccessful && response.body()?.success == true) {
                Result.success(response.body()!!.data!!)
            } else {
                Result.failure(Exception(response.body()?.message ?: "Registration failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // Dashboard
    suspend fun getDashboard(): Result<MobileDashboardDto> {
        return try {
            val response = api.getDashboard(getAuthHeader())
            if (response.isSuccessful && response.body()?.success == true) {
                Result.success(response.body()!!.data!!)
            } else {
                Result.failure(Exception(response.body()?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // Analytics
    suspend fun trackEvent(
        deviceId: Int,
        category: String,
        action: String,
        label: String? = null,
        screen: String? = null
    ): Result<Boolean> {
        return try {
            val event = AnalyticsEventDto(
                category = category,
                action = action,
                label = label,
                screen = screen,
                properties = mapOf(
                    "timestamp" to System.currentTimeMillis(),
                    "app_version" to context.packageManager.getPackageInfo(context.packageName, 0).versionName
                )
            )

            val response = api.trackEvent(getAuthHeader(), deviceId, event)
            if (response.isSuccessful && response.body()?.success == true) {
                Result.success(true)
            } else {
                Result.failure(Exception(response.body()?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

---

## Step 4: Firebase Cloud Messaging

### MyFirebaseMessagingService.kt
```kotlin
package com.yourcompany.rmms.fcm

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.yourcompany.rmms.MainActivity
import com.yourcompany.rmms.R
import com.yourcompany.rmms.repository.RmmsRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class MyFirebaseMessagingService : FirebaseMessagingService() {

    private val repository by lazy { RmmsRepository(applicationContext) }

    override fun onNewToken(token: String) {
        super.onNewToken(token)

        // Send token to backend
        CoroutineScope(Dispatchers.IO).launch {
            val deviceId = repository.getDeviceId()
            // Update push token on server
            // repository.updatePushToken(deviceId, token)
        }
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)

        // Show notification
        message.notification?.let {
            showNotification(it.title ?: "RMMS", it.body ?: "", message.data)
        }
    }

    private fun showNotification(title: String, body: String, data: Map<String, String>) {
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // Create notification channel (Android 8.0+)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "rmms_channel",
                "RMMS Notifications",
                NotificationManager.IMPORTANCE_DEFAULT
            )
            notificationManager.createNotificationChannel(channel)
        }

        // Create intent for notification tap
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            // Add data from push notification
            data.forEach { (key, value) ->
                putExtra(key, value)
            }
        }

        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

        // Build notification
        val notification = NotificationCompat.Builder(this, "rmms_channel")
            .setContentTitle(title)
            .setContentText(body)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }
}
```

### AndroidManifest.xml
```xml
<manifest>
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <application>
        <!-- Firebase Messaging Service -->
        <service
            android:name=".fcm.MyFirebaseMessagingService"
            android:exported="false">
            <intent-filter>
                <action android:name="com.google.firebase.MESSAGING_EVENT" />
            </intent-filter>
        </service>

        <!-- ... other components -->
    </application>
</manifest>
```

---

## Step 5: ViewModel Example

### DashboardViewModel.kt
```kotlin
package com.yourcompany.rmms.ui.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.yourcompany.rmms.network.MobileDashboardDto
import com.yourcompany.rmms.repository.RmmsRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class DashboardViewModel(private val repository: RmmsRepository) : ViewModel() {

    private val _dashboardState = MutableStateFlow<DashboardState>(DashboardState.Loading)
    val dashboardState: StateFlow<DashboardState> = _dashboardState

    fun loadDashboard() {
        viewModelScope.launch {
            _dashboardState.value = DashboardState.Loading

            repository.getDashboard().fold(
                onSuccess = { dashboard ->
                    _dashboardState.value = DashboardState.Success(dashboard)
                    // Track analytics
                    repository.trackEvent(1, "navigation", "screen_view", "dashboard")
                },
                onFailure = { error ->
                    _dashboardState.value = DashboardState.Error(error.message ?: "Unknown error")
                }
            )
        }
    }
}

sealed class DashboardState {
    object Loading : DashboardState()
    data class Success(val dashboard: MobileDashboardDto) : DashboardState()
    data class Error(val message: String) : DashboardState()
}
```

---

## Step 6: UI Example (Jetpack Compose)

### DashboardScreen.kt
```kotlin
package com.yourcompany.rmms.ui.dashboard

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun DashboardScreen(viewModel: DashboardViewModel = viewModel()) {
    val state by viewModel.dashboardState.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.loadDashboard()
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text("RMMS Dashboard", style = MaterialTheme.typography.headlineMedium)

        Spacer(modifier = Modifier.height(16.dp))

        when (val currentState = state) {
            is DashboardState.Loading -> {
                CircularProgressIndicator()
            }
            is DashboardState.Success -> {
                DashboardContent(dashboard = currentState.dashboard)
            }
            is DashboardState.Error -> {
                Text("Error: ${currentState.message}", color = MaterialTheme.colorScheme.error)
                Button(onClick = { viewModel.loadDashboard() }) {
                    Text("Retry")
                }
            }
        }
    }
}

@Composable
fun DashboardContent(dashboard: MobileDashboardDto) {
    // Production
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("Production", style = MaterialTheme.typography.titleMedium)
            Text("Active Batches: ${dashboard.production.activeBatches}")
            Text("Today Output: ${dashboard.production.todayOutput}")
            Text("Average Yield: ${dashboard.production.averageYield}%")
        }
    }

    Spacer(modifier = Modifier.height(8.dp))

    // Inventory
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("Inventory", style = MaterialTheme.typography.titleMedium)
            Text("Total Value: ${dashboard.inventory.totalStockValue}")
            Text("Low Stock Items: ${dashboard.inventory.lowStockItems}")
        }
    }

    Spacer(modifier = Modifier.height(8.dp))

    // Sales
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("Sales", style = MaterialTheme.typography.titleMedium)
            Text("Today: ${dashboard.sales.todaySales}")
            Text("This Week: ${dashboard.sales.weekSales}")
            Text("This Month: ${dashboard.sales.monthSales}")
        }
    }
}
```

---

## Testing the App

1. **Update BASE_URL** in `RetrofitClient.kt` with your server IP
2. **Add google-services.json** from Firebase Console
3. **Build and run** the app
4. **Test login** with credentials
5. **Verify device registration**
6. **Check push notifications**
7. **Test dashboard loading**

---

## Complete Flow

```
App Start
   ↓
Check Version (Public API)
   ↓
Is Update Required? → Yes → Show Update Dialog
   ↓ No
Show Login Screen
   ↓
User Logs In (Auth API)
   ↓
Get JWT Token
   ↓
Get FCM Token
   ↓
Register Device (Mobile Device API)
   ↓
Load Dashboard (Mobile Dashboard API)
   ↓
App Ready - Track Analytics
```

---

## Troubleshooting

1. **Network Error**: Check if server IP is correct and server is running
2. **401 Unauthorized**: JWT token expired, login again
3. **FCM Not Working**: Check google-services.json and Firebase configuration
4. **Cannot Connect**: Ensure mobile device and server on same WiFi

---

**Your Android app is now connected to RMMS backend!**
