# Multi-stage build for AI Healthcare Platform
# Optimized for Google Cloud Run and GKE deployment

# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy project files
COPY ["HealthcareManagement.AI.csproj", "."]
COPY ["../HealthcareManagement.Models/HealthcareManagement.Models.csproj", "../HealthcareManagement.Models/"]
COPY ["../HealthcareManagement.Services/HealthcareManagement.Services.csproj", "../HealthcareManagement.Services/"]
COPY ["../HealthcareManagement.DataAccess/HealthcareManagement.DataAccess.csproj", "../HealthcareManagement.DataAccess/"]

# Restore dependencies
RUN dotnet restore "HealthcareManagement.AI.csproj"

# Copy source code
COPY . .

# Build application
RUN dotnet build "HealthcareManagement.AI.csproj" -c Release -o /app/build

# Publish stage
FROM build AS publish
RUN dotnet publish "HealthcareManagement.AI.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

# Install Google Cloud SDK for AI services
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && \
    apt-get install -y google-cloud-sdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python for AI model serving (if needed)
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir google-cloud-aiplatform google-cloud-bigquery && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for Google Cloud
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/gcp-key.json
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy published application
COPY --from=publish /app/publish .

# Create directories for credentials and logs
RUN mkdir -p /app/credentials /app/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# Entry point
ENTRYPOINT ["dotnet", "HealthcareManagement.AI.dll"]