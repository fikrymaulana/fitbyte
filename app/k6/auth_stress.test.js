import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// ================= OPTIONS =================
export const options = {
  scenarios: {
    // REGISTER: model VU + per-VU pacing (1 request per VU tiap 30 detik)
    register_vu: {
      executor: 'ramping-vus',
      startVUs: 1,
      stages: [
        { duration: '30s', target: 250 },
        { duration: '30s', target: 500 },
        { duration: '30s', target: 1000 },
        { duration: '30s', target: 2000 },
        { duration: '30s', target: 5000 },
        { duration: '30s', target: 8000 },
        { duration: '30s', target: 10000 },
      ],
      gracefulRampDown: '0s',
      exec: 'authRegisterPaced',
      tags: { scenario: 'register' },
    },

    // LOGIN: arrival-rate agar match target total request per stage
    // targets (RPS) = total_requests_per_stage / 30s
    // LOGIN: arrival-rate (targets must be integers)
    login_arr: {
      executor: 'ramping-arrival-rate',
      startRate: 1,
      timeUnit: '1s',
      preAllocatedVUs: 1200,
      maxVUs: 20000,
      stages: [
        { duration: '30s', target: 83 },     // 2500 / 30 ≈ 83.33 -> 83
        { duration: '30s', target: 417 },    // 12500 / 30 ≈ 416.67 -> 417
        { duration: '30s', target: 1000 },   // 30000 / 30 = 1000
        { duration: '30s', target: 2133 },   // 64000 / 30 ≈ 2133.33 -> 2133
        { duration: '30s', target: 5500 },   // 165000 / 30 = 5500
        { duration: '30s', target: 9333 },   // 280000 / 30 ≈ 9333.33 -> 9333
        { duration: '30s', target: 12133 },  // 364000 / 30 ≈ 12133.33 -> 12133
      ],
      gracefulStop: '0s',
      exec: 'doLogin',
      tags: { scenario: 'login' },
    },
  },

  thresholds: {
    // FAIL kalau rate 5xx ≥ 10%
    http_5xx_rate: ['rate<0.10'],
  },

  discardResponseBodies: false,
};

// ================= ENV =================
const BASE_URL = __ENV.K6_BASE_URL || 'http://localhost:8000/api/v1';
const LOGIN_EMAIL = __ENV.K6_LOGIN_EMAIL || 'k6-login@example.com';
const LOGIN_PASSWORD = __ENV.K6_LOGIN_PASSWORD || 'Passw0rd!';

// ================= METRICS =================
const http5xx = new Rate('http_5xx_rate');

// ================= HELPERS =================
function req(method, url, body, params) {
  const res = http.request(method, url, body, params);
  http5xx.add(res.status >= 500);
  return res;
}
function jsonHeaders() {
  return { headers: { 'Content-Type': 'application/json' } };
}
function randStr() {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

// ================= SETUP: seed akun login =================
export function setup() {
  const res = req(
    'POST',
    `${BASE_URL}/register`,
    JSON.stringify({ email: LOGIN_EMAIL, password: LOGIN_PASSWORD }),
    jsonHeaders()
  );
  // 201 (created) atau 409 (sudah ada) sama-sama OK
  if (![201, 409].includes(res.status)) {
    throw new Error(`setup register failed: ${res.status} ${res.body}`);
  }
}

// ================= REGISTER (VU pacing) =================
// per-VU rate: 1 request per 30 detik di setiap stage
const STAGE_SECS = 30;
const registerPerVU_30s = [1, 1, 1, 1, 1, 1, 1];
const registerPerSec = registerPerVU_30s.map(v => v / STAGE_SECS);
const TEST_START_MS = Date.now();
function currentStageIndex() {
  const elapsedSec = (Date.now() - TEST_START_MS) / 1000;
  const idx = Math.floor(elapsedSec / STAGE_SECS);
  return Math.min(idx, 6); // 0..6
}
let accRegister = 0;

export function authRegisterPaced() {
  // tambahkan kuota per detik sesuai stage aktif
  const stage = currentStageIndex();
  accRegister += registerPerSec[stage];

  // eksekusi request kalau kuota >= 1 (bisa lebih dari sekali jika akumulasi)
  while (accRegister >= 1) {
    const email = `u_${randStr()}@k6.local`;
    const r = req(
      'POST',
      `${BASE_URL}/register`,
      JSON.stringify({ email, password: 'Passw0rd!' }),
      jsonHeaders()
    );
    check(r, { 'register 201': (res) => res.status === 201 });
    accRegister -= 1;
  }

  // pacing 1s per tick
  sleep(1);
}

// ================= LOGIN (arrival-rate) =================
export function doLogin() {
  const r = req(
    'POST',
    `${BASE_URL}/login`,
    JSON.stringify({ email: LOGIN_EMAIL, password: LOGIN_PASSWORD }),
    jsonHeaders()
  );
  check(r, { 'login 200': (res) => res.status === 200 });
}
