/**
 * File Validation and Security Utilities
 * Provides comprehensive file and text validation for uploads
 */

// File size limits (in bytes)
export const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
export const MAX_TEXT_LENGTH = 50000; // 50k characters

// Allowed file types
export const ALLOWED_MIME_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // .docx
  'application/msword', // .doc
  'text/plain',
];

export const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt'];

/**
 * Malicious patterns to detect in text content
 */
const MALICIOUS_PATTERNS = [
  // Script injections
  /<script[^>]*>[\s\S]*?<\/script>/gi,
  /javascript:/gi,
  /on\w+\s*=/gi, // Event handlers like onclick=, onload=
  
  // SQL injection attempts
  /('\s*OR\s*'?1'?\s*=\s*'?1)/gi,
  /(UNION\s+SELECT)/gi,
  /(DROP\s+TABLE)/gi,
  /(INSERT\s+INTO)/gi,
  /(DELETE\s+FROM)/gi,
  
  // Command injection
  /;\s*(rm|del|format|shutdown|reboot)/gi,
  /\|\s*(curl|wget|powershell|bash|sh|cmd)/gi,
  
  // Path traversal
  /\.\.[\/\\]/g,
  
  // File system access
  /file:\/\//gi,
  
  // Excessive special characters (potential encoding attacks)
  /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]/g,
];

/**
 * Suspicious keywords that might indicate malicious content
 */
const SUSPICIOUS_KEYWORDS = [
  'eval(',
  'exec(',
  'system(',
  '__import__',
  'base64.b64decode',
  'subprocess',
  'os.system',
  'shell_exec',
  'passthru',
  'proc_open',
];

/**
 * Validate file type and extension
 */
export function validateFileType(file: File): { valid: boolean; error?: string } {
  // Check extension
  const fileName = file.name.toLowerCase();
  const hasValidExtension = ALLOWED_EXTENSIONS.some(ext => fileName.endsWith(ext));
  
  if (!hasValidExtension) {
    return {
      valid: false,
      error: `Invalid file type. Only ${ALLOWED_EXTENSIONS.join(', ')} files are allowed.`,
    };
  }
  
  // Check MIME type
  if (!ALLOWED_MIME_TYPES.includes(file.type)) {
    return {
      valid: false,
      error: 'File type mismatch. The file may be corrupted or renamed.',
    };
  }
  
  return { valid: true };
}

/**
 * Validate file size
 */
export function validateFileSize(file: File): { valid: boolean; error?: string } {
  if (file.size > MAX_FILE_SIZE) {
    const sizeMB = (MAX_FILE_SIZE / 1024 / 1024).toFixed(0);
    return {
      valid: false,
      error: `File size exceeds ${sizeMB}MB limit. Please upload a smaller file.`,
    };
  }
  
  if (file.size === 0) {
    return {
      valid: false,
      error: 'File is empty. Please select a valid file.',
    };
  }
  
  return { valid: true };
}

/**
 * Scan text content for malicious patterns
 */
export function scanTextContent(text: string): { safe: boolean; threats: string[] } {
  const threats: string[] = [];
  
  // Check for malicious patterns
  MALICIOUS_PATTERNS.forEach((pattern, index) => {
    if (pattern.test(text)) {
      threats.push(`Detected potential security threat (Pattern ${index + 1})`);
    }
  });
  
  // Check for suspicious keywords
  const lowerText = text.toLowerCase();
  SUSPICIOUS_KEYWORDS.forEach(keyword => {
    if (lowerText.includes(keyword.toLowerCase())) {
      threats.push(`Detected suspicious keyword: ${keyword}`);
    }
  });
  
  return {
    safe: threats.length === 0,
    threats,
  };
}

/**
 * Validate text input length
 */
export function validateTextLength(text: string): { valid: boolean; error?: string } {
  if (text.trim().length === 0) {
    return {
      valid: false,
      error: 'Text cannot be empty.',
    };
  }
  
  if (text.length > MAX_TEXT_LENGTH) {
    return {
      valid: false,
      error: `Text exceeds maximum length of ${MAX_TEXT_LENGTH.toLocaleString()} characters.`,
    };
  }
  
  return { valid: true };
}

/**
 * Comprehensive file validation
 */
export function validateFile(file: File): { valid: boolean; error?: string } {
  // Check file type
  const typeValidation = validateFileType(file);
  if (!typeValidation.valid) {
    return typeValidation;
  }
  
  // Check file size
  const sizeValidation = validateFileSize(file);
  if (!sizeValidation.valid) {
    return sizeValidation;
  }
  
  return { valid: true };
}

/**
 * Validate and sanitize job description text
 */
export function validateJobDescriptionText(text: string): {
  valid: boolean;
  error?: string;
  warnings?: string[];
} {
  // Check length
  const lengthValidation = validateTextLength(text);
  if (!lengthValidation.valid) {
    return lengthValidation;
  }
  
  // Scan for malicious content
  const securityScan = scanTextContent(text);
  if (!securityScan.safe) {
    return {
      valid: false,
      error: 'Content contains potentially malicious code or patterns. Please remove any scripts or suspicious content.',
      warnings: securityScan.threats,
    };
  }
  
  return { valid: true };
}

/**
 * Sanitize filename for display
 */
export function sanitizeFileName(fileName: string): string {
  return fileName
    .replace(/[<>:"/\\|?*\x00-\x1f]/g, '') // Remove illegal characters
    .substring(0, 100); // Limit length
}

/**
 * Format file size for display
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
