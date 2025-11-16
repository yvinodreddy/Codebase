using System;
using System.Collections.Generic;

namespace FHIRHealthcareAPI.Models
{
    /// <summary>
    /// Represents a user in the healthcare system with role-based access
    /// </summary>
    public class User
    {
        public int Id { get; set; }
        public string Username { get; set; }  // Unique identifier for login
        public string Email { get; set; }
        public string PasswordHash { get; set; }  // Never store plain passwords
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Role { get; set; }  // Doctor, Nurse, Patient, Admin
        public string LicenseNumber { get; set; }  // For medical professionals
        public DateTime CreatedAt { get; set; }
        public DateTime LastLogin { get; set; }
        public bool IsActive { get; set; }

        // If this user is a patient, their FHIR Patient ID
        public string FhirPatientId { get; set; }

        // For tracking failed login attempts (security)
        public int FailedLoginAttempts { get; set; }
        public DateTime? LockedUntil { get; set; }
    }

    /// <summary>
    /// Defines the roles available in the system
    /// </summary>
    public static class UserRoles
    {
        public const string Admin = "Admin";
        public const string Doctor = "Doctor";
        public const string Nurse = "Nurse";
        public const string Patient = "Patient";

        // Define what each role can do
        public static readonly Dictionary<string, List<string>> RolePermissions = new()
        {
            { Admin, new List<string> { "All" } },
            { Doctor, new List<string> { "ReadAll", "CreatePrescription", "CreateDiagnosis", "UpdatePatient" } },
            { Nurse, new List<string> { "ReadAll", "CreateObservation", "UpdateObservation" } },
            { Patient, new List<string> { "ReadOwn" } }
        };
    }
}