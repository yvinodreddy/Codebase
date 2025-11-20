/**
 * K6 Load Testing Script for ULTRATHINK API
 * Alternative to Locust for cloud-native load testing
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const promptDuration = new Trend('prompt_duration');

// Test configuration
export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Ramp-up to 10 users
    { duration: '1m', target: 50 },    // Ramp-up to 50 users
    { duration: '2m', target: 50 },    // Stay at 50 users
    { duration: '30s', target: 100 },  // Spike to 100 users
    { duration: '1m', target: 100 },   // Stay at 100 users
    { duration: '30s', target: 0 },    // Ramp-down to 0 users
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500', 'p(99)<1000'],  // 95% under 500ms, 99% under 1s
    'http_req_failed': ['rate<0.01'],  // Error rate < 1%
    'errors': ['rate<0.05'],  // Custom error rate < 5%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export default function () {
  // Test 1: Health check
  let healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health check status is 200': (r) => r.status === 200,
  });

  // Test 2: Root endpoint
  let rootRes = http.get(`${BASE_URL}/`);
  check(rootRes, {
    'root status is 200': (r) => r.status === 200,
  });

  // Test 3: Prompt processing (20% of requests)
  if (Math.random() < 0.2) {
    const payload = JSON.stringify({
      prompt: 'What is 2+2?',
      verbose: false,
      max_iterations: 5,
      confidence_threshold: 95.0,
    });

    const params = {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: '30s',
    };

    const startTime = Date.now();
    let promptRes = http.post(`${BASE_URL}/v1/prompt`, payload, params);
    const duration = Date.now() - startTime;

    const success = check(promptRes, {
      'prompt status is 200': (r) => r.status === 200,
      'prompt has response': (r) => {
        try {
          const body = JSON.parse(r.body);
          return body.response && body.confidence;
        } catch (e) {
          return false;
        }
      },
    });

    errorRate.add(!success);
    promptDuration.add(duration);
  }

  // Test 4: Metrics endpoint
  let metricsRes = http.get(`${BASE_URL}/metrics`);
  check(metricsRes, {
    'metrics status is 200': (r) => r.status === 200,
  });

  sleep(1);
}

export function handleSummary(data) {
  return {
    'summary.json': JSON.stringify(data),
    'stdout': textSummary(data, { indent: ' ', enableColors: true }),
  };
}
