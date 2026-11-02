/* Non-grading deterministic check definitions; these do not validate reasoning. */
export const factReviewChecks={
  "network": {
    "label": "HTTP 503 means application-side unavailable; DNS/TCP/TLS already succeeded",
    "expected": [
      "503",
      "tls"
    ]
  },
  "subnet": {
    "label": "192.0.2.70/26 is in 192.0.2.64/26; .110 is on-link",
    "expected": [
      "192.0.2.64",
      "direct"
    ]
  },
  "monitoring": {
    "label": "Precision 80%, recall 60%, accuracy 89%",
    "expected": [
      "80%",
      "60%",
      "89%"
    ]
  }
};
